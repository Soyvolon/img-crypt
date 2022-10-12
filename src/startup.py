from UI import ImageCryptApp

# TODO: Documentation.

class Startup(object):
    def __init__(self):
        # do inital application registration here, along with any configuration reading
        self.__db_conn_string = ""
        self.__app = ImageCryptApp()

    def initalize(self):
        pass