import folium, io, json, sys, math, random, os
import psycopg2
from folium.plugins import Draw, MousePosition, MeasureControl
from jinja2 import Template
from branca.element import Element
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

malocation = [0,0]

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.resize(600, 600)
        font = QFont('terminus',10)
	
        main = QWidget()
        self.setCentralWidget(main)
        main.setLayout(QVBoxLayout())
        main.setFocusPolicy(Qt.StrongFocus)

        self.tableWidget = QTableWidget()
        self.tableWidget.doubleClicked.connect(self.table_Click)
        self.rows = []

        self.webView = myWebView()
        controls_panel = QHBoxLayout()
        mysplit = QSplitter(Qt.Vertical)
        mysplit.addWidget(self.tableWidget)
        mysplit.addWidget(self.webView)

        main.layout().addLayout(controls_panel)
        main.layout().addWidget(mysplit)

        _label = QLabel('From:', self)
        _label.setFixedSize(40,25)
        _label.setFont(font)
        self.from_box = QComboBox() 
        self.from_box.setFont(font)
        self.from_box.setEditable(True)
        self.from_box.completer().setCompletionMode(QCompleter.PopupCompletion)
        self.from_box.setInsertPolicy(QComboBox.NoInsert)
        controls_panel.addWidget(_label)
        controls_panel.addWidget(self.from_box)

        _label = QLabel('To:', self)
        _label.setFixedSize(20,25)
        _label.setFont(font)
        self.to_box = QComboBox() 
        self.to_box.setFont(font)
        self.to_box.setEditable(True)
        self.to_box.completer().setCompletionMode(QCompleter.PopupCompletion)
        self.to_box.setInsertPolicy(QComboBox.NoInsert)
        controls_panel.addWidget(_label)
        controls_panel.addWidget(self.to_box)

        _label = QLabel('Correspondance:', self)
        _label.setFixedSize(110,25)
        _label.setFont(font)
        self.hop_box = QComboBox() 
        self.hop_box.addItems( ['1', '2', '3', '4', '5'] )
        self.hop_box.setCurrentIndex( 2 )
        controls_panel.addWidget(_label)
        controls_panel.addWidget(self.hop_box)

        _label = QLabel('Transport:', self)
        _label.setFixedSize(65,25)
        _label.setFont(font)
        self.transport_box = QComboBox()
        self.transport_box.setFont(font)
        self.transport_box.addItems(['Tram','Ferry','Bus','Métro','Rail','Tous'])
        self.transport_box.setCurrentIndex( 3 )
        controls_panel.addWidget(_label)
        controls_panel.addWidget(self.transport_box)

        _label = QLabel('Ville:', self)
        _label.setFixedSize(30,25)
        _label.setFont(font)
        self.ville_box = QComboBox()
        self.ville_box.setFont(font)
        self.ville_box.addItems(['Bordeaux','Grenoble','Nantes','Rennes','Toulouse','Paris'])
        self.ville_box.currentTextChanged.connect(self.connect_DB)
        self.ville_box.setCurrentIndex( 0 )
        controls_panel.addWidget(_label)
        controls_panel.addWidget(self.ville_box)

        self.go_button = QPushButton("Go!")
        self.go_button.clicked.connect(self.button_Go)
        self.go_button.setFont(font)
        self.go_button.setFixedSize(30,25)
        controls_panel.addWidget(self.go_button)
           
        self.clear_button = QPushButton("Clear")
        self.clear_button.clicked.connect(self.button_Clear)
        self.clear_button.setFont(font)
        self.clear_button.setFixedSize(50,25)
        controls_panel.addWidget(self.clear_button)

        self.maptype_box = QComboBox()
        self.maptype_box.addItems(self.webView.maptypes)
        self.maptype_box.currentIndexChanged.connect(self.webView.setMap)
        self.maptype_box.setFont(font)
        controls_panel.addWidget(self.maptype_box)
           
        self.connect_DB()

        self.startingpoint = True
                   
        self.show()
        

    def connect_DB(self):
        self.conn = psycopg2.connect(database="matable", user="jonathantable", host="localhost", password="laplaycmieu")
        self.cursor = self.conn.cursor()
        ville = str(self.ville_box.currentText())
        self.from_box.clear()
        self.to_box.clear()

        if ville == 'Bordeaux':
            self.cursor.execute("""SELECT distinct stop_name FROM nodesb ORDER BY stop_name""")
            self.conn.commit()
            rows = self.cursor.fetchall()

            for row in rows : 
                self.from_box.addItem(str(row[0]))
                self.to_box.addItem(str(row[0]))
            self.webView.setMap(4)

        if ville == 'Grenoble':
            self.cursor.execute("""SELECT distinct stop_name FROM nodesg ORDER BY stop_name""")
            self.conn.commit()
            rows = self.cursor.fetchall()

            for row in rows : 
                self.from_box.addItem(str(row[0]))
                self.to_box.addItem(str(row[0]))
            self.webView.setMap(7) 

        if ville == 'Nantes':
            self.cursor.execute("""SELECT distinct stop_name FROM nodesn ORDER BY stop_name""")
            self.conn.commit()
            rows = self.cursor.fetchall()

            for row in rows : 
                self.from_box.addItem(str(row[0]))
                self.to_box.addItem(str(row[0]))
            self.webView.setMap(8)
            
        if ville == 'Rennes':
            self.cursor.execute("""SELECT distinct stop_name FROM nodesr ORDER BY stop_name""")
            self.conn.commit()
            rows = self.cursor.fetchall()

            for row in rows : 
                self.from_box.addItem(str(row[0]))
                self.to_box.addItem(str(row[0]))
            self.webView.setMap(6)

        if ville == 'Toulouse':
            self.cursor.execute("""SELECT distinct stop_name FROM nodest ORDER BY stop_name""")
            self.conn.commit()
            rows = self.cursor.fetchall()

            for row in rows : 
                self.from_box.addItem(str(row[0]))
                self.to_box.addItem(str(row[0]))
            self.webView.setMap(9)
            
        if ville == 'Paris':
            self.cursor.execute("""SELECT distinct stop_name FROM nodesp ORDER BY stop_name""")
            self.conn.commit()
            rows = self.cursor.fetchall()

            for row in rows : 
                self.from_box.addItem(str(row[0]))
                self.to_box.addItem(str(row[0]))
            self.webView.setMap(5)
        


    def table_Click(self):
        k = 0
        prev_lat = 0
        for col in self.rows[self.tableWidget.currentRow()] :
            if (k % 3) == 0:
                lst = col.split(',')
                lat = float(lst[0])
                lon = float(lst[1]) 

                if prev_lat != 0:
                    self.webView.addSegment( prev_lat, prev_lon, lat, lon )
                prev_lat = lat
                prev_lon = lon

                self.webView.addMarker( lat, lon )
            k = k + 1
        

    def button_Go(self):
        #wait = QProgressDialog("Executing Query...", "Cancel", 0, 100, self)
        #self._waiting = QProgressDialog("Executing Query...", "Cancel", 0, 100, self)
        #self._waiting.setWindowModality()
        #waiting.setText("Please Wait")
        #waiting.setIcon(QMessageBox.Information)
        #self._waiting.show()
        #wait.show()
        #self.set_view(self._waiting)

        self.tableWidget.clearContents()

        _fromstation = str(self.from_box.currentText())
        _tostation = str(self.to_box.currentText())
        _hops = int(self.hop_box.currentText())
        _transport_type = str(self.transport_box.currentText())
        _ville = str(self.ville_box.currentText())

        self.rows = []
        if _ville == 'Bordeaux':
            if _transport_type=='Tous':
                if _hops >= 1 : 
                    self.cursor.execute(""f" SELECT (A.latitude,A.longitude) AS coord1, A.stop_name, A.route_name, (B.latitude,B.longitude) AS coord2, B.stop_name FROM (SELECT marouteb.latitude, marouteb.longitude, stop_name, route_name, route_type FROM nodesb, marouteb WHERE nodesb.longitude=marouteb.longitude AND nodesb.latitude=marouteb.latitude) AS A , (SELECT marouteb.latitude, marouteb.longitude, stop_name, route_name, route_type FROM nodesb, marouteb WHERE nodesb.longitude=marouteb.longitude AND nodesb.latitude=marouteb.latitude) AS B WHERE A.stop_name=$${_fromstation}$$ AND B.stop_name=$${_tostation}$$ AND A.route_name=B.route_name AND A.stop_name<>B.stop_name""")
                    self.conn.commit()
                    self.rows += self.cursor.fetchall()

                if _hops >= 2 : 
                    self.cursor.execute (""f"SELECT (A.latitude,A.longitude) AS coord1, A.stop_name, A.route_name, (B.latitude,B.longitude) AS coord2, B.stop_name, D.route_name, (D.latitude,D.longitude) AS coord3, D.stop_name FROM (SELECT marouteb.latitude, marouteb.longitude, stop_name, route_name, route_type FROM nodesb, marouteb WHERE nodesb.longitude=marouteb.longitude AND nodesb.latitude=marouteb.latitude) AS A, (SELECT marouteb.latitude, marouteb.longitude, stop_name, route_name, route_type FROM nodesb, marouteb WHERE nodesb.longitude=marouteb.longitude AND nodesb.latitude=marouteb.latitude) AS B, (SELECT marouteb.latitude, marouteb.longitude, stop_name, route_name, route_type FROM nodesb, marouteb WHERE nodesb.longitude=marouteb.longitude AND nodesb.latitude=marouteb.latitude) AS C , (SELECT marouteb.latitude, marouteb.longitude, stop_name, route_name, route_type FROM nodesb, marouteb WHERE nodesb.longitude=marouteb.longitude AND nodesb.latitude=marouteb.latitude) AS D WHERE A.stop_name=$${_fromstation}$$ AND D.stop_name=$${_tostation}$$ AND A.route_name=B.route_name AND B.stop_name=C.stop_name AND C.route_name=D.route_name AND A.route_name<>C.route_name""")
                    self.conn.commit()
                    self.rows += self.cursor.fetchall()

                if _hops >= 3 : 
                    self.cursor.execute(""f"SELECT (A.latitude,A.longitude) AS coord1, A.stop_name, A.route_name, (B.latitude,B.longitude) AS coord2, B.stop_name, D.route_name, (D.latitude,D.longitude) AS coord3, D.stop_name, F.route_name, (F.latitude, F.longitude) AS coord4, F.stop_name FROM (SELECT marouteb.latitude, marouteb.longitude, stop_name, route_name, route_type FROM nodesb, marouteb WHERE nodesb.longitude=marouteb.longitude AND nodesb.latitude=marouteb.latitude) AS A , (SELECT marouteb.latitude, marouteb.longitude, stop_name, route_name, route_type FROM nodesb, marouteb WHERE nodesb.longitude=marouteb.longitude AND nodesb.latitude=marouteb.latitude) AS B , (SELECT marouteb.latitude, marouteb.longitude, stop_name, route_name, route_type FROM nodesb, marouteb WHERE nodesb.longitude=marouteb.longitude AND nodesb.latitude=marouteb.latitude) AS C , (SELECT marouteb.latitude, marouteb.longitude, stop_name, route_name, route_type FROM nodesb, marouteb WHERE nodesb.longitude=marouteb.longitude AND nodesb.latitude=marouteb.latitude) AS D, (SELECT marouteb.latitude, marouteb.longitude, stop_name, route_name, route_type FROM nodesb, marouteb WHERE nodesb.longitude=marouteb.longitude AND nodesb.latitude=marouteb.latitude) AS E , (SELECT marouteb.latitude, marouteb.longitude, stop_name, route_name, route_type FROM nodesb, marouteb WHERE nodesb.longitude=marouteb.longitude AND nodesb.latitude=marouteb.latitude) AS F WHERE A.stop_name=$${_fromstation}$$ AND F.stop_name=$${_tostation}$$ AND A.route_name=B.route_name AND B.stop_name=C.stop_name AND C.route_name=D.route_name AND D.stop_name=E.stop_name AND E.route_name=F.route_name AND A.route_name<>C.route_name AND C.route_name<>F.route_name""")
                    self.conn.commit()
                    self.rows += self.cursor.fetchall()

            if _transport_type=='Bus':
                if _hops >= 1 : 
                    self.cursor.execute(""f" SELECT (A.latitude,A.longitude) AS coord1, A.stop_name, A.route_name, (B.latitude,B.longitude) AS coord2, B.stop_name FROM (SELECT marouteb.latitude, marouteb.longitude, stop_name, route_name, route_type FROM nodesb, marouteb WHERE nodesb.longitude=marouteb.longitude AND nodesb.latitude=marouteb.latitude) AS A , (SELECT marouteb.latitude, marouteb.longitude, stop_name, route_name, route_type FROM nodesb, marouteb WHERE nodesb.longitude=marouteb.longitude AND nodesb.latitude=marouteb.latitude) AS B WHERE A.stop_name=$${_fromstation}$$ AND B.stop_name=$${_tostation}$$ AND A.route_name=B.route_name AND A.stop_name<>B.stop_name AND A.route_type=3""")
                    self.conn.commit()
                    self.rows += self.cursor.fetchall()

                if _hops >= 2 : 
                    self.cursor.execute (""f"SELECT (A.latitude,A.longitude) AS coord1, A.stop_name, A.route_name, (B.latitude,B.longitude) AS coord2, B.stop_name, D.route_name, (D.latitude,D.longitude) AS coord3, D.stop_name FROM (SELECT marouteb.latitude, marouteb.longitude, stop_name, route_name, route_type FROM nodesb, marouteb WHERE nodesb.longitude=marouteb.longitude AND nodesb.latitude=marouteb.latitude) AS A, (SELECT marouteb.latitude, marouteb.longitude, stop_name, route_name, route_type FROM nodesb, marouteb WHERE nodesb.longitude=marouteb.longitude AND nodesb.latitude=marouteb.latitude) AS B, (SELECT marouteb.latitude, marouteb.longitude, stop_name, route_name, route_type FROM nodesb, marouteb WHERE nodesb.longitude=marouteb.longitude AND nodesb.latitude=marouteb.latitude) AS C , (SELECT marouteb.latitude, marouteb.longitude, stop_name, route_name, route_type FROM nodesb, marouteb WHERE nodesb.longitude=marouteb.longitude AND nodesb.latitude=marouteb.latitude) AS D WHERE A.stop_name=$${_fromstation}$$ AND D.stop_name=$${_tostation}$$ AND A.route_name=B.route_name AND B.stop_name=C.stop_name AND C.route_name=D.route_name AND A.route_name<>C.route_name AND A.route_type=3 AND D.route_type=3""")
                    self.conn.commit()
                    self.rows += self.cursor.fetchall()

                if _hops >= 3 : 
                    self.cursor.execute(""f"SELECT (A.latitude,A.longitude) AS coord1, A.stop_name, A.route_name, (B.latitude,B.longitude) AS coord2, B.stop_name, D.route_name, (D.latitude,D.longitude) AS coord3, D.stop_name, F.route_name, (F.latitude, F.longitude) AS coord4, F.stop_name FROM (SELECT marouteb.latitude, marouteb.longitude, stop_name, route_name, route_type FROM nodesb, marouteb WHERE nodesb.longitude=marouteb.longitude AND nodesb.latitude=marouteb.latitude) AS A , (SELECT marouteb.latitude, marouteb.longitude, stop_name, route_name, route_type FROM nodesb, marouteb WHERE nodesb.longitude=marouteb.longitude AND nodesb.latitude=marouteb.latitude) AS B , (SELECT marouteb.latitude, marouteb.longitude, stop_name, route_name, route_type FROM nodesb, marouteb WHERE nodesb.longitude=marouteb.longitude AND nodesb.latitude=marouteb.latitude) AS C , (SELECT marouteb.latitude, marouteb.longitude, stop_name, route_name, route_type FROM nodesb, marouteb WHERE nodesb.longitude=marouteb.longitude AND nodesb.latitude=marouteb.latitude) AS D, (SELECT marouteb.latitude, marouteb.longitude, stop_name, route_name, route_type FROM nodesb, marouteb WHERE nodesb.longitude=marouteb.longitude AND nodesb.latitude=marouteb.latitude) AS E , (SELECT marouteb.latitude, marouteb.longitude, stop_name, route_name, route_type FROM nodesb, marouteb WHERE nodesb.longitude=marouteb.longitude AND nodesb.latitude=marouteb.latitude) AS F WHERE A.stop_name=$${_fromstation}$$ AND F.stop_name=$${_tostation}$$ AND A.route_name=B.route_name AND B.stop_name=C.stop_name AND C.route_name=D.route_name AND D.stop_name=E.stop_name AND E.route_name=F.route_name AND A.route_name<>C.route_name AND C.route_name<>F.route_name AND A.route_type=3 AND D.route_type=3 AND F.route_type=3""")
                    self.conn.commit()
                    self.rows += self.cursor.fetchall()

            if _transport_type=='Tram':
                if _hops >= 1 : 
                    self.cursor.execute(""f" SELECT (A.latitude,A.longitude) AS coord1, A.stop_name, A.route_name, (B.latitude,B.longitude) AS coord2, B.stop_name FROM (SELECT marouteb.latitude, marouteb.longitude, stop_name, route_name, route_type FROM nodesb, marouteb WHERE nodesb.longitude=marouteb.longitude AND nodesb.latitude=marouteb.latitude) AS A , (SELECT marouteb.latitude, marouteb.longitude, stop_name, route_name, route_type FROM nodesb, marouteb WHERE nodesb.longitude=marouteb.longitude AND nodesb.latitude=marouteb.latitude) AS B WHERE A.stop_name=$${_fromstation}$$ AND B.stop_name=$${_tostation}$$ AND A.route_name=B.route_name AND A.stop_name<>B.stop_name AND A.route_type=0""")
                    self.conn.commit()
                    self.rows += self.cursor.fetchall()

                if _hops >= 2 : 
                    self.cursor.execute (""f"SELECT (A.latitude,A.longitude) AS coord1, A.stop_name, A.route_name, (B.latitude,B.longitude) AS coord2, B.stop_name, D.route_name, (D.latitude,D.longitude) AS coord3, D.stop_name FROM (SELECT marouteb.latitude, marouteb.longitude, stop_name, route_name, route_type FROM nodesb, marouteb WHERE nodesb.longitude=marouteb.longitude AND nodesb.latitude=marouteb.latitude) AS A, (SELECT marouteb.latitude, marouteb.longitude, stop_name, route_name, route_type FROM nodesb, marouteb WHERE nodesb.longitude=marouteb.longitude AND nodesb.latitude=marouteb.latitude) AS B, (SELECT marouteb.latitude, marouteb.longitude, stop_name, route_name, route_type FROM nodesb, marouteb WHERE nodesb.longitude=marouteb.longitude AND nodesb.latitude=marouteb.latitude) AS C , (SELECT marouteb.latitude, marouteb.longitude, stop_name, route_name, route_type FROM nodesb, marouteb WHERE nodesb.longitude=marouteb.longitude AND nodesb.latitude=marouteb.latitude) AS D WHERE A.stop_name=$${_fromstation}$$ AND D.stop_name=$${_tostation}$$ AND A.route_name=B.route_name AND B.stop_name=C.stop_name AND C.route_name=D.route_name AND A.route_name<>C.route_name AND A.route_type=0 AND D.route_type=0""")
                    self.conn.commit()
                    self.rows += self.cursor.fetchall()

                if _hops >= 3 : 
                    self.cursor.execute(""f"SELECT (A.latitude,A.longitude) AS coord1, A.stop_name, A.route_name, (B.latitude,B.longitude) AS coord2, B.stop_name, D.route_name, (D.latitude,D.longitude) AS coord3, D.stop_name, F.route_name, (F.latitude, F.longitude) AS coord4, F.stop_name FROM (SELECT marouteb.latitude, marouteb.longitude, stop_name, route_name, route_type FROM nodesb, marouteb WHERE nodesb.longitude=marouteb.longitude AND nodesb.latitude=marouteb.latitude) AS A , (SELECT marouteb.latitude, marouteb.longitude, stop_name, route_name, route_type FROM nodesb, marouteb WHERE nodesb.longitude=marouteb.longitude AND nodesb.latitude=marouteb.latitude) AS B , (SELECT marouteb.latitude, marouteb.longitude, stop_name, route_name, route_type FROM nodesb, marouteb WHERE nodesb.longitude=marouteb.longitude AND nodesb.latitude=marouteb.latitude) AS C , (SELECT marouteb.latitude, marouteb.longitude, stop_name, route_name, route_type FROM nodesb, marouteb WHERE nodesb.longitude=marouteb.longitude AND nodesb.latitude=marouteb.latitude) AS D, (SELECT marouteb.latitude, marouteb.longitude, stop_name, route_name, route_type FROM nodesb, marouteb WHERE nodesb.longitude=marouteb.longitude AND nodesb.latitude=marouteb.latitude) AS E , (SELECT marouteb.latitude, marouteb.longitude, stop_name, route_name, route_type FROM nodesb, marouteb WHERE nodesb.longitude=marouteb.longitude AND nodesb.latitude=marouteb.latitude) AS F WHERE A.stop_name=$${_fromstation}$$ AND F.stop_name=$${_tostation}$$ AND A.route_name=B.route_name AND B.stop_name=C.stop_name AND C.route_name=D.route_name AND D.stop_name=E.stop_name AND E.route_name=F.route_name AND A.route_name<>C.route_name AND C.route_name<>F.route_name AND A.route_type=0 AND D.route_type=0 AND F.route_type=0""")
                    self.conn.commit()
                    self.rows += self.cursor.fetchall()

            if _transport_type=='Ferry':
                if _hops >= 1 : 
                    self.cursor.execute(""f" SELECT (A.latitude,A.longitude) AS coord1, A.stop_name, A.route_name, (B.latitude,B.longitude) AS coord2, B.stop_name FROM (SELECT marouteb.latitude, marouteb.longitude, stop_name, route_name, route_type FROM nodesb, marouteb WHERE nodesb.longitude=marouteb.longitude AND nodesb.latitude=marouteb.latitude) AS A , (SELECT marouteb.latitude, marouteb.longitude, stop_name, route_name, route_type FROM nodesb, marouteb WHERE nodesb.longitude=marouteb.longitude AND nodesb.latitude=marouteb.latitude) AS B WHERE A.stop_name=$${_fromstation}$$ AND B.stop_name=$${_tostation}$$ AND A.route_name=B.route_name AND A.stop_name<>B.stop_name AND A.route_type=4""")
                    self.conn.commit()
                    self.rows += self.cursor.fetchall()

                if _hops >= 2 : 
                    self.cursor.execute (""f"SELECT (A.latitude,A.longitude) AS coord1, A.stop_name, A.route_name, (B.latitude,B.longitude) AS coord2, B.stop_name, D.route_name, (D.latitude,D.longitude) AS coord3, D.stop_name FROM (SELECT marouteb.latitude, marouteb.longitude, stop_name, route_name , route_type FROM nodesb, marouteb WHERE nodesb.longitude=marouteb.longitude AND nodesb.latitude=marouteb.latitude) AS A, (SELECT marouteb.latitude, marouteb.longitude, stop_name, route_name, route_type FROM nodesb, marouteb WHERE nodesb.longitude=marouteb.longitude AND nodesb.latitude=marouteb.latitude) AS B, (SELECT marouteb.latitude, marouteb.longitude, stop_name, route_name, route_type FROM nodesb, marouteb WHERE nodesb.longitude=marouteb.longitude AND nodesb.latitude=marouteb.latitude) AS C , (SELECT marouteb.latitude, marouteb.longitude, stop_name, route_name, route_type FROM nodesb, marouteb WHERE nodesb.longitude=marouteb.longitude AND nodesb.latitude=marouteb.latitude) AS D WHERE A.stop_name=$${_fromstation}$$ AND D.stop_name=$${_tostation}$$ AND A.route_name=B.route_name AND B.stop_name=C.stop_name AND C.route_name=D.route_name AND A.route_name<>C.route_name AND A.route_type=4 AND D.route_type=4""")
                    self.conn.commit()
                    self.rows += self.cursor.fetchall()

                if _hops >= 3 : 
                    self.cursor.execute(""f"SELECT (A.latitude,A.longitude) AS coord1, A.stop_name, A.route_name, (B.latitude,B.longitude) AS coord2, B.stop_name, D.route_name, (D.latitude,D.longitude) AS coord3, D.stop_name, F.route_name, (F.latitude, F.longitude) AS coord4, F.stop_name FROM (SELECT marouteb.latitude, marouteb.longitude, stop_name, route_name, route_type FROM nodesb, marouteb WHERE nodesb.longitude=marouteb.longitude AND nodesb.latitude=marouteb.latitude) AS A , (SELECT marouteb.latitude, marouteb.longitude, stop_name, route_name, route_type FROM nodesb, marouteb WHERE nodesb.longitude=marouteb.longitude AND nodesb.latitude=marouteb.latitude) AS B , (SELECT marouteb.latitude, marouteb.longitude, stop_name, route_name, route_type FROM nodesb, marouteb WHERE nodesb.longitude=marouteb.longitude AND nodesb.latitude=marouteb.latitude) AS C , (SELECT marouteb.latitude, marouteb.longitude, stop_name, route_name, route_type FROM nodesb, marouteb WHERE nodesb.longitude=marouteb.longitude AND nodesb.latitude=marouteb.latitude) AS D, (SELECT marouteb.latitude, marouteb.longitude, stop_name, route_name, route_type FROM nodesb, marouteb WHERE nodesb.longitude=marouteb.longitude AND nodesb.latitude=marouteb.latitude) AS E , (SELECT marouteb.latitude, marouteb.longitude, stop_name, route_name, route_type FROM nodesb, marouteb WHERE nodesb.longitude=marouteb.longitude AND nodesb.latitude=marouteb.latitude) AS F WHERE A.stop_name=$${_fromstation}$$ AND F.stop_name=$${_tostation}$$ AND A.route_name=B.route_name AND B.stop_name=C.stop_name AND C.route_name=D.route_name AND D.stop_name=E.stop_name AND E.route_name=F.route_name AND A.route_name<>C.route_name AND C.route_name<>F.route_name AND A.route_type=4 AND D.route_type=4 AND F.route_type=4""")
                    self.conn.commit()
                    self.rows += self.cursor.fetchall()

        if _ville == 'Grenoble':
            if _transport_type=='Tous':
                if _hops >= 1 : 
                    self.cursor.execute(""f" SELECT (A.latitude,A.longitude) AS coord1, A.stop_name, A.route_name, (B.latitude,B.longitude) AS coord2, B.stop_name FROM (SELECT marouteg.latitude, marouteg.longitude, stop_name, route_name, route_type FROM nodesg, marouteg WHERE nodesg.longitude=marouteg.longitude AND nodesg.latitude=marouteg.latitude) AS A , (SELECT marouteg.latitude, marouteg.longitude, stop_name, route_name, route_type FROM nodesg, marouteg WHERE nodesg.longitude=marouteg.longitude AND nodesg.latitude=marouteg.latitude) AS B WHERE A.stop_name=$${_fromstation}$$ AND B.stop_name=$${_tostation}$$ AND A.route_name=B.route_name AND A.stop_name<>B.stop_name""")
                    self.conn.commit()
                    self.rows += self.cursor.fetchall()

                if _hops >= 2 : 
                    self.cursor.execute (""f"SELECT (A.latitude,A.longitude) AS coord1, A.stop_name, A.route_name, (B.latitude,B.longitude) AS coord2, B.stop_name, D.route_name, (D.latitude,D.longitude) AS coord3, D.stop_name FROM (SELECT marouteg.latitude, marouteg.longitude, stop_name, route_name, route_type FROM nodesg, marouteg WHERE nodesg.longitude=marouteg.longitude AND nodesg.latitude=marouteg.latitude) AS A, (SELECT marouteg.latitude, marouteg.longitude, stop_name, route_name, route_type FROM nodesg, marouteg WHERE nodesg.longitude=marouteg.longitude AND nodesg.latitude=marouteg.latitude) AS B, (SELECT marouteg.latitude, marouteg.longitude, stop_name, route_name, route_type FROM nodesg, marouteg WHERE nodesg.longitude=marouteg.longitude AND nodesg.latitude=marouteg.latitude) AS C , (SELECT marouteg.latitude, marouteg.longitude, stop_name, route_name, route_type FROM nodesg, marouteg WHERE nodesg.longitude=marouteg.longitude AND nodesg.latitude=marouteg.latitude) AS D WHERE A.stop_name=$${_fromstation}$$ AND D.stop_name=$${_tostation}$$ AND A.route_name=B.route_name AND B.stop_name=C.stop_name AND C.route_name=D.route_name AND A.route_name<>C.route_name""")
                    self.conn.commit()
                    self.rows += self.cursor.fetchall()

                if _hops >= 3 : 
                    self.cursor.execute(""f"SELECT (A.latitude,A.longitude) AS coord1, A.stop_name, A.route_name, (B.latitude,B.longitude) AS coord2, B.stop_name, D.route_name, (D.latitude,D.longitude) AS coord3, D.stop_name, F.route_name, (F.latitude, F.longitude) AS coord4, F.stop_name FROM (SELECT marouteg.latitude, marouteg.longitude, stop_name, route_name, route_type FROM nodesg, marouteg WHERE nodesg.longitude=marouteg.longitude AND nodesg.latitude=marouteg.latitude) AS A , (SELECT marouteg.latitude, marouteg.longitude, stop_name, route_name, route_type FROM nodesg, marouteg WHERE nodesg.longitude=marouteg.longitude AND nodesg.latitude=marouteg.latitude) AS B , (SELECT marouteg.latitude, marouteg.longitude, stop_name, route_name, route_type FROM nodesg, marouteg WHERE nodesg.longitude=marouteg.longitude AND nodesg.latitude=marouteg.latitude) AS C , (SELECT marouteg.latitude, marouteg.longitude, stop_name, route_name, route_type FROM nodesg, marouteg WHERE nodesg.longitude=marouteg.longitude AND nodesg.latitude=marouteg.latitude) AS D, (SELECT marouteg.latitude, marouteg.longitude, stop_name, route_name, route_type FROM nodesg, marouteg WHERE nodesg.longitude=marouteg.longitude AND nodesg.latitude=marouteg.latitude) AS E , (SELECT marouteg.latitude, marouteg.longitude, stop_name, route_name, route_type FROM nodesg, marouteg WHERE nodesg.longitude=marouteg.longitude AND nodesg.latitude=marouteg.latitude) AS F WHERE A.stop_name=$${_fromstation}$$ AND F.stop_name=$${_tostation}$$ AND A.route_name=B.route_name AND B.stop_name=C.stop_name AND C.route_name=D.route_name AND D.stop_name=E.stop_name AND E.route_name=F.route_name AND A.route_name<>C.route_name AND C.route_name<>F.route_name""")
                    self.conn.commit()
                    self.rows += self.cursor.fetchall()

            if _transport_type=='Bus':
                if _hops >= 1 : 
                    self.cursor.execute(""f" SELECT (A.latitude,A.longitude) AS coord1, A.stop_name, A.route_name, (B.latitude,B.longitude) AS coord2, B.stop_name FROM (SELECT marouteg.latitude, marouteg.longitude, stop_name, route_name, route_type FROM nodesg, marouteg WHERE nodesg.longitude=marouteg.longitude AND nodesg.latitude=marouteg.latitude) AS A , (SELECT marouteg.latitude, marouteg.longitude, stop_name, route_name, route_type FROM nodesg, marouteg WHERE nodesg.longitude=marouteg.longitude AND nodesg.latitude=marouteg.latitude) AS B WHERE A.stop_name=$${_fromstation}$$ AND B.stop_name=$${_tostation}$$ AND A.route_name=B.route_name AND A.stop_name<>B.stop_name AND A.route_type=3""")
                    self.conn.commit()
                    self.rows += self.cursor.fetchall()

                if _hops >= 2 : 
                    self.cursor.execute (""f"SELECT (A.latitude,A.longitude) AS coord1, A.stop_name, A.route_name, (B.latitude,B.longitude) AS coord2, B.stop_name, D.route_name, (D.latitude,D.longitude) AS coord3, D.stop_name FROM (SELECT marouteg.latitude, marouteg.longitude, stop_name, route_name, route_type FROM nodesg, marouteg WHERE nodesg.longitude=marouteg.longitude AND nodesg.latitude=marouteg.latitude) AS A, (SELECT marouteg.latitude, marouteg.longitude, stop_name, route_name, route_type FROM nodesg, marouteg WHERE nodesg.longitude=marouteg.longitude AND nodesg.latitude=marouteg.latitude) AS B, (SELECT marouteg.latitude, marouteg.longitude, stop_name, route_name, route_type FROM nodesg, marouteg WHERE nodesg.longitude=marouteg.longitude AND nodesg.latitude=marouteg.latitude) AS C , (SELECT marouteg.latitude, marouteg.longitude, stop_name, route_name, route_type FROM nodesg, marouteg WHERE nodesg.longitude=marouteg.longitude AND nodesg.latitude=marouteg.latitude) AS D WHERE A.stop_name=$${_fromstation}$$ AND D.stop_name=$${_tostation}$$ AND A.route_name=B.route_name AND B.stop_name=C.stop_name AND C.route_name=D.route_name AND A.route_name<>C.route_name AND A.route_type=3 AND D.route_type=3""")
                    self.conn.commit()
                    self.rows += self.cursor.fetchall()

                if _hops >= 3 : 
                    self.cursor.execute(""f"SELECT (A.latitude,A.longitude) AS coord1, A.stop_name, A.route_name, (B.latitude,B.longitude) AS coord2, B.stop_name, D.route_name, (D.latitude,D.longitude) AS coord3, D.stop_name, F.route_name, (F.latitude, F.longitude) AS coord4, F.stop_name FROM (SELECT marouteg.latitude, marouteg.longitude, stop_name, route_name, route_type FROM nodesg, marouteg WHERE nodesg.longitude=marouteg.longitude AND nodesg.latitude=marouteg.latitude) AS A , (SELECT marouteg.latitude, marouteg.longitude, stop_name, route_name, route_type FROM nodesg, marouteg WHERE nodesg.longitude=marouteg.longitude AND nodesg.latitude=marouteg.latitude) AS B , (SELECT marouteg.latitude, marouteg.longitude, stop_name, route_name, route_type FROM nodesg, marouteg WHERE nodesg.longitude=marouteg.longitude AND nodesg.latitude=marouteg.latitude) AS C , (SELECT marouteg.latitude, marouteg.longitude, stop_name, route_name, route_type FROM nodesg, marouteg WHERE nodesg.longitude=marouteg.longitude AND nodesg.latitude=marouteg.latitude) AS D, (SELECT marouteg.latitude, marouteg.longitude, stop_name, route_name, route_type FROM nodesg, marouteg WHERE nodesg.longitude=marouteg.longitude AND nodesg.latitude=marouteg.latitude) AS E , (SELECT marouteg.latitude, marouteg.longitude, stop_name, route_name, route_type FROM nodesg, marouteg WHERE nodesg.longitude=marouteg.longitude AND nodesg.latitude=marouteg.latitude) AS F WHERE A.stop_name=$${_fromstation}$$ AND F.stop_name=$${_tostation}$$ AND A.route_name=B.route_name AND B.stop_name=C.stop_name AND C.route_name=D.route_name AND D.stop_name=E.stop_name AND E.route_name=F.route_name AND A.route_name<>C.route_name AND C.route_name<>F.route_name AND A.route_type=3 AND D.route_type=3 AND F.route_type=3""")
                    self.conn.commit()
                    self.rows += self.cursor.fetchall()

            if _transport_type=='Tram':
                if _hops >= 1 : 
                    self.cursor.execute(""f" SELECT (A.latitude,A.longitude) AS coord1, A.stop_name, A.route_name, (B.latitude,B.longitude) AS coord2, B.stop_name FROM (SELECT marouteg.latitude, marouteg.longitude, stop_name, route_name, route_type FROM nodesg, marouteg WHERE nodesg.longitude=marouteg.longitude AND nodesg.latitude=marouteg.latitude) AS A , (SELECT marouteg.latitude, marouteg.longitude, stop_name, route_name, route_type FROM nodesg, marouteg WHERE nodesg.longitude=marouteg.longitude AND nodesg.latitude=marouteg.latitude) AS B WHERE A.stop_name=$${_fromstation}$$ AND B.stop_name=$${_tostation}$$ AND A.route_name=B.route_name AND A.stop_name<>B.stop_name AND A.route_type=0""")
                    self.conn.commit()
                    self.rows += self.cursor.fetchall()

                if _hops >= 2 : 
                    self.cursor.execute (""f"SELECT (A.latitude,A.longitude) AS coord1, A.stop_name, A.route_name, (B.latitude,B.longitude) AS coord2, B.stop_name, D.route_name, (D.latitude,D.longitude) AS coord3, D.stop_name FROM (SELECT marouteg.latitude, marouteg.longitude, stop_name, route_name, route_type FROM nodesg, marouteg WHERE nodesg.longitude=marouteg.longitude AND nodesg.latitude=marouteg.latitude) AS A, (SELECT marouteg.latitude, marouteg.longitude, stop_name, route_name, route_type FROM nodesg, marouteg WHERE nodesg.longitude=marouteg.longitude AND nodesg.latitude=marouteg.latitude) AS B, (SELECT marouteg.latitude, marouteg.longitude, stop_name, route_name, route_type FROM nodesg, marouteg WHERE nodesg.longitude=marouteg.longitude AND nodesg.latitude=marouteg.latitude) AS C , (SELECT marouteg.latitude, marouteg.longitude, stop_name, route_name, route_type FROM nodesg, marouteg WHERE nodesg.longitude=marouteg.longitude AND nodesg.latitude=marouteg.latitude) AS D WHERE A.stop_name=$${_fromstation}$$ AND D.stop_name=$${_tostation}$$ AND A.route_name=B.route_name AND B.stop_name=C.stop_name AND C.route_name=D.route_name AND A.route_name<>C.route_name AND A.route_type=0 AND D.route_type=0""")
                    self.conn.commit()
                    self.rows += self.cursor.fetchall()

                if _hops >= 3 : 
                    self.cursor.execute(""f"SELECT (A.latitude,A.longitude) AS coord1, A.stop_name, A.route_name, (B.latitude,B.longitude) AS coord2, B.stop_name, D.route_name, (D.latitude,D.longitude) AS coord3, D.stop_name, F.route_name, (F.latitude, F.longitude) AS coord4, F.stop_name FROM (SELECT marouteg.latitude, marouteg.longitude, stop_name, route_name, route_type FROM nodesg, marouteg WHERE nodesg.longitude=marouteg.longitude AND nodesg.latitude=marouteg.latitude) AS A , (SELECT marouteg.latitude, marouteg.longitude, stop_name, route_name, route_type FROM nodesg, marouteg WHERE nodesg.longitude=marouteg.longitude AND nodesg.latitude=marouteg.latitude) AS B , (SELECT marouteg.latitude, marouteg.longitude, stop_name, route_name, route_type FROM nodesg, marouteg WHERE nodesg.longitude=marouteg.longitude AND nodesg.latitude=marouteg.latitude) AS C , (SELECT marouteg.latitude, marouteg.longitude, stop_name, route_name, route_type FROM nodesg, marouteg WHERE nodesg.longitude=marouteg.longitude AND nodesg.latitude=marouteg.latitude) AS D, (SELECT marouteg.latitude, marouteg.longitude, stop_name, route_name, route_type FROM nodesg, marouteg WHERE nodesg.longitude=marouteg.longitude AND nodesg.latitude=marouteg.latitude) AS E , (SELECT marouteg.latitude, marouteg.longitude, stop_name, route_name, route_type FROM nodesg, marouteg WHERE nodesg.longitude=marouteg.longitude AND nodesg.latitude=marouteg.latitude) AS F WHERE A.stop_name=$${_fromstation}$$ AND F.stop_name=$${_tostation}$$ AND A.route_name=B.route_name AND B.stop_name=C.stop_name AND C.route_name=D.route_name AND D.stop_name=E.stop_name AND E.route_name=F.route_name AND A.route_name<>C.route_name AND C.route_name<>F.route_name AND A.route_type=0 AND D.route_type=0 AND F.route_type=0""")
                    self.conn.commit()
                    self.rows += self.cursor.fetchall()
        if _ville == 'Nantes':
            if _transport_type=='Tous':
                if _hops >= 1 : 
                    self.cursor.execute(""f" SELECT (A.latitude,A.longitude) AS coord1, A.stop_name, A.route_name, (B.latitude,B.longitude) AS coord2, B.stop_name FROM (SELECT marouten.latitude, marouten.longitude, stop_name, route_name, route_type FROM nodesn, marouten WHERE nodesn.longitude=marouten.longitude AND nodesn.latitude=marouten.latitude) AS A , (SELECT marouten.latitude, marouten.longitude, stop_name, route_name, route_type FROM nodesn, marouten WHERE nodesn.longitude=marouten.longitude AND nodesn.latitude=marouten.latitude) AS B WHERE A.stop_name=$${_fromstation}$$ AND B.stop_name=$${_tostation}$$ AND A.route_name=B.route_name AND A.stop_name<>B.stop_name""")
                    self.conn.commit()
                    self.rows += self.cursor.fetchall()

                if _hops >= 2 : 
                    self.cursor.execute (""f"SELECT (A.latitude,A.longitude) AS coord1, A.stop_name, A.route_name, (B.latitude,B.longitude) AS coord2, B.stop_name, D.route_name, (D.latitude,D.longitude) AS coord3, D.stop_name FROM (SELECT marouten.latitude, marouten.longitude, stop_name, route_name, route_type FROM nodesn, marouten WHERE nodesn.longitude=marouten.longitude AND nodesn.latitude=marouten.latitude) AS A, (SELECT marouten.latitude, marouten.longitude, stop_name, route_name, route_type FROM nodesn, marouten WHERE nodesn.longitude=marouten.longitude AND nodesn.latitude=marouten.latitude) AS B, (SELECT marouten.latitude, marouten.longitude, stop_name, route_name, route_type FROM nodesn, marouten WHERE nodesn.longitude=marouten.longitude AND nodesn.latitude=marouten.latitude) AS C , (SELECT marouten.latitude, marouten.longitude, stop_name, route_name, route_type FROM nodesn, marouten WHERE nodesn.longitude=marouten.longitude AND nodesn.latitude=marouten.latitude) AS D WHERE A.stop_name=$${_fromstation}$$ AND D.stop_name=$${_tostation}$$ AND A.route_name=B.route_name AND B.stop_name=C.stop_name AND C.route_name=D.route_name AND A.route_name<>C.route_name""")
                    self.conn.commit()
                    self.rows += self.cursor.fetchall()

                if _hops >= 3 : 
                    self.cursor.execute(""f"SELECT (A.latitude,A.longitude) AS coord1, A.stop_name, A.route_name, (B.latitude,B.longitude) AS coord2, B.stop_name, D.route_name, (D.latitude,D.longitude) AS coord3, D.stop_name, F.route_name, (F.latitude, F.longitude) AS coord4, F.stop_name FROM (SELECT marouten.latitude, marouten.longitude, stop_name, route_name, route_type FROM nodesn, marouten WHERE nodesn.longitude=marouten.longitude AND nodesn.latitude=marouten.latitude) AS A , (SELECT marouten.latitude, marouten.longitude, stop_name, route_name, route_type FROM nodesn, marouten WHERE nodesn.longitude=marouten.longitude AND nodesn.latitude=marouten.latitude) AS B , (SELECT marouten.latitude, marouten.longitude, stop_name, route_name, route_type FROM nodesn, marouten WHERE nodesn.longitude=marouten.longitude AND nodesn.latitude=marouten.latitude) AS C , (SELECT marouten.latitude, marouten.longitude, stop_name, route_name, route_type FROM nodesn, marouten WHERE nodesn.longitude=marouten.longitude AND nodesn.latitude=marouten.latitude) AS D, (SELECT marouten.latitude, marouten.longitude, stop_name, route_name, route_type FROM nodesn, marouten WHERE nodesn.longitude=marouten.longitude AND nodesn.latitude=marouten.latitude) AS E , (SELECT marouten.latitude, marouten.longitude, stop_name, route_name, route_type FROM nodesn, marouten WHERE nodesn.longitude=marouten.longitude AND nodesn.latitude=marouten.latitude) AS F WHERE A.stop_name=$${_fromstation}$$ AND F.stop_name=$${_tostation}$$ AND A.route_name=B.route_name AND B.stop_name=C.stop_name AND C.route_name=D.route_name AND D.stop_name=E.stop_name AND E.route_name=F.route_name AND A.route_name<>C.route_name AND C.route_name<>F.route_name""")
                    self.conn.commit()
                    self.rows += self.cursor.fetchall()

            if _transport_type=='Bus':
                if _hops >= 1 : 
                    self.cursor.execute(""f" SELECT (A.latitude,A.longitude) AS coord1, A.stop_name, A.route_name, (B.latitude,B.longitude) AS coord2, B.stop_name FROM (SELECT marouten.latitude, marouten.longitude, stop_name, route_name, route_type FROM nodesn, marouten WHERE nodesn.longitude=marouten.longitude AND nodesn.latitude=marouten.latitude) AS A , (SELECT marouten.latitude, marouten.longitude, stop_name, route_name, route_type FROM nodesn, marouten WHERE nodesn.longitude=marouten.longitude AND nodesn.latitude=marouten.latitude) AS B WHERE A.stop_name=$${_fromstation}$$ AND B.stop_name=$${_tostation}$$ AND A.route_name=B.route_name AND A.stop_name<>B.stop_name AND A.route_type=3""")
                    self.conn.commit()
                    self.rows += self.cursor.fetchall()

                if _hops >= 2 : 
                    self.cursor.execute (""f"SELECT (A.latitude,A.longitude) AS coord1, A.stop_name, A.route_name, (B.latitude,B.longitude) AS coord2, B.stop_name, D.route_name, (D.latitude,D.longitude) AS coord3, D.stop_name FROM (SELECT marouten.latitude, marouten.longitude, stop_name, route_name, route_type FROM nodesn, marouten WHERE nodesn.longitude=marouten.longitude AND nodesn.latitude=marouten.latitude) AS A, (SELECT marouten.latitude, marouten.longitude, stop_name, route_name, route_type FROM nodesn, marouten WHERE nodesn.longitude=marouten.longitude AND nodesn.latitude=marouten.latitude) AS B, (SELECT marouten.latitude, marouten.longitude, stop_name, route_name, route_type FROM nodesn, marouten WHERE nodesn.longitude=marouten.longitude AND nodesn.latitude=marouten.latitude) AS C , (SELECT marouten.latitude, marouten.longitude, stop_name, route_name, route_type FROM nodesn, marouten WHERE nodesn.longitude=marouten.longitude AND nodesn.latitude=marouten.latitude) AS D WHERE A.stop_name=$${_fromstation}$$ AND D.stop_name=$${_tostation}$$ AND A.route_name=B.route_name AND B.stop_name=C.stop_name AND C.route_name=D.route_name AND A.route_name<>C.route_name AND A.route_type=3 AND D.route_type=3""")
                    self.conn.commit()
                    self.rows += self.cursor.fetchall()

                if _hops >= 3 : 
                    self.cursor.execute(""f"SELECT (A.latitude,A.longitude) AS coord1, A.stop_name, A.route_name, (B.latitude,B.longitude) AS coord2, B.stop_name, D.route_name, (D.latitude,D.longitude) AS coord3, D.stop_name, F.route_name, (F.latitude, F.longitude) AS coord4, F.stop_name FROM (SELECT marouten.latitude, marouten.longitude, stop_name, route_name, route_type FROM nodesn, marouten WHERE nodesn.longitude=marouten.longitude AND nodesn.latitude=marouten.latitude) AS A , (SELECT marouten.latitude, marouten.longitude, stop_name, route_name, route_type FROM nodesn, marouten WHERE nodesn.longitude=marouten.longitude AND nodesn.latitude=marouten.latitude) AS B , (SELECT marouten.latitude, marouten.longitude, stop_name, route_name, route_type FROM nodesn, marouten WHERE nodesn.longitude=marouten.longitude AND nodesn.latitude=marouten.latitude) AS C , (SELECT marouten.latitude, marouten.longitude, stop_name, route_name, route_type FROM nodesn, marouten WHERE nodesn.longitude=marouten.longitude AND nodesn.latitude=marouten.latitude) AS D, (SELECT marouten.latitude, marouten.longitude, stop_name, route_name, route_type FROM nodesn, marouten WHERE nodesn.longitude=marouten.longitude AND nodesn.latitude=marouten.latitude) AS E , (SELECT marouten.latitude, marouten.longitude, stop_name, route_name, route_type FROM nodesn, marouten WHERE nodesn.longitude=marouten.longitude AND nodesn.latitude=marouten.latitude) AS F WHERE A.stop_name=$${_fromstation}$$ AND F.stop_name=$${_tostation}$$ AND A.route_name=B.route_name AND B.stop_name=C.stop_name AND C.route_name=D.route_name AND D.stop_name=E.stop_name AND E.route_name=F.route_name AND A.route_name<>C.route_name AND C.route_name<>F.route_name AND A.route_type=3 AND D.route_type=3 AND F.route_type=3""")
                    self.conn.commit()
                    self.rows += self.cursor.fetchall()

            if _transport_type=='Tram':
                if _hops >= 1 : 
                    self.cursor.execute(""f" SELECT (A.latitude,A.longitude) AS coord1, A.stop_name, A.route_name, (B.latitude,B.longitude) AS coord2, B.stop_name FROM (SELECT marouten.latitude, marouten.longitude, stop_name, route_name, route_type FROM nodesn, marouten WHERE nodesn.longitude=marouten.longitude AND nodesn.latitude=marouten.latitude) AS A , (SELECT marouten.latitude, marouten.longitude, stop_name, route_name, route_type FROM nodesn, marouten WHERE nodesn.longitude=marouten.longitude AND nodesn.latitude=marouten.latitude) AS B WHERE A.stop_name=$${_fromstation}$$ AND B.stop_name=$${_tostation}$$ AND A.route_name=B.route_name AND A.stop_name<>B.stop_name AND A.route_type=0""")
                    self.conn.commit()
                    self.rows += self.cursor.fetchall()

                if _hops >= 2 : 
                    self.cursor.execute (""f"SELECT (A.latitude,A.longitude) AS coord1, A.stop_name, A.route_name, (B.latitude,B.longitude) AS coord2, B.stop_name, D.route_name, (D.latitude,D.longitude) AS coord3, D.stop_name FROM (SELECT marouten.latitude, marouten.longitude, stop_name, route_name, route_type FROM nodesn, marouten WHERE nodesn.longitude=marouten.longitude AND nodesn.latitude=marouten.latitude) AS A, (SELECT marouten.latitude, marouten.longitude, stop_name, route_name, route_type FROM nodesn, marouten WHERE nodesn.longitude=marouten.longitude AND nodesn.latitude=marouten.latitude) AS B, (SELECT marouten.latitude, marouten.longitude, stop_name, route_name, route_type FROM nodesn, marouten WHERE nodesn.longitude=marouten.longitude AND nodesn.latitude=marouten.latitude) AS C , (SELECT marouten.latitude, marouten.longitude, stop_name, route_name, route_type FROM nodesn, marouten WHERE nodesn.longitude=marouten.longitude AND nodesn.latitude=marouten.latitude) AS D WHERE A.stop_name=$${_fromstation}$$ AND D.stop_name=$${_tostation}$$ AND A.route_name=B.route_name AND B.stop_name=C.stop_name AND C.route_name=D.route_name AND A.route_name<>C.route_name AND A.route_type=0 AND D.route_type=0""")
                    self.conn.commit()
                    self.rows += self.cursor.fetchall()

                if _hops >= 3 : 
                    self.cursor.execute(""f"SELECT (A.latitude,A.longitude) AS coord1, A.stop_name, A.route_name, (B.latitude,B.longitude) AS coord2, B.stop_name, D.route_name, (D.latitude,D.longitude) AS coord3, D.stop_name, F.route_name, (F.latitude, F.longitude) AS coord4, F.stop_name FROM (SELECT marouten.latitude, marouten.longitude, stop_name, route_name, route_type FROM nodesn, marouten WHERE nodesn.longitude=marouten.longitude AND nodesn.latitude=marouten.latitude) AS A , (SELECT marouten.latitude, marouten.longitude, stop_name, route_name, route_type FROM nodesn, marouten WHERE nodesn.longitude=marouten.longitude AND nodesn.latitude=marouten.latitude) AS B , (SELECT marouten.latitude, marouten.longitude, stop_name, route_name, route_type FROM nodesn, marouten WHERE nodesn.longitude=marouten.longitude AND nodesn.latitude=marouten.latitude) AS C , (SELECT marouten.latitude, marouten.longitude, stop_name, route_name, route_type FROM nodesn, marouten WHERE nodesn.longitude=marouten.longitude AND nodesn.latitude=marouten.latitude) AS D, (SELECT marouten.latitude, marouten.longitude, stop_name, route_name, route_type FROM nodesn, marouten WHERE nodesn.longitude=marouten.longitude AND nodesn.latitude=marouten.latitude) AS E , (SELECT marouten.latitude, marouten.longitude, stop_name, route_name, route_type FROM nodesn, marouten WHERE nodesn.longitude=marouten.longitude AND nodesn.latitude=marouten.latitude) AS F WHERE A.stop_name=$${_fromstation}$$ AND F.stop_name=$${_tostation}$$ AND A.route_name=B.route_name AND B.stop_name=C.stop_name AND C.route_name=D.route_name AND D.stop_name=E.stop_name AND E.route_name=F.route_name AND A.route_name<>C.route_name AND C.route_name<>F.route_name AND A.route_type=0 AND D.route_type=0 AND F.route_type=0""")
                    self.conn.commit()
                    self.rows += self.cursor.fetchall()
        if _ville == 'Rennes':
            if _transport_type=='Tous':
                if _hops >= 1 : 
                    self.cursor.execute(""f" SELECT (A.latitude,A.longitude) AS coord1, A.stop_name, A.route_name, (B.latitude,B.longitude) AS coord2, B.stop_name FROM (SELECT marouter.latitude, marouter.longitude, stop_name, route_name, route_type FROM nodesr, marouter WHERE nodesr.longitude=marouter.longitude AND nodesr.latitude=marouter.latitude) AS A , (SELECT marouter.latitude, marouter.longitude, stop_name, route_name, route_type FROM nodesr, marouter WHERE nodesr.longitude=marouter.longitude AND nodesr.latitude=marouter.latitude) AS B WHERE A.stop_name=$${_fromstation}$$ AND B.stop_name=$${_tostation}$$ AND A.route_name=B.route_name AND A.stop_name<>B.stop_name""")
                    self.conn.commit()
                    self.rows += self.cursor.fetchall()

                if _hops >= 2 : 
                    self.cursor.execute (""f"SELECT (A.latitude,A.longitude) AS coord1, A.stop_name, A.route_name, (B.latitude,B.longitude) AS coord2, B.stop_name, D.route_name, (D.latitude,D.longitude) AS coord3, D.stop_name FROM (SELECT marouter.latitude, marouter.longitude, stop_name, route_name, route_type FROM nodesr, marouter WHERE nodesr.longitude=marouter.longitude AND nodesr.latitude=marouter.latitude) AS A, (SELECT marouter.latitude, marouter.longitude, stop_name, route_name, route_type FROM nodesr, marouter WHERE nodesr.longitude=marouter.longitude AND nodesr.latitude=marouter.latitude) AS B, (SELECT marouter.latitude, marouter.longitude, stop_name, route_name, route_type FROM nodesr, marouter WHERE nodesr.longitude=marouter.longitude AND nodesr.latitude=marouter.latitude) AS C , (SELECT marouter.latitude, marouter.longitude, stop_name, route_name, route_type FROM nodesr, marouter WHERE nodesr.longitude=marouter.longitude AND nodesr.latitude=marouter.latitude) AS D WHERE A.stop_name=$${_fromstation}$$ AND D.stop_name=$${_tostation}$$ AND A.route_name=B.route_name AND B.stop_name=C.stop_name AND C.route_name=D.route_name AND A.route_name<>C.route_name""")
                    self.conn.commit()
                    self.rows += self.cursor.fetchall()

                if _hops >= 3 : 
                    self.cursor.execute(""f"SELECT (A.latitude,A.longitude) AS coord1, A.stop_name, A.route_name, (B.latitude,B.longitude) AS coord2, B.stop_name, D.route_name, (D.latitude,D.longitude) AS coord3, D.stop_name, F.route_name, (F.latitude, F.longitude) AS coord4, F.stop_name FROM (SELECT marouter.latitude, marouter.longitude, stop_name, route_name, route_type FROM nodesr, marouter WHERE nodesr.longitude=marouter.longitude AND nodesr.latitude=marouter.latitude) AS A , (SELECT marouter.latitude, marouter.longitude, stop_name, route_name, route_type FROM nodesr, marouter WHERE nodesr.longitude=marouter.longitude AND nodesr.latitude=marouter.latitude) AS B , (SELECT marouter.latitude, marouter.longitude, stop_name, route_name, route_type FROM nodesr, marouter WHERE nodesr.longitude=marouter.longitude AND nodesr.latitude=marouter.latitude) AS C , (SELECT marouter.latitude, marouter.longitude, stop_name, route_name, route_type FROM nodesr, marouter WHERE nodesr.longitude=marouter.longitude AND nodesr.latitude=marouter.latitude) AS D, (SELECT marouter.latitude, marouter.longitude, stop_name, route_name, route_type FROM nodesr, marouter WHERE nodesr.longitude=marouter.longitude AND nodesr.latitude=marouter.latitude) AS E , (SELECT marouter.latitude, marouter.longitude, stop_name, route_name, route_type FROM nodesr, marouter WHERE nodesr.longitude=marouter.longitude AND nodesr.latitude=marouter.latitude) AS F WHERE A.stop_name=$${_fromstation}$$ AND F.stop_name=$${_tostation}$$ AND A.route_name=B.route_name AND B.stop_name=C.stop_name AND C.route_name=D.route_name AND D.stop_name=E.stop_name AND E.route_name=F.route_name AND A.route_name<>C.route_name AND C.route_name<>F.route_name""")
                    self.conn.commit()
                    self.rows += self.cursor.fetchall()

            if _transport_type=='Bus':
                if _hops >= 1 : 
                    self.cursor.execute(""f" SELECT (A.latitude,A.longitude) AS coord1, A.stop_name, A.route_name, (B.latitude,B.longitude) AS coord2, B.stop_name FROM (SELECT marouter.latitude, marouter.longitude, stop_name, route_name, route_type FROM nodesr, marouter WHERE nodesr.longitude=marouter.longitude AND nodesr.latitude=marouter.latitude) AS A , (SELECT marouter.latitude, marouter.longitude, stop_name, route_name, route_type FROM nodesr, marouter WHERE nodesr.longitude=marouter.longitude AND nodesr.latitude=marouter.latitude) AS B WHERE A.stop_name=$${_fromstation}$$ AND B.stop_name=$${_tostation}$$ AND A.route_name=B.route_name AND A.stop_name<>B.stop_name AND A.route_type=3""")
                    self.conn.commit()
                    self.rows += self.cursor.fetchall()

                if _hops >= 2 : 
                    self.cursor.execute (""f"SELECT (A.latitude,A.longitude) AS coord1, A.stop_name, A.route_name, (B.latitude,B.longitude) AS coord2, B.stop_name, D.route_name, (D.latitude,D.longitude) AS coord3, D.stop_name FROM (SELECT marouter.latitude, marouter.longitude, stop_name, route_name, route_type FROM nodesr, marouter WHERE nodesr.longitude=marouter.longitude AND nodesr.latitude=marouter.latitude) AS A, (SELECT marouter.latitude, marouter.longitude, stop_name, route_name, route_type FROM nodesr, marouter WHERE nodesr.longitude=marouter.longitude AND nodesr.latitude=marouter.latitude) AS B, (SELECT marouter.latitude, marouter.longitude, stop_name, route_name, route_type FROM nodesr, marouter WHERE nodesr.longitude=marouter.longitude AND nodesr.latitude=marouter.latitude) AS C , (SELECT marouter.latitude, marouter.longitude, stop_name, route_name, route_type FROM nodesr, marouter WHERE nodesr.longitude=marouter.longitude AND nodesr.latitude=marouter.latitude) AS D WHERE A.stop_name=$${_fromstation}$$ AND D.stop_name=$${_tostation}$$ AND A.route_name=B.route_name AND B.stop_name=C.stop_name AND C.route_name=D.route_name AND A.route_name<>C.route_name AND A.route_type=3 AND D.route_type=3""")
                    self.conn.commit()
                    self.rows += self.cursor.fetchall()

                if _hops >= 3 : 
                    self.cursor.execute(""f"SELECT (A.latitude,A.longitude) AS coord1, A.stop_name, A.route_name, (B.latitude,B.longitude) AS coord2, B.stop_name, D.route_name, (D.latitude,D.longitude) AS coord3, D.stop_name, F.route_name, (F.latitude, F.longitude) AS coord4, F.stop_name FROM (SELECT marouter.latitude, marouter.longitude, stop_name, route_name, route_type FROM nodesr, marouter WHERE nodesr.longitude=marouter.longitude AND nodesr.latitude=marouter.latitude) AS A , (SELECT marouter.latitude, marouter.longitude, stop_name, route_name, route_type FROM nodesr, marouter WHERE nodesr.longitude=marouter.longitude AND nodesr.latitude=marouter.latitude) AS B , (SELECT marouter.latitude, marouter.longitude, stop_name, route_name, route_type FROM nodesr, marouter WHERE nodesr.longitude=marouter.longitude AND nodesr.latitude=marouter.latitude) AS C , (SELECT marouter.latitude, marouter.longitude, stop_name, route_name, route_type FROM nodesr, marouter WHERE nodesr.longitude=marouter.longitude AND nodesr.latitude=marouter.latitude) AS D, (SELECT marouter.latitude, marouter.longitude, stop_name, route_name, route_type FROM nodesr, marouter WHERE nodesr.longitude=marouter.longitude AND nodesr.latitude=marouter.latitude) AS E , (SELECT marouter.latitude, marouter.longitude, stop_name, route_name, route_type FROM nodesr, marouter WHERE nodesr.longitude=marouter.longitude AND nodesr.latitude=marouter.latitude) AS F WHERE A.stop_name=$${_fromstation}$$ AND F.stop_name=$${_tostation}$$ AND A.route_name=B.route_name AND B.stop_name=C.stop_name AND C.route_name=D.route_name AND D.stop_name=E.stop_name AND E.route_name=F.route_name AND A.route_name<>C.route_name AND C.route_name<>F.route_name AND A.route_type=3 AND D.route_type=3 AND F.route_type=3""")
                    self.conn.commit()
                    self.rows += self.cursor.fetchall()

            if _transport_type=='Métro':
                if _hops >= 1 : 
                    self.cursor.execute(""f" SELECT (A.latitude,A.longitude) AS coord1, A.stop_name, A.route_name, (B.latitude,B.longitude) AS coord2, B.stop_name FROM (SELECT marouter.latitude, marouter.longitude, stop_name, route_name, route_type FROM nodesr, marouter WHERE nodesr.longitude=marouter.longitude AND nodesr.latitude=marouter.latitude) AS A , (SELECT marouter.latitude, marouter.longitude, stop_name, route_name, route_type FROM nodesr, marouter WHERE nodesr.longitude=marouter.longitude AND nodesr.latitude=marouter.latitude) AS B WHERE A.stop_name=$${_fromstation}$$ AND B.stop_name=$${_tostation}$$ AND A.route_name=B.route_name AND A.stop_name<>B.stop_name AND A.route_type=1""")
                    self.conn.commit()
                    self.rows += self.cursor.fetchall()

                if _hops >= 2 : 
                    self.cursor.execute (""f"SELECT (A.latitude,A.longitude) AS coord1, A.stop_name, A.route_name, (B.latitude,B.longitude) AS coord2, B.stop_name, D.route_name, (D.latitude,D.longitude) AS coord3, D.stop_name FROM (SELECT marouter.latitude, marouter.longitude, stop_name, route_name, route_type FROM nodesr, marouter WHERE nodesr.longitude=marouter.longitude AND nodesr.latitude=marouter.latitude) AS A, (SELECT marouter.latitude, marouter.longitude, stop_name, route_name, route_type FROM nodesr, marouter WHERE nodesr.longitude=marouter.longitude AND nodesr.latitude=marouter.latitude) AS B, (SELECT marouter.latitude, marouter.longitude, stop_name, route_name, route_type FROM nodesr, marouter WHERE nodesr.longitude=marouter.longitude AND nodesr.latitude=marouter.latitude) AS C , (SELECT marouter.latitude, marouter.longitude, stop_name, route_name, route_type FROM nodesr, marouter WHERE nodesr.longitude=marouter.longitude AND nodesr.latitude=marouter.latitude) AS D WHERE A.stop_name=$${_fromstation}$$ AND D.stop_name=$${_tostation}$$ AND A.route_name=B.route_name AND B.stop_name=C.stop_name AND C.route_name=D.route_name AND A.route_name<>C.route_name AND A.route_type=1 AND D.route_type=1""")
                    self.conn.commit()
                    self.rows += self.cursor.fetchall()

                if _hops >= 3 : 
                    self.cursor.execute(""f"SELECT (A.latitude,A.longitude) AS coord1, A.stop_name, A.route_name, (B.latitude,B.longitude) AS coord2, B.stop_name, D.route_name, (D.latitude,D.longitude) AS coord3, D.stop_name, F.route_name, (F.latitude, F.longitude) AS coord4, F.stop_name FROM (SELECT marouter.latitude, marouter.longitude, stop_name, route_name, route_type FROM nodesr, marouter WHERE nodesr.longitude=marouter.longitude AND nodesr.latitude=marouter.latitude) AS A , (SELECT marouter.latitude, marouter.longitude, stop_name, route_name, route_type FROM nodesr, marouter WHERE nodesr.longitude=marouter.longitude AND nodesr.latitude=marouter.latitude) AS B , (SELECT marouter.latitude, marouter.longitude, stop_name, route_name, route_type FROM nodesr, marouter WHERE nodesr.longitude=marouter.longitude AND nodesr.latitude=marouter.latitude) AS C , (SELECT marouter.latitude, marouter.longitude, stop_name, route_name, route_type FROM nodesr, marouter WHERE nodesr.longitude=marouter.longitude AND nodesr.latitude=marouter.latitude) AS D, (SELECT marouter.latitude, marouter.longitude, stop_name, route_name, route_type FROM nodesr, marouter WHERE nodesr.longitude=marouter.longitude AND nodesr.latitude=marouter.latitude) AS E , (SELECT marouter.latitude, marouter.longitude, stop_name, route_name, route_type FROM nodesr, marouter WHERE nodesr.longitude=marouter.longitude AND nodesr.latitude=marouter.latitude) AS F WHERE A.stop_name=$${_fromstation}$$ AND F.stop_name=$${_tostation}$$ AND A.route_name=B.route_name AND B.stop_name=C.stop_name AND C.route_name=D.route_name AND D.stop_name=E.stop_name AND E.route_name=F.route_name AND A.route_name<>C.route_name AND C.route_name<>F.route_name AND A.route_type=1 AND D.route_type=1 AND F.route_type=1""")
                    self.conn.commit()
                    self.rows += self.cursor.fetchall()
        if _ville == 'Toulouse':
            if _transport_type=='Tous':
                if _hops >= 1 : 
                    self.cursor.execute(""f" SELECT (A.latitude,A.longitude) AS coord1, A.stop_name, A.route_name, (B.latitude,B.longitude) AS coord2, B.stop_name FROM (SELECT maroutet.latitude, maroutet.longitude, stop_name, route_name, route_type FROM nodest, maroutet WHERE nodest.longitude=maroutet.longitude AND nodest.latitude=maroutet.latitude) AS A , (SELECT maroutet.latitude, maroutet.longitude, stop_name, route_name, route_type FROM nodest, maroutet WHERE nodest.longitude=maroutet.longitude AND nodest.latitude=maroutet.latitude) AS B WHERE A.stop_name=$${_fromstation}$$ AND B.stop_name=$${_tostation}$$ AND A.route_name=B.route_name AND A.stop_name<>B.stop_name""")
                    self.conn.commit()
                    self.rows += self.cursor.fetchall()

                if _hops >= 2 : 
                    self.cursor.execute (""f"SELECT (A.latitude,A.longitude) AS coord1, A.stop_name, A.route_name, (B.latitude,B.longitude) AS coord2, B.stop_name, D.route_name, (D.latitude,D.longitude) AS coord3, D.stop_name FROM (SELECT maroutet.latitude, maroutet.longitude, stop_name, route_name, route_type FROM nodest, maroutet WHERE nodest.longitude=maroutet.longitude AND nodest.latitude=maroutet.latitude) AS A, (SELECT maroutet.latitude, maroutet.longitude, stop_name, route_name, route_type FROM nodest, maroutet WHERE nodest.longitude=maroutet.longitude AND nodest.latitude=maroutet.latitude) AS B, (SELECT maroutet.latitude, maroutet.longitude, stop_name, route_name, route_type FROM nodest, maroutet WHERE nodest.longitude=maroutet.longitude AND nodest.latitude=maroutet.latitude) AS C , (SELECT maroutet.latitude, maroutet.longitude, stop_name, route_name, route_type FROM nodest, maroutet WHERE nodest.longitude=maroutet.longitude AND nodest.latitude=maroutet.latitude) AS D WHERE A.stop_name=$${_fromstation}$$ AND D.stop_name=$${_tostation}$$ AND A.route_name=B.route_name AND B.stop_name=C.stop_name AND C.route_name=D.route_name AND A.route_name<>C.route_name""")
                    self.conn.commit()
                    self.rows += self.cursor.fetchall()

                if _hops >= 3 : 
                    self.cursor.execute(""f"SELECT (A.latitude,A.longitude) AS coord1, A.stop_name, A.route_name, (B.latitude,B.longitude) AS coord2, B.stop_name, D.route_name, (D.latitude,D.longitude) AS coord3, D.stop_name, F.route_name, (F.latitude, F.longitude) AS coord4, F.stop_name FROM (SELECT maroutet.latitude, maroutet.longitude, stop_name, route_name, route_type FROM nodest, maroutet WHERE nodest.longitude=maroutet.longitude AND nodest.latitude=maroutet.latitude) AS A , (SELECT maroutet.latitude, maroutet.longitude, stop_name, route_name, route_type FROM nodest, maroutet WHERE nodest.longitude=maroutet.longitude AND nodest.latitude=maroutet.latitude) AS B , (SELECT maroutet.latitude, maroutet.longitude, stop_name, route_name, route_type FROM nodest, maroutet WHERE nodest.longitude=maroutet.longitude AND nodest.latitude=maroutet.latitude) AS C , (SELECT maroutet.latitude, maroutet.longitude, stop_name, route_name, route_type FROM nodest, maroutet WHERE nodest.longitude=maroutet.longitude AND nodest.latitude=maroutet.latitude) AS D, (SELECT maroutet.latitude, maroutet.longitude, stop_name, route_name, route_type FROM nodest, maroutet WHERE nodest.longitude=maroutet.longitude AND nodest.latitude=maroutet.latitude) AS E , (SELECT maroutet.latitude, maroutet.longitude, stop_name, route_name, route_type FROM nodest, maroutet WHERE nodest.longitude=maroutet.longitude AND nodest.latitude=maroutet.latitude) AS F WHERE A.stop_name=$${_fromstation}$$ AND F.stop_name=$${_tostation}$$ AND A.route_name=B.route_name AND B.stop_name=C.stop_name AND C.route_name=D.route_name AND D.stop_name=E.stop_name AND E.route_name=F.route_name AND A.route_name<>C.route_name AND C.route_name<>F.route_name""")
                    self.conn.commit()
                    self.rows += self.cursor.fetchall()

            if _transport_type=='Bus':
                if _hops >= 1 : 
                    self.cursor.execute(""f" SELECT (A.latitude,A.longitude) AS coord1, A.stop_name, A.route_name, (B.latitude,B.longitude) AS coord2, B.stop_name FROM (SELECT maroutet.latitude, maroutet.longitude, stop_name, route_name, route_type FROM nodest, maroutet WHERE nodest.longitude=maroutet.longitude AND nodest.latitude=maroutet.latitude) AS A , (SELECT maroutet.latitude, maroutet.longitude, stop_name, route_name, route_type FROM nodest, maroutet WHERE nodest.longitude=maroutet.longitude AND nodest.latitude=maroutet.latitude) AS B WHERE A.stop_name=$${_fromstation}$$ AND B.stop_name=$${_tostation}$$ AND A.route_name=B.route_name AND A.stop_name<>B.stop_name AND A.route_type=3""")
                    self.conn.commit()
                    self.rows += self.cursor.fetchall()

                if _hops >= 2 : 
                    self.cursor.execute (""f"SELECT (A.latitude,A.longitude) AS coord1, A.stop_name, A.route_name, (B.latitude,B.longitude) AS coord2, B.stop_name, D.route_name, (D.latitude,D.longitude) AS coord3, D.stop_name FROM (SELECT maroutet.latitude, maroutet.longitude, stop_name, route_name, route_type FROM nodest, maroutet WHERE nodest.longitude=maroutet.longitude AND nodest.latitude=maroutet.latitude) AS A, (SELECT maroutet.latitude, maroutet.longitude, stop_name, route_name, route_type FROM nodest, maroutet WHERE nodest.longitude=maroutet.longitude AND nodest.latitude=maroutet.latitude) AS B, (SELECT maroutet.latitude, maroutet.longitude, stop_name, route_name, route_type FROM nodest, maroutet WHERE nodest.longitude=maroutet.longitude AND nodest.latitude=maroutet.latitude) AS C , (SELECT maroutet.latitude, maroutet.longitude, stop_name, route_name, route_type FROM nodest, maroutet WHERE nodest.longitude=maroutet.longitude AND nodest.latitude=maroutet.latitude) AS D WHERE A.stop_name=$${_fromstation}$$ AND D.stop_name=$${_tostation}$$ AND A.route_name=B.route_name AND B.stop_name=C.stop_name AND C.route_name=D.route_name AND A.route_name<>C.route_name AND A.route_type=3 AND D.route_type=3""")
                    self.conn.commit()
                    self.rows += self.cursor.fetchall()

                if _hops >= 3 : 
                    self.cursor.execute(""f"SELECT (A.latitude,A.longitude) AS coord1, A.stop_name, A.route_name, (B.latitude,B.longitude) AS coord2, B.stop_name, D.route_name, (D.latitude,D.longitude) AS coord3, D.stop_name, F.route_name, (F.latitude, F.longitude) AS coord4, F.stop_name FROM (SELECT maroutet.latitude, maroutet.longitude, stop_name, route_name, route_type FROM nodest, maroutet WHERE nodest.longitude=maroutet.longitude AND nodest.latitude=maroutet.latitude) AS A , (SELECT maroutet.latitude, maroutet.longitude, stop_name, route_name, route_type FROM nodest, maroutet WHERE nodest.longitude=maroutet.longitude AND nodest.latitude=maroutet.latitude) AS B , (SELECT maroutet.latitude, maroutet.longitude, stop_name, route_name, route_type FROM nodest, maroutet WHERE nodest.longitude=maroutet.longitude AND nodest.latitude=maroutet.latitude) AS C , (SELECT maroutet.latitude, maroutet.longitude, stop_name, route_name, route_type FROM nodest, maroutet WHERE nodest.longitude=maroutet.longitude AND nodest.latitude=maroutet.latitude) AS D, (SELECT maroutet.latitude, maroutet.longitude, stop_name, route_name, route_type FROM nodest, maroutet WHERE nodest.longitude=maroutet.longitude AND nodest.latitude=maroutet.latitude) AS E , (SELECT maroutet.latitude, maroutet.longitude, stop_name, route_name, route_type FROM nodest, maroutet WHERE nodest.longitude=maroutet.longitude AND nodest.latitude=maroutet.latitude) AS F WHERE A.stop_name=$${_fromstation}$$ AND F.stop_name=$${_tostation}$$ AND A.route_name=B.route_name AND B.stop_name=C.stop_name AND C.route_name=D.route_name AND D.stop_name=E.stop_name AND E.route_name=F.route_name AND A.route_name<>C.route_name AND C.route_name<>F.route_name AND A.route_type=3 AND D.route_type=3 AND F.route_type=3""")
                    self.conn.commit()
                    self.rows += self.cursor.fetchall()

            if _transport_type=='Métro':
                if _hops >= 1 : 
                    self.cursor.execute(""f" SELECT (A.latitude,A.longitude) AS coord1, A.stop_name, A.route_name, (B.latitude,B.longitude) AS coord2, B.stop_name FROM (SELECT maroutet.latitude, maroutet.longitude, stop_name, route_name, route_type FROM nodest, maroutet WHERE nodest.longitude=maroutet.longitude AND nodest.latitude=maroutet.latitude) AS A , (SELECT maroutet.latitude, maroutet.longitude, stop_name, route_name, route_type FROM nodest, maroutet WHERE nodest.longitude=maroutet.longitude AND nodest.latitude=maroutet.latitude) AS B WHERE A.stop_name=$${_fromstation}$$ AND B.stop_name=$${_tostation}$$ AND A.route_name=B.route_name AND A.stop_name<>B.stop_name AND A.route_type=1""")
                    self.conn.commit()
                    self.rows += self.cursor.fetchall()

                if _hops >= 2 : 
                    self.cursor.execute (""f"SELECT (A.latitude,A.longitude) AS coord1, A.stop_name, A.route_name, (B.latitude,B.longitude) AS coord2, B.stop_name, D.route_name, (D.latitude,D.longitude) AS coord3, D.stop_name FROM (SELECT maroutet.latitude, maroutet.longitude, stop_name, route_name, route_type FROM nodest, maroutet WHERE nodest.longitude=maroutet.longitude AND nodest.latitude=maroutet.latitude) AS A, (SELECT maroutet.latitude, maroutet.longitude, stop_name, route_name, route_type FROM nodest, maroutet WHERE nodest.longitude=maroutet.longitude AND nodest.latitude=maroutet.latitude) AS B, (SELECT maroutet.latitude, maroutet.longitude, stop_name, route_name, route_type FROM nodest, maroutet WHERE nodest.longitude=maroutet.longitude AND nodest.latitude=maroutet.latitude) AS C , (SELECT maroutet.latitude, maroutet.longitude, stop_name, route_name, route_type FROM nodest, maroutet WHERE nodest.longitude=maroutet.longitude AND nodest.latitude=maroutet.latitude) AS D WHERE A.stop_name=$${_fromstation}$$ AND D.stop_name=$${_tostation}$$ AND A.route_name=B.route_name AND B.stop_name=C.stop_name AND C.route_name=D.route_name AND A.route_name<>C.route_name AND A.route_type=1 AND D.route_type=1""")
                    self.conn.commit()
                    self.rows += self.cursor.fetchall()

                if _hops >= 3 : 
                    self.cursor.execute(""f"SELECT (A.latitude,A.longitude) AS coord1, A.stop_name, A.route_name, (B.latitude,B.longitude) AS coord2, B.stop_name, D.route_name, (D.latitude,D.longitude) AS coord3, D.stop_name, F.route_name, (F.latitude, F.longitude) AS coord4, F.stop_name FROM (SELECT maroutet.latitude, maroutet.longitude, stop_name, route_name, route_type FROM nodest, maroutet WHERE nodest.longitude=maroutet.longitude AND nodest.latitude=maroutet.latitude) AS A , (SELECT maroutet.latitude, maroutet.longitude, stop_name, route_name, route_type FROM nodest, maroutet WHERE nodest.longitude=maroutet.longitude AND nodest.latitude=maroutet.latitude) AS B , (SELECT maroutet.latitude, maroutet.longitude, stop_name, route_name, route_type FROM nodest, maroutet WHERE nodest.longitude=maroutet.longitude AND nodest.latitude=maroutet.latitude) AS C , (SELECT maroutet.latitude, maroutet.longitude, stop_name, route_name, route_type FROM nodest, maroutet WHERE nodest.longitude=maroutet.longitude AND nodest.latitude=maroutet.latitude) AS D, (SELECT maroutet.latitude, maroutet.longitude, stop_name, route_name, route_type FROM nodest, maroutet WHERE nodest.longitude=maroutet.longitude AND nodest.latitude=maroutet.latitude) AS E , (SELECT maroutet.latitude, maroutet.longitude, stop_name, route_name, route_type FROM nodest, maroutet WHERE nodest.longitude=maroutet.longitude AND nodest.latitude=maroutet.latitude) AS F WHERE A.stop_name=$${_fromstation}$$ AND F.stop_name=$${_tostation}$$ AND A.route_name=B.route_name AND B.stop_name=C.stop_name AND C.route_name=D.route_name AND D.stop_name=E.stop_name AND E.route_name=F.route_name AND A.route_name<>C.route_name AND C.route_name<>F.route_name AND A.route_type=1 AND D.route_type=1 AND F.route_type=1""")
                    self.conn.commit()
                    self.rows += self.cursor.fetchall()
            if _transport_type=='Tram':
                if _hops >= 1 : 
                    self.cursor.execute(""f" SELECT (A.latitude,A.longitude) AS coord1, A.stop_name, A.route_name, (B.latitude,B.longitude) AS coord2, B.stop_name FROM (SELECT maroutet.latitude, maroutet.longitude, stop_name, route_name, route_type FROM nodest, maroutet WHERE nodest.longitude=maroutet.longitude AND nodest.latitude=maroutet.latitude) AS A , (SELECT maroutet.latitude, maroutet.longitude, stop_name, route_name, route_type FROM nodest, maroutet WHERE nodest.longitude=maroutet.longitude AND nodest.latitude=maroutet.latitude) AS B WHERE A.stop_name=$${_fromstation}$$ AND B.stop_name=$${_tostation}$$ AND A.route_name=B.route_name AND A.stop_name<>B.stop_name AND A.route_type=0""")
                    self.conn.commit()
                    self.rows += self.cursor.fetchall()

                if _hops >= 2 : 
                    self.cursor.execute (""f"SELECT (A.latitude,A.longitude) AS coord1, A.stop_name, A.route_name, (B.latitude,B.longitude) AS coord2, B.stop_name, D.route_name, (D.latitude,D.longitude) AS coord3, D.stop_name FROM (SELECT maroutet.latitude, maroutet.longitude, stop_name, route_name, route_type FROM nodest, maroutet WHERE nodest.longitude=maroutet.longitude AND nodest.latitude=maroutet.latitude) AS A, (SELECT maroutet.latitude, maroutet.longitude, stop_name, route_name, route_type FROM nodest, maroutet WHERE nodest.longitude=maroutet.longitude AND nodest.latitude=maroutet.latitude) AS B, (SELECT maroutet.latitude, maroutet.longitude, stop_name, route_name, route_type FROM nodest, maroutet WHERE nodest.longitude=maroutet.longitude AND nodest.latitude=maroutet.latitude) AS C , (SELECT maroutet.latitude, maroutet.longitude, stop_name, route_name, route_type FROM nodest, maroutet WHERE nodest.longitude=maroutet.longitude AND nodest.latitude=maroutet.latitude) AS D WHERE A.stop_name=$${_fromstation}$$ AND D.stop_name=$${_tostation}$$ AND A.route_name=B.route_name AND B.stop_name=C.stop_name AND C.route_name=D.route_name AND A.route_name<>C.route_name AND A.route_type=0 AND D.route_type=0""")
                    self.conn.commit()
                    self.rows += self.cursor.fetchall()

                if _hops >= 3 : 
                    self.cursor.execute(""f"SELECT (A.latitude,A.longitude) AS coord1, A.stop_name, A.route_name, (B.latitude,B.longitude) AS coord2, B.stop_name, D.route_name, (D.latitude,D.longitude) AS coord3, D.stop_name, F.route_name, (F.latitude, F.longitude) AS coord4, F.stop_name FROM (SELECT maroutet.latitude, maroutet.longitude, stop_name, route_name, route_type FROM nodest, maroutet WHERE nodest.longitude=maroutet.longitude AND nodest.latitude=maroutet.latitude) AS A , (SELECT maroutet.latitude, maroutet.longitude, stop_name, route_name, route_type FROM nodest, maroutet WHERE nodest.longitude=maroutet.longitude AND nodest.latitude=maroutet.latitude) AS B , (SELECT maroutet.latitude, maroutet.longitude, stop_name, route_name, route_type FROM nodest, maroutet WHERE nodest.longitude=maroutet.longitude AND nodest.latitude=maroutet.latitude) AS C , (SELECT maroutet.latitude, maroutet.longitude, stop_name, route_name, route_type FROM nodest, maroutet WHERE nodest.longitude=maroutet.longitude AND nodest.latitude=maroutet.latitude) AS D, (SELECT maroutet.latitude, maroutet.longitude, stop_name, route_name, route_type FROM nodest, maroutet WHERE nodest.longitude=maroutet.longitude AND nodest.latitude=maroutet.latitude) AS E , (SELECT maroutet.latitude, maroutet.longitude, stop_name, route_name, route_type FROM nodest, maroutet WHERE nodest.longitude=maroutet.longitude AND nodest.latitude=maroutet.latitude) AS F WHERE A.stop_name=$${_fromstation}$$ AND F.stop_name=$${_tostation}$$ AND A.route_name=B.route_name AND B.stop_name=C.stop_name AND C.route_name=D.route_name AND D.stop_name=E.stop_name AND E.route_name=F.route_name AND A.route_name<>C.route_name AND C.route_name<>F.route_name AND A.route_type=0 AND D.route_type=0 AND F.route_type=0""")
                    self.conn.commit()
                    self.rows += self.cursor.fetchall()
        
        
        if _ville == 'Paris':
            if _transport_type=='Tous':
                if _hops >= 1 : 
                    self.cursor.execute(""f" SELECT (A.latitude,A.longitude) AS coord1, A.stop_name, A.route_name, (B.latitude,B.longitude) AS coord2, B.stop_name FROM (SELECT maroutep.latitude, maroutep.longitude, stop_name, route_name, route_type FROM nodesp, maroutep WHERE nodesp.longitude=maroutep.longitude AND nodesp.latitude=maroutep.latitude) AS A , (SELECT maroutep.latitude, maroutep.longitude, stop_name, route_name, route_type FROM nodesp, maroutep WHERE nodesp.longitude=maroutep.longitude AND nodesp.latitude=maroutep.latitude) AS B WHERE A.stop_name=$${_fromstation}$$ AND B.stop_name=$${_tostation}$$ AND A.route_name=B.route_name AND A.stop_name<>B.stop_name""")
                    self.conn.commit()
                    self.rows += self.cursor.fetchall()

                if _hops >= 2 : 
                    self.cursor.execute (""f"SELECT (A.latitude,A.longitude) AS coord1, A.stop_name, A.route_name, (B.latitude,B.longitude) AS coord2, B.stop_name, D.route_name, (D.latitude,D.longitude) AS coord3, D.stop_name FROM (SELECT maroutep.latitude, maroutep.longitude, stop_name, route_name, route_type FROM nodesp, maroutep WHERE nodesp.longitude=maroutep.longitude AND nodesp.latitude=maroutep.latitude) AS A, (SELECT maroutep.latitude, maroutep.longitude, stop_name, route_name, route_type FROM nodesp, maroutep WHERE nodesp.longitude=maroutep.longitude AND nodesp.latitude=maroutep.latitude) AS B, (SELECT maroutep.latitude, maroutep.longitude, stop_name, route_name, route_type FROM nodesp, maroutep WHERE nodesp.longitude=maroutep.longitude AND nodesp.latitude=maroutep.latitude) AS C , (SELECT maroutep.latitude, maroutep.longitude, stop_name, route_name, route_type FROM nodesp, maroutep WHERE nodesp.longitude=maroutep.longitude AND nodesp.latitude=maroutep.latitude) AS D WHERE A.stop_name=$${_fromstation}$$ AND D.stop_name=$${_tostation}$$ AND A.route_name=B.route_name AND B.stop_name=C.stop_name AND C.route_name=D.route_name AND A.route_name<>C.route_name""")
                    self.conn.commit()
                    self.rows += self.cursor.fetchall()

                if _hops >= 3 : 
                    self.cursor.execute(""f"SELECT (A.latitude,A.longitude) AS coord1, A.stop_name, A.route_name, (B.latitude,B.longitude) AS coord2, B.stop_name, D.route_name, (D.latitude,D.longitude) AS coord3, D.stop_name, F.route_name, (F.latitude, F.longitude) AS coord4, F.stop_name FROM (SELECT maroutep.latitude, maroutep.longitude, stop_name, route_name, route_type FROM nodesp, maroutep WHERE nodesp.longitude=maroutep.longitude AND nodesp.latitude=maroutep.latitude) AS A , (SELECT maroutep.latitude, maroutep.longitude, stop_name, route_name, route_type FROM nodesp, maroutep WHERE nodesp.longitude=maroutep.longitude AND nodesp.latitude=maroutep.latitude) AS B , (SELECT maroutep.latitude, maroutep.longitude, stop_name, route_name, route_type FROM nodesp, maroutep WHERE nodesp.longitude=maroutep.longitude AND nodesp.latitude=maroutep.latitude) AS C , (SELECT maroutep.latitude, maroutep.longitude, stop_name, route_name, route_type FROM nodesp, maroutep WHERE nodesp.longitude=maroutep.longitude AND nodesp.latitude=maroutep.latitude) AS D, (SELECT maroutep.latitude, maroutep.longitude, stop_name, route_name, route_type FROM nodesp, maroutep WHERE nodesp.longitude=maroutep.longitude AND nodesp.latitude=maroutep.latitude) AS E , (SELECT maroutep.latitude, maroutep.longitude, stop_name, route_name, route_type FROM nodesp, maroutep WHERE nodesp.longitude=maroutep.longitude AND nodesp.latitude=maroutep.latitude) AS F WHERE A.stop_name=$${_fromstation}$$ AND F.stop_name=$${_tostation}$$ AND A.route_name=B.route_name AND B.stop_name=C.stop_name AND C.route_name=D.route_name AND D.stop_name=E.stop_name AND E.route_name=F.route_name AND A.route_name<>C.route_name AND C.route_name<>F.route_name""")
                    self.conn.commit()
                    self.rows += self.cursor.fetchall()

            if _transport_type=='Bus':
                if _hops >= 1 : 
                    self.cursor.execute(""f" SELECT (A.latitude,A.longitude) AS coord1, A.stop_name, A.route_name, (B.latitude,B.longitude) AS coord2, B.stop_name FROM (SELECT maroutep.latitude, maroutep.longitude, stop_name, route_name, route_type FROM nodesp, maroutep WHERE nodesp.longitude=maroutep.longitude AND nodesp.latitude=maroutep.latitude) AS A , (SELECT maroutep.latitude, maroutep.longitude, stop_name, route_name, route_type FROM nodesp, maroutep WHERE nodesp.longitude=maroutep.longitude AND nodesp.latitude=maroutep.latitude) AS B WHERE A.stop_name=$${_fromstation}$$ AND B.stop_name=$${_tostation}$$ AND A.route_name=B.route_name AND A.stop_name<>B.stop_name AND A.route_type=3""")
                    self.conn.commit()
                    self.rows += self.cursor.fetchall()

                if _hops >= 2 : 
                    self.cursor.execute (""f"SELECT (A.latitude,A.longitude) AS coord1, A.stop_name, A.route_name, (B.latitude,B.longitude) AS coord2, B.stop_name, D.route_name, (D.latitude,D.longitude) AS coord3, D.stop_name FROM (SELECT maroutep.latitude, maroutep.longitude, stop_name, route_name, route_type FROM nodesp, maroutep WHERE nodesp.longitude=maroutep.longitude AND nodesp.latitude=maroutep.latitude) AS A, (SELECT maroutep.latitude, maroutep.longitude, stop_name, route_name, route_type FROM nodesp, maroutep WHERE nodesp.longitude=maroutep.longitude AND nodesp.latitude=maroutep.latitude) AS B, (SELECT maroutep.latitude, maroutep.longitude, stop_name, route_name, route_type FROM nodesp, maroutep WHERE nodesp.longitude=maroutep.longitude AND nodesp.latitude=maroutep.latitude) AS C , (SELECT maroutep.latitude, maroutep.longitude, stop_name, route_name, route_type FROM nodesp, maroutep WHERE nodesp.longitude=maroutep.longitude AND nodesp.latitude=maroutep.latitude) AS D WHERE A.stop_name=$${_fromstation}$$ AND D.stop_name=$${_tostation}$$ AND A.route_name=B.route_name AND B.stop_name=C.stop_name AND C.route_name=D.route_name AND A.route_name<>C.route_name AND A.route_type=3 AND D.route_type=3""")
                    self.conn.commit()
                    self.rows += self.cursor.fetchall()

                if _hops >= 3 : 
                    self.cursor.execute(""f"SELECT (A.latitude,A.longitude) AS coord1, A.stop_name, A.route_name, (B.latitude,B.longitude) AS coord2, B.stop_name, D.route_name, (D.latitude,D.longitude) AS coord3, D.stop_name, F.route_name, (F.latitude, F.longitude) AS coord4, F.stop_name FROM (SELECT maroutep.latitude, maroutep.longitude, stop_name, route_name, route_type FROM nodesp, maroutep WHERE nodesp.longitude=maroutep.longitude AND nodesp.latitude=maroutep.latitude) AS A , (SELECT maroutep.latitude, maroutep.longitude, stop_name, route_name, route_type FROM nodesp, maroutep WHERE nodesp.longitude=maroutep.longitude AND nodesp.latitude=maroutep.latitude) AS B , (SELECT maroutep.latitude, maroutep.longitude, stop_name, route_name, route_type FROM nodesp, maroutep WHERE nodesp.longitude=maroutep.longitude AND nodesp.latitude=maroutep.latitude) AS C , (SELECT maroutep.latitude, maroutep.longitude, stop_name, route_name, route_type FROM nodesp, maroutep WHERE nodesp.longitude=maroutep.longitude AND nodesp.latitude=maroutep.latitude) AS D, (SELECT maroutep.latitude, maroutep.longitude, stop_name, route_name, route_type FROM nodesp, maroutep WHERE nodesp.longitude=maroutep.longitude AND nodesp.latitude=maroutep.latitude) AS E , (SELECT maroutep.latitude, maroutep.longitude, stop_name, route_name, route_type FROM nodesp, maroutep WHERE nodesp.longitude=maroutep.longitude AND nodesp.latitude=maroutep.latitude) AS F WHERE A.stop_name=$${_fromstation}$$ AND F.stop_name=$${_tostation}$$ AND A.route_name=B.route_name AND B.stop_name=C.stop_name AND C.route_name=D.route_name AND D.stop_name=E.stop_name AND E.route_name=F.route_name AND A.route_name<>C.route_name AND C.route_name<>F.route_name AND A.route_type=3 AND D.route_type=3 AND F.route_type=3""")
                    self.conn.commit()
                    self.rows += self.cursor.fetchall()

            if _transport_type=='Métro':
                if _hops >= 1 : 
                    self.cursor.execute(""f" SELECT (A.latitude,A.longitude) AS coord1, A.stop_name, A.route_name, (B.latitude,B.longitude) AS coord2, B.stop_name FROM (SELECT maroutep.latitude, maroutep.longitude, stop_name, route_name, route_type FROM nodesp, maroutep WHERE nodesp.longitude=maroutep.longitude AND nodesp.latitude=maroutep.latitude) AS A , (SELECT maroutep.latitude, maroutep.longitude, stop_name, route_name, route_type FROM nodesp, maroutep WHERE nodesp.longitude=maroutep.longitude AND nodesp.latitude=maroutep.latitude) AS B WHERE A.stop_name=$${_fromstation}$$ AND B.stop_name=$${_tostation}$$ AND A.route_name=B.route_name AND A.stop_name<>B.stop_name AND A.route_type=1""")
                    self.conn.commit()
                    self.rows += self.cursor.fetchall()

                if _hops >= 2 : 
                    self.cursor.execute (""f"SELECT (A.latitude,A.longitude) AS coord1, A.stop_name, A.route_name, (B.latitude,B.longitude) AS coord2, B.stop_name, D.route_name, (D.latitude,D.longitude) AS coord3, D.stop_name FROM (SELECT maroutep.latitude, maroutep.longitude, stop_name, route_name, route_type FROM nodesp, maroutep WHERE nodesp.longitude=maroutep.longitude AND nodesp.latitude=maroutep.latitude) AS A, (SELECT maroutep.latitude, maroutep.longitude, stop_name, route_name, route_type FROM nodesp, maroutep WHERE nodesp.longitude=maroutep.longitude AND nodesp.latitude=maroutep.latitude) AS B, (SELECT maroutep.latitude, maroutep.longitude, stop_name, route_name, route_type FROM nodesp, maroutep WHERE nodesp.longitude=maroutep.longitude AND nodesp.latitude=maroutep.latitude) AS C , (SELECT maroutep.latitude, maroutep.longitude, stop_name, route_name, route_type FROM nodesp, maroutep WHERE nodesp.longitude=maroutep.longitude AND nodesp.latitude=maroutep.latitude) AS D WHERE A.stop_name=$${_fromstation}$$ AND D.stop_name=$${_tostation}$$ AND A.route_name=B.route_name AND B.stop_name=C.stop_name AND C.route_name=D.route_name AND A.route_name<>C.route_name AND A.route_type=1 AND D.route_type=1""")
                    self.conn.commit()
                    self.rows += self.cursor.fetchall()

                if _hops >= 3 : 
                    self.cursor.execute(""f"SELECT (A.latitude,A.longitude) AS coord1, A.stop_name, A.route_name, (B.latitude,B.longitude) AS coord2, B.stop_name, D.route_name, (D.latitude,D.longitude) AS coord3, D.stop_name, F.route_name, (F.latitude, F.longitude) AS coord4, F.stop_name FROM (SELECT maroutep.latitude, maroutep.longitude, stop_name, route_name, route_type FROM nodesp, maroutep WHERE nodesp.longitude=maroutep.longitude AND nodesp.latitude=maroutep.latitude) AS A , (SELECT maroutep.latitude, maroutep.longitude, stop_name, route_name, route_type FROM nodesp, maroutep WHERE nodesp.longitude=maroutep.longitude AND nodesp.latitude=maroutep.latitude) AS B , (SELECT maroutep.latitude, maroutep.longitude, stop_name, route_name, route_type FROM nodesp, maroutep WHERE nodesp.longitude=maroutep.longitude AND nodesp.latitude=maroutep.latitude) AS C , (SELECT maroutep.latitude, maroutep.longitude, stop_name, route_name, route_type FROM nodesp, maroutep WHERE nodesp.longitude=maroutep.longitude AND nodesp.latitude=maroutep.latitude) AS D, (SELECT maroutep.latitude, maroutep.longitude, stop_name, route_name, route_type FROM nodesp, maroutep WHERE nodesp.longitude=maroutep.longitude AND nodesp.latitude=maroutep.latitude) AS E , (SELECT maroutep.latitude, maroutep.longitude, stop_name, route_name, route_type FROM nodesp, maroutep WHERE nodesp.longitude=maroutep.longitude AND nodesp.latitude=maroutep.latitude) AS F WHERE A.stop_name=$${_fromstation}$$ AND F.stop_name=$${_tostation}$$ AND A.route_name=B.route_name AND B.stop_name=C.stop_name AND C.route_name=D.route_name AND D.stop_name=E.stop_name AND E.route_name=F.route_name AND A.route_name<>C.route_name AND C.route_name<>F.route_name AND A.route_type=1 AND D.route_type=1 AND F.route_type=1""")
                    self.conn.commit()
                    self.rows += self.cursor.fetchall()
            if _transport_type=='Tram':
                if _hops >= 1 : 
                    self.cursor.execute(""f" SELECT (A.latitude,A.longitude) AS coord1, A.stop_name, A.route_name, (B.latitude,B.longitude) AS coord2, B.stop_name FROM (SELECT maroutep.latitude, maroutep.longitude, stop_name, route_name, route_type FROM nodesp, maroutep WHERE nodesp.longitude=maroutep.longitude AND nodesp.latitude=maroutep.latitude) AS A , (SELECT maroutep.latitude, maroutep.longitude, stop_name, route_name, route_type FROM nodesp, maroutep WHERE nodesp.longitude=maroutep.longitude AND nodesp.latitude=maroutep.latitude) AS B WHERE A.stop_name=$${_fromstation}$$ AND B.stop_name=$${_tostation}$$ AND A.route_name=B.route_name AND A.stop_name<>B.stop_name AND A.route_type=0""")
                    self.conn.commit()
                    self.rows += self.cursor.fetchall()

                if _hops >= 2 : 
                    self.cursor.execute (""f"SELECT (A.latitude,A.longitude) AS coord1, A.stop_name, A.route_name, (B.latitude,B.longitude) AS coord2, B.stop_name, D.route_name, (D.latitude,D.longitude) AS coord3, D.stop_name FROM (SELECT maroutep.latitude, maroutep.longitude, stop_name, route_name, route_type FROM nodesp, maroutep WHERE nodesp.longitude=maroutep.longitude AND nodesp.latitude=maroutep.latitude) AS A, (SELECT maroutep.latitude, maroutep.longitude, stop_name, route_name, route_type FROM nodesp, maroutep WHERE nodesp.longitude=maroutep.longitude AND nodesp.latitude=maroutep.latitude) AS B, (SELECT maroutep.latitude, maroutep.longitude, stop_name, route_name, route_type FROM nodesp, maroutep WHERE nodesp.longitude=maroutep.longitude AND nodesp.latitude=maroutep.latitude) AS C , (SELECT maroutep.latitude, maroutep.longitude, stop_name, route_name, route_type FROM nodesp, maroutep WHERE nodesp.longitude=maroutep.longitude AND nodesp.latitude=maroutep.latitude) AS D WHERE A.stop_name=$${_fromstation}$$ AND D.stop_name=$${_tostation}$$ AND A.route_name=B.route_name AND B.stop_name=C.stop_name AND C.route_name=D.route_name AND A.route_name<>C.route_name AND A.route_type=0 AND D.route_type=0""")
                    self.conn.commit()
                    self.rows += self.cursor.fetchall()

                if _hops >= 3 : 
                    self.cursor.execute(""f"SELECT (A.latitude,A.longitude) AS coord1, A.stop_name, A.route_name, (B.latitude,B.longitude) AS coord2, B.stop_name, D.route_name, (D.latitude,D.longitude) AS coord3, D.stop_name, F.route_name, (F.latitude, F.longitude) AS coord4, F.stop_name FROM (SELECT maroutep.latitude, maroutep.longitude, stop_name, route_name, route_type FROM nodesp, maroutep WHERE nodesp.longitude=maroutep.longitude AND nodesp.latitude=maroutep.latitude) AS A , (SELECT maroutep.latitude, maroutep.longitude, stop_name, route_name, route_type FROM nodesp, maroutep WHERE nodesp.longitude=maroutep.longitude AND nodesp.latitude=maroutep.latitude) AS B , (SELECT maroutep.latitude, maroutep.longitude, stop_name, route_name, route_type FROM nodesp, maroutep WHERE nodesp.longitude=maroutep.longitude AND nodesp.latitude=maroutep.latitude) AS C , (SELECT maroutep.latitude, maroutep.longitude, stop_name, route_name, route_type FROM nodesp, maroutep WHERE nodesp.longitude=maroutep.longitude AND nodesp.latitude=maroutep.latitude) AS D, (SELECT maroutep.latitude, maroutep.longitude, stop_name, route_name, route_type FROM nodesp, maroutep WHERE nodesp.longitude=maroutep.longitude AND nodesp.latitude=maroutep.latitude) AS E , (SELECT maroutep.latitude, maroutep.longitude, stop_name, route_name, route_type FROM nodesp, maroutep WHERE nodesp.longitude=maroutep.longitude AND nodesp.latitude=maroutep.latitude) AS F WHERE A.stop_name=$${_fromstation}$$ AND F.stop_name=$${_tostation}$$ AND A.route_name=B.route_name AND B.stop_name=C.stop_name AND C.route_name=D.route_name AND D.stop_name=E.stop_name AND E.route_name=F.route_name AND A.route_name<>C.route_name AND C.route_name<>F.route_name AND A.route_type=0 AND D.route_type=0 AND F.route_type=0""")
                    self.conn.commit()
                    self.rows += self.cursor.fetchall()

            if _transport_type=='Rail':
                if _hops >= 1 : 
                    self.cursor.execute(""f" SELECT (A.latitude,A.longitude) AS coord1, A.stop_name, A.route_name, (B.latitude,B.longitude) AS coord2, B.stop_name FROM (SELECT maroutep.latitude, maroutep.longitude, stop_name, route_name, route_type FROM nodesp, maroutep WHERE nodesp.longitude=maroutep.longitude AND nodesp.latitude=maroutep.latitude) AS A , (SELECT maroutep.latitude, maroutep.longitude, stop_name, route_name, route_type FROM nodesp, maroutep WHERE nodesp.longitude=maroutep.longitude AND nodesp.latitude=maroutep.latitude) AS B WHERE A.stop_name=$${_fromstation}$$ AND B.stop_name=$${_tostation}$$ AND A.route_name=B.route_name AND A.stop_name<>B.stop_name AND A.route_type=2""")
                    self.conn.commit()
                    self.rows += self.cursor.fetchall()

                if _hops >= 2 : 
                    self.cursor.execute (""f"SELECT (A.latitude,A.longitude) AS coord1, A.stop_name, A.route_name, (B.latitude,B.longitude) AS coord2, B.stop_name, D.route_name, (D.latitude,D.longitude) AS coord3, D.stop_name FROM (SELECT maroutep.latitude, maroutep.longitude, stop_name, route_name, route_type FROM nodesp, maroutep WHERE nodesp.longitude=maroutep.longitude AND nodesp.latitude=maroutep.latitude) AS A, (SELECT maroutep.latitude, maroutep.longitude, stop_name, route_name, route_type FROM nodesp, maroutep WHERE nodesp.longitude=maroutep.longitude AND nodesp.latitude=maroutep.latitude) AS B, (SELECT maroutep.latitude, maroutep.longitude, stop_name, route_name, route_type FROM nodesp, maroutep WHERE nodesp.longitude=maroutep.longitude AND nodesp.latitude=maroutep.latitude) AS C , (SELECT maroutep.latitude, maroutep.longitude, stop_name, route_name, route_type FROM nodesp, maroutep WHERE nodesp.longitude=maroutep.longitude AND nodesp.latitude=maroutep.latitude) AS D WHERE A.stop_name=$${_fromstation}$$ AND D.stop_name=$${_tostation}$$ AND A.route_name=B.route_name AND B.stop_name=C.stop_name AND C.route_name=D.route_name AND A.route_name<>C.route_name AND A.route_type=2 AND D.route_type=2""")
                    self.conn.commit()
                    self.rows += self.cursor.fetchall()

                if _hops >= 3 : 
                    self.cursor.execute(""f"SELECT (A.latitude,A.longitude) AS coord1, A.stop_name, A.route_name, (B.latitude,B.longitude) AS coord2, B.stop_name, D.route_name, (D.latitude,D.longitude) AS coord3, D.stop_name, F.route_name, (F.latitude, F.longitude) AS coord4, F.stop_name FROM (SELECT maroutep.latitude, maroutep.longitude, stop_name, route_name, route_type FROM nodesp, maroutep WHERE nodesp.longitude=maroutep.longitude AND nodesp.latitude=maroutep.latitude) AS A , (SELECT maroutep.latitude, maroutep.longitude, stop_name, route_name, route_type FROM nodesp, maroutep WHERE nodesp.longitude=maroutep.longitude AND nodesp.latitude=maroutep.latitude) AS B , (SELECT maroutep.latitude, maroutep.longitude, stop_name, route_name, route_type FROM nodesp, maroutep WHERE nodesp.longitude=maroutep.longitude AND nodesp.latitude=maroutep.latitude) AS C , (SELECT maroutep.latitude, maroutep.longitude, stop_name, route_name, route_type FROM nodesp, maroutep WHERE nodesp.longitude=maroutep.longitude AND nodesp.latitude=maroutep.latitude) AS D, (SELECT maroutep.latitude, maroutep.longitude, stop_name, route_name, route_type FROM nodesp, maroutep WHERE nodesp.longitude=maroutep.longitude AND nodesp.latitude=maroutep.latitude) AS E , (SELECT maroutep.latitude, maroutep.longitude, stop_name, route_name, route_type FROM nodesp, maroutep WHERE nodesp.longitude=maroutep.longitude AND nodesp.latitude=maroutep.latitude) AS F WHERE A.stop_name=$${_fromstation}$$ AND F.stop_name=$${_tostation}$$ AND A.route_name=B.route_name AND B.stop_name=C.stop_name AND C.route_name=D.route_name AND D.stop_name=E.stop_name AND E.route_name=F.route_name AND A.route_name<>C.route_name AND C.route_name<>F.route_name AND A.route_type=2 AND D.route_type=0 AND F.route_type=2""")
                    self.conn.commit()
                    self.rows += self.cursor.fetchall()

                    
        

        if len(self.rows) == 0 : 
            self.tableWidget.setRowCount(0)
            self.tableWidget.setColumnCount(0)
            return

        numrows = len(self.rows)
        numcols = len(self.rows[-1]) - math.floor(len(self.rows[-1]) / 3.0) - 1 
        self.tableWidget.setRowCount(numrows)
        self.tableWidget.setColumnCount(numcols)

        i = 0
        for row in self.rows : 
            j = 0
            k = 0 
            for col in row :
                if j % 3 == 0 : 
                    k = k + 1
                else : 
                    self.tableWidget.setItem(i, j-k, QTableWidgetItem(str(col)))
                j = j + 1
            i = i + 1

        header = self.tableWidget.horizontalHeader()
        j = 0
        while j < numcols : 
            header.setSectionResizeMode(j, QHeaderView.ResizeToContents)
            j = j+1
        
        #wait.close()
        self.update()	
        #waiting.setValue(100)
        #self._waiting.close()


    def button_Clear(self):
        self.webView.clearMap(self.maptype_box.currentIndex())
        self.startingpoint = True
        self.tableWidget.clearContents()
        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnCount(0)
        self.rows = []
        self.update()


    def mouseClick(self, lat, lng):
        self.webView.addPointMarker(lat, lng)
        ville = str(self.ville_box.currentText())
        print(f"Clicked on: latitude {lat}, longitude {lng}")
        if ville == 'Bordeaux':
            self.cursor.execute(""f" WITH mytable (distance, name) AS (SELECT ( ABS(latitude-$${lat}$$) + ABS(longitude-$${lng}$$) ), stop_name FROM nodesb) SELECT A.name FROM mytable as A WHERE A.distance <=  (SELECT min(B.distance) FROM mytable as B)  """)
            self.conn.commit()
            rows = self.cursor.fetchall()
            if self.startingpoint :
                self.from_box.setCurrentIndex(self.from_box.findText(rows[0][0], Qt.MatchFixedString))
            else :
                self.to_box.setCurrentIndex(self.to_box.findText(rows[0][0], Qt.MatchFixedString))
            self.startingpoint = not self.startingpoint
        if ville == 'Grenoble':
            self.cursor.execute(""f" WITH mytable (distance, name) AS (SELECT ( ABS(latitude-$${lat}$$) + ABS(longitude-$${lng}$$) ), stop_name FROM nodesg) SELECT A.name FROM mytable as A WHERE A.distance <=  (SELECT min(B.distance) FROM mytable as B)  """)
            self.conn.commit()
            rows = self.cursor.fetchall()
            if self.startingpoint :
                self.from_box.setCurrentIndex(self.from_box.findText(rows[0][0], Qt.MatchFixedString))
            else :
                self.to_box.setCurrentIndex(self.to_box.findText(rows[0][0], Qt.MatchFixedString))
            self.startingpoint = not self.startingpoint
        if ville == 'Nantes':
            self.cursor.execute(""f" WITH mytable (distance, name) AS (SELECT ( ABS(latitude-$${lat}$$) + ABS(longitude-$${lng}$$) ), stop_name FROM nodesn) SELECT A.name FROM mytable as A WHERE A.distance <=  (SELECT min(B.distance) FROM mytable as B)  """)
            self.conn.commit()
            rows = self.cursor.fetchall()
            if self.startingpoint :
                self.from_box.setCurrentIndex(self.from_box.findText(rows[0][0], Qt.MatchFixedString))
            else :
                self.to_box.setCurrentIndex(self.to_box.findText(rows[0][0], Qt.MatchFixedString))
            self.startingpoint = not self.startingpoint
        if ville == 'Rennes':
            self.cursor.execute(""f" WITH mytable (distance, name) AS (SELECT ( ABS(latitude-$${lat}$$) + ABS(longitude-$${lng}$$) ), stop_name FROM nodesr) SELECT A.name FROM mytable as A WHERE A.distance <=  (SELECT min(B.distance) FROM mytable as B)  """)
            self.conn.commit()
            rows = self.cursor.fetchall()
            if self.startingpoint :
                self.from_box.setCurrentIndex(self.from_box.findText(rows[0][0], Qt.MatchFixedString))
            else :
                self.to_box.setCurrentIndex(self.to_box.findText(rows[0][0], Qt.MatchFixedString))
            self.startingpoint = not self.startingpoint
        if ville == 'Toulouse':
            self.cursor.execute(""f" WITH mytable (distance, name) AS (SELECT ( ABS(latitude-$${lat}$$) + ABS(longitude-$${lng}$$) ), stop_name FROM nodest) SELECT A.name FROM mytable as A WHERE A.distance <=  (SELECT min(B.distance) FROM mytable as B)  """)
            self.conn.commit()
            rows = self.cursor.fetchall()
            if self.startingpoint :
                self.from_box.setCurrentIndex(self.from_box.findText(rows[0][0], Qt.MatchFixedString))
            else :
                self.to_box.setCurrentIndex(self.to_box.findText(rows[0][0], Qt.MatchFixedString))
            self.startingpoint = not self.startingpoint
        if ville == 'Paris':
            self.cursor.execute(""f" WITH mytable (distance, name) AS (SELECT ( ABS(latitude-$${lat}$$) + ABS(longitude-$${lng}$$) ), stop_name FROM nodesp) SELECT A.name FROM mytable as A WHERE A.distance <=  (SELECT min(B.distance) FROM mytable as B)  """)
            self.conn.commit()
            rows = self.cursor.fetchall()
            if self.startingpoint :
                self.from_box.setCurrentIndex(self.from_box.findText(rows[0][0], Qt.MatchFixedString))
            else :
                self.to_box.setCurrentIndex(self.to_box.findText(rows[0][0], Qt.MatchFixedString))
            self.startingpoint = not self.startingpoint


