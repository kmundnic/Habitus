import rumps
import controller


class Habitus(rumps.App):

    def __init__(self):
        super(Habitus, self).__init__("Habitus", icon="images/icon-bw.png")
        self.menu = ['Start',
                     'Stop',
                     # rumps.MenuItem('Stopped', callback=Habitus.state),
                     None]

    @rumps.clicked('Start')
    def start_data_collection_timer(self, sender):
        controller.retrieve_data_timer.start()
        if controller.retrieve_data_timer.is_alive():
            try:
                del self.menu['Stopped']
            except KeyError:
                "Has never stopped yet"
            self.menu.insert_after('Stop', 'Running...')

    @rumps.clicked('Stop')
    def stop_data_collection_timer(self, sender):
        controller.retrieve_data_timer.stop()
        if not controller.retrieve_data_timer.is_alive():
            try:
                del self.menu['Running...']
                self.menu.insert_after('Stop', 'Stopped')
            except KeyError:
                print "Already stopped"
