import threading
import logging
import time
import smtplib
import rumps
import controller
from data_sender import DataSender
from log import Log

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG,
                    format='[%(asctime)s %(threadName)s] %(message)s',
                    datefmt='%H:%M:%S')


class DataHandler(threading.Thread):
    """
    This class uses the data_sender module to
    """

    def __init__(self, retriever, delay=900):
        threading.Thread.__init__(self)
        self._started = False  # The life flag of the thread.
        self.gui_block = threading.Event()  # Event controlled by the GUI
        self.delay = delay  # Delay for data sender timer
        self.retriever = retriever  # Copy of the data retriever thread
        self.sender = DataSender()
        self.log = None  # New log is created every time data is sent

    def run(self):
        """
        Run the Thread created with the class DataHandler.
        :return: None
        """
        self._started = True  # Only set once to true!
        self.gui_block.set()  # Unblocked by the GUI
        time.sleep(self.delay)  # Should collect data before sending it
        while self._started:
            # If the application has been stopped, wait until it is unblocked
            if not self.gui_block.is_set():
                self.gui_block.wait()
            else:
                # The retriever thread is put into pause, and we wait until it
                # is actually paused. Then, we try to send the data. Finally, we
                # wake up the data retrieving thread back again.
                self.retriever.resume.clear()
                self.retriever.is_waiting.wait()
                self.send_data()
                self.retriever.resume.set()
                time.sleep(self.delay)

    def stop(self):
        """
        Kills the thread.
        :return: None
        """
        self._started = False

    def is_paused(self):
        """
        Returns the state of the thread according to the GUI options.
        :return: None
        """
        return not self.gui_block.is_set()

    def pause(self):
        """
        Pause the thread from the GUI.
        :return: None
        """
        self.gui_block.clear()

    def restart(self):
        """
        Restarts the thread from the GUI.
        :return: None
        """
        self.gui_block.set()

    def write_data(self, data):
        """
        Function that writes the retrieved data into a CSV file.
        These lines come from data_retriever.retrieve_active_app_name() as
        current_date + "," + current_time + "," + active_app_name to be written
        easily and immediately into the CSV file without necessity of
        formatting.
        :param data: List containing lines of data to be included in the CSV
        file.
        :return: None
        """
        print "Writing data..."
        # Write data into log
        self.log.write_file(data)

        # Close log so information can be sent
        self.log.close_log()

    def send_data(self):
        """
        Data is sent to email_recipient using the gmail module.
        :return: None
        """

        data_to_send = list(controller.retriever.data)
        # If the data retriever has worked properly and data has been retrieved,
        # we try to write the data into a file and send it.
        if data_to_send:
            try:
                # Try to open a new log
                self.log = Log()
            except (IOError, OSError):
                logger.debug("Can't open log")
            try:
                # Try to write the log
                self.write_data(data_to_send)
            except (IOError, OSError):
                logger.debug("Can't write data into file")

            # If there was data and it has been written into a file, then the
            # list should be re-initialized so no data is written twice.
            controller.retriever.data = []

        try:
            # Try to send data. If there is no internet connection or the
            # connection to the server can't be established, then the
            # data is put back to the list controller.retriever.data, so it can
            # be re-sent when there is a connection.
            # TODO: Retry sending files instead of saving info to list
            # There should be a file list with the files that haven't been
            # sent. If the connections fails, the data is already written
            # into a file, and every time info is sent, the list of files
            # to be sent should be popped from this list. If the connection
            # fails, the file is appended back to the list.
            self.sender.send_email(subject=self.log.user + "-threads",
                                   text="",
                                   attach=self.log.file_name)
        except smtplib.socket.gaierror:
            logger.debug("Connection to send data not established.")
            controller.retriever.data = list(data_to_send)
            print len(controller.retriever.data)
            rumps.notification("Warning!",
                               "Please check internet connection",
                               "Data has not been sent",
                               sound=False)