import rumps
from data_retriever import DataRetriever
from data_sender import DataSender


class Habitus(rumps.App):
    def __init__(self):
        super(Habitus, self).__init__("Habitus", icon="images/icon-bw.png")
        self.menu = ['Start', 'Stop', None]
        self.data_retriever = DataRetriever()
        self.data_sender = DataSender()

    @staticmethod
    def retrieve_data_callback(self, sender):
        print self.data_retriever.retrieve_active_app_name()

    @rumps.timer(900)  # Data is sent every 15min
    def send_data_callback(self, sender):
        if retrieve_data_timer.is_alive():
            retrieve_data_timer.stop()
            data_to_send = list(self.data_retriever.data)
            self.data_retriever.data = []
            retrieve_data_timer.start()

            if data_to_send:
                self.data_sender.write_data(data_to_send)
                print "Sending data..."
                self.data_sender.send_data()


    @rumps.clicked('Start')
    def start_data_collection_timer(self):
        retrieve_data_timer.start()

    @rumps.clicked('Stop')
    def stop_data_collection_timer(self):
        retrieve_data_timer.stop()

retrieve_data_timer = rumps.Timer(Habitus.retrieve_data_callback,
                                  interval=1)  # 1[s] interval