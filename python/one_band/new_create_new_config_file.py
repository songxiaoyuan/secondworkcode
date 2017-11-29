# -*- coding:utf8 -*-
import csv
import basic_fun as bf
import os
import cx_Oracle  
import time
import shutil

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

date = time.strftime('%Y%m%d',time.localtime(time.time()))
hour = time.strftime('%H',time.localtime(time.time()))

# 这个是铅的
param_dict_pb = {"rsi_period":14,"limit_ema_tick_5":600,"limit_ema_tick_1":120,
			"multiple":5,"file":file,"config_file":310}
# 这个是螺纹钢的
param_dict_rb = {"rsi_period":14,"limit_ema_tick_5":600,"limit_ema_tick_1":120,
			"multiple":10,"file":file,"config_file":320}

# 这个是橡胶的
param_dic_ru = {"rsi_period":14,"limit_ema_tick_5":600,"limit_ema_tick_1":120,
			"multiple":10,"file":file,"config_file":330}

# 这个是锌的
param_dic_zn = {"rsi_period":14,"limit_ema_tick_5":600,"limit_ema_tick_1":120,
			"multiple":5,"file":file,"config_file":340}

# param_dict_i = {"rsi_period":14,"limit_ema_tick_5":600,"limit_ema_tick_1":120,
# 			"multiple":100,"file":file,"config_file":340}

param_dic_ni = {"rsi_period":14,"limit_ema_tick_5":600,"limit_ema_tick_1":120,
			"multiple":1,"file":file,"config_file":350}

param_dic_al = {"rsi_period":14,"limit_ema_tick_5":600,"limit_ema_tick_1":120,
			"multiple":5,"file":file,"config_file":360}

# param_dict_hc = {"rsi_period":14,"limit_ema_tick_5":600,"limit_ema_tick_1":120,
# 			"multiple":10,"file":file,"config_file":380}

param_dict_cu = {"rsi_period":14,"limit_ema_tick_5":600,"limit_ema_tick_1":120,
			"multiple":5,"file":file,"config_file":370}

param_dict_pp = {"rsi_period":14,"limit_ema_tick_5":600,"limit_ema_tick_1":120,
			"multiple":5,"file":file,"config_file":380}
param_dict_v = {"rsi_period":14,"limit_ema_tick_5":600,"limit_ema_tick_1":120,
			"multiple":5,"file":file,"config_file":390}
param_dict_au = {"rsi_period":14,"limit_ema_tick_5":600,"limit_ema_tick_1":120,
			"multiple":1000,"file":file,"config_file":400}
param_dict_ag = {"rsi_period":14,"limit_ema_tick_5":600,"limit_ema_tick_1":120,
			"multiple":15,"file":file,"config_file":410}
param_dict_bu = {"rsi_period":14,"limit_ema_tick_5":600,"limit_ema_tick_1":120,
			"multiple":10,"file":file,"config_file":420}

param_dict_i = {"rsi_period":14,"limit_ema_tick_5":600,"limit_ema_tick_1":120,
			"multiple":100,"file":file,"config_file":430}
param_dict_hc = {"rsi_period":14,"limit_ema_tick_5":600,"limit_ema_tick_1":120,
			"multiple":10,"file":file,"config_file":440}
param_dict_j = {"rsi_period":14,"limit_ema_tick_5":600,"limit_ema_tick_1":120,
			"multiple":100,"file":file,"config_file":450}
param_dict_jm = {"rsi_period":14,"limit_ema_tick_5":600,"limit_ema_tick_1":120,
			"multiple":60,"file":file,"config_file":460}
param_dict_y = {"rsi_period":14,"limit_ema_tick_5":600,"limit_ema_tick_1":120,
			"multiple":10,"file":file,"config_file":470}
param_dict_p = {"rsi_period":14,"limit_ema_tick_5":600,"limit_ema_tick_1":120,
			"multiple":10,"file":file,"config_file":480}
param_dict_c = {"rsi_period":14,"limit_ema_tick_5":600,"limit_ema_tick_1":120,
			"multiple":10,"file":file,"config_file":490}
param_dict_a = {"rsi_period":14,"limit_ema_tick_5":600,"limit_ema_tick_1":120,
			"multiple":10,"file":file,"config_file":500}
param_dict_m = {"rsi_period":14,"limit_ema_tick_5":600,"limit_ema_tick_1":120,
			"multiple":10,"file":file,"config_file":510}
param_dict_cs = {"rsi_period":14,"limit_ema_tick_5":600,"limit_ema_tick_1":120,
			"multiple":10,"file":file,"config_file":522}

