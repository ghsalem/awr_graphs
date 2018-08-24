# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'choose_stats.ui'
#
# Created by: PyQt5 UI code generator 5.8
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
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

class Ui_ChooseDB(object):
	def __init__(self):
		self.db_name=[]
		self.dbs_list=[]
		self.db_name==""
		self.db_id=None
		self.instance_number=''
		self.begin_snap=''
		self.end_snap=''		
	def setupUi(self, ChooseDB, parent):
		self.ChooseDB=ChooseDB
		self.db=parent.db
		self.awr_location=parent.awr_location
		ChooseDB.setObjectName("ChooseDB")
		ChooseDB.resize(546, 433)
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(ChooseDB.sizePolicy().hasHeightForWidth())
		ChooseDB.setSizePolicy(sizePolicy)
		self.verticalLayout = QtWidgets.QVBoxLayout(self.ChooseDB)
		self.verticalLayout.setSpacing(7)
		self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
		self.buttonBox = QtWidgets.QDialogButtonBox(ChooseDB)
		self.buttonBox.setGeometry(QtCore.QRect(159, 300, 171, 31))
		self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
		self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
		self.buttonBox.setObjectName("buttonBox")
		self.DBList = QtWidgets.QTreeWidget(ChooseDB)#QtWidgets.QAbstractItemView.SingleSelection)
		self.DBList.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
		self.DBList.setGeometry(QtCore.QRect(20, 20, 331, 310))
		self.DBList.setColumnCount(7)
		self.DBList.setObjectName("DBList")
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.DBList.sizePolicy().hasHeightForWidth())
		self.DBList.setSizePolicy(sizePolicy)
		self.verticalLayout.addWidget(self.DBList)
		self.verticalLayout.addWidget(self.buttonBox)
		self.load_metric_def()
		self.retranslateUi(ChooseDB)
		self.buttonBox.accepted.connect(self.get_selected_stat)
		self.buttonBox.rejected.connect(self.reject)
		#print(self.DBList.SelectionMode(), QtWidgets.QAbstractItemView.SingleSelection)
		QtCore.QMetaObject.connectSlotsByName(ChooseDB)

	def reject(self):
		self.is_accepted=False
		self.ChooseDB.close()

	def get_selected_stat(self):
		iterator = QtWidgets.QTreeWidgetItemIterator(self.DBList, QtWidgets.QTreeWidgetItemIterator.Checked)
		self.db_name=""
		self.begin_snap=0
		self.end_snap=0
		startup_time=''
		while iterator.value():
			item = iterator.value()
			if self.db_name=="":
				self.db_name=item.text(0)
				self.db_id=item.text(1)
				self.instance_number=item.text(3)
				self.begin_snap=item.text(5)
				self.begin_interval=item.text(4)
				startup_time=item.text(6)
			elif item.text(0)!=self.db_name or self.instance_number!=item.text(3) or startup_time!=item.text(6):
				choice = QMessageBox.question(self.ChooseDB, 'Error',"Please select snapshots for same DB, instance and startup time", QMessageBox.Yes)
				self.db_name=""
			else:
				self.end_snap=item.text(5)
				self.end_interval=item.text(4)
			iterator += 1
		# self.db_name=selected_db_span.text(0)
		# self.db_id=selected_db_span.text(1)
		# self.instance_number=selected_db_span.text(2)
		# self.begin_snap=selected_db_span.text(4)
		# self.end_snap=selected_db_span.text(5)
#		print(self.db_name,self.begin_snap)
		if self.db_name!="":
			self.ChooseDB.close()

	def load_metric_def(self):
		if self.db is not None:
			# self.dbs_list=pd.read_sql_query("select to_char(dbs.dbid) db_id, db_name,to_char(dbs.instance_number) instance_number,\
			# to_char(dbs.startup_time,'dd/mm/yyyy hh24:mi:ss') startup_time,  min_snap, max_snap \
			# from awr_pdb_database_instance dbs, (select dbid, startup_time, instance_number, to_char(min(snap_id)) min_snap, to_char(max(snap_id)) max_snap \
			# from awr_pdb_snapshot s \
			# group by dbid,instance_number,startup_time) s \
			# where dbs.dbid=s.dbid and dbs.startup_time=s.startup_time and dbs.instance_number=s.instance_number \
			# order by dbs.db_name,dbs.startup_time",self.db)
			self.dbs_list=pd.read_sql_query("select distinct to_char(dbs.dbid) db_id, db_name,pdb_name,to_char(dbs.instance_number) instance_number, \
			to_char(s.startup_time,'dd/mm/yyyy hh24:mi:ss') startup_time, \
			to_char(begin_interval_time,'dd/mm/yyyy hh24:mi:ss') begin_time,to_char(s.snap_id) snap_id \
			from "+self.awr_location+"_database_instance dbs,"+self.awr_location+"_ash_snapshot s , "+self.awr_location+"_pdb_instance p \
			where dbs.dbid=s.dbid and  dbs.instance_number=s.instance_number \
			and p.dbid(+)=dbs.dbid and p.con_id(+)=dbs.con_id \
			order by dbs.db_name,dbs.dbid,snap_id",self.db)
			root_ot=""
			for i in range(len(self.dbs_list)):
				if root_ot!=self.dbs_list.iloc[i]['DB_NAME']:
					rootl=[self.dbs_list.iloc[i]['DB_NAME'],'','','','','','']
					root = QtWidgets.QTreeWidgetItem(self.DBList, rootl)
					root_ot=self.dbs_list.iloc[i]['DB_NAME']
					root.setFlags(root.flags() )
				child=QtWidgets.QTreeWidgetItem(root, list(self.dbs_list.iloc[i][['DB_NAME','DB_ID','PDB_NAME','INSTANCE_NUMBER','BEGIN_TIME','SNAP_ID','STARTUP_TIME']]))
				child.setFlags(child.flags() | QtCore.Qt.ItemIsUserCheckable)
				# if self.dbs_list.iloc[i]['DB_NAME'] in self.db_name:
				# 	child.setCheckState(0, QtCore.Qt.Checked)
				# else:
				child.setCheckState(0, QtCore.Qt.Unchecked)
			# for i in range(len(self.dbs_list)):
			# 	root = QtWidgets.QTreeWidgetItem(self.DBList, list(self.dbs_list.iloc[i][['DB_NAME','DB_ID','INSTANCE_NUMBER','STARTUP_TIME','MIN_SNAP','MAX_SNAP']]))
			self.DBList.expandAll()
			for i in range(self.DBList.columnCount()):
				self.DBList.resizeColumnToContents(i)
			self.DBList.collapseAll()


	def retranslateUi(self, ChooseDB):
		_translate = QtCore.QCoreApplication.translate
		ChooseDB.setWindowTitle(_translate("ChooseDB", "Choose Databse and span to Graph"))
		self.DBList.headerItem().setText(0, _translate("ChooseDB", "DB NAME"))
		self.DBList.headerItem().setText(1, _translate("ChooseDB", "Database ID"))
		self.DBList.headerItem().setText(2, _translate("ChooseDB", "PDB Name"))
		self.DBList.headerItem().setText(3, _translate("ChooseDB", "Instance"))
		self.DBList.headerItem().setText(4, _translate("ChooseDB", "Snapshot Begin Interval"))
		self.DBList.headerItem().setText(5, _translate("ChooseDB", "Snapshot Id"))
		self.DBList.headerItem().setText(6, _translate("ChooseDB", "Startup Time"))

