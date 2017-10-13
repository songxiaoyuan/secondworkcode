# -*- coding:utf8 -*-
import csv
import basic_fun as bf
import os
import cx_Oracle  

LASTPRICE = 4
VOLUME = 11
OPENINTEREST = 13
TURNONER = 12
BIDPRICE1 = 22
BIDPRICE1VOLUME = 23
ASKPRICE1 =24
ASKPRICE1VOLUME =25
TIME = 20
LONG =1
SHORT =0

# 这个是铅的
param_dict_pb = {"band_period":7200}
# 这个是螺纹钢的
param_dict_rb = {"band_period":7200}

# 这个是橡胶的
param_dic_ru = {"band_period":7200}

# 这个是锌的
param_dic_zn = {"band_period":7200}

param_dict_i = {"band_period":7200}

param_dic_ni = {"band_period":7200}

param_dic_al = {"band_period":7200}

param_dict_hc = {"band_period":7200}

param_dict_cu = {"band_period":7200}


param_dic_au = {"band_period":7200}

param_dic_ag = {"band_period":7200}

param_dic_bu = {"band_period":7200}

param_dic_sn = {"band_period":7200}

nameDict = {
	"rb1801":{"param":param_dict_rb},
	"ru1801":{"param":param_dic_ru},
	"zn1711":{"param":param_dic_zn},
	"cu1710":{"param":param_dict_cu},
	"i1801":{"param":param_dict_i},
	"hc1801":{"param":param_dict_hc},
	"ni1801":{"param":param_dic_ni},
	"al1710":{"param":param_dic_al},
	"au1712":{"param":param_dic_au},
	"ag1712":{"param":param_dic_ag},
	"bu1712":{"param":param_dic_bu},
	"sn1709":{"param":param_dic_sn},
	"pb1710":{"param":param_dict_pb}
}

class BandAndTrigger(object):
	"""docstring for BandAndTrigger"""
	def __init__(self,param_dic):
		super(BandAndTrigger, self).__init__()

		self._write_to_csv_data = []

		self._pre_md_price = []
		self._now_md_price = []
		self._lastprice_array = []
		self._lastprice_map = dict()
		self._pre_ema_val = 0
		self._now_middle_value =0
		self._now_sd_val = 0

		# self._limit_twice_sd = 2

		self._moving_theo = "EMA"
		# band param
		self._param_period = param_dic["band_period"]


	def __del__(self):
		print "this is del"

	# get the md data ,every line;
	def get_md_data(self,md_array):
		# tranfer the string to float
		md_array[LASTPRICE] = float(md_array[LASTPRICE])
		md_array[VOLUME] = float(md_array[VOLUME])
		md_array[OPENINTEREST] = float(md_array[OPENINTEREST])
		md_array[TURNONER] = float(md_array[TURNONER])
		md_array[BIDPRICE1] = float(md_array[BIDPRICE1])
		md_array[ASKPRICE1] = float(md_array[ASKPRICE1])


		self._pre_md_price = self._now_md_price
		self._now_md_price = md_array

		lastprice = self._now_md_price[LASTPRICE]
		# self._lastprice_array.append(lastprice)
		# print lastprice
		if len(self._pre_md_price) ==0:
			# "the is the first line data"
			return

		self._lastprice_array.append(lastprice)
		if len(self._lastprice_array) <= self._param_period:
			# this is we dont start the period.
			# print  "the lastprice length is small: " +str(len(self._lastprice_array))
			ema_period = len(self._lastprice_array)
			pre_ema_val = bf.get_ema_data(lastprice,self._pre_ema_val,ema_period)
			self._pre_ema_val = pre_ema_val
			# save the pre_ema_val and return
			if lastprice not in self._lastprice_map:
				self._lastprice_map[lastprice] =1
			else:
				self._lastprice_map[lastprice] +=1
			return True

		front_lastprice = self._lastprice_array[0]
		self._lastprice_array.pop(0)
		if front_lastprice != lastprice:
			if lastprice not in self._lastprice_map :
				self._lastprice_map[lastprice] = 1
			else:
				self._lastprice_map[lastprice] +=1

			self._lastprice_map[front_lastprice] -=1
		# start the judge
		if self._moving_theo =="EMA":
			self._now_middle_value = bf.get_ema_data(lastprice,self._pre_ema_val,self._param_period)
			self._pre_ema_val = self._now_middle_value
		else:
			self._now_middle_value = bf.get_ma_data(self._lastprice_array,self._param_period)
		

		
		# self._ris_data = bf.get_rsi_data(self._rsi_array,self._rsi_period)
		# self._now_sd_val =bf.get_sd_data(self._now_md_price[TIME], self._lastprice_array,self._param_period)
		self._now_sd_val =bf.get_sd_data_by_map(self._lastprice_map,self._param_period)	

		tmp_to_csv = [self._now_md_price[TIME],self._now_md_price[LASTPRICE],round(self._now_middle_value,2),
					round(self._now_sd_val,2)]
		# print tmp_to_csv
		self._write_to_csv_data.append(tmp_to_csv)

		return True

	def get_to_csv_data(self):
		return self._write_to_csv_data

def clean_night_data(data):
	ret = []
	amBegin = 9*3600
	pmEnd = 15*3600

	for line in data:
		# print line
		timeLine = line[0].split(":")
		# print timeLine
		# tick = line[21]
		nowTime = int(timeLine[0])*3600+int(timeLine[1])*60+int(timeLine[2])

		if nowTime>=amBegin and nowTime <=pmEnd:
			ret.append(line)
		# if int(line[22]) ==0 or int(line[4]) ==3629:
		# 	continue
	return ret

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

		mysql="select *from hyqh.quotatick where TRADINGDAY = '%s' AND INSTRUMENTID = '%s' " % (date,instrumentid)

		print mysql
		cursor.execute (mysql)  

		icresult = cursor.fetchall()
		# get the data and sort it.
		# sortedlist = sorted(icresult, key = lambda x: (x[20], int(x[21])))
		cleandata = getSortedData(icresult)
		filename='./data/'+"%s_"%instrumentid
		filename=filename+str(date)+'.csv'
		print "we get the instrument id %s" % instrumentid

		bf.write_data_to_csv(filename,cleandata)

	cursor.close ()  
	conn.close () 


def main(filename):
	path = "./data/"+filename+".csv"
	f = open(path,'rb')
	instrumentid = filename.split("_")[0]
	print "the instrument id is: "+instrumentid
	reader = csv.reader(f)

	# reader =getSortedData(reader)
	
	bt = BandAndTrigger(nameDict[instrumentid]["param"])
	for row in reader:
		bt.get_md_data(row)
		# tranfer the string to float
	f.close()
	
	data = bt.get_to_csv_data()

	data = clean_night_data(data)
	path_new = "./data/"+filename+ "_band_data"+".csv"
	bf.write_data_to_csv(path_new,data)



if __name__=='__main__':

	data =[20170904]
	# instrumentid_array = ["ru1801","rb1801","zn1710","pb1710","cu1710","hc1801","i1801","ni1801","al1710","au1712","ag1712","bu1712"]
	instrumentid_array = ["zn1711"]
	for item in data:
		for instrumentid in instrumentid_array:
			# first get the sql data
			getSqlData(item,instrumentid)

			path = instrumentid+ "_"+str(item)
			print path
			main(path)	
