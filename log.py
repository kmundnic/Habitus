import datetime
import os


def create_directory(directory_name):
    """
    Creates a new directory to store logs. If a directory with the same name
    already exists, the directory is not created.
    :param directory_name: Name of the created directory
    :return: None
    """
    if type(directory_name) is str:
        if not os.path.exists(directory_name):
            os.makedirs(directory_name)


def open_log():
    """
    Open log. Checks if directory is created. If not, it is created. Returns the
    log file.
    Log is opened with the keyword letter 'a' for append. This is, the pointer
    points at the end of the file when the log is opened. This way, information
    is not overwritten.
    :return: file
    """
    # Create directory named "logs"
    directory_name = "logs"
    create_directory(directory_name)

    # Get current date and user login name to create file
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    user = os.getlogin()
    log_name = "{}/{}_{}.txt".format(directory_name, user, current_date)

    # Open log
    log = open(log_name, 'a')

    return log


def close_log(log):
    """
    Checks if log is open and then closes the file.
    :param log: txt file
    :return: None
    """
    if type(log) is file:
        if not log.closed:
            log.close()
