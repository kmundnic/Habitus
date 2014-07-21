import datetime
import csv
import os


class Log:
    def __init__(self):
        self.user = os.getlogin()
        self.directory_name = "logs/" + self.user
        self.current_date = datetime.datetime.now().strftime("%Y%m%d")
        self.current_time = datetime.datetime.now().strftime("%H%M%S")
        self.is_open = False
        self.file_name = None
        self.file = self.open_log()

    def create_directory(self):
        """
        Creates a new directory to store logs. If a directory with the same name
        already exists, the directory is not created.
        :return: None
        """
        if not os.path.exists(self.directory_name):
            os.makedirs(self.directory_name)

    def open_log(self):
        """
        Open log. Checks if directory is created. If not, it is created. Returns
        the log file.
        Log is opened with the keyword letter 'w' to overwrite data and only
        send small chunks of information.
        More info on file opening options available on http://stackoverflow.com
        /questions/1466000
        /python-open-built-in-function-difference-between-modes-a-a-w-w-and-r
        :return: csv file
        """
        # Create directory named "logs"
        self.create_directory()

        # Get current date and user login name to create file
        self.file_name = "{}/{}T{}.csv".format(self.directory_name,
                                               self.current_date,
                                               self.current_time)

        # Open log and set self.is_open to true
        self.file = open(self.file_name, 'w')
        self.is_open = True

        return self.file

    def write_file(self, data):
        for item in data:
            try:
                self.file.write(item + '\n')
            except UnicodeEncodeError:
                # item is a pyobjc_unicode type. For non-ascii
                # characters it is necessary to convert encode into UTF-8 before
                # saving them into a log file.
                item = item.encode('utf-8')
                self.file.write(item + '\n')

    def reopen_log(self):
        if not self.is_open:
            self.file = open(self.file_name, 'w')
            self.is_open = True

    def close_log(self):
        """
        Checks if log is open and then closes the file.
        :return: None
        """
        if self.is_open:
            self.file.close()
            self.is_open = False