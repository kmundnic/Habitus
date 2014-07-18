from AppKit import NSWorkspace
from subprocess import Popen, PIPE
import time
import datetime
import urlparse
from log import Log


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


def run_apple_script(script):
    """
  Run AppleScript script in order to collect the currently open URL from either
  Chrome or Safari. This function is called by
  :rtype : object
    """
    p = Popen(['osascript'], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    standard_out, standard_error = p.communicate(script)
    url = urlparse.urlparse(standard_out)

    if url.netloc != "":
        return url.netloc
    else:
        return "newtab"

def retrieve_web_page(active_app_name):
    """
  Receives the active application name. If the currently open application is
  either Safari or Google Chrome, the URL of the currently open web page is
  returned. If the application is any other web browser, then the name of the
  browser is returned.
    :rtype : String
    """
    if "Safari" == active_app_name:
        return run_apple_script(SAFARI_APPLE_SCRIPT)

    if "Google Chrome" == active_app_name:
        return run_apple_script(CHROME_APPLE_SCRIPT)

    return active_app_name


def run(log):
    global RETRIEVING_DATA
    RETRIEVING_DATA = True

    if not log.is_open:
        log.reopen_log()

    while RETRIEVING_DATA:
        active_app_name = NSWorkspace.sharedWorkspace(). \
            frontmostApplication().localizedName()

        active_app_name = retrieve_web_page(active_app_name)

        current_date = datetime.datetime.now().strftime("%Y-%m-%d")
        current_time = datetime.datetime.now().strftime("%H:%M:%S")

        print current_date, current_time, active_app_name # debugging purposes

        try:
            log.file.write("{},{},{}\n".format(current_date,
                                               current_time,
                                               active_app_name))
        except UnicodeEncodeError:
            # active_app_name is a pyobjc_unicode type. For non-ascii characters
            # it is necessary to convert encode into UTF-8 before saving them
            # into a log file.
            active_app_name = active_app_name.encode('utf-8')
            log.file.write("{},{},{}\n".format(current_date,
                                               current_time,
                                               active_app_name))
        time.sleep(1)


def stop():
    # Close log
    global RETRIEVING_DATA
    RETRIEVING_DATA = False