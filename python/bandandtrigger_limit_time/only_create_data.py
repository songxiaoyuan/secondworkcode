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
param_dict_pb = {"limit_max_profit":125,"limit_max_loss":50,"rsi_bar_period":50
			,"limit_rsi_data":75,"rsi_period":10,"diff_period":60,"tick_num":5
			,"band_open_edge":0.5,"band_loss_edge":1,"band_profit_edge":3,"band_period":7200
			,"volume_open_edge":20,"limit_max_draw_down":0,"multiple":5,"file":file
			,"sd_lastprice":100,"open_interest_edge":0,"spread":100,"config_file":310}
# 这个是螺纹钢的
param_dict_rb = {"rsi_bar_period":120,"limit_rsi_data":80,"rsi_period":14,
			    "band_period":7200,"multiple":10,"file":file,"config_file":320}

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
	"al1712":{"param":param_dic_al},
	"au1712":{"param":param_dic_au},
	"ag1712":{"param":param_dic_ag},
	"bu1712":{"param":param_dic_bu},
	"sn1709":{"param":param_dic_sn},
	"pb1712":{"param":param_dict_pb}
}

class BandAndTrigger(object):
	"""docstring for BandAndTrigger"""
	def __init__(self,param_dic):
		super(BandAndTrigger, self).__init__()

		self._write_to_csv_data = []

		self._pre_md_price = []
		self._now_md_price = []
		self._lastprice_array = []
		self._pre_ema_val = 0
		self._now_middle_value =0

		self._multiple = param_dic["multiple"]
		self._moving_theo = "EMA"
		# band param
		self._param_period = param_dic["band_period"]


		self._file = param_dic["file"]
		self._config_file = param_dic["config_file"]

		if len(self._lastprice_array) ==0:
			print "this is init function " + str(self._config_file)
			tmp_pre_ema_array = []
			config_file = "../config/"+str(self._config_file)
			bf.get_config_info(tmp_pre_ema_array,self._lastprice_array,config_file)
			if len(tmp_pre_ema_array)==0:
				self._pre_ema_val = 0
			else:
				self._pre_ema_val = tmp_pre_ema_array[0]
		print self._pre_ema_val
		print len(self._lastprice_array)


	def write_config(self):
		config_file = "../config/"+str(self._config_file)
		bf.write_config_info(self._pre_ema_val,self._lastprice_array,config_file)


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
		if self._pre_ema_val ==0:
			self._pre_ema_val = lastprice

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
			return True

		if self._moving_theo =="EMA":
			self._now_middle_value = bf.get_ema_data(lastprice,self._pre_ema_val,self._param_period)
			self._pre_ema_val = self._now_middle_value
		else:
			self._now_middle_value = bf.get_ma_data(self._lastprice_array,self._param_period)	
		self._lastprice_array.pop(0)

		diff_volume = self._now_md_price[VOLUME] - self._pre_md_price[VOLUME]
		diff_interest = self._now_md_price[OPENINTEREST] - self._pre_md_price[OPENINTEREST]
		diff_turnover = self._now_md_price[TURNONER] - self._pre_md_price[TURNONER]

		if diff_volume != 0 and (self._pre_md_price[ASKPRICE1] - self._pre_md_price[BIDPRICE1]) !=0:
			avg_price = float(diff_turnover)/diff_volume/self._multiple
			spread = 100*(avg_price - self._pre_md_price[BIDPRICE1])/(self._pre_md_price[ASKPRICE1] - self._pre_md_price[BIDPRICE1])
		else:
			spread = 50


		tmp_to_csv = [self._now_md_price[TIME],self._now_md_price[LASTPRICE],
					round(self._now_middle_value,2),
					round(diff_volume,2),round(diff_interest,2),round(spread,2)]
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


def main(filename):
	path = "../data/"+filename+".csv"
	f = open(path,'rb')
	instrumentid = filename.split("_")[0]
	print "the instrument id is: "+instrumentid
	reader = csv.reader(f)
	bt = BandAndTrigger(nameDict[instrumentid]["param"])
	for row in reader:
		bt.get_md_data(row)
		# tranfer the string to float
	bt.write_config()
	f.close()
	
	data = bt.get_to_csv_data()
	data = clean_night_data(data)
	path_new = "../create_data/"+filename+ "_band_data"+".csv"
	bf.write_data_to_csv(path_new,data)



if __name__=='__main__':
	data1 =[20170801,20170802,20170803,20170804]
	data2 =[20170807,20170808,20170809,20170810,20170811]
	data3 =[20170814,20170815,20170816,20170817,20170818]
	data4 =[20170821,20170822,20170823,20170824,20170825]	
	data5 =[20170828,20170829,20170830,20170831,20170901]
	data6 =[20170904,20170905,20170906,20170907,20170908]
	data7 =[20170911,20170912,20170913,20170914,20170915]	
	data8 =[20170918,20170919,20170920,20170921,20170922]
	data9 =[20170925,20170926,20170927,20170928,20170929]
	data10 =[20171009,20171010,20171011,20171012,20171013]
	data11 =[20171016,20171017,20171018,20171019,20171020]	
	data12 =[20171023,20171024,20171025,20171026,20171027]
	data13 = [20171030,20171031]
	data = data1+data2+data3+data4+data5+data6+data7+data8+data9+data10+data11+data12+data13
	# data =[20171020]
	instrumentid_array = ["rb1801"]
	# instrumentid_array = ["al1712","ni1801","cu1712"]
	for item in data:
		for instrumentid in instrumentid_array:
			path = instrumentid+ "_"+str(item)
			print path
			main(path)	
