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

	conn = cx_Oracle.connect('hq','hq','114.251.16.210:9921/quota')    
	cursor = conn.cursor () 
	for index in xrange(0,1):
		date=myday+index
		print date

		mysql="select *from hyqh.quotatick where TRADINGDAY = '%s' AND instr(INSTRUMENTID,'%s')>0" % (date,instrumentid)

		print mysql
		cursor.execute (mysql)  

		icresult = cursor.fetchall()
		# get the data and sort it.
		# sortedlist = sorted(icresult, key = lambda x: (x[20], int(x[21])))
		cleandata = getSortedData(icresult)
		filename='../data/'+"%s_"%instrumentid
		filename=filename+str(date)+'.csv'
		print "we get the instrument id %s" % instrumentid

		writefile(cleandata,filename)

	cursor.close ()  
	conn.close () 

if __name__=='__main__': 
	# data1 = [20170630,20170629,20170628,20170627,20170623,20170622,20170621,20170620,20170619,20170616]
	# data2 =[20170711,20170712,20170713,20170714,20170717]
	# data3 =[20170718,20170719,20170720,20170721,20170724,20170725,20170726]
	# data = data2+ data3
	data = [20170728]
	instrumentid_array = ["ru1709","rb1710","zn1709","pb1709"]
	# instrumentid_array = ["ru1801"]
	for myday in data:
		# pass
		for instrumentid in instrumentid_array:
			getSqlData(myday,instrumentid)