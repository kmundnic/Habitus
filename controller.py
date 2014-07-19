import rumps
from data_retriever import DataRetriever
from data_sender import DataSender

# TODO: Is it necessary to change this file into a class? Reference problems...

SEND_DATA_BETWEEN_SECONDS = 900

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
            data_sender.send_data()

retrieve_data_timer = rumps.Timer(retrieve_data_callback,
                                  interval=1)  # 1[s] interval