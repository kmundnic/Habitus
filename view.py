import rumps
from data_retriever import DataRetriever
from data_sender import DataSender
import controller


class Habitus(rumps.App):
    def __init__(self):
        super(Habitus, self).__init__("Habitus", icon="images/icon-bw.png")
        self.menu = ['Start', 'Stop', None]

    @rumps.clicked('Start')
    def start_data_collection_timer(self):
        controller.retrieve_data_timer.start()

    @rumps.clicked('Stop')
    def stop_data_collection_timer(self):
        controller.retrieve_data_timer.stop()