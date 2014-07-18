from AppKit import NSWorkspace
from subprocess import Popen, PIPE
import time
import datetime
import urlparse


class DataRetriever():
    # Define AppleScript scripts to retrieve URL information from Safari or
    # Chrome. AppleScript offers a direct interface in order to obtain the
    # complete URL of these browsers. Up to date, Firefox and Opera do not offer
    # the necessary interface.
    SAFARI_APPLE_SCRIPT = '''tell application "Safari"
                               URL of current tab of window 1
                            end tell'''
    CHROME_APPLE_SCRIPT = '''tell application "Google Chrome"
                               URL of active tab of window 1
                             end tell'''

    def __init__(self):
        self.data = []

    @staticmethod
    def run_apple_script(script):
        """
      Run AppleScript script in order to collect the currently open URL from '
      either Chrome or Safari. This function is called by
      :rtype : object
        """
        p = Popen(['osascript'], stdin=PIPE, stdout=PIPE, stderr=PIPE)
        standard_out, standard_error = p.communicate(script)
        url = urlparse.urlparse(standard_out)

        if url.netloc != "":
            return url.netloc
        else:
            return "newtab"

    @staticmethod
    def retrieve_web_page(active_app_name):
        """
      Receives the active application name. If the currently open application is
      either Safari or Google Chrome, the URL of the currently open web page is
      returned. If the application is any other web browser, then the name of
      the browser is returned.
        :rtype : String
        """
        if "Safari" == active_app_name:
            return DataRetriever.\
                run_apple_script(DataRetriever.SAFARI_APPLE_SCRIPT)

        if "Google Chrome" == active_app_name:
            return DataRetriever.\
                run_apple_script(DataRetriever.CHROME_APPLE_SCRIPT)

        return active_app_name

    def retrieve_active_app_name(self):
        active_app_name = NSWorkspace.sharedWorkspace(). \
            frontmostApplication().localizedName()

        active_app_name = self.retrieve_web_page(active_app_name)

        current_date = datetime.datetime.now().strftime("%Y-%m-%d")
        current_time = datetime.datetime.now().strftime("%H:%M:%S")

        return current_date, current_time, active_app_name