import rumps
from data_retriever import DataRetriever
from data_sender import DataSender


data_retriever = DataRetriever()
data_sender = DataSender()


def retrieve_data_callback(_):
    print data_retriever.retrieve_active_app_name()


@rumps.timer(10)  # Data is sent every 15min
def send_data_callback(_):
    if retrieve_data_timer.is_alive():
        retrieve_data_timer.stop()
        data_to_send = list(data_retriever.data)
        data_retriever.data = []
        retrieve_data_timer.start()

        if data_to_send:
            data_sender.write_data(data_to_send)
            print "Sending data..."
            data_sender.send_data()

retrieve_data_timer = rumps.Timer(retrieve_data_callback,
                                  interval=1)  # 1[s] interval