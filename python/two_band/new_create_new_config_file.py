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
param_dic_ru = {"limit_max_profit":250,"limit_max_loss":100,"rsi_bar_period":120
			,"limit_rsi_data":80,"rsi_period":14,"diff_period":60,"tick_num":5
			,"band_open_edge":0.5,"band_loss_edge":1,"band_profit_edge":3,"band_period":7200
			,"volume_open_edge":120,"limit_max_draw_down":0,"multiple":10,"file":file
			,"sd_lastprice":0,"open_interest_edge":0,"spread":100,"config_file":330}

# 这个是锌的
param_dic_zn = {"limit_max_profit":125,"limit_max_loss":50,"rsi_bar_period":120
			,"limit_rsi_data":80,"rsi_period":14,"diff_period":60,"tick_num":5
			,"band_open_edge":0.5,"band_loss_edge":1,"band_profit_edge":3,"band_period":7200
			,"volume_open_edge":100,"limit_max_draw_down":0,"multiple":5,"file":file
			,"sd_lastprice":0,"open_interest_edge":0,"spread":100,"config_file":340}

param_dict_i = {"limit_max_profit":10000,"limit_max_loss":10000,"multiple":100
			,"rsi_bar_period":120,"limit_rsi_data":80,"rsi_period":14
			,"diff_period":60
			,"band_open_edge":0.5,"band_loss_edge":1,"band_profit_edge":3,"band_period":7200
			,"limit_max_draw_down":0,"file":file
			,"open_interest_edge":0,"spread":100,"volume_open_edge":900
			,"limit_sd":2,"limit_sd_open_edge":1,"limit_sd_close_edge":3,"config_file":350}

param_dic_ni = {"limit_max_profit":125,"limit_max_loss":50,"rsi_bar_period":120
			,"limit_rsi_data":80,"rsi_period":14,"diff_period":60
			,"band_open_edge":0.5,"band_loss_edge":1,"band_profit_edge":3,"band_period":7200
			,"volume_open_edge":100,"limit_max_draw_down":0,"multiple":1,"file":file
			,"sd_lastprice":0,"open_interest_edge":0,"spread":100,"config_file":360}

param_dic_al = {"limit_max_profit":125,"limit_max_loss":50,"rsi_bar_period":120
			,"limit_rsi_data":80,"rsi_period":14,"diff_period":60
			,"band_open_edge":0.5,"band_loss_edge":1,"band_profit_edge":3,"band_period":7200
			,"volume_open_edge":100,"limit_max_draw_down":0,"multiple":5,"file":file
			,"sd_lastprice":0,"open_interest_edge":0,"spread":100,"config_file":370}

param_dict_hc = {"limit_max_profit":10000,"limit_max_loss":10000,"multiple":10
			,"rsi_bar_period":120,"limit_rsi_data":80,"rsi_period":14
			,"diff_period":60
			,"band_open_edge":0.5,"band_loss_edge":1,"band_profit_edge":3,"band_period":7200
			,"limit_max_draw_down":0,"file":file
			,"open_interest_edge":0,"spread":100,"volume_open_edge":100
			,"limit_sd":2,"limit_sd_open_edge":1,"limit_sd_close_edge":3,"config_file":380}

param_dict_cu = {"limit_max_profit":10000,"limit_max_loss":10000,"multiple":5
			,"rsi_bar_period":120,"limit_rsi_data":80,"rsi_period":14
			,"diff_period":60
			,"band_open_edge":0.5,"band_loss_edge":1,"band_profit_edge":3,"band_period":7200
			,"limit_max_draw_down":0,"file":file
			,"open_interest_edge":0,"spread":100,"volume_open_edge":900
			,"limit_sd":40,"limit_sd_open_edge":1,"limit_sd_close_edge":3,"config_file":390}


param_dic_au = {"limit_max_profit":125,"limit_max_loss":50,"rsi_bar_period":120
			,"limit_rsi_data":80,"rsi_period":14,"diff_period":60
			,"band_open_edge":0.5,"band_loss_edge":1,"band_profit_edge":3,"band_period":7200
			,"volume_open_edge":100,"limit_max_draw_down":0,"multiple":1000,"file":file
			,"sd_lastprice":0,"open_interest_edge":0,"spread":100,"config_file":400}

param_dic_ag = {"limit_max_profit":125,"limit_max_loss":50,"rsi_bar_period":120
			,"limit_rsi_data":80,"rsi_period":14,"diff_period":60
			,"band_open_edge":0.5,"band_loss_edge":1,"band_profit_edge":3,"band_period":7200
			,"volume_open_edge":100,"limit_max_draw_down":0,"multiple":15,"file":file
			,"sd_lastprice":0,"open_interest_edge":0,"spread":100,"config_file":410}

param_dic_bu = {"limit_max_profit":125,"limit_max_loss":50,"rsi_bar_period":120
			,"limit_rsi_data":80,"rsi_period":14,"diff_period":60
			,"band_open_edge":0.5,"band_loss_edge":1,"band_profit_edge":3,"band_period":7200
			,"volume_open_edge":100,"limit_max_draw_down":0,"multiple":10,"file":file
			,"sd_lastprice":0,"open_interest_edge":0,"spread":100,"config_file":420}

param_dic_sn = {"limit_max_profit":125,"limit_max_loss":50,"rsi_bar_period":120
			,"limit_rsi_data":80,"rsi_period":14,"diff_period":60
			,"band_open_edge":0.5,"band_loss_edge":1,"band_profit_edge":3,"band_period":7200
			,"volume_open_edge":100,"limit_max_draw_down":0,"multiple":5,"file":file
			,"sd_lastprice":0,"open_interest_edge":0,"spread":100,"config_file":430}

nameDict = {
	"rb1801":{"param":param_dict_rb},
	"ru1801":{"param":param_dic_ru},
	"zn1712":{"param":param_dic_zn},
	"cu1712":{"param":param_dict_cu},
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
			config_file = "../config/"+str(self._config_file+2)
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

		config_file = "../config/"+str(self._config_file+2)
		bf.write_config_info(self._pre_ema_val_60,self._pre_ema_val_5,self._pre_ema_val_5,
			self._lastprice_array,self._ema_period,config_file)

		config_file = "../config/"+str(self._config_file+3)
		bf.write_config_info(self._pre_ema_val_60,self._pre_ema_val_5,self._pre_ema_val_5,
			self._lastprice_array,self._ema_period,config_file)

		config_file = "../config/"+str(self._config_file+4)
		bf.write_config_info(self._pre_ema_val_60,self._pre_ema_val_5,self._pre_ema_val_5,
			self._lastprice_array,self._ema_period,config_file)

		config_file = "../config/"+str(self._config_file+5)
		bf.write_config_info(self._pre_ema_val_60,self._pre_ema_val_5,self._pre_ema_val_5,
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
	data1 =[20171009,20171010,20171011,20171012,20171013]
	data2 =[20171016,20171017,20171018,20171019,20171020]	
	data3 =[20171023,20171024,20171025,20171026]
	data = data1+data2+data3
	# instrumentid_array = ["ru1801","rb1801","zn1710","pb1710","cu1710","hc1801","i1801","ni1801","al1710","au1712","ag1712","bu1712"]
	instrumentid_array = ["rb1801"]

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