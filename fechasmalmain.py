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

        self.twitter = { "followers": "lines",
                         "averageLikesTwiiter": "lines",
                         "averageRetweets": "lines",
        #                 "accountsReached": "bars",
        #                 "impressions": "bars",
        #                 "tweetingSchedule": "schedule",
        #                 "averageEngRate": "percentage"
        }
#
        #self.facebook = { "totalPageLikes": "lines",
        #       "averageLikesFacebook": "lines",
        #       "averageComments": "lines",
        #       "averageShares": "lines",
        #       "peopleTalking": "bars",
        #       "averageEngagement": "percentage",
        #       "frontPage": "percentage",
        #       "activity": "percentage",
        #       "about": "percentage",
        #       "response": "percentage",
        #       "engagement": "percentage"
        #}
#
        #self.internet = { "strength": "percentage",
        #       "passion": "percentage",
        #       "reach": "percentage",
        #       "sentiment": "lines"
        #}

        with open('config.json', 'r') as f:
            config = json.load(f)
            connection = pymongo.MongoClient(
                config['MONGODB_SERVER'],
                config['MONGODB_PORT']
            )
            db = connection[config['MONGODB_DB']]
            self.collection = db[config['MONGODB_COLLECTION']]
            self.names = config['SEARCH']

        loader = QUiLoader()
        self.window = loader.load(ui_file)
        ui_file.close()

        boton1 = self.window.findChild(QSpinBox, "spinBoxTwitter")
        boton2 = self.window.findChild(QSpinBox, "spinBoxFacebook")
        boton3 = self.window.findChild(QSpinBox, "spinBoxInternet")

        a = self.window.findChild(QVBoxLayout, "TwitterChartsVL")

        for field in self.twitter:
            a.addWidget(self.createChart(field,boton1.value(), self.twitter[field], self.collection))

        b = self.window.findChild(QVBoxLayout, "FacebookChartsVL")
        #for field in self.facebook:
        #    b.addWidget(self.createChart(field,boton2.value(), self.facebook[field], self.collection))

        c = self.window.findChild(QVBoxLayout, "InternetChartsVL")
        #for field in self.internet:
        #    c.addWidget(self.createChart(field,boton3.value(), self.internet[field], self.collection))

        boton1.valueChanged.connect(lambda: self.valueChanged(boton1.value(),a,self.collection))
        boton2.valueChanged.connect(lambda: self.valueChanged(boton2.value(),b,self.collection))
        boton3.valueChanged.connect(lambda: self.valueChanged(boton3.value(),c,self.collection))

        self.setIcons()

        self.window.show()

    def valueChanged(self, days, layout, db):
        #items = [layout.itemAt(index) for index in range(layout.count())]

        for idx in reversed(range(layout.count())):
            layout.itemAt(idx).widget().setParent(None)

        for field in self.twitter:
            layout.addWidget(self.createChart(field,days, self.twitter[field], db))


    def createChart(self, title, days, type, db):

        with open('config.json', 'r') as f:
            config = json.load(f)
            names = config['SEARCH']

        if(type == "lines"):
            datesLookUp = self.DateSeriesMongoDB(self.calcultateFirstDate(days))

            series = []

            for name in names:
                newSeries = QtCharts.QLineSeries()
                newSeries.setName(name)
                series.append(self.fillLineSeries(newSeries, datesLookUp, db, title))


            chart = QtCharts.QChart()
            for serie in series:
                chart.addSeries(serie)

            chart.setTitle(title)

            datesAxis = self.calculateDateSeries(self.calcultateFirstDate(days))
            chart.createDefaultAxes()
            axisX = QtCharts.QBarCategoryAxis()
            axisY = QtCharts.QValueAxis()
            axisX.append(datesAxis)
            axisX.setRange(datesAxis[0], datesAxis[len(datesAxis)-1])

            for serie in series:
                chart.setAxisX(axisX,serie)
                chart.setAxisY(axisY,serie)

            chart.legend().setVisible(True)
            chart.legend().setAlignment(Qt.AlignBottom)
            chartView = QtCharts.QChartView(chart)
            chartView.setMinimumSize(700,500)
            chartView.setRenderHint(QPainter.Antialiasing)

            return chartView

        elif(type == "bars"):

            datesLookUp = self.DateSeriesMongoDB(self.calcultateFirstDate(days))

            series = []

            for name in names:
                newSeries = QtCharts.QBarSet(name)
                series.append(self.fillBarSeries(newSeries, datesLookUp, db, title))

            chart = QtCharts.QChart()
            barSeries = QtCharts.QBarSeries()
            for serie in series:
                barSeries.append(serie)

            chart.setTitle(title)
            chart.addSeries(barSeries)

            datesAxis = self.calculateDateSeries(self.calcultateFirstDate(days))
            chart.createDefaultAxes()

            axisX = QtCharts.QBarCategoryAxis()
            axisX.append(datesAxis)
            chart.setAxisX(axisX,barSeries)
            axisX.setRange(datesAxis[0], datesAxis[len(datesAxis)-1])

            axisY = QtCharts.QValueAxis()

            chart.legend().setVisible(True)
            chart.legend().setAlignment(Qt.AlignBottom)
            chartView = QtCharts.QChartView(chart)
            chartView.setMinimumSize(700,500)
            chartView.setRenderHint(QPainter.Antialiasing)

            return chartView

        elif(type == "percentage"):

            datesLookUp = self.DateSeriesMongoDB(self.calcultateFirstDate(days))
            datesAxis = self.calculateDateSeries(self.calcultateFirstDate(days))

            series = []

            for name in names:
                newSeries = QtCharts.QBarSet(name)
                series.append(self.fillBarSeries(newSeries, datesLookUp, db, title))

            if(len(names) == 1):
                filler = QtCharts.QBarSet("")
                filler.append([100 for item in range(0,len(datesAxis))])
                series.append(filler)

            chart = QtCharts.QChart()
            percentBarSeries = QtCharts.QPercentBarSeries()
            for serie in series:
                percentBarSeries.append(serie)

            chart.setTitle(title)
            chart.addSeries(percentBarSeries)

            chart.createDefaultAxes()

            axisX = QtCharts.QBarCategoryAxis()
            axisX.append(datesAxis)
            chart.setAxisX(axisX,percentBarSeries)
            axisX.setRange(datesAxis[0], datesAxis[len(datesAxis)-1])

            axisY = QtCharts.QValueAxis()

            chart.legend().setVisible(True)
            chart.legend().setAlignment(Qt.AlignBottom)
            chartView = QtCharts.QChartView(chart)
            chartView.setMinimumSize(700,500)
            chartView.setRenderHint(QPainter.Antialiasing)

            return chartView
        elif(type == "schedule"):

            datesLookUp = self.DateSeriesMongoDB(self.calcultateFirstDate(days))
            series = []

            for name in names:
                newSeries = QtCharts.QBarSet(name)
                series.append(self.fillScheduleSeries(newSeries, datesLookUp, db, title))

            chart = QtCharts.QChart()
            barSeries = QtCharts.QBarSeries()
            for serie in series:
                barSeries.append(serie)

            chart.setTitle(title)
            datesAxis = self.scheduleAxis(newSeries, datesLookUp, db, title)
            chart.addSeries(barSeries)

            chart.createDefaultAxes()

            axisX = QtCharts.QBarCategoryAxis()
            axisX.append(datesAxis)
            chart.setAxisX(axisX,barSeries)
            axisX.setRange(datesAxis[0], datesAxis[len(datesAxis)-1])

            axisY = QtCharts.QValueAxis()

            chart.legend().setVisible(True)
            chart.legend().setAlignment(Qt.AlignBottom)
            chartView = QtCharts.QChartView(chart)
            chartView.setMinimumSize(700,500)
            #chartView.setMaximumSize(1000,500)
            chartView.setRenderHint(QPainter.Antialiasing)

            return chartView
        else:
            raise "Wrong chart type"

