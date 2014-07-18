import rumps
import data_collector as dc
from log import Log


class Habitus(rumps.App):
    def __init__(self):
        super(Habitus, self).__init__("Habitus", icon="images/icon-bw.png")
        self.menu = ['Start', 'Stop', None]
        # log is opened using the log module. It is opened using the append
        # ('a') keyword, so no information is overwritten
        self.log = Log()

    @staticmethod
    def callback_function(self, sender):
        print dc.retrieve_active_app_name()

    @rumps.clicked('Start')
    def start_data_collection_timer(self):
        data_collection_timer.start()

    @rumps.clicked('Stop')
    def stop_data_collection_timer(self):
        data_collection_timer.stop()

data_collection_timer = rumps.Timer(Habitus.callback_function,
                                    interval=1)