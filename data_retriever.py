from AppKit import NSWorkspace
from subprocess import Popen, PIPE
import time
import threading
import datetime
import urlparse


class DataRetriever(threading.Thread):
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

    def __init__(self, delay=1):
        threading.Thread.__init__(self)
        self._running = False
        self.is_waiting = threading.Event()  # starts in False
        self.resume = threading.Event()
        self.delay = delay
        self.active_app_name = None
        self.data = []

    @staticmethod
    def run_apple_script(script):
        """
      Run AppleScript script in order to collect the currently open URL from
      either Chrome or Safari. This function is called by
      :rtype : object
        """
        p = Popen(['osascript'], stdin=PIPE, stdout=PIPE, stderr=PIPE)
        standard_out, standard_error = p.communicate(script)
        url = urlparse.urlparse(standard_out)

        # Safari returns a blank web page if there is a new open tab with blank
        # page, while Chrome returns a 'newtab'. To regularize this situation,
        # when a new tab is opened, 'newtab' is returned for both.
        if url.netloc != "":
            return url.netloc
        else:
            return "newtab"

    def retrieve_web_page(self):
        """
      Receives the active application name. If the currently open application is
      either Safari or Google Chrome, the URL of the currently open web page is
      returned. If the application is any other web browser, then the name of
      the browser is returned.
        :rtype : String
        """
        if "Safari" == self.active_app_name:
            return self.run_apple_script(DataRetriever.SAFARI_APPLE_SCRIPT)

        if "Google Chrome" == self.active_app_name:
            return self.run_apple_script(DataRetriever.CHROME_APPLE_SCRIPT)

        return self.active_app_name

    def retrieve_active_app_name(self):
        try:
            self.active_app_name = NSWorkspace.sharedWorkspace(). \
                frontmostApplication().localizedName()
        except AttributeError:
            # If NSWorkspace.sharedWorkspace().frontmostApplication() fails,
            # then NoneType is returned and therefore, Attribute Error is
            # raised. If this occurs, execution shall continue.
            self.active_app_name = None

        # If self.active_app_name is None, then no web page has been visited.
        self.active_app_name = self.retrieve_web_page()

        current_date = datetime.datetime.now().strftime("%Y-%m-%d")
        current_time = datetime.datetime.now().strftime("%H:%M:%S")

        data_string = current_date + "," + current_time + "," + \
            self.active_app_name
        self.data.append(data_string)
        return data_string

    def stop(self):
        self._running = False

    def is_paused(self):
        return self._running

    def pause(self):
        self.resume.clear()
        self.is_waiting.set()

    def restart(self):
        self.resume.set()
        self.is_waiting.clear()

    def run(self):
        self._running = True
        self.resume.set()
        while self._running:
            if not self.resume.is_set():
                self.is_waiting.set()
                self.resume.wait()
                self.is_waiting.clear()
            print self.retrieve_active_app_name()
            time.sleep(self.delay)