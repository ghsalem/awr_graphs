import subprocess
import os,re

import pandas as pd
import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets
from matplotlib import pyplot as plt

from matplotlib import dates as mdates
from matplotlib.pyplot import cm
import datetime as dt
from matplotlib import rcParams
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from scipy.interpolate import spline

class Sysstatsg:

	def __init__(self,obj, statname):
		self.class_sql_text=""
		self.chosen_class=""
		self.lines=dict()
		self.graph=""
		#rcParams.update({'figure.autolayout': True})
		self.parent=obj
		self.qfigwidget=QtWidgets.QWidget(self.parent.ga_sa_contents)
		self.db_id=obj.db_id
		self.begin_snap=obj.begin_snap
		self.end_snap=obj.end_snap
		self.instance_number=obj.instance_number
		self.begin_interval=obj.begin_interval
		self.end_interval=obj.end_interval
		winWidth = 383
		winHeight = 384
		self.dpi=100
		self.figure=plt.Figure((winWidth/self.dpi, winHeight/self.dpi), dpi=self.dpi, facecolor='w')
		self.canvas=FigureCanvas(self.figure)
		self.canvas.setParent(self.qfigwidget)
		self.navi_toolbar = NavigationToolbar(self.canvas,self.qfigwidget)#self.parent.centralwidget)
		self.navi_toolbar.setFixedHeight(15)
		self.plotLayout = QtWidgets.QVBoxLayout()
		self.plotLayout.addWidget(self.canvas)
		self.plotLayout.addWidget(self.navi_toolbar)
		self.qfigwidget.setLayout(self.plotLayout)
		self.parent.ga_vert_layout.addWidget(self.qfigwidget)
		self.ax=None
		self.old_waits=""
		self.dpi=self.figure.dpi
		self.begin_date=None
		self.all_data=None
		self.sysdate=True
		self.starting_date=(dt.datetime.now()-dt.timedelta(minutes=5)).strftime(' %Y-%m-%dT%H:%M:%S+01:00')
		self.xfmt = mdates.DateFormatter('%H:%M:%S')
		self.canvas.setMinimumSize(self.canvas.size())
		self.metric=statname
		self.metric_rn=self.metric[3:] if self.metric[:3] in ["OS ","ST ","WE ","IS "] else self.metric
		self.metric_rnws=re.sub('[^0-9a-zA-Z]','_',self.metric_rn)
		with_text="with snaps as (select to_char(begin_interval_time,'yyyy-mm-dd HH24:MI:ss') timestamp ,snap_id \
		from "+self.parent.awr_location+"_snapshot \
		where dbid="+self.db_id+" and instance_number="+self.instance_number+" and snap_id between "+self.begin_snap+" and "+self.end_snap+") "
		if self.metric[:3]=="OS ":
			self.sql_text=with_text+"select timestamp, delta as "+self.metric_rnws+" from (select  value, timestamp, s.snap_id, value-nvl(lag(value,1) over (order by s.snap_id),value) DELTA \
			from "+self.parent.awr_location+"_osstat s, snaps where s.dbid="+self.db_id+" and s.snap_id between "+self.begin_snap+" and "+self.end_snap+" and s.stat_name='"+self.metric[3:]+"' and instance_number="+self.instance_number+" and snaps.snap_id=s.snap_id \
			order by snap_id)"			
		elif self.metric[:3]=="ST ":
				self.sql_text=with_text+"select timestamp, delta as "+self.metric_rnws+" from (select  value, timestamp, s.snap_id, value-nvl(lag(value,1) over (order by s.snap_id),value) DELTA \
				from "+self.parent.awr_location+"_sys_time_model s, snaps where s.dbid="+self.db_id+" and s.snap_id between "+self.begin_snap+" and "+self.end_snap+" and s.stat_name='"+self.metric[3:]+"' and instance_number="+self.instance_number+" and snaps.snap_id=s.snap_id \
				order by snap_id)"
		elif self.metric[:3]=="IS ":
				self.sql_text=with_text+"select timestamp, delta as "+self.metric_rnws+" from (select  value, timestamp, s.snap_id, value-nvl(lag(value,1) over (order by s.snap_id),value) DELTA \
				from "+self.parent.awr_location+"_sys_time_model s, snaps where s.dbid="+self.db_id+" and s.snap_id between "+self.begin_snap+" and "+self.end_snap+" and s.stat_name='"+self.metric[3:]+"' and instance_number="+self.instance_number+" and snaps.snap_id=s.snap_id \
				order by snap_id)"
				self.sql_text=with_text+", stats as (select  snap_id, \
				nvl(SMALL_READ_MEGABYTES-lag(SMALL_READ_MEGABYTES,1) over (order by snap_id),0) as SMALL_READ_MEGABYTES, \
				nvl(SMALL_WRITE_MEGABYTES-lag(SMALL_WRITE_MEGABYTES,1) over (order by snap_id),0) as SMALL_WRITE_MEGABYTES, \
				nvl(LARGE_READ_MEGABYTES-lag(LARGE_READ_MEGABYTES,1) over (order by snap_id),0) as LARGE_READ_MEGABYTES, \
				nvl(LARGE_WRITE_MEGABYTES-lag(LARGE_WRITE_MEGABYTES,1) over (order by snap_id),0) as LARGE_WRITE_MEGABYTES, \
				nvl(NUMBER_OF_WAITS-lag(NUMBER_OF_WAITS,1) over (order by snap_id),0) as NUMBER_OF_WAITS, \
				nvl(WAIT_TIME-lag(WAIT_TIME,1) over (order by snap_id),0) as WAIT_TIME \
				from "+self.parent.awr_location+"_iostat_function s where s.dbid="+self.db_id+" and s.snap_id between "+self.begin_snap+" and "+self.end_snap+" and s.function_name='"+self.metric[3:]+"' \
				and instance_number="+self.instance_number+") \
				select timestamp, SMALL_READ_MEGABYTES, SMALL_WRITE_MEGABYTES, LARGE_READ_MEGABYTES, LARGE_WRITE_MEGABYTES, \
				NUMBER_OF_WAITS, WAIT_TIME \
				from (select s.snap_id,timestamp, SMALL_READ_MEGABYTES, SMALL_WRITE_MEGABYTES, LARGE_READ_MEGABYTES, LARGE_WRITE_MEGABYTES, \
				NUMBER_OF_WAITS, WAIT_TIME \
				from snaps s, stats t \
				where s.snap_id=t.snap_id order by s.snap_id)"

		elif self.metric[:3]=="WE ":
				self.sql_text="select timestamp, delta as "+self.metric_rnws+" from (select sample_time, to_char(sample_time,'yyyy-mm-dd hh24:mi:ss') timestamp, delta from ( \
				select  trunc(sample_time,'mi') sample_time,  count(0)  DELTA \
				from "+self.parent.awr_location+"_active_sess_history s where s.dbid="+self.db_id+" and s.snap_id between "+self.begin_snap+" and "+self.end_snap+" and s.event='"+self.metric[3:]+"' and instance_number="+self.instance_number+" \
				group by trunc(sample_time,'mi')) order by sample_time)"
		else:
				self.sql_text=with_text+"select timestamp, delta as "+self.metric_rnws+" from (select  value, timestamp, s.snap_id, value-nvl(lag(value,1) over (order by s.snap_id),value) DELTA \
				from "+self.parent.awr_location+"_sysstat s, snaps where s.dbid="+self.db_id+" and s.snap_id between "+self.begin_snap+" and "+self.end_snap+" and s.stat_name='"+self.metric+"' and instance_number="+self.instance_number+" and snaps.snap_id=s.snap_id \
				order by snap_id)"
		#print(self.sql_text)
		self.redraw_events()

	def remove_graph(self):
		self.parent.ga_vert_layout.removeWidget(self.qfigwidget)

	def redraw_events(self):
		#print("metric ",self.metric)
		if self.metric!="":
				self.all_data=pd.read_sql_query(self.sql_text, self.parent.db)