nameDict = {
	"rb1805":{"param":param_dict_rb},
	"ru1801":{"param":param_dic_ru},
	"zn1801":{"param":param_dic_zn},
	"cu1801":{"param":param_dict_cu},
	# "i1801":{"param":param_dict_i},
	# "hc1801":{"param":param_dict_hc},
	"ni1805":{"param":param_dic_ni},
	"al1801":{"param":param_dic_al},
	"pp1801":{"param":param_dict_pp},
	"v1801":{"param":param_dict_v},
	"au1806":{"param":param_dict_au},
	"ag1712":{"param":param_dict_ag},
	"bu1712":{"param":param_dict_bu},
	"i1805":{"param":param_dict_i},
	"hc1805":{"param":param_dict_hc},
	"j1801":{"param":param_dict_j},
	"jm1801":{"param":param_dict_jm},
	"y1801":{"param":param_dict_y},
	"p1801":{"param":param_dict_p},
	"c1801":{"param":param_dict_c},
	"a1801":{"param":param_dict_a},
	"m1801":{"param":param_dict_m},
	"cs1801":{"param":param_dict_cs},
	"pb1801":{"param":param_dict_pb}
}

class BandAndTrigger(object):
	"""docstring for BandAndTrigger"""
	def __init__(self,param_dic):
		super(BandAndTrigger, self).__init__()

		self._write_to_csv_data = []

		self._pre_md_price = []
		self._now_md_price = []
		self._lastprice_array = []


		self._pre_ema_val_60 = 0
		self._now_middle_60 =0

		self._pre_ema_val_5 = 0
		self._now_middle_5 = 0
		self._now_ema_tick_5 = 0
		self._limit_ema_tick_5 = param_dic["limit_ema_tick_5"]

		self._pre_ema_val_1 = 0
		self._now_middle_1 = 0
		self._now_ema_tick_1 = 0
		self._limit_ema_tick_1 = param_dic["limit_ema_tick_1"]

		self._ema_period = 20
		self._current_hour = 9

		self._multiple = param_dic["multiple"]

		self._rsi_period = param_dic["rsi_period"]
		self._rsi_val = 0

		self._file = param_dic["file"]
		self._config_file = param_dic["config_file"]

		if len(self._lastprice_array) ==0:
			print "this is init function " + str(self._config_file)
			tmp_pre_ema_array_60 = []
			tmp_pre_ema_array_5 = []
			tmp_pre_ema_array_1 = []
			config_file = "../hour_config/config/"+str(self._config_file+2)
			bf.get_config_info(tmp_pre_ema_array_60,tmp_pre_ema_array_5,tmp_pre_ema_array_1,self._lastprice_array,config_file)
			if len(tmp_pre_ema_array_60)==0:
				self._pre_ema_val_60 = 0
				self._pre_ema_val_5 = 0
				self._pre_ema_val_1 = 0
			else:
				self._pre_ema_val_60 = tmp_pre_ema_array_60[0]
				self._pre_ema_val_5 = tmp_pre_ema_array_5[0]
				self._pre_ema_val_1 = tmp_pre_ema_array_1[0]
		# print self._pre_ema_val_60
		print len(self._lastprice_array)
		# print "the length of lastprice is: " +str(len(self._lastprice_array))


	def __del__(self):
		print "this is the over function " + str(self._config_file)

		config_file = "../hour_config/config/"+str(self._config_file+2)
		bf.write_config_info(self._pre_ema_val_60,self._pre_ema_val_5,self._pre_ema_val_1,
			self._lastprice_array,self._ema_period,config_file)

		config_file = "../hour_config/config/"+str(self._config_file+3)
		bf.write_config_info(self._pre_ema_val_60,self._pre_ema_val_5,self._pre_ema_val_1,
			self._lastprice_array,self._ema_period,config_file)

		config_file = "../hour_config/config/"+str(self._config_file+4)
		bf.write_config_info(self._pre_ema_val_60,self._pre_ema_val_5,self._pre_ema_val_1,
			self._lastprice_array,self._ema_period,config_file)

		config_file = "../hour_config/config/"+str(self._config_file+5)
		bf.write_config_info(self._pre_ema_val_60,self._pre_ema_val_5,self._pre_ema_val_1,
			self._lastprice_array,self._ema_period,config_file)
		print "has write the config file"


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

		if self._pre_ema_val_60 ==0:
			self._pre_ema_val_60 = lastprice
			self._pre_ema_val_5 = lastprice
			self._pre_ema_val_1 = lastprice
		self._now_middle_60 = bf.get_ema_data(lastprice,self._pre_ema_val_60,self._ema_period)
		self._now_middle_5 = bf.get_ema_data(lastprice,self._pre_ema_val_5,self._ema_period)
		self._now_middle_1 = bf.get_ema_data(lastprice,self._pre_ema_val_1,self._ema_period)
		
		self._sd_val = bf.get_sd_data(lastprice,self._lastprice_array,self._ema_period)
		self._rsi_val = bf.get_rsi_data(lastprice,self._lastprice_array,self._rsi_period)

		# print len(self._lastprice_array)
		hour = int(self._now_md_price[TIME].split(':')[0])
		if hour != self._current_hour and hour !=13 and hour != 21:
			# print "the hour is not  equal "
			self._current_hour = hour
			self._pre_ema_val_60 = self._now_middle_60
			self._lastprice_array.append(lastprice)
		if self._now_ema_tick_1 >= self._limit_ema_tick_1:
			self._now_ema_tick_1 = 0
			self._pre_ema_val_1 = self._now_middle_1
		else:
			self._now_ema_tick_1 +=1
		if self._now_ema_tick_5 >= self._limit_ema_tick_5:
			self._now_ema_tick_5 = 0
			self._pre_ema_val_5 = self._now_middle_5
		else:
			self._now_ema_tick_5 +=1

		diff_volume = self._now_md_price[VOLUME] - self._pre_md_price[VOLUME]
		diff_interest = self._now_md_price[OPENINTEREST] - self._pre_md_price[OPENINTEREST]
		diff_turnover = self._now_md_price[TURNONER] - self._pre_md_price[TURNONER]

		if diff_volume != 0 and (self._pre_md_price[ASKPRICE1] - self._pre_md_price[BIDPRICE1]) !=0:
			avg_price = float(diff_turnover)/diff_volume/self._multiple
			spread = 100*(avg_price - self._pre_md_price[BIDPRICE1])/(self._pre_md_price[ASKPRICE1] - self._pre_md_price[BIDPRICE1])
		else:
			spread = 50


		tmp_to_csv = [self._now_md_price[TIME],self._now_md_price[LASTPRICE],
					round(self._now_middle_60,2),round(self._now_middle_5,2),round(self._now_middle_1,2),round(self._sd_val,2),
					round(self._rsi_val,2),round(diff_volume,2),round(spread,2)]
		# print tmp_to_csv
		self._write_to_csv_data.append(tmp_to_csv)

		return True

	def get_to_csv_data(self):
		return self._write_to_csv_data

