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


def cleanMdData(data):
	ret = []
	amBegin = 9*3600
	amEnd = 11*3600+30*60
	pmBegin = 13*3600+30*60
	pmEnd = 15*3600
	amRestBegin = 10*3600+15*60
	amRestEnd = 10*3600+30*60

	for line in data:
		# print line
		timeLine = line[20].split(":")
		# print timeLine
		# tick = line[21]
		nowTime = int(timeLine[0])*3600+int(timeLine[1])*60+int(timeLine[2])
		# print nowTime
		# print time
		# import pdb
		# pdb.set_trace()
		if nowTime<amBegin:
			continue
		if nowTime>pmEnd:
			break
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
		sortedlist = sorted(icresult, key = lambda x: (x[20], int(x[21])))
		# remove the 00:00 and 21:00 data,we dont need it
		cleandata = cleanMdData(sortedlist)
		filename='../data/'+"%s_"%instrumentid
		filename=filename+str(date)+'.csv'
		print "we get the instrument id %s" % instrumentid

		writefile(cleandata,filename)

	cursor.close ()  
	conn.close () 

if __name__=='__main__': 
	listtime=[20170620]
	instrumentid = "rb1710"
	for myday in listtime:
		# pass
		getSqlData(myday,instrumentid)