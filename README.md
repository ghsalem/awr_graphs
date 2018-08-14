# awr_stats
python code to display awr graphs (sysstat, time_model, os_stats and some ASH)
The code is for python 3, won't work with version 2.
It requires the following modules:

PyQt5

Matplotlib

cx_Oracle

pandas

scipy

numpy

The other modules used are usually installed by default.

**Intallation:**

Just copy the files to any directory, insure that you have the modules listed above, and that's it
As cx_Oracle requires Oracle client, be sure to have one installed. I have tested mainly with 12.2 client, but it should work 
with older ones

**Usage:**

You can use the tool either in interactive mode (i.e. have the graphs displayed on the screen), or in 'batch' mode, 
where it will produce pdf files containing the graphs.
To start it in interactive mode, just:

python awr_sysstat.py (or python3 ..., depending on your installation)

The parameters are:

-u [Connection String], --user_id [Connection String]
                        Full connection string to the db

-s Statistic name [Statistic name ...], --statname Statistic name [Statistic name ...]
                        Statistic Name as in v$statname


-f [File name], --filename [File name]
                        File name prefix, including directory, default=local directory

-t Time model stats [Time model stats ...], --time_model Time model stats [Time model stats ...]
                        List of stat from sys_time_model to plot

-d [Database Id], --db_id [Database Id]
                        Database Id, defaults to the DB you are connecting to

-b [Begin Timestamp], --begin_date [Begin Timestamp]
                        Begin Time stamp (dd/mm/yyyy hh24:mi:ss) for the period you want to plot

-e [End Timestamp], --end_date [End Timestamp]
                        End Time stamp (dd/mm/yyyy hh24:mi:ss)

-i [Instance Number], --instance [Instance Number]
                        Instance number (default=1)

The db_id parameter can be used to plot graphs for other databases than the one you are connecting to, this is
very much usefull if you imported AWR data from another database.


 
