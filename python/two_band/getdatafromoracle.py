import cx_Oracle  
import os
import csv
import time
#!/usr/bin/python
# -*- coding:utf8 -*-


conn = cx_Oracle.connect('hq','hq','114.251.16.210:9921/quota')    
# conn = cx_Oracle.connect('hyqh','hyqh','114.251.16.210:9921/quota')    
cursor = conn.cursor () 


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
		try:
			nowTime = int(timeLine[0])*3600+int(timeLine[1])*60+int(timeLine[2])
		except Exception as e:
			continue
		

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

	for index in xrange(0,1):
		date=myday+index
		print date

		mysql="select *from hyqh.quotatick where TRADINGDAY = '%s' AND INSTRUMENTID = '%s' " % (date,instrumentid)

		print mysql
		cursor.execute (mysql)  

		icresult = cursor.fetchall()
		# get the data and sort it.
		# sortedlist = sorted(icresult, key = lambda x: (x[20], int(x[21])))
		cleandata = getSortedData(icresult)
		# filename='../data/'+"%s_"%instrumentid
		filename='../tmp/'+"%s_"%instrumentid
		filename=filename+str(date)+'.csv'
		print "we get the instrument id %s" % instrumentid

		writefile(cleandata,filename)


if __name__=='__main__': 
	# data1 =[20170801,20170802,20170803,20170804]
	# data2 =[20170807,20170808,20170809,20170810,20170811]
	# data3 =[20170814,20170815,20170816,20170817,20170818]
	# data4 =[20170821,20170822,20170823,20170824,20170825]	
	# data5 =[20170828,20170829,20170830,20170831,20170901]
	# data6 =[20170904,20170905,20170906,20170907,20170908]
	# data7 =[20170911,20170912,20170913,20170914,20170915]	
	# data8 =[20170918,20170919,20170920,20170921,20170922]
	# data9 =[20170925,20170926,20170927,20170928,20170929]
	# data10 =[20171009,20171010,20171011,20171012,20171013]
	# data11 =[20171016,20171017,20171018,20171019,20171020]	
	# data12 =[20171023,20171024,20171025,20171026,20171027]
	# data13 = [20171030,20171031,20171101,20171102,20171103]
	# data14 = [20171106,20171107,20171108,20171109,20171110]
	# data15 = [20171113,20171114,20171115,20171116,20171117]
	# data16 = [20171120,20171121,20171122]

	# # # # # data = data1+data2+data3+data4+data5+data6+data7+data8+data9+data10+data11+data12+data13
	# data = data14+data15+data16
	data = [20171123]
	# instrumentid_array = ["c1801","a1801"]
	# instrumentid_array = ["m1801","cs1801"]
	# instrumentid_array = ["j1801","jm1801","m1801","cs1801","c1801","a1801","i1805","hc1805"]
	instrumentid_array = ["y1801","p1801","v1801","pp1801","jm1801","j1801","a1801","ni1805"]
	# instrumentid_array = ["rb1805","ru1801","zn1801","cu1801","al1801","ni1805","pp1801","v1801","au1806","ag1712","pb1801","bu1712"]
	for myday in data:
		for instrumentid in instrumentid_array:
			getSqlData(myday,instrumentid)


	cursor.close ()  
	conn.close () 