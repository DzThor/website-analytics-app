import sys
import pymongo
import json
from datetime import datetime,timedelta
from random import randint

from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication, QPushButton, QLineEdit, QTextEdit, QWidget, QGridLayout, QScrollArea, QVBoxLayout, QListWidget, QHBoxLayout, QSpacerItem, QSpinBox
from PySide2.QtCore import QFile, QObject, QSize, QPoint, Qt
from PySide2.QtGui import QIcon, QPainter
from PySide2.QtCharts import QtCharts


class WebsiteAnalytics(QObject):

    def __init__(self, ui_file, parent=None):
        super(WebsiteAnalytics, self).__init__(parent)
        ui_file = QFile(ui_file)
        ui_file.open(QFile.ReadOnly)

        #"date"
        #"source"
        #"platform"
        #"followers"
        #"averageLikesTwiiter"
        #"averageRetweets"
        #"averageEngRate"
        #"accountsReached"
        #"impressions"
        #"tweetingSchedule"
        #"totalPageLikes"
        #"averageLikesFacebook"
        #"averageComments"
        #"averageShares"
        #"averageEngagement"
        #"peopleTalking"
        #"frontPage"
        #"activity"
        #"about"
        #"response"
        #"engagement"
        #"strength"
        #"passion"
        #"reach"
        #"sentiment"

        #print(self.mongodb_conn())
        #print(db.find_one())

        with open('config.json', 'r') as f:
            config = json.load(f)
            connection = pymongo.MongoClient(
                config['MONGODB_SERVER'],
                config['MONGODB_PORT']
            )
            db = connection[config['MONGODB_DB']]
            self.collection = db[config['MONGODB_COLLECTION']]

        loader = QUiLoader()
        self.window = loader.load(ui_file)
        ui_file.close()

        tw = ["Followers","Retweets" ,"Average Likes" ,"Average Retweets", "Average Engagement Rate", "Accounts reached", "Impressions", "Tweeting schedule"]
        fb = ["Total Page Likes","Average Likes","Average Comments","Average Shares","Average Engagement","People talking about you","Front page","About","Activity","Response","Engagement"]
        internet = ["Strength" ,"Reach" ,"Passion" ,"Sentiment"]

        boton1 = self.window.findChild(QSpinBox, "spinBoxTwitter")
        boton1.valueChanged.connect(lambda: self.valueChanged("hola"))
        boton2 = self.window.findChild(QSpinBox, "spinBoxFacebook")
        boton3 = self.window.findChild(QSpinBox, "spinBoxInternet")

        a = self.window.findChild(QVBoxLayout, "TwitterChartsVL")

        #for i in range(0,8):
        #    a.addWidget(self.createLineChart())
        for title in tw:
            a.addWidget(self.createLineChart(title))
        
        print(a.count())

        b = self.window.findChild(QVBoxLayout, "FacebookChartsVL")
        for title in fb:
            b.addWidget(self.createBarChart(title))

        #for i in range(0,11):
        #    b.addWidget(self.createBarChart())

        c = self.window.findChild(QVBoxLayout, "InternetChartsVL")
        for title in internet:
            c.addWidget(self.createPercentBarChart(title))
        
        print(c.count())

        #for i in range(0,4):
        #    c.addWidget(self.createPercentBarChart())


        self.setIcons()
        #self.window.setWindowIcon(QIcon('images/logo256.png'))

        self.window.show()

    def valueChanged(self, cadena):
        print("slot usado")
        print(cadena)
        

    def createBarChart(self, title):

        set0 = QtCharts.QBarSet("Audi")
        set1 = QtCharts.QBarSet("BMW")

        datesAxis = self.calculateDateSeries(self.calcultateFirstDate())

        set0.append([randint(1,200) for x in range(0,len(datesAxis))])
        set1.append([randint(1,200) for x in range(0,len(datesAxis))])

        barSeries = QtCharts.QBarSeries()
        chart = QtCharts.QChart()
        barSeries.append(set0)
        barSeries.append(set1)
        chart.addSeries(barSeries)
        chart.setTitle(title)
        #categories = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]

        chart.createDefaultAxes()

        axisX = QtCharts.QBarCategoryAxis()
        axisX.append(datesAxis)
        chart.setAxisX(axisX, barSeries)
        axisX.setRange(datesAxis[0], datesAxis[len(datesAxis)-1])

        axisY = QtCharts.QValueAxis()
        #chart.setAxisY(axisY, barSeries)


        #axisY.setRange(0, 200)
        chart.legend().setVisible(True)
        chart.legend().setAlignment(Qt.AlignBottom)
        chartView = QtCharts.QChartView(chart)
        chartView.setMinimumSize(700,500)
        #chartView.setMaximumSize(1000,500)
        chartView.setRenderHint(QPainter.Antialiasing)

        return chartView

    def createPercentBarChart(self, title):
        set0 = QtCharts.QBarSet("Audi")
        set1 = QtCharts.QBarSet("BMW")


        datesAxis = self.calculateDateSeries(self.calcultateFirstDate())

        set0.append([randint(1,100) for x in range(0,len(datesAxis))])
        set1.append([randint(1,100) for x in range(0,len(datesAxis))])

        series = QtCharts.QPercentBarSeries()
        series.append(set0)
        series.append(set1)

        chart = QtCharts.QChart()
        chart.addSeries(series)
        chart.setTitle(title)
        chart.setAnimationOptions(QtCharts.QChart.SeriesAnimations)

        axis = QtCharts.QBarCategoryAxis()
        axis.append(datesAxis)
        chart.createDefaultAxes()
        chart.setAxisX(axis, series)

        chart.legend().setVisible(True)
        chart.legend().setAlignment(Qt.AlignBottom)

        chart_view = QtCharts.QChartView(chart)
        chart_view.setMinimumSize(700,500)
        chart_view.setRenderHint(QPainter.Antialiasing)

        return chart_view

    def createLineChart(self, title):

        datesAxis = self.calculateDateSeries(self.calcultateFirstDate())

        lineSeries1 = QtCharts.QLineSeries()
        lineSeries1.setName("Audi")

        lineSeries2 = QtCharts.QLineSeries()
        lineSeries2.setName("BMW")

        for idx in range(0,len(datesAxis)):
            lineSeries1.append(idx,randint(1,200))
            lineSeries2.append(idx,randint(1,200))

        chart = QtCharts.QChart()
        chart.addSeries(lineSeries1)
        chart.addSeries(lineSeries2)
        chart.setTitle(title)

        chart.createDefaultAxes()

        axisX = QtCharts.QBarCategoryAxis()
        axisX.append(datesAxis)
        chart.setAxisX(axisX, lineSeries1)
        chart.setAxisX(axisX, lineSeries2)
        axisX.setRange(datesAxis[0], datesAxis[len(datesAxis)-1])

        axisY = QtCharts.QValueAxis()
        chart.setAxisY(axisY, lineSeries1)
        chart.setAxisY(axisY, lineSeries2)

        #axisY.setRange(0, 200)

        chart.legend().setVisible(True)
        chart.legend().setAlignment(Qt.AlignBottom)
        chartView = QtCharts.QChartView(chart)
        chartView.setMinimumSize(700,500)
        #chartView.setMaximumSize(1000,500)
        chartView.setRenderHint(QPainter.Antialiasing)

        return chartView

    def calcultateFirstDate(self):
        N = 30
        return(datetime.now() - timedelta(days=N))

    def daterange(self,date1, date2):
        for n in range(int ((date2 - date1).days)+1):
            yield date1 + timedelta(n)

    def calculateDateSeries(self,initialDate):

        return  [dt.strftime("%m-%d") for dt in self.daterange(initialDate, datetime.now())]

    def setIcons(self):
        app_icon = QIcon()
        app_icon.addFile('images/logo256.png', QSize(256,256))
        self.window.setWindowIcon(app_icon)


    #def mongodb_conn(self):
    #    try:
    #        self.client = pymongo.MongoClient()
    #    except pymongo.errors.ConnectionFailure as err:
    #        print("Connection failure: {0}".format(err))

    #def __del__(self):
    #    self.client.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    website_analytics = WebsiteAnalytics('mainwindow.ui')
    sys.exit(app.exec_())

