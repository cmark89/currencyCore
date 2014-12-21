#!/usr/bin/python

import sys
from urllib.request import urlopen
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class Form(QDialog):
	def __init__(self, parent=None):
		super(Form, self).__init__(parent)

		date = self.getdata()
		rates = sorted(self.rates.keys())

		dateLabel = QLabel(date)
		self.fromComboBox = QComboBox()
		self.fromComboBox.addItems(rates)
		self.fromSpinBox = QDoubleSpinBox()
		self.fromSpinBox.setRange(.01, 100000000)
		self.toComboBox = QComboBox()
		self.toComboBox.addItems(rates)
		self.toLabel = QLabel("1.00")

		grid = QGridLayout()
		grid.addWidget(dateLabel, 0, 0)
		grid.addWidget(self.fromComboBox, 1, 0)
		grid.addWidget(self.fromSpinBox, 1, 1)
		grid.addWidget(self.toComboBox, 2, 0)
		grid.addWidget(self.toLabel,2, 1)
		self.setLayout(grid)

		self.connect(self.fromComboBox, SIGNAL("currentIndexChanged(int)"), \
					self.updateUi)
		self.connect(self.toComboBox, SIGNAL("currentIndexChanged(int)"), \
					self.updateUi)
		self.connect(self.fromSpinBox, SIGNAL("valueChanged(double)"), \
					self.updateUi)
		self.setWindowTitle("Currency")

	def updateUi(self):
		to = self.toComboBox.currentText()
		from_ = self.fromComboBox.currentText()
		amount = (self.rates[from_] / self.rates[to]) * \
				self.fromSpinBox.value()
		self.toLabel.setText("%0.2f" % amount)

	def getdata(self):
		self.rates = {}
		try:
			date = "Unknown"
			url = ("http://www.bankofcanada.ca"
				    	"/en/markets/csv/exchange_eng.csv")
			fh = urlopen(url)
			for b_line in fh.readlines():
				line = b_line.decode('utf-8')
				if not line or line.startswith(("#", "Closing")):
					continue

				fields = line.split(",")
				if line.startswith("Date"):
					date = fields[-1]
				else:
					try:
						value = float(fields[-1])
						self.rates[fields[0]] = value
					except ValueError as e:
						pass
			return "Exchange Rates Date: " + date
		except Exception as e:
			return "%s" % e


app = QApplication(sys.argv)
form = Form()
form.show()
app.exec_()
