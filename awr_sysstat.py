# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'c:\Users\gs3f628n\Downloads\graph_qt\cellmh.ui'
#
# Created: Tue Feb 28 11:33:50 2017
#      by: PyQt4 UI code generator 4.11.3
#
# WARNING! All changes made in this file will be lost!
import subprocess, re
import datetime as dt
import os,sys, time
import pandas as pd
import cx_Oracle
import argparse
from matplotlib.pyplot import cm
import numpy as np
from PyQt5 import QtCore, QtGui , QtWidgets
from qt_connect import Ui_qt_connect
from sysstat import Sysstatsg
from ChooseStats import Ui_ChooseStats
from ChooseDB import Ui_ChooseDB
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib import dates as mdates
from matplotlib import pyplot as plt
from matplotlib import rcParams

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

class Ui_CellMH(object):
	def setupUi(self, CellMH, db,connect_string):
		CellMH.setObjectName(_fromUtf8("CellMH"))
		CellMH.resize(800, 600)
		self.db=db
		self.is_pdb=False
		self.connect_string=connect_string
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(CellMH.sizePolicy().hasHeightForWidth())
		CellMH.setSizePolicy(sizePolicy)
		self.centralwidget = QtWidgets.QWidget(CellMH)
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
		self.centralwidget.setSizePolicy(sizePolicy)
		self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
		self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
		self.verticalLayout.setSpacing(7)
		self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
		self.GraphScrollArea = QtWidgets.QScrollArea(self.centralwidget)#self.GraphArea)
		self.GraphScrollArea.setWidgetResizable(True)
		self.GraphScrollArea.setObjectName(_fromUtf8("GraphScrollArea"))
		self.verticalLayout.addWidget(self.GraphScrollArea)
		self.ga_sa_contents = QtWidgets.QWidget()
		self.ga_sa_contents.setGeometry(QtCore.QRect(0, 0, 728, 476))
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.ga_sa_contents.sizePolicy().hasHeightForWidth())
		self.ga_sa_contents.setSizePolicy(sizePolicy)
		self.ga_sa_contents.setObjectName("ga_sa_contents")

		self.ga_vert_layout = QtWidgets.QVBoxLayout(self.ga_sa_contents)
		self.ga_vert_layout.setContentsMargins(0, 0, 0, 0)
		self.ga_vert_layout.setObjectName("ga_vert_layout")
		self.GraphScrollArea.setWidget(self.ga_sa_contents)

		self.chosen_os_stats=None
		self.chosen_DB=None
		CellMH.setCentralWidget(self.centralwidget)
		self.menubar = QtWidgets.QMenuBar(CellMH)
		self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
		self.menubar.setObjectName(_fromUtf8("menubar"))
		self.menuFile = QtWidgets.QMenu(self.menubar)
		self.menuFile.setObjectName(_fromUtf8("menuFile"))
		CellMH.setMenuBar(self.menubar)
		self.statusbar = QtWidgets.QStatusBar(CellMH)
		self.statusbar.setObjectName(_fromUtf8("statusbar"))
		CellMH.setStatusBar(self.statusbar)
		self.actionConfigure = QtWidgets.QAction(CellMH)
		self.actionConfigure.setObjectName(_fromUtf8("actionConfigure"))
		self.ChooseStats = QtWidgets.QAction(CellMH)
		self.ChooseStats.setObjectName(_fromUtf8("ChooseStats"))
		self.ChooseDB = QtWidgets.QAction(CellMH)
		self.ChooseDB.setObjectName(_fromUtf8("ChooseDB"))
		self.Save_to_PDF = QtWidgets.QAction(CellMH)
		self.Save_to_PDF.setObjectName(_fromUtf8("Save_to_PDF"))
		self.actionExit = QtWidgets.QAction(CellMH)
		self.actionExit.setObjectName(_fromUtf8("actionExit"))
		self.menuFile.addAction(self.actionConfigure)
		self.menuFile.addAction(self.ChooseStats)
		self.menuFile.addAction(self.ChooseDB)
		self.menuFile.addAction(self.Save_to_PDF)
		self.menuFile.addAction(self.actionExit)
		self.menubar.addAction(self.menuFile.menuAction())
		self.metric_name=[]
		self.metric_descriptions=[]
		self.preferences=None
		self.metric_name=[]
		self.chosen_stats=None
		self.metric_graph=dict()
		self.timer = QtCore.QTimer(self.centralwidget)
		self.refresh_rate=15
		self.db_id=None
