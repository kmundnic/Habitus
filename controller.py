import rumps
import smtplib
from data_retriever import DataRetriever
from data_sender import DataSender

# TODO: Is it necessary to change this file into a class? Reference problems...

SEND_DATA_BETWEEN_SECONDS = 3600

data_retriever = DataRetriever()


# Retrieve data every 1[s]
def retrieve_data_callback(_):
    print data_retriever.retrieve_active_app_name()


# Data is sent every 15min
@rumps.timer(SEND_DATA_BETWEEN_SECONDS)
def send_data_callback(_):
    if retrieve_data_timer.is_alive():
        retrieve_data_timer.stop()
        data_to_send = list(data_retriever.data)
        data_retriever.data = []
        retrieve_data_timer.start()

        if data_to_send:
            # We create a different log every time to have logs with names
            # according to date and time when information is written and sent
            data_sender = DataSender()
            data_sender.write_data(data_to_send)
            print "Sending data..."
            try:
                # Try to send data. If there is no internet connection or the
                # connection to the server can't be established, then the
                # data is put back to the list data_retriever.data, so it can
                # be resent when the connection establishes.
                # TODO: Retry sending files instead of saving info to list
                # There should be a file list with the files that haven't been
                # sent. If the connections fails, the data is already written
                # into a file, and every time info is sent, the list of files
                # to be sent should be popped from this list. If the connection
                # fails, the file is appended back to the list.
                data_sender.send_data()
            except smtplib.socket.gaierror:
                retrieve_data_timer.stop()
                data_retriever.data = data_to_send + data_retriever.data
                retrieve_data_timer.start()
                rumps.notification("Warning:",
                                   "Please check internet connection",
                                   "Data has not been sent",
                                   sound=False)

retrieve_data_timer = rumps.Timer(retrieve_data_callback,
                                  interval=1)  # 1[s] interval