class myWebView (QWebEngineView):
    def __init__(self):
        super().__init__()

        self.maptypes = ["OpenStreetMap", "Stamen Terrain", "stamentoner", "cartodbpositron"]
        self.setMap(0)


    def add_customjs(self, map_object):
        my_js = f"""{map_object.get_name()}.on("click",
                 function (e) {{
                    var data = `{{"coordinates": ${{JSON.stringify(e.latlng)}}}}`;
                    console.log(data)}}); """
        e = Element(my_js)
        html = map_object.get_root()
        html.script.get_root().render()
        html.script._children[e.get_name()] = e

        return map_object


    def handleClick(self, msg):
        data = json.loads(msg)
        lat = data['coordinates']['lat']
        lng = data['coordinates']['lng']

        window.mouseClick(lat, lng)
        


    def addSegment(self, lat1, lng1, lat2, lng2):
        js = Template(
        """
        L.polyline(
            [ [{{latitude1}}, {{longitude1}}], [{{latitude2}}, {{longitude2}}] ], {
                "color": "red",
                "opacity": 1.0,
                "weight": 4,
                "line_cap": "butt"
            }
        ).addTo({{map}});
        """
        ).render(map=self.mymap.get_name(), latitude1=lat1, longitude1=lng1, latitude2=lat2, longitude2=lng2 )

        self.page().runJavaScript(js)


    def addMarker(self, lat, lng):
        js = Template(
        """
        L.marker([{{latitude}}, {{longitude}}] ).addTo({{map}});
        L.circleMarker(
            [{{latitude}}, {{longitude}}], {
                "bubblingMouseEvents": true,
                "color": "#3388ff",
                "popup": "hello",
                "dashArray": null,
                "dashOffset": null,
                "fill": false,
                "fillColor": "#3388ff",
                "fillOpacity": 0.2,
                "fillRule": "evenodd",
                "lineCap": "round",
                "lineJoin": "round",
                "opacity": 1.0,
                "radius": 2,
                "stroke": true,
                "weight": 5
            }
        ).addTo({{map}});
        """
        ).render(map=self.mymap.get_name(), latitude=lat, longitude=lng)
        self.page().runJavaScript(js)


    def addPointMarker(self, lat, lng):
        js = Template(
        """
        L.circleMarker(
            [{{latitude}}, {{longitude}}], {
                "bubblingMouseEvents": true,
                "color": 'green',
                "popup": "hello",
                "dashArray": null,
                "dashOffset": null,
                "fill": false,
                "fillColor": 'green',
                "fillOpacity": 0.2,
                "fillRule": "evenodd",
                "lineCap": "round",
                "lineJoin": "round",
                "opacity": 1.0,
                "radius": 2,
                "stroke": true,
                "weight": 5
            }
        ).addTo({{map}});
        """
        ).render(map=self.mymap.get_name(), latitude=lat, longitude=lng)
        self.page().runJavaScript(js)


    def setMap (self, i):

        global malocation

        ###### Bordeaux = 4 ######
        if i == 4:
            self.mymap = folium.Map(location=[44.8305, -0.56], tiles=self.maptypes[0], zoom_start=12, prefer_canvas=True)
            malocation = [44.8305, -0.56]

        #debut + changement map Bordeaux
        if i == 0 and malocation == [44.8305, -0.56] or malocation == [0,0]:
            self.mymap = folium.Map(location=[44.8305, -0.56], tiles=self.maptypes[0], zoom_start=12, prefer_canvas=True)
            malocation = [44.8305, -0.56]

        if i == 1 and malocation == [44.8305, -0.56]:
            self.mymap = folium.Map(location=[44.8305, -0.56], tiles=self.maptypes[1], zoom_start=12, prefer_canvas=True)
            malocation = [44.8305, -0.56]

        if i == 2 and malocation == [44.8305, -0.56]:
            self.mymap = folium.Map(location=[44.8305, -0.56], tiles=self.maptypes[2], zoom_start=12, prefer_canvas=True)
            malocation = [44.8305, -0.56]

        if i == 3 and malocation == [44.8305, -0.56]:
            self.mymap = folium.Map(location=[44.8305, -0.56], tiles=self.maptypes[3], zoom_start=12, prefer_canvas=True)
            malocation = [44.8305, -0.56]
        
        ###### Paris = 5 ######
        if i == 5:
            self.mymap = folium.Map(location=[48.8619, 2.3519], tiles=self.maptypes[0], zoom_start=12, prefer_canvas=True)
            malocation = [48.8619, 2.3519]

        #changement map Paris
        if i == 0 and malocation == [48.8619, 2.3519]:
            self.mymap = folium.Map(location=[48.8619, 2.3519], tiles=self.maptypes[0], zoom_start=12, prefer_canvas=True)
            malocation = [48.8619, 2.3519]

        if i == 1 and malocation == [48.8619, 2.3519]:
            self.mymap = folium.Map(location=[48.8619, 2.3519], tiles=self.maptypes[1], zoom_start=12, prefer_canvas=True)
            malocation = [48.8619, 2.3519]
        
        if i == 2 and malocation == [48.8619, 2.3519]:
            self.mymap = folium.Map(location=[48.8619, 2.3519], tiles=self.maptypes[2], zoom_start=12, prefer_canvas=True)
            malocation = [48.8619, 2.3519]

        if i == 3 and malocation == [48.8619, 2.3519]:
            self.mymap = folium.Map(location=[48.8619, 2.3519], tiles=self.maptypes[3], zoom_start=12, prefer_canvas=True)
            malocation = [48.8619, 2.3519]

        ###### Rennes = 6 ######
        if i == 6:
            self.mymap = folium.Map(location=[48.1079, -1.6749], tiles=self.maptypes[0], zoom_start=12, prefer_canvas=True)
            malocation = [48.1079, -1.6749]

        #changement map Rennes
        if i == 0 and malocation == [48.1079, -1.6749]:
            self.mymap = folium.Map(location=[48.1079, -1.6749], tiles=self.maptypes[0], zoom_start=12, prefer_canvas=True)
            malocation = [48.1079, -1.6749]

        if i == 1 and malocation == [48.1079, -1.6749]:
            self.mymap = folium.Map(location=[48.1079, -1.6749], tiles=self.maptypes[1], zoom_start=12, prefer_canvas=True)
            malocation = [48.1079, -1.6749]

        if i == 2 and malocation == [48.1079, -1.6749]:
            self.mymap = folium.Map(location=[48.1079, -1.6749], tiles=self.maptypes[2], zoom_start=12, prefer_canvas=True)
            malocation = [48.1079, -1.6749]

        if i == 3 and malocation == [48.1079, -1.6749]:
            self.mymap = folium.Map(location=[48.1079, -1.6749], tiles=self.maptypes[3], zoom_start=12, prefer_canvas=True)
            malocation = [48.1079, -1.6749]

        ###### Grenoble = 7 ######
        if i == 7:
            self.mymap = folium.Map(location=[45.1772, 5.7228], tiles=self.maptypes[0], zoom_start=12, prefer_canvas=True)
            malocation = [45.1772, 5.7228]

        #changement map Grenoble
        if i == 0 and malocation == [45.1772, 5.7228]:
            self.mymap = folium.Map(location=[45.1772, 5.7228], tiles=self.maptypes[0], zoom_start=12, prefer_canvas=True)
            malocation = [45.1772, 5.7228]

        if i == 1 and malocation == [45.1772, 5.7228]:
            self.mymap = folium.Map(location=[45.1772, 5.7228], tiles=self.maptypes[1], zoom_start=12, prefer_canvas=True)
            malocation = [45.1772, 5.7228]
        
        if i == 2 and malocation == [45.1772, 5.7228]:
            self.mymap = folium.Map(location=[45.1772, 5.7228], tiles=self.maptypes[2], zoom_start=12, prefer_canvas=True)
            malocation = [45.1772, 5.7228]

        if i == 3 and malocation == [45.1772, 5.7228]:
            self.mymap = folium.Map(location=[45.1772, 5.7228], tiles=self.maptypes[3], zoom_start=12, prefer_canvas=True)
            malocation = [45.1772, 5.7228]

        ###### Nantes = 8 ######
        if i == 8:
            self.mymap = folium.Map(location=[47.2133, -1.5516], tiles=self.maptypes[0], zoom_start=12, prefer_canvas=True)
            malocation = [47.2133, -1.5516]

        #changement map Nantes
        if i == 0 and malocation == [47.2133, -1.5516]:
            self.mymap = folium.Map(location=[47.2133, -1.5516], tiles=self.maptypes[0], zoom_start=12, prefer_canvas=True)
            malocation = [47.2133, -1.5516]

        if i == 1 and malocation == [47.2133, -1.5516]:
            self.mymap = folium.Map(location=[47.2133, -1.5516], tiles=self.maptypes[1], zoom_start=12, prefer_canvas=True)
            malocation = [47.2133, -1.5516]
        
        if i == 2 and malocation == [47.2133, -1.5516]:
            self.mymap = folium.Map(location=[47.2133, -1.5516], tiles=self.maptypes[2], zoom_start=12, prefer_canvas=True)
            malocation = [47.2133, -1.5516]

        if i == 3 and malocation == [47.2133, -1.5516]:
            self.mymap = folium.Map(location=[47.2133, -1.5516], tiles=self.maptypes[3], zoom_start=12, prefer_canvas=True)
            malocation = [47.2133, -1.5516]

        ###### Toulouse = 9 ######
        if i == 9:
            self.mymap = folium.Map(location=[43.6021, 1.4428], tiles=self.maptypes[0], zoom_start=12, prefer_canvas=True)
            malocation = [43.6021, 1.4428]

        #changement map Toulouse
        if i == 0 and malocation == [43.6021, 1.4428]:
            self.mymap = folium.Map(location=[43.6021, 1.4428], tiles=self.maptypes[0], zoom_start=12, prefer_canvas=True)
            malocation = [43.6021, 1.4428]

        if i == 1 and malocation == [43.6021, 1.4428]:
            self.mymap = folium.Map(location=[43.6021, 1.4428], tiles=self.maptypes[1], zoom_start=12, prefer_canvas=True)
            malocation = [43.6021, 1.4428]
        
        if i == 2 and malocation == [43.6021, 1.4428]:
            self.mymap = folium.Map(location=[43.6021, 1.4428], tiles=self.maptypes[2], zoom_start=12, prefer_canvas=True)
            malocation = [43.6021, 1.4428]
        
        if i == 3 and malocation == [43.6021, 1.4428]:
            self.mymap = folium.Map(location=[43.6021, 1.4428], tiles=self.maptypes[3], zoom_start=12, prefer_canvas=True)
            malocation = [43.6021, 1.4428]



        self.mymap = self.add_customjs(self.mymap)

        page = WebEnginePage(self)
        self.setPage(page)

        data = io.BytesIO()
        self.mymap.save(data, close_file=False)

        self.setHtml(data.getvalue().decode())

    def clearMap(self, index):
        self.setMap(index)



class WebEnginePage(QWebEnginePage):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

    def javaScriptConsoleMessage(self, level, msg, line, sourceID):
        #print(msg)
        if 'coordinates' in msg:
            self.parent.handleClick(msg)


       
			
if __name__ == '__main__':
    app = QApplication(sys.argv) 
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())