import sys
import pymongo
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

        print(self.mongodb_conn())
        db = self.client.website_analytics.scraped_data
        print(db.find_one())

        loader = QUiLoader()
        self.window = loader.load(ui_file)
        ui_file.close()
        #self.line = self.window.findChild(QTextEdit, "textEdit")
        #self.line.setText("VAYA KKITA")


        a = self.window.findChild(QVBoxLayout, "TwitterChartsVL")

        for i in range(0,2):
            a.addWidget(self.createLineChart())

        b = self.window.findChild(QVBoxLayout, "FacebookChartsVL")

        for i in range(0,2):
            b.addWidget(self.createBarChart())

        c = self.window.findChild(QVBoxLayout, "InternetChartsVL")

        for i in range(0,2):
            c.addWidget(self.createPercentBarChart())


        self.setIcons()
        #self.window.setWindowIcon(QIcon('images/logo256.png'))

        self.window.show()

    def createBarChart(self):

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
        chart.setTitle("Average Likes")
        #categories = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]

        chart.createDefaultAxes()

        axisX = QtCharts.QBarCategoryAxis()
        axisX.append(datesAxis)
        chart.setAxisX(axisX, barSeries)
        axisX.setRange(datesAxis[0], datesAxis[len(datesAxis)-1])

        axisY = QtCharts.QValueAxis()
        #chart.setAxisY(axisY, barSeries)


        axisY.setRange(0, 200)
        chart.legend().setVisible(True)
        chart.legend().setAlignment(Qt.AlignBottom)
        chartView = QtCharts.QChartView(chart)
        chartView.setMinimumSize(700,500)
        #chartView.setMaximumSize(1000,500)
        chartView.setRenderHint(QPainter.Antialiasing)

        return chartView

    def createPercentBarChart(self):
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
        chart.setTitle("Brand Strength")
        chart.setAnimationOptions(QtCharts.QChart.SeriesAnimations)

        axis = QtCharts.QBarCategoryAxis()
        axis.append(datesAxis)
        chart.createDefaultAxes()
        chart.setAxisX(axis, series)

        chart.legend().setVisible(True)
        chart.legend().setAlignment(Qt.AlignBottom)

        chart_view = QtCharts.QChartView(chart)
        chart_view.setRenderHint(QPainter.Antialiasing)

        return chart_view

    def createLineChart(self):

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
        chart.setTitle("Average Retweets")

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

