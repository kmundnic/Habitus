import datetime
import os


class Log:
    def __init__(self):
        self.directory_name = "logs/"
        self.user = os.getlogin()
        self.current_date = datetime.datetime.now().strftime("%Y-%m-%d")
        self.is_open = False
        self.name = None
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
        Log is opened with the keyword letter 'a' for append. This is, the
        pointer points at the end of the file when the log is opened. This way,
        information is not overwritten.
        :return: file
        """
        # Create directory named "logs"
        self.create_directory()

        # Get current date and user login name to create file

        self.name = "{}/{}_{}.txt".format(self.directory_name,
                                         self.user,
                                         self.current_date)

        # Open log and set self.is_open to true
        self.file = open(self.name, 'a')
        self.is_open = True

        return self.file

    def close_log(self):
        """
        Checks if log is open and then closes the file.
        :param log: txt file
        :return: None
        """
        if not self.is_open:
            self.file.close()
            self.is_open = False