#		self.timer.start(self.refresh_rate*1000)
		if self.db is None:
			self.get_prefs()
			self.get_selected_DB()
			if self.db_id!=None:
				self.get_selected_stat()
		self.retranslateUi(CellMH)
		self.ChooseStats.triggered.connect(self.get_selected_stat)
		self.ChooseDB.triggered.connect(self.get_selected_DB)
		self.actionExit.triggered.connect(self.close_application)
		self.actionConfigure.triggered.connect(self.get_prefs)
		self.Save_to_PDF.triggered.connect(self.save_all_figs)
#		self.timer.timeout.connect(self.redraw_graphs)
		QtCore.QMetaObject.connectSlotsByName(CellMH)

	def save_all_figs(self):
		save_file_name, _ =QtWidgets.QFileDialog.getSaveFileName(self.centralwidget, 'Save plots to PDF file','','*.pdf')
		if save_file_name:
			with PdfPages(save_file_name) as pdf:
				for n in self.metric_graph:
					pdf.savefig(self.metric_graph[n].figure)

	def check_pdb(self):
		self.non_cdb=True
		self.in_pdb=False
		self.awr_location="dba_hist"
		type_of_db=self.db.cursor()
		type_of_db.execute("select nvl(sys_context('userenv','cdb_name'),'NON-CDB') cdb_name, \
		sys_context('userenv','con_name') con_name from dual")
		for i in type_of_db:
			if i[0]=="NON-CDB":
				self.non_cdb=True
				self.awr_location="dba_hist"
			else:
				self.non_cdb=False
			if i[1]=="CDB$ROOT":
				self.in_pdb=False
				self.awr_location='CDB_HIST'
			else:
				self.in_pdb=True
				self.awr_location="awr_pdb"
		type_of_db.close()
	def redraw_graphs(self):
		for i in self.metric_graph:
			self.metric_graph[i].redraw_events()
	def get_selected_stat(self):
		get_stats_sel = QtWidgets.QDialog()
		if self.chosen_stats==None:
			self.chosen_stats=Ui_ChooseStats()
		self.chosen_stats.setupUi(get_stats_sel,self.db)
		get_stats_sel.exec_()
		get_stats_sel.show()
		get_stats_sel.close()
		what_is_selected=self.chosen_stats.metric_name
		current_items=[]
		for i in  what_is_selected:
			current_items.append(i)
			if i not in self.metric_name:
				print("added ",i)
				self.metric_name.append(i)
				self.first_time=True
				self.metric_graph[i]=Sysstatsg(self,i)
		metric_names=self.metric_name.copy()
		for i in self.metric_name:
			if i not in current_items:
				print("removing in main ", i)
				self.metric_graph[i].remove_graph()
				self.metric_graph.pop(i)
				metric_names.pop(metric_names.index(i))
		self.metric_name=metric_names.copy()


	def get_selected_DB(self):
		get_db_sel = QtWidgets.QDialog()
		if self.chosen_DB==None:
			self.chosen_DB=Ui_ChooseDB()
		self.chosen_DB.setupUi(get_db_sel,self)
		get_db_sel.exec_()
		get_db_sel.show()
		get_db_sel.close()
		if self.chosen_DB.db_id!=None:
			self.db_id=self.chosen_DB.db_id
			self.begin_snap=self.chosen_DB.begin_snap
			self.end_snap=self.chosen_DB.end_snap
			self.instance_number=self.chosen_DB.instance_number
			self.begin_interval=self.chosen_DB.begin_interval
			self.end_interval=self.chosen_DB.end_interval

	def get_prefs(self):
		qt_connect = QtWidgets.QDialog()
		if self.preferences==None:
			self.preferences=Ui_qt_connect()
		self.preferences.setupUi(qt_connect)
		qt_connect.exec_()
		qt_connect.show()
		qt_connect.close()
		if self.preferences.db!=self.db and self.preferences.db!=None:
			self.db=self.preferences.db
			self.check_pdb()
			print("removing all graphs")
			for i in self.metric_name:
					self.metric_graph[i].remove_graph()
					self.metric_graph.pop(i)
			self.metric_name=[]
		else:
			exit()
		#self.timer.setInterval(float(self.preferences.refresh_rate)*1000)

	def close_application(self):
		choice = QtWidgets.QMessageBox.question(self.centralwidget, 'Confirm Exit',
													"Exit the tool?",
													QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
		if choice == QtWidgets.QMessageBox.Yes:
					print("Exiting")
					sys.exit()
		else:
					pass
	def retranslateUi(self, CellMH):
		CellMH.setWindowTitle(_translate("CellMH", "Graphing AWR sysstat", None))
		self.menuFile.setTitle(_translate("CellMH", "File", None))
		self.actionConfigure.setText(_translate("CellMH", "Configure ...", None))
		self.ChooseStats.setText(_translate("CellMH", "Pick Stats to graph ...", None))
		self.ChooseDB.setText(_translate("CellMH", "Pick DB and snap span ...", None))
		self.Save_to_PDF.setText(_translate("CellMH", "Save Plots to PDF ...", None))
		self.actionExit.setText(_translate("CellMH", "Exit", None))

def	get_args():
	parser = argparse.ArgumentParser(description='AWR statistics analyzer.')
	parser.add_argument('-u','--user_id', metavar='Connection String',  nargs='?',required=True,
											help='Full connection string to the db')
	parser.add_argument('-s','--statname', metavar='Statistic name',  nargs='+',
											help='Statistic Name as in v\$statname')
	parser.add_argument('-f','--filename', metavar='File name',  nargs='?',
											help='File name prefix, including directory, default=local dir')
	parser.add_argument('-t','--time_model', metavar='Time model stats',  nargs='+', default=["DB time", "DB CPU"],
											help='List of stat from sys_time_model to plot')
	parser.add_argument('-d','--db_id', metavar='Database Id',  nargs='?',
											help='Database Id')
	parser.add_argument('-b','--begin_date', metavar='Begin Timestamp',  nargs='?',
											help='Begin Time stamp (dd/mm/yyyy hh24:mi:ss)')
	parser.add_argument('-e','--end_date', metavar='End Timestamp',  nargs='?',
											help='End Time stamp (dd/mm/yyyy hh24:mi:ss)')
	parser.add_argument('-i','--instance', metavar='Instance Number',  nargs='?',default="1",
											help='Instance number (default=1)')
	parser.add_argument('-l','--list_stats', metavar='List Stats',  nargs='?',const="Y",
											help='Ths flag will list all the stats that you can choose from. It requires -u')
	args=parser.parse_args()
#	print(args)
	user_id=args.user_id
#	print(user_id)
	try:
		db=cx_Oracle.connect(user_id)
		if args.list_stats=="Y":
			get_st=db.cursor()
			get_st.execute("select 'SysStats ',name from v$sysstat where class<128\
						union all \
						select 'OS Stats ','OS '||stat_name \
						from v$osstat \
						union all \
						select 'System Time Model','ST '||stat_name \
						from v$sys_time_model \
						union all \
						select 'IOStat Function', 'IO '||function_name \
						from v$IOstat_function \
						order by 1,2")
			print("List of stats you can specify on the command line:")
			for stn in get_st:
				print (stn[0],": ",stn[1])
			get_st.close()
		return db,args
	except	cx_Oracle.DatabaseError as	exc:
		error,	=	exc.args
		print('cannot connect to the specified db, please specify a correct one using the preferences menu entry ', user_id)
		return None,None
def print_graph(db,args):
	# printing the graph directly and exiting
	# first let's get the ranges of snap_ids for the db_id and requested time interval
	awr_location="awr_pdb"
	dbname=""
	expand_stats={"OS ":"select stat_name from v$osstat where upper(stat_name) like upper(:stn)",
				"IO ":"select function_name from v$iostat_function where upper(function_name) like upper(:stn)",
				"ST ":"select stat_name from v$sys_time_model where upper(stat_name) like upper(:stn)"}
	if args.db_id==None:
		cursor=db.cursor();
		awr_location='dba_hist'
		cursor.execute("select dbid, to_char(systimestamp,'dd/mm/YYYY hh24:mi:ss') cts, to_char(systimestamp-1,'dd/mm/YYYY hh24:mi:ss') min_24,name from v$database")
		for row in cursor:
			db_id=str(row[0])
			ets=row[1]
			bts=row[2]
			dbname=row[3]
		cursor.close()
	else:
		db_id=args.db_id
		if args.begin_date!=None:
			bts=args.begin_date
			ets=args.end_date
		else:
			bts="01/01/2000 00:00:00"
			ets=dt.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
	get_stats=db.cursor()
	metrics=[]
#	get_stats.prepare('select name from v$statname where upper(name) like upper(:stn)')
	for met in args.statname:
		if len(met)==len(met.replace('%','')):
			metrics.append(met)
		else:
			metf3=met[:3]
			if metf3 in expand_stats:
				get_stats.prepare(expand_stats[metf3])
				mettab=met[3:]
			else:
				mettab=met
				get_stats.prepare('select name from v$statname where upper(name) like upper(:stn)')
			get_stats.execute(None,stn=mettab)
			for name in get_stats:
				metrics.append(name[0])
	tmodel_st=[]
	print(metrics)
	get_stats.prepare('select stat_name from v$sys_time_model where upper(stat_name) like upper(:stn)')
	for met in args.time_model:
		if len(met)==len(met.replace('%','')):
			tmodel_st.append(met)
		else:
			get_stats.execute(None,stn=met)
			for name in get_stats:
				tmodel_st.append(name[0])
	if dbname=="":
		get_stats.prepare('select db_name from '+awr_location+'_database_instance where dbid='+db_id+' and rownum=1')
		get_stats.execute(None)
		for rs in get_stats:
			dbname=rs[0]
	get_stats.close()
	if args.filename!=None:
		file_name_prefix=args.filename
		if os.path.isdir(file_name_prefix) and file_name_prefix[-1]!='/':
			file_name_prefix+="/"
	else:
		file_name_prefix=""
	sqlstmt="select startup_time,  to_char(min(snap_id)) min_snap, to_char(max(snap_id)) max_snap \
			from "+awr_location+"_snapshot s \
			where s.dbid="+db_id+" and begin_interval_time between to_date('"+bts+"','dd/mm/yyyy hh24:mi:ss') \
			and to_date('"+ets+"','dd/mm/yyyy hh24:mi:ss') and instance_number="+args.instance+" \
			group by s.startup_time \
			order by s.startup_time"
	snap_id_df=pd.read_sql_query(sqlstmt,db)
	min_snaps=list(snap_id_df.MIN_SNAP.unique())
	max_snaps=list(snap_id_df.MAX_SNAP.unique())

	#metric=args.statname
	instance_number=args.instance
	xfmt = mdates.DateFormatter('%H:%M:%S')
	#print(awr_location)
	rcParams.update({'figure.autolayout': True})
	for i in range(len(min_snaps)):
		begin_snap=min_snaps[i]
		end_snap=max_snaps[i]
		tmlist="'"+"','".join(tmodel_st)+"'"
		sqlstmt="with st as (select round(value) value, stat_name,snap_id \
			from "+awr_location+"_sys_time_model \
			where dbid="+db_id+" \
			and snap_id between "+begin_snap+" and "+ end_snap+" \
			and instance_number="+instance_number+" \
			and stat_name in ("+tmlist+")) \
			select stat_name, st.snap_id,value - lag(value,1) over (partition by stat_name order by st.snap_id) value, to_char(st_time,'dd/mm/yyyy hh24:mi:ss') st_time \
			from st,(select snap_id, begin_interval_time st_time \
			from "+awr_location+"_SNAPSHOT \
			where dbid="+db_id+" and snap_id between "+begin_snap+" and "+ end_snap+" \
			) secs \
			where st.snap_id=secs.snap_id \
			order by st.snap_id"
		all_data=pd.read_sql_query(sqlstmt,db)
		#print(metric," max delta ", max(all_data.DELTA))
		if len(all_data)>0:
			xticklabels=[dt.datetime.strptime(ts,"%d/%m/%Y %H:%M:%S") for ts in all_data.ST_TIME.unique()]
			min_ts=xticklabels[0]
			max_ts=xticklabels[-1]
			for met in all_data.STAT_NAME.unique():
					total_waits=all_data[all_data['STAT_NAME']==met]['VALUE']
					if total_waits.max()>0:
						plt.plot(xticklabels,total_waits,label=met)
#			total_waits=all_data[all_data['STAT_NAME']=='DB CPU']['VALUE']
#			plt.plot(xticklabels,total_waits,label="DB CPU")
			mplot=plt.gca()
			metricd="Time Model Stats"
			mplot.xaxis.set_major_formatter(xfmt)
			for tick in mplot.xaxis.get_major_ticks():
				tick.label.set_fontsize(8)
				tick.label.set_rotation(40)
			for tick in mplot.yaxis.get_major_ticks():
				tick.label.set_fontsize(8)
			mplot.legend(loc='center left', bbox_to_anchor=(1.,.5),
			fontsize=8, ncol=1,fancybox=True, shadow=True)
			mplot.set_title(metricd+'(delta) \n from '+min_ts.strftime('%Y-%m-%d %H:%M')+' to '+max_ts.strftime('%Y-%m-%d %H:%M'), fontsize=8)
	#		plt.gcf().subplots_adjust(bottom=.20, left=.2)
			fname=file_name_prefix+re.sub('[^0-9a-zA-Z]','_',metricd)+'_'+begin_snap+'_'+end_snap+'_'+dbname+'_'+instance_number+'.pdf'
			plt.savefig(fname)
			mplot.cla()
		for metric in metrics:
				metric_rn=metric[3:] if metric[:3] in ["OS ","ST ","WE "] else metric
				metric_rnws=re.sub('[^0-9a-zA-Z]','_',metric_rn)
				with_text="with snaps as (select to_char(begin_interval_time,'yyyy-mm-dd HH24:MI:ss') timestamp ,snap_id \
				from "+awr_location+"_snapshot \
				where dbid="+db_id+" and instance_number="+instance_number+" and snap_id between "+begin_snap+" and "+end_snap+") "
				if metric[:3]=="OS ":
					sql_text=with_text+"select timestamp,delta as "+metric_rnws+" from (select  value, timestamp, s.snap_id, value-nvl(lag(value,1) over (order by s.snap_id),value) DELTA \
					from "+awr_location+"_osstat s, snaps where s.dbid="+db_id+" and s.snap_id between "+begin_snap+" and "+end_snap+" and s.stat_name='"+metric[3:]+"' and instance_number="+instance_number+" and snaps.snap_id=s.snap_id \
					order by snap_id)"
				elif metric[:3]=="ST ":
						sql_text=with_text+"select timestamp, delta as "+metric_rnws+" from (select  value, timestamp, s.snap_id, value-nvl(lag(value,1) over (order by s.snap_id),value) DELTA \
						from "+awr_location+"_sys_time_model s, snaps where s.dbid="+db_id+" and s.snap_id between "+begin_snap+" and "+end_snap+" and s.stat_name='"+metric[3:]+"' and instance_number="+instance_number+" and snaps.snap_id=s.snap_id \
						order by snap_id)"
				elif metric[:3]=="IS ":
						sql_text=with_text+"select timestamp, delta as "+metric_rnws+" from (select  value, timestamp, s.snap_id, value-nvl(lag(value,1) over (order by s.snap_id),value) DELTA \
						from "+awr_location+"_sys_time_model s, snaps where s.dbid="+db_id+" and s.snap_id between "+begin_snap+" and "+end_snap+" and s.stat_name='"+metric[3:]+"' and instance_number="+instance_number+" and snaps.snap_id=s.snap_id \
						order by snap_id)"
						sql_text=with_text+", stats as (select  snap_id, \
						nvl(SMALL_READ_MEGABYTES-lag(SMALL_READ_MEGABYTES,1) over (order by snap_id),0) as SMALL_READ_MEGABYTES, \
						nvl(SMALL_WRITE_MEGABYTES-lag(SMALL_WRITE_MEGABYTES,1) over (order by snap_id),0) as SMALL_WRITE_MEGABYTES, \
						nvl(LARGE_READ_MEGABYTES-lag(LARGE_READ_MEGABYTES,1) over (order by snap_id),0) as LARGE_READ_MEGABYTES, \
						nvl(LARGE_WRITE_MEGABYTES-lag(LARGE_WRITE_MEGABYTES,1) over (order by snap_id),0) as LARGE_WRITE_MEGABYTES, \
						nvl(NUMBER_OF_WAITS-lag(NUMBER_OF_WAITS,1) over (order by snap_id),0) as NUMBER_OF_WAITS, \
						nvl(WAIT_TIME-lag(WAIT_TIME,1) over (order by snap_id),0) as WAIT_TIME \
						from "+awr_location+"_iostat_function s where s.dbid="+db_id+" and s.snap_id between "+begin_snap+" and "+end_snap+" and s.function_name='"+metric[3:]+"' \
						and instance_number="+instance_number+") \
						select timestamp, SMALL_READ_MEGABYTES, SMALL_WRITE_MEGABYTES, LARGE_READ_MEGABYTES, LARGE_WRITE_MEGABYTES, \
						NUMBER_OF_WAITS, WAIT_TIME \
						from (select s.snap_id,timestamp, SMALL_READ_MEGABYTES, SMALL_WRITE_MEGABYTES, LARGE_READ_MEGABYTES, LARGE_WRITE_MEGABYTES, \
						NUMBER_OF_WAITS, WAIT_TIME \
						from snaps s, stats t \
						where s.snap_id=t.snap_id order by s.snap_id)"
				else:
					sql_text=with_text+"select timestamp, delta as "+metric_rnws+" from (select  value, timestamp, s.snap_id, value-nvl(lag(value,1) over (order by s.snap_id),value) DELTA \
					from "+awr_location+"_sysstat s, snaps where s.dbid="+db_id+" and s.snap_id between "+begin_snap+" and "+end_snap+" and s.stat_name='"+metric+"' and instance_number="+instance_number+" and snaps.snap_id=s.snap_id \
					order by snap_id)"
				all_data=pd.read_sql_query(sql_text,db)
				#print(sql_text)
				if len(all_data)>0:
					xticklabels=[dt.datetime.strptime(ts,"%Y-%m-%d %H:%M:%S") for ts in all_data.TIMESTAMP.unique()]
					min_ts=xticklabels[0]
					max_ts=xticklabels[-1]
					returned_data=list(all_data.columns.values)
					color=iter(cm.rainbow(np.linspace(0,1,len(returned_data))))
					for colnbr in range(1,len(returned_data)):
						total_waits=all_data[returned_data[colnbr]]
						if max(total_waits)>0:
							color_n=next(color)
							plt.plot(xticklabels,total_waits, color=color_n,label=returned_data[colnbr])
					mplot=plt.gca()

					mplot.xaxis.set_major_formatter(xfmt)
					for tick in mplot.xaxis.get_major_ticks():
						tick.label.set_fontsize(8)
						tick.label.set_rotation(40)
					for tick in mplot.yaxis.get_major_ticks():
						tick.label.set_fontsize(8)
					mplot.legend(loc='center left', bbox_to_anchor=(1.,.5),
					fontsize=8, ncol=1,fancybox=True, shadow=True)
					mplot.set_title(metric+'(delta) \nfrom '+min_ts.strftime('%Y-%m-%d %H:%M:%S')+' to '+max_ts.strftime('%Y-%m-%d %H:%M:%S'), fontsize=8)
			#		plt.gcf().subplots_adjust(bottom=.20, left=.2)
					fname=file_name_prefix+re.sub('[^0-9a-zA-Z]','_',metric)+'_'+begin_snap+'_'+end_snap+'_'+dbname+'_'+instance_number+'.pdf'
					plt.savefig(fname)
					mplot.cla()
				#print ("query is "+sql_text)
	exit()

if __name__ == "__main__":
	app = QtWidgets.QApplication(sys.argv)
	GraphingDynViews = QtWidgets.QMainWindow()
	if len(sys.argv)>1:
		db,args=get_args()
		if args!=None:
			connect_string=args.user_id
			if args.statname!=None:
				print_graph(db,args)
			if args.list_stats=='Y':
				db.close()
				exit()
		else:
			db=None
			connect_string=None
	else:
		db=None
		connect_string=None
	ui = Ui_CellMH()
	ui.setupUi(GraphingDynViews, db, connect_string)
	GraphingDynViews.show()
	sys.exit(app.exec_())
