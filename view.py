import rumps
import controller


class Habitus(rumps.App):

    def __init__(self):
        super(Habitus, self).__init__("Habitus", icon="images/icon-bw.png")
        self.menu = ['Start', 'Stop', None]

    def set_status(self):
        """
        Changes an element in the menu for the user to know if the application
        is running or is stopped.
        It is called by the callback functions of the MenuItems 'Start' and
        'Stop', and checks if the application is running by checking if the
        data retrieving thread is alive.
        :return: None
        """
        if controller.retrieve_data_timer.is_alive():
            try:
                del self.menu['Stopped']
            except KeyError:
                "Has never stopped yet"
            self.menu.insert_after('Stop', 'Running...')
        else:
            try:
                del self.menu['Running...']
                self.menu.insert_after('Stop', 'Stopped')
            except KeyError:
                print "Already stopped"


    @rumps.clicked('Start')
    def start_data_collection_timer(self, sender):
        """
        Callback function for MenuItem 'Start'. self, sender are used as
        arguments to differentiate between this app (self) and the sender object
        (MenuItem).
        :param sender: MenuItem
        :return: None
        """
        controller.retrieve_data_timer.start()
        self.set_status()

    @rumps.clicked('Stop')
    def stop_data_collection_timer(self, sender):
        """
        Callback function for MenuItem 'Stop'. self, sender are used as
        arguments to differentiate between this app (self) and the sender object
        (MenuItem).
        :param sender: MenuItem
        :return: None
        """
        controller.retrieve_data_timer.stop()
        self.set_status()