# TODO : Los axis sean fechas de la bd, no generadas.

    def fillLineSeries(self, series, dateseries, db, title):

        records = db.find({ "date": { '$gte': dateseries[0], '$lt': dateseries[-1]}},{title : 1, '_id' : False})
        values = [int(value[title]) if value else 0 for value in records]

        for idx in range(len(dateseries)):
            series.append(idx, values[idx])

        return series

    def fillBarSeries(self, series, dateseries, db, title):

        records = db.find({ "date": { '$gte': dateseries[0], '$lt': dateseries[-1]}},{title : 1, '_id' : False})
        values = [int(value[title]) if value else 0 for value in records]

        series.append(values)

        return series

    def datesWithData(self, dateseries, db, title):
        records = db.find({ "date": { '$gte': dateseries[0], '$lt': dateseries[-1]}, title : {"$exists" : True}},{"date" : 1, '_id' : False}).limit(len(dateseries)).sort("date", 1).distinct("date")
        #return [dt.strftime("%m-%d") for dt in list(records)]
        return list(records)

    def fillScheduleSeries(self, series, dateseries, db, title):

        records = db.find({ "date": { '$gte': dateseries[0], '$lt': dateseries[-1]}},{title : 1, '_id' : False}).sort("date", -1).limit(1)
        values = [value[title] if value else 0 for value in records].pop(0)

        innerValues = [int(counter[1]) for counter in values]
        series.append(innerValues)

        return series


    def scheduleAxis(self, series, dateseries, db, title):

        records = db.find({ "date": { '$gte': dateseries[0], '$lt': dateseries[-1]}},{title : 1, '_id' : False})
        values = [value for value in records].pop(0)[title]

        innerValues = [int(counter[0]) for counter in values]

        return innerValues

    def calcultateFirstDate(self, days):
        N = days
        return(datetime.now() - timedelta(days=N))

    def daterange(self,date1, date2):
        for n in range(int ((date2 - date1).days)+1):
            yield date1 + timedelta(n)

    def calculateDateSeries(self,initialDate):

        return  [dt.strftime("%m-%d") for dt in self.daterange(initialDate, datetime.now())]

    def DateSeriesMongoDB(self,initialDate):
        return  [dt for dt in self.daterange(initialDate, datetime.now())]

    def setIcons(self):
        app_icon = QIcon()
        app_icon.addFile('images/logo256.png', QSize(256,256))
        self.window.setWindowIcon(app_icon)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    website_analytics = WebsiteAnalytics('mainwindow.ui')
    sys.exit(app.exec_())

