import rumps
import smtplib
from data_retriever import DataRetriever
from data_sender import DataSender

# TODO: Is it necessary to change this file into a class? Reference problems...
#
# TODO: Erase files that have been sent
# If the files that have been sent are erased, it is quite easy to keep track
# of the information that has not been sent, and this can be saved into a list
# that can be easily put into a file and therefore, read to create a queue.
#
# TODO: Keep log with logger

RETRIEVE_DATA_INTERVAL = 1
SEND_DATA_INTERVAL = 15

retriever = DataRetriever(RETRIEVE_DATA_INTERVAL)


# Data is sent every 15min
@rumps.timer(SEND_DATA_INTERVAL)
def send_data_callback(_):
    if not retriever.is_paused():
        retriever.pause()
        data_to_send = list(retriever.data)
        retriever.data = []
        retriever.restart()

        if data_to_send:
            # We create a different log every time to have logs with names
            # according to date and time when information is written and sent
            sender = DataSender()
            sender.write_data(data_to_send)
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
                sender.send_data()
            except smtplib.socket.gaierror:
                retriever.pause()
                retriever.data = data_to_send + retriever.data
                retriever.restart()
                rumps.notification("Warning:",
                                   "Please check internet connection",
                                   "Data has not been sent",
                                   sound=False)
