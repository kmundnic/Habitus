from AppKit import NSWorkspace
from subprocess import Popen, PIPE
import time
import datetime
import urlparse
import signal
import sys

reload(sys)
sys.setdefaultencoding("utf-8")

# This variable is used to control the data retrieving loop inside run()
# function.
RETRIEVING_DATA = True

# Define AppleScript scripts to retrieve URL information from Safari or Chrome.
# AppleScript offers a direct interface in order to obtain the complete URL of
# these browsers. Up to date, Firefox and Opera do not offer the necessary
# interface.
SAFARI_APPLE_SCRIPT = '''tell application "Safari"
                           URL of current tab of window 1
                        end tell'''
CHROME_APPLE_SCRIPT = '''tell application "Google Chrome"
                           URL of active tab of window 1
                         end tell'''
# Open log
log = open('log.txt', 'w')


def run_apple_script(script):
    """
  Run AppleScript script in order to collect the currently open URL from either
  Chrome or Safari. This function is called by
  :rtype : object
    """
    p = Popen(['osascript'], stdin =PIPE, stdout=PIPE, stderr=PIPE)
    stdout, stderr = p.communicate(script)
    url = urlparse.urlparse(stdout)
    return url.netloc


def retrieve_web_page(active_app_name):
    """
  Receives the active application name. If the currently open application is
  either Safari or Google Chrome, the URL of the currently open web page is
  returned.
    """
    if "Safari" == active_app_name:
        return run_apple_script(SAFARI_APPLE_SCRIPT)

    if "Google Chrome" == active_app_name:
        return run_apple_script(CHROME_APPLE_SCRIPT)

    return active_app_name


def set_signal_handler():
    def signal_handler(signal, frame):
        stop()
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)


def run():
    global RETRIEVING_DATA
    RETRIEVING_DATA = True

    while RETRIEVING_DATA:
        active_app_name = NSWorkspace.sharedWorkspace(). \
            activeApplication()['NSApplicationName']

        active_app_name = retrieve_web_page(active_app_name)

        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        print current_time, active_app_name

        try:
            log.write("{} {}\n".format(current_time, active_app_name))
        except UnicodeEncodeError:
            # To prevent encoding issues in the log regarding encoding of
            # non-ascii characters, active_app_name is converted from ascii to
            # utf-8 before it is written into the log file. This works
            # successfully with uTorrent app name.
            active_app_name = (active_app_name.decode('ascii',
                                                      'ignore')).encode('utf-8')
            log.write("{} {}\n".format(current_time, active_app_name))
        time.sleep(1)


def stop():
    # Close log
    global RETRIEVING_DATA
    RETRIEVING_DATA = False
    # global log
    # log.close()