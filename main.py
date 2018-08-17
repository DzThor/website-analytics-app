import sys
import pymongo

from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication, QPushButton, QLineEdit, QTextEdit
from PySide2.QtCore import QFile, QObject, QSize
from PySide2.QtGui import QIcon
import PySide2.QtCharts


class WebsiteAnalytics(QObject):

    def __init__(self, ui_file, parent=None):
        super(WebsiteAnalytics, self).__init__(parent)
        ui_file = QFile(ui_file)
        ui_file.open(QFile.ReadOnly)

        print(self.mongodb_conn())
        db = self.client.website_analytics.scraped_data
        print(db.find_one())

        loader = QUiLoader()
        self.window = loader.load(ui_file)
        ui_file.close()
        #self.line = self.window.findChild(QTextEdit, "textEdit")
        #self.line.setText("VAYA KKITA")

        self.setIcons()
        #self.window.setWindowIcon(QIcon('images/logo256.png'))

        self.window.show()

    def setIcons(self):
        app_icon = QIcon()
        app_icon.addFile('images/logo256.png', QSize(256,256))
        self.window.setWindowIcon(app_icon)


    def mongodb_conn(self):
        try:
            self.client = pymongo.MongoClient()
        except pymongo.errors.ConnectionFailure as err:
            print("Connection failure: {0}".format(err))

    def __del__(self):
        self.client.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    website_analytics = WebsiteAnalytics('mainwindow.ui')
    sys.exit(app.exec_())

