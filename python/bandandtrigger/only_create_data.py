# -*- coding:utf8 -*-
import csv
import band_and_trigger
import basic_fun as bf
import os
import adv
import wvad

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
			,"limit_rsi_data":75,"rsi_period":10,"diff_period":1
			,"band_open_edge":0.5,"band_loss_edge":1,"band_profit_edge":3,"band_period":3600
			,"volume_open_edge":20,"limit_max_draw_down":0,"multiple":5,"file":file
			,"sd_lastprice":100,"open_interest_edge":0,"spread":100,"config_file":310}
# 这个是螺纹钢的
param_dict_rb = {"limit_max_profit":25,"limit_max_loss":10,"rsi_bar_period":120
			,"limit_rsi_data":80,"rsi_period":14,"diff_period":10
			,"band_open_edge":0.5,"band_loss_edge":1,"band_profit_edge":3,"band_period":7200
			,"volume_open_edge":900,"limit_max_draw_down":0,"multiple":10,"file":file
			,"sd_lastprice":100,"open_interest_edge":0,"spread":100,"config_file":320}

# 这个是橡胶的
param_dic_ru = {"limit_max_profit":250,"limit_max_loss":100,"rsi_bar_period":120
			,"limit_rsi_data":80,"rsi_period":14,"diff_period":1
			,"band_open_edge":0.5,"band_loss_edge":1,"band_profit_edge":3,"band_period":7200
			,"volume_open_edge":120,"limit_max_draw_down":0,"multiple":10,"file":file
			,"sd_lastprice":0,"open_interest_edge":0,"spread":100,"config_file":330}

# 这个是锌的
param_dic_zn = {"limit_max_profit":125,"limit_max_loss":50,"rsi_bar_period":120
			,"limit_rsi_data":80,"rsi_period":14,"diff_period":1
			,"band_open_edge":0.5,"band_loss_edge":1,"band_profit_edge":3,"band_period":7200
			,"volume_open_edge":100,"limit_max_draw_down":0,"multiple":5,"file":file
			,"sd_lastprice":0,"open_interest_edge":0,"spread":100,"config_file":340}

param_dic_cu = {"limit_max_profit":25000,"limit_max_loss":10000,"rsi_bar_period":120
			,"limit_rsi_data":80,"rsi_period":14,"diff_period":1
			,"band_open_edge":0.5,"band_loss_edge":1,"band_profit_edge":3,"band_period":7200
			,"volume_open_edge":120,"limit_max_draw_down":0,"multiple":5,"file":file
			,"sd_lastprice":0,"open_interest_edge":0,"spread":100,"config_file":390}

param_dic_i = {"limit_max_profit":25000,"limit_max_loss":10000,"rsi_bar_period":120
			,"limit_rsi_data":80,"rsi_period":14,"diff_period":1
			,"band_open_edge":0.5,"band_loss_edge":1,"band_profit_edge":3,"band_period":7200
			,"volume_open_edge":120,"limit_max_draw_down":0,"multiple":100,"file":file
			,"sd_lastprice":0,"open_interest_edge":0,"spread":100,"config_file":350}


param_dict_cu = {"limit_max_profit":10000,"limit_max_loss":10000,"multiple":5
			,"rsi_bar_period":120,"limit_rsi_data":80,"rsi_period":14
			,"diff_period":1
			,"band_open_edge":0.5,"band_loss_edge":1,"band_profit_edge":3,"band_period":7200
			,"limit_max_draw_down":0,"file":file
			,"open_interest_edge":0,"spread":100,"volume_open_edge":900
			,"limit_sd":40,"limit_sd_open_edge":1,"limit_sd_close_edge":3,"config_file":390}

param_dict_i = {"limit_max_profit":10000,"limit_max_loss":10000,"multiple":100
			,"rsi_bar_period":120,"limit_rsi_data":80,"rsi_period":14
			,"diff_period":1
			,"band_open_edge":0.5,"band_loss_edge":1,"band_profit_edge":3,"band_period":7200
			,"limit_max_draw_down":0,"file":file
			,"open_interest_edge":0,"spread":100,"volume_open_edge":900
			,"limit_sd":2,"limit_sd_open_edge":1,"limit_sd_close_edge":3,"config_file":350}

param_dict_hc = {"limit_max_profit":10000,"limit_max_loss":10000,"multiple":10
			,"rsi_bar_period":120,"limit_rsi_data":80,"rsi_period":14
			,"diff_period":1
			,"band_open_edge":0.5,"band_loss_edge":1,"band_profit_edge":3,"band_period":7200
			,"limit_max_draw_down":0,"file":file
			,"open_interest_edge":0,"spread":100,"volume_open_edge":100
			,"limit_sd":2,"limit_sd_open_edge":1,"limit_sd_close_edge":3,"config_file":380}