def copy_file():
	print "start create the real server data"


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
			nowTime = 0

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

def start_create_config(instrumentid,data):
	print "start create the config file of " + instrumentid
	if instrumentid not in nameDict:
		print "the instrument id " + instrumentid + " is not in the dict"
	param =  nameDict[instrumentid]["param"]
	bt = BandAndTrigger(param)
	for row in data:
		bt.get_md_data(row)
		# tranfer the string to float


def main():
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
	# data13 =[20171030]
	# data = data1+data2+data3+data4+data5+data6+data7+data8+data9+data10+data11+data12+data13
	# instrumentid_array = ["ru1801","rb1801","zn1710","pb1710","cu1710","hc1801","i1801","ni1801","al1710","au1712","ag1712","bu1712"]
	# data13 = [20171030,20171031,20171101,20171102,20171103]
	data14 = [20171106,20171107,20171108,20171109,20171110]
	data15 = [20171113,20171114,20171115,20171116,20171117]
	data16 = [20171120,20171121,20171122,20171123]
	# data = data1+data2+data3+data4+data5+data6+data7+data8+data9+data10+data11+data12+data13
	data = data14+data15+data16
	# instrumentid_array = ["rb1805","ru1801","zn1801","cu1801","al1801","ni1805","pp1801","v1801","au1806","ag1712","pb1801","bu1712"]
	# instrumentid_array = ["j1801","jm1801","m1801","cs1801","c1801","a1801","i1805","hc1805"]
	instrumentid_array = ["y1801","p1801"]

	for mydate in data:
		for instrumentid in instrumentid_array:
			# first get the sql data
			filename = instrumentid+ "_"+str(mydate)
			path = "../data/"+filename+".csv"
			f = open(path,'rb')
			print "the instrument id is: "+filename
			reader = csv.reader(f)
			start_create_config(instrumentid,reader)


if __name__=='__main__':
	main()