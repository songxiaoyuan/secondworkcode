import cx_Oracle  
import os
import csv
import time
#!/usr/bin/python
# -*- coding:utf8 -*-

def writefile(result,filename):
	print "start to write the file "+filename
	csvfile = file(filename, 'wb')
	writer = csv.writer(csvfile)
 	writer.writerows(result)
	csvfile.close()


def getSortedData(data):
	ret = []
	night = []
	zero = []
	day = []
	nightBegin = 21*3600
	nightEnd = 23*3600+59*60+60
	zeroBegin = 0
	zeroEnd = 9*3600 - 100
	dayBegin = 9*3600
	dayEnd = 15*3600

	for line in data:
		# print line
		timeLine = line[20].split(":")
		# print timeLine
		nowTime = int(timeLine[0])*3600+int(timeLine[1])*60+int(timeLine[2])

		if nowTime >= zeroBegin and nowTime <zeroEnd:
			zero.append(line)
		elif nowTime >= dayBegin and nowTime <= dayEnd:
			day.append(line)
		elif nowTime >=nightBegin and nowTime <=nightEnd:
			night.append(line)
		# if int(line[22]) ==0 or int(line[4]) ==3629:
		# 	continue
	night = sorted(night, key = lambda x: (x[20], int(x[21])))
	zero = sorted(zero, key = lambda x: (x[20], int(x[21])))
	day = sorted(day, key = lambda x: (x[20], int(x[21])))
	for line in night:
		ret.append(line)
	for line in zero:
		ret.append(line)
	for line in day:
		ret.append(line)

	return ret


def getSqlData(myday,instrumentid): 

	# conn = cx_Oracle.connect('hq','hq','114.251.16.210:9921/quota')    
	conn = cx_Oracle.connect('hyqh','hyqh','192.168.1.15:1521/asp')    
	cursor = conn.cursor () 
	for index in xrange(0,1):
		date=myday+index
		print date

		mysql="select *from hyqh.test where TRADINGDAY = '%s' AND INSTRUMENTID = '%s' " % (date,instrumentid)
		# mysql="select *from hyqh.quotatick where TRADINGDAY = '%s' AND INSTRUMENTID = '%s' " % (date,instrumentid)

		print mysql
		cursor.execute (mysql)  

		icresult = cursor.fetchall()
		# get the data and sort it.
		# sortedlist = sorted(icresult, key = lambda x: (x[20], int(x[21])))
		cleandata = getSortedData(icresult)
		filename='../tmp/'+"%s_"%instrumentid
		filename=filename+str(date)+'_test.csv'
		# filename=filename+str(date)+'_quotatick.csv'
		print "we get the instrument id %s" % instrumentid

		writefile(cleandata,filename)

	cursor.close ()  
	conn.close () 

if __name__=='__main__': 
	# data1 = [20170630,20170629,20170628,20170627,20170623,20170622,20170621,20170620,20170619,20170616]
	# data2 =[20170802,20170803,20170804,20170807,20170808,20170809,20170810,20170811,20170814,20170815,20170816]
	# data3 =[20170817,20170818,20170821,20170822,20170823,20170824,20170825,20170828,20170829]
	# data = data2+ data3
	data = [20171109]
	# instrumentid_array = ["ru1801","rb1801","zn1710","pb1710","cu1710","hc1801","i1801","ni1801","al1710","au1712","ag1712","bu1712"]
	instrumentid_array = ["rb1805"]
	for myday in data:
		# pass
		for instrumentid in instrumentid_array:
			getSqlData(myday,instrumentid)