#                print(current_metrics)
				if len(self.all_data)>0:
					if self.ax is None:
						self.ax=self.figure.add_axes([.06,.09,.75,.85])
						self.ax.set_facecolor('w')
					xticklabels=[dt.datetime.strptime(ts,"%Y-%m-%d %H:%M:%S") for ts in self.all_data.TIMESTAMP.unique()]
	#					print(self.all_data)
					xtickmin=xticklabels[0]
					xtickmax=xticklabels[len(xticklabels)-1]
					xticks=np.arange(len(xticklabels))
					self.ax.cla()
					nbr_lines=0
					color=iter(cm.rainbow(np.linspace(0,1,1)))
					returned_data=list(self.all_data.columns.values)
					color=iter(cm.rainbow(np.linspace(0,1,len(returned_data))))
					for colnbr in range(1,len(returned_data)):
						total_waits=self.all_data[returned_data[colnbr]]
						if max(total_waits)>0:
							color_n=next(color)
							#print(xticklabels)
							nbr_lines+=1
							self.ax.plot(xticklabels,total_waits, color=color_n,label=returned_data[colnbr])
			
					if nbr_lines>0:
						self.ax.xaxis.set_major_formatter(self.xfmt)
						for tick in self.ax.xaxis.get_major_ticks():
							tick.label.set_fontsize(8)
							tick.label.set_rotation(40)
						for tick in self.ax.yaxis.get_major_ticks():
							tick.label.set_fontsize(8)
						self.ax.legend(loc='center left', bbox_to_anchor=(1.,.5),
						fontsize=8, ncol=1,fancybox=True, shadow=True)#, borderpad=1.5)
						if self.metric[:3]=="WE ":
							self.ax.set_title(self.metric_rn+" (CNT/min, ASH) snaps between "+self.begin_interval+' and '+self.end_interval, fontsize=8)
						else:
							self.ax.set_title(self.metric_rn+'(delta)\n snaps between '+self.begin_interval+' and '+self.end_interval, fontsize=8)
						#plt.tight_layout(pad=.04, h_pad=1.0)
						plt.gcf().subplots_adjust(bottom=.20, left=.2)
						self.canvas.draw()
				else:
					print("No data for metric=",self.metric, " sql= ",self.sql_text)