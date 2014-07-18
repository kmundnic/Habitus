import rumps
from data_retriever import DataRetriever
from log import Log


class Habitus(rumps.App):
    def __init__(self):
        super(Habitus, self).__init__("Habitus", icon="images/icon-bw.png")
        self.menu = ['Start', 'Stop', None]
        # log is opened using the log module. It is opened using the append
        # ('a') keyword, so no information is overwritten
        self.log = Log()
        self.data_retriever = DataRetriever()

    @staticmethod
    def retrieve_data_callback(self, sender):
        print self.data_retriever.retrieve_active_app_name()

    @rumps.clicked('Start')
    def start_data_collection_timer(self):
        retrieve_data_timer.start()

    @rumps.clicked('Stop')
    def stop_data_collection_timer(self):
        retrieve_data_timer.stop()

retrieve_data_timer = rumps.Timer(Habitus.retrieve_data_callback,
                                  interval=1)  # 1[s] interval