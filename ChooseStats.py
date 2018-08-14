# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'choose_stats.ui'
#
# Created by: PyQt5 UI code generator 5.8
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import pandas as pd
import cx_Oracle

try:
	_fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
	def _fromUtf8(s):
		return s

try:
	_encoding = QtWidgets.QApplication.UnicodeUTF8
	def _translate(context, text, disambig):
		return QtWidgets.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
	def _translate(context, text, disambig):
		return QtWidgets.QApplication.translate(context, text, disambig)

class Ui_ChooseStats(object):
	def __init__(self):
		self.metric_name=[]
		self.metric_descriptions=[]
		self.metric_names_original=[]
		
	def setupUi(self, ChooseStats, db):
		self.ChooseStats=ChooseStats
		self.db=db
		ChooseStats.setObjectName("ChooseStats")
		ChooseStats.resize(346, 333)
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(ChooseStats.sizePolicy().hasHeightForWidth())
		ChooseStats.setSizePolicy(sizePolicy)
		self.verticalLayout = QtWidgets.QVBoxLayout(self.ChooseStats)
		self.verticalLayout.setSpacing(7)
		self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))

		self.SearchStat = QtWidgets.QLineEdit(ChooseStats)
		self.SearchStat.setGeometry(QtCore.QRect(159, 300, 171, 31))
		
		self.buttonBox = QtWidgets.QDialogButtonBox(ChooseStats)
		self.buttonBox.setGeometry(QtCore.QRect(159, 300, 171, 31))
		self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
		self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
		self.buttonBox.setObjectName("buttonBox")
		self.MetricDef = QtWidgets.QTreeWidget(ChooseStats)
		self.MetricDef.setGeometry(QtCore.QRect(20, 20, 331, 310))
		self.MetricDef.setColumnCount(2)
		self.MetricDef.setObjectName("MetricDef")
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.MetricDef.sizePolicy().hasHeightForWidth())
		self.MetricDef.setSizePolicy(sizePolicy)
		self.verticalLayout.addWidget(self.SearchStat)
		self.verticalLayout.addWidget(self.MetricDef)
		self.verticalLayout.addWidget(self.buttonBox)
		self.load_metric_def()
		self.retranslateUi(ChooseStats)
		self.buttonBox.accepted.connect(self.get_selected_stat)
		self.buttonBox.rejected.connect(self.reject)
		self.SearchStat.textChanged.connect(self.searchtree)
		self.metric_classes={"OS STAT":"OS ","IO Stats":"IS ", "Wait Events":"WE ","SYS Time Model":"ST ",'User':'', 'Redo':'',
		'Enqueue':'', 'Cache':'', 'OS':'', 'RAC':'','SQL':'','USER+RAC':'', 'Redo+RAC':'','Cache+RAC':'','SQL+Cache':''}
		QtCore.QMetaObject.connectSlotsByName(ChooseStats)

	def searchtree(self):
		# trying to search the tree to only show the items corresponding to what is in the SearchStat field
		st=self.SearchStat.text()
		matching_items=self.MetricDef.findItems(st,QtCore.Qt.MatchContains|QtCore.Qt.MatchRecursive,1)
		iter=QtWidgets.QTreeWidgetItemIterator(self.MetricDef) 
		while iter.value():
			i=iter.value()
			if st=="CLEAR":
				i.setCheckState(0, QtCore.Qt.Unchecked)
			if i not in matching_items  and i.parent():
				i.setHidden(True)
			else:
				i.setHidden(False)
			iter+=1
		if st=="CLEAR":
			self.metric_names_original=[]
	def reject(self):
		self.is_accepted=False
		self.ChooseStats.close()

	def get_selected_stat(self):
		iterator = QtWidgets.QTreeWidgetItemIterator(self.MetricDef, QtWidgets.QTreeWidgetItemIterator.Checked)
		current_items=[]
		self.metric_names_original=[]
		while iterator.value():
			item = iterator.value()
			met_class=item.text(0)
			metr=item.text(1)
			#print("class= ",met_class)
			met=self.metric_classes[met_class]+metr
			# if met_class=="OS STAT":
			# 	met="OS "+metr
			# elif met_class=="SYS Time Model":
			# 		met="ST "+metr
			# elif met_class=="Wait Events":
			# 		met="WE "+metr
			# else:
			# 		met=item.text(1)

			self.metric_names_original.append([met_class,metr])
			current_items.append(met)
			if met not in self.metric_name:
				self.metric_name.append(met)
				self.first_time=True
			iterator += 1
		metric_names=self.metric_name.copy()
		for i in self.metric_name:
			if i not in current_items:
#				print("removing in choose ", i)
				metric_names.pop(metric_names.index(i))
		self.metric_name=metric_names.copy()
		self.ChooseStats.close()

	def load_metric_def(self):
		if self.db is not None:
			if len(self.metric_descriptions)==0:
				self.metric_descriptions=pd.read_sql_query("select case class when 1  then 'User' when 2  then 'Redo' when 4 then 'Enqueue' when \
						8 then 'Cache' when 16 then 'OS' when 32 then 'RAC' when 64 then 'SQL' when 33 then	 'USER+RAC' when 34 then 'Redo+RAC' when 40 then 'Cache+RAC' \
						when 72 then 'SQL+Cache' end class,	 name from v$sysstat where class<128  \
						union all \
						select 'OS STAT', stat_name \
						from v$osstat \
						union all \
						select 'SYS Time Model', stat_name \
						from v$sys_time_model \
						union all \
						select 'Wait Events', name \
						from v$event_name \
						union all \
						select 'IO Stats', function_name \
						from v$IOstat_function \
						order by 1,2",self.db)
			root_ot=""
			mxl1=0
			mxl2=0
			for i in range(len(self.metric_descriptions)):
				if root_ot!=self.metric_descriptions.iloc[i]['CLASS']:
					rootl=[self.metric_descriptions.iloc[i]['CLASS']," "]
					root = QtWidgets.QTreeWidgetItem(self.MetricDef, rootl)
#					root = QtWidgets.QTreeWidgetItem(self.MetricDef, list(self.metric_descriptions.iloc[i][['CLASS','NAME']]))
					root_ot=self.metric_descriptions.iloc[i]['CLASS']
					if mxl1<len(root_ot):
						mxl1=len(root_ot)
					root.setFlags(root.flags())# | QtCore.Qt.ItemIsUserCheckable)
#					if self.metric_descriptions.iloc[i]['NAME'] in self.metric_name:
#						root.setCheckState(0, QtCore.Qt.Checked)
#					else:
#						root.setCheckState(0, QtCore.Qt.Unchecked)
#				else:
				class_name=list(self.metric_descriptions.iloc[i][['CLASS','NAME']])
				child=QtWidgets.QTreeWidgetItem(root, list(self.metric_descriptions.iloc[i][['CLASS','NAME']]))
				if mxl2<len(self.metric_descriptions.iloc[i]['NAME']):
					mxl2=len(self.metric_descriptions.iloc[i]['NAME'])
				child.setFlags(child.flags() | QtCore.Qt.ItemIsUserCheckable)
				if class_name in self.metric_names_original:
					child.setCheckState(0, QtCore.Qt.Checked)
				else:
					child.setCheckState(0, QtCore.Qt.Unchecked)
			for i in range(self.MetricDef.columnCount()):
				self.MetricDef.resizeColumnToContents(i)


	def retranslateUi(self, ChooseStats):
		_translate = QtCore.QCoreApplication.translate
		ChooseStats.setWindowTitle(_translate("ChooseStats", "Choose Statistics to Graph"))
		self.MetricDef.headerItem().setText(0, _translate("ChooseStats", "Class"))
		self.MetricDef.headerItem().setText(1, _translate("ChooseStats", "Name"))