nameDict = {
	"rb1801":{"param":param_dict_rb},
	"ru1801":{"param":param_dic_ru},
	"zn1710":{"param":param_dic_zn},
	"cu1710":{"param":param_dict_cu},
	"i1801":{"param":param_dict_i},
	"hc1801":{"param":param_dict_hc},
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

		self._diff_volume_array = []
		self._diff_open_interest_array = []
		self._diff_spread_array = []
		self._diff_turn_over_array = []
		self._diff_period =param_dic["diff_period"]

		self._multiple = param_dic["multiple"]

		self._rsi_array = []
		self._pre_rsi_lastprice =0 
		self._now_bar_rsi_tick = 0
		self._ris_data = 0
		self._rsi_period = param_dic["rsi_period"]
		self._rsi_bar_period = param_dic["rsi_bar_period"]
		self._limit_rsi_data = param_dic["limit_rsi_data"]

		self._now_bar_num = 1
		self._limit_bar_num = 120
		self._bar_min_lastprice = 0
		self._bar_max_lastprice = 0

		# self._limit_twice_sd = 2

		self._moving_theo = "EMA"
		# band param
		self._param_period = param_dic["band_period"]


		adv_param_dict = {}
		adv_param_dict["period"] = 120
		adv_param_dict["pre_adv"] = 0
		self._adv_obj = adv.ADV(adv_param_dict)

		wavd_param_dict = {}
		wavd_param_dict["period"] = 120
		wavd_param_dict["bar_num"] = 1
		self._wvad_obj = wvad.WVAD(wavd_param_dict)

		self._file = param_dic["file"]
		self._config_file = param_dic["config_file"]

		if len(self._lastprice_array) ==0:
			print "this is init function " + str(self._config_file)
			tmp_pre_ema_array = []
			tmp_rsi_lastprice = []
			config_file = "../config_pic/"+str(self._config_file)
			bf.get_config_info(tmp_pre_ema_array,self._lastprice_array,self._lastprice_map
				,self._rsi_array,tmp_rsi_lastprice,config_file)
			if len(tmp_pre_ema_array)==0:
				self._pre_ema_val = 0
				self._pre_rsi_lastprice = 0 
			else:
				self._pre_ema_val = tmp_pre_ema_array[0]
				self._pre_rsi_lastprice = tmp_rsi_lastprice[0]
		print self._pre_ema_val
		print len(self._lastprice_array)
		print self._rsi_array
		print self._pre_rsi_lastprice
		# print "the length of lastprice is: " +str(len(self._lastprice_array))


	def __del__(self):
		print "this is the over function " + str(self._config_file)
		config_file = "../config_pic/"+str(self._config_file)
		bf.write_config_info(self._pre_ema_val,self._lastprice_array
			,self._rsi_array,self._rsi_period,self._now_md_price[LASTPRICE],config_file)


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
		else:
			# self._rsi_array.append(lastprice - self._pre_md_price[LASTPRICE])
			if self._now_bar_rsi_tick >= self._rsi_bar_period:
				# 表示已经到了一个bar的周期。
				tmpdiff = lastprice - self._pre_rsi_lastprice		
				self._pre_rsi_lastprice = lastprice
				self._now_bar_rsi_tick = 1
				self._ris_data =bf.get_rsi_data2(tmpdiff,self._rsi_array,self._rsi_period)
				self._rsi_array.append(tmpdiff)
			else:
				self._now_bar_rsi_tick +=1
				tmpdiff = lastprice - self._pre_rsi_lastprice
				self._ris_data =bf.get_rsi_data2(tmpdiff,self._rsi_array,self._rsi_period)
				# self._ris_data = 0

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

		diff_volume = self._now_md_price[VOLUME] - self._pre_md_price[VOLUME]
		diff_interest = self._now_md_price[OPENINTEREST] - self._pre_md_price[OPENINTEREST]
		diff_turnover = self._now_md_price[TURNONER] - self._pre_md_price[TURNONER]

		self._diff_volume_array.append(diff_volume)
		self._diff_open_interest_array.append(diff_interest)
		self._diff_turn_over_array.append(diff_turnover)
		# 直接就是diff_interest
		# ema_diff_volume = bf.get_ema_data_2(self._diff_volume_array,self._diff_period)
		if self._now_bar_num > self._limit_bar_num:
			ema_diff_volume = bf.get_sum(self._diff_volume_array,self._limit_bar_num)
			ema_diff_openinterest = bf.get_sum(self._diff_open_interest_array,self._limit_bar_num)
			ema_diff_turnonver = bf.get_sum(self._diff_turn_over_array,self._limit_bar_num)
			self._now_bar_num = 1
			self._bar_max_lastprice = self._now_md_price[LASTPRICE]
			self._bar_min_lastprice = self._now_md_price[LASTPRICE]
		else:
			ema_diff_volume = bf.get_sum(self._diff_volume_array,self._now_bar_num)
			ema_diff_openinterest = bf.get_sum(self._diff_open_interest_array,self._now_bar_num)
			ema_diff_turnonver = bf.get_sum(self._diff_turn_over_array,self._now_bar_num)
			self._now_bar_num +=1
			if self._bar_max_lastprice ==0 or self._bar_max_lastprice < self._now_md_price[LASTPRICE]:
				self._bar_max_lastprice = self._now_md_price[LASTPRICE]
			if self._bar_min_lastprice ==0 or self._bar_min_lastprice > self._now_md_price[LASTPRICE]:
				self._bar_min_lastprice = self._now_md_price[LASTPRICE]

		if ema_diff_volume ==0:
			spread =50
			self._diff_spread_array.append(spread)
		else:

			# avg_price = float(diff_turnover)/diff_volume/self._multiple
			avg_price = float(ema_diff_turnonver)/ema_diff_volume/self._multiple
			# if lastprice > self._now_middle_value:
			# if self._pre_md_price[ASKPRICE1] != self._pre_md_price[BIDPRICE1]:
			# 注意，现在算的只是和买一价的位置关系。
			# spread = 100*(avg_price - self._pre_md_price[BIDPRICE1])/(self._pre_md_price[ASKPRICE1] - self._pre_md_price[BIDPRICE1])
			# spread = 100*(avg_price - self._now_md_price[BIDPRICE1])/(self._now_md_price[ASKPRICE1] - self._now_md_price[BIDPRICE1])
			if self._bar_max_lastprice == self._bar_min_lastprice:
				spread = 50
			else:
				spread = 100*(avg_price - self._bar_min_lastprice)/(self._bar_max_lastprice - self._bar_min_lastprice)
			self._diff_spread_array.append(spread)
			# spread = bf.get_weighted_mean(self._diff_spread_array,self._diff_volume_array,self._diff_period)
		
		# avg = (int(self._now_md_price[BIDPRICE1VOLUME])+int(self._now_md_price[ASKPRICE1VOLUME]))/2
		tmp_adv = self._adv_obj.get_md_data(md_array)
		tmp_wvad = self._wvad_obj.get_md_data(md_array)
		tmp_to_csv = [self._now_md_price[TIME],self._now_md_price[LASTPRICE],round(self._now_middle_value,2),
					round(self._now_sd_val,2),round(self._ris_data,2),diff_volume,diff_interest,round(self._diff_spread_array[-1],2),
					round(ema_diff_volume,2),round(ema_diff_openinterest,2),round(tmp_wvad,2)
					]
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
	for line in night:
		ret.append(line)
	for line in zero:
		ret.append(line)
	for line in day:
		ret.append(line)

	return ret

def main(filename):
	path = "../data/"+filename+".csv"
	# path = "../data/"+filename
	# read_data_from_csv(pth)
	f = open(path,'rb')
	instrumentid = filename.split("_")[0]
	print "the instrument id is: "+instrumentid
	reader = csv.reader(f)

	reader =getSortedData(reader)
	
	bt = BandAndTrigger(nameDict[instrumentid]["param"])
	for row in reader:
		bt.get_md_data(row)
		# tranfer the string to float
	f.close()
	
	data = bt.get_to_csv_data()

	data = clean_night_data(data)
	path_new = "../data/"+filename+ "_band_data"+".csv"
	bf.write_data_to_csv(path_new,data)


if __name__=='__main__':
	# data2 =[20170724,20170725,20170726,20170727,20170728]
	# data3 =[20170731,20170801,20170802,20170803,20170804,20170807,20170808,20170809]
	# data = data2+ data3
	# file_dir = "../zn"
	# for root, dirs, files in os.walk(file_dir):
	#     for file in files:
	#     	if "band_data" not in file and "csv" in file:
	#     		tmp_path = os.path.join(root,file)
	#     		tmp_path = tmp_path.split('/')[2]
	#     		print tmp_path
	#     		main(tmp_path)



	# data = [20170821,20170822,20170823,20170824,20170825]
	data = [20170828,20170829,20170830]
	# instrumentid_array = ["ru1801","rb1801","zn1710","pb1710","cu1710","hc1801","i1801"]
	instrumentid_array = ["rb1801"]
	for item in data:
		for instrumentid in instrumentid_array:
			path = instrumentid+ "_"+str(item)
			print path
			main(path)	
