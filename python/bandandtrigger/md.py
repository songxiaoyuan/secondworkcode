# -*- coding:utf8 -*-
import csv
import basic_fun as bf
import os

TIME = 0
LASTPRICE = 1
MIDDLE = 2
SD = 3
RSI = 4
DIFF_VOLUME = 5
DIFF_OPENINTEREST = 6
SPREAD = 7
EMA_DIFF_VOLUME = 8
EMA_DIFF_OPENINTEREST = 9
EMA_SPREAD = 10
CONTINUOUS_PRICE = 11
WAVD_CONTINUE = 12
LONG =1
SHORT =0

class BandAndTrigger(object):
	"""docstring for BandAndTrigger"""
	def __init__(self,param_dic):
		super(BandAndTrigger, self).__init__()
		# self.arg = arg
		self._direction = param_dic["direction"]


		self._limit_rsi_data = param_dic["limit_rsi_data"]

		self._direction = param_dic["direction"]
		self._moving_theo = "EMA"
		# now we have the cangwei and the limit cangwei
		self._now_interest = 0
		self._limit_interest = 1

		self._profit = 0

		# band param
		self._param_open_edge1 = param_dic["band_open_edge1"]
		self._param_open_edge2 = param_dic["band_open_edge2"]
		self._param_loss_edge = param_dic["band_loss_edge"]
		self._param_close_edge =param_dic["band_profit_edge"]		

		# trigger param
		self._param_volume_open_edge = param_dic["volume_open_edge"]
		self._param_open_interest_edge = param_dic["open_interest_edge"]
		self._param_spread = param_dic["spread"]

		self._ris_data = 0

		self._limit_sd = param_dic["limit_sd"]
		self._limit_sd_open_edge = param_dic["limit_sd_open_edge"]
		self._limit_sd_close_edge = param_dic["limit_sd_close_edge"]

		self._now_interest = 0
		self._limit_interest = 1

		self._limit_wavd = param_dic["limit_wvad"]

		self._file = param_dic["file"]

		self._limit_continuous_price = 3


	def __del__(self):
		print "this is the over function"
		# bf.write_config_info(self._pre_ema_val,self._lastprice_array
		# 	,self._rsi_array,self._rsi_period,self._now_md_price[LASTPRICE],self._config_file)

	# get the md data ,every line;
	def get_md_data(self,md_array):
		# tranfer the string to float
		self._time = md_array[TIME]
		self._lastprice = float(md_array[LASTPRICE])
		self._now_middle_value = float(md_array[MIDDLE])
		self._now_sd_val = float(md_array[SD])
		self._ris_data = float(md_array[RSI])
		self._diff_volume = float(md_array[DIFF_VOLUME])
		self._diff_openinterest = float(md_array[DIFF_OPENINTEREST])
		self._spread = float(md_array[SPREAD])
		self._ema_diff_volume = float(md_array[EMA_DIFF_VOLUME])
		self._ema_diff_openinterest = float(md_array[EMA_DIFF_OPENINTEREST])
		self._ema_spread = float(md_array[EMA_SPREAD])
		# self._avg_sum = float(md_array[AVG_SUM])
		self._ema_diff_volume = self._diff_volume
		self._ema_diff_openinterest = self._diff_openinterest
		self._ema_spread = self._spread
		self._wavd = float(md_array[EMA_SPREAD])
		# self._wavd = float(md_array[WAVD_CONTINUE])
		self._continuous_price = float(md_array[CONTINUOUS_PRICE])


		open_time = self.is_trend_open_time()
		close_time = self.is_trend_close_time()
		# close_time = False
		
		if open_time and self._now_interest < self._limit_interest:
		# if open_time:
			self._now_interest +=1
			# print "we start to open"
			self._open_lastprice = self._lastprice
			mesg= "the time of open: "+self._time + ",the price: " + str(self._lastprice)
			mesg1 = "the diff volume: "+str(self._ema_diff_volume)+", the interest: " + str(self._ema_diff_openinterest) + ", the spread: "+ str(self._wavd)
			self._file.write(mesg+"\n")
			self._file.write(mesg1+"\n")
			# print "the diff volume is:" + str(self._now_md_price[VOLUME] - self._pre_md_price[VOLUME])
		# elif close_time:
		elif close_time and self._now_interest >0:
			self._now_interest -=1
			# print "we need to close"
			if self._direction ==LONG:
				self._profit +=(self._lastprice - self._open_lastprice)
			elif self._direction ==SHORT:
				self._profit +=(self._open_lastprice - self._lastprice)
			self._open_lastprice = 0
			mesg= "the time of close:"+self._time+ ",the price: " + str(self._lastprice)
			self._file.write(mesg+"\n")

		return True

	def is_trend_open_time(self):

		open_val1 = self._param_open_edge1
		open_val2 = self._param_open_edge2
		is_band_open = self.is_band_open_time(self._direction,self._lastprice,
											self._now_middle_value,self._now_sd_val,open_val1,open_val2,
											self._limit_sd,self._limit_sd_open_edge)
		# return is_band_open
		if is_band_open ==False:
			return False
		# return True
		is_trigger_open = self.is_trigger_size_open_time(self._direction,self._param_volume_open_edge,
													self._param_open_interest_edge,self._param_spread,
													self._limit_wavd,self._limit_continuous_price)
		return is_trigger_open

	def is_trigger_size_open_time(self,direction,volume_open_edge,
								openinterest_edge,spread_edge,limit_wavd,limit_continuous_pric):

		# if self._ema_diff_volume < volume_open_edge:
		# 	return False
		# if openinterest_edge != 0 and self._ema_diff_openinterest <= openinterest_edge:
		# 	return False
		# if self._direction ==SHORT:
		# 	self._ema_spread = 100 - self._ema_spread
		# if self._ema_spread < spread_edge:
		# 	return False
		# return True
		if self._direction ==SHORT:
			self._wavd = 0 - self._wavd
		if self._wavd < limit_wavd and limit_wavd != 0:
			return False
		return True
		# if self._direction ==SHORT:
		# 	self._continuous_price = 0 - self._continuous_price
		# if self._continuous_price < limit_continuous_pric and limit_continuous_pric != 0:
		# 	return False
		# return True

	def is_trend_close_time(self):
		# this is used to jude the time to close return bool
		# first base band, if the sd is too small ,wo need to bigger
		# current the close signal is only band
		if self._now_interest <=0:
			return False
		
		loss_val = self._param_loss_edge
		close_val = self._param_close_edge
		is_band_close = self.is_band_close_time(self._direction,self._lastprice,
											self._now_middle_value,self._now_sd_val,loss_val,close_val
											,self._ris_data,self._limit_rsi_data,self._limit_sd,self._limit_sd_close_edge)
		return is_band_close


	def is_band_open_time(self,direction,lastprice,middle_val,sd_val,open_edge1,open_edge2,limit_sd,limit_sd_open_edge):
		# this is used to judge is time to band open
		if sd_val <=limit_sd:
			open_edge2 = limit_sd_open_edge
		if direction ==LONG:
			upval = middle_val + open_edge2*sd_val
			if lastprice > middle_val+open_edge1*sd_val and lastprice < upval:
				return True
		elif direction ==SHORT:
			downval = middle_val - open_edge2*sd_val
			if lastprice < middle_val - open_edge1*sd_val and lastprice > downval:
				return True
		return False

	def is_band_close_time(self,direction,lastprice,middle_val,sd_val,open_edge,close_edge,cur_rsi_data,limit_rsi_data,limit_sd,limit_sd_close_edge):
		# this is used to judge is time to band is close time
		if sd_val <= limit_sd:
			open_edge = limit_sd_close_edge
		if direction ==LONG:
			profitval = middle_val + close_edge*sd_val
			lossvla = middle_val - open_edge*sd_val
			# 尽量避免损失，如果达到止损条件，即使止损
			if lastprice < lossvla:
				return True
			# 判断止盈条件，大于几倍的band，并且同时rsi大于80，然后可能在加上最大回撤的值。
			# 因为ris是按照这个bar来计算的，所以应该一段时间判断一次，如果没有达到这个段的时间，应该就直接不平仓
			if lastprice > profitval and cur_rsi_data >= limit_rsi_data and cur_rsi_data >=0:
				return True
		elif direction ==SHORT:
			profitval = middle_val - close_edge*sd_val
			lossval = middle_val + open_edge*sd_val
			if lastprice > lossval:
				return True
			ris = 100 - cur_rsi_data
			if lastprice < profitval and ris >= limit_rsi_data and cur_rsi_data >=0 :
				return True
		return False

	def get_total_profit(self):
		return  self._profit
		

def read_data_from_csv(path):
	f = open(path,'rb')
	reader = csv.reader(f)
	ret = []
	for row in reader:
		# obj.get_md_data(row)
		ret.append(row)
	# only get the day data
	return ret

def start_to_run_md(band_obj,data):
	for row in data:
		band_obj.get_md_data(row)

def create_band_obj(data,param_dict):
	file = param_dict["file"]
	for i in xrange(0,2):
		param_dict["direction"] = i
		if i==0:
			# continue
			# param_dict["open_interest_edge"] =1
			band_and_trigger_obj = BandAndTrigger(param_dict)
			print "方向是short的交易情况:"
			file.write("方向是short的交易情况:\n")
			start_to_run_md(band_and_trigger_obj,data)
			profit = band_and_trigger_obj.get_total_profit()
			file.write(str(profit)+"\n")
		else:
			print "方向是long的交易情况："
			# param_dict["open_interest_edge"] =1
			band_and_trigger_obj = BandAndTrigger(param_dict)
			file.write("方向是long的交易情况：:\n")
			start_to_run_md(band_and_trigger_obj,data)
			profit = band_and_trigger_obj.get_total_profit()
			file.write(str(profit)+"\n")



def main(filename):
	path = "../data/"+filename+"_band_data.csv"
	# path = "../zn/"+filename
	csv_data = read_data_from_csv(path)
	path = "../outdata/"+filename+"_trade_wvad.txt"
	file = open(path,"w")

	# 这个是螺纹钢的 tick 1
	param_dict = {"limit_rsi_data":80,"band_open_edge1":0.5,
				"band_open_edge2":1,"band_loss_edge":0.5,"band_profit_edge":3,
				 "file":file
				,"open_interest_edge":0,"spread":95,"volume_open_edge":0
				,"limit_sd":50,"limit_sd_open_edge":1,"limit_sd_close_edge":0.5
				,"limit_wvad":0}
	if "rb" in filename:
		param_dict["volume_open_edge"] =650
		param_dict["limit_sd"] =7
		param_dict["open_interest_edge"] =0
		param_dict["band_open_edge1"] =0
		param_dict["band_open_edge2"] =0.5
		param_dict["band_loss_edge"] =0.5
		param_dict["limit_sd_close_edge"] =1
		param_dict["limit_sd_open_edge"] =2
		param_dict["spread"] =100
		param_dict["limit_wvad"] =10000
	elif "ru" in filename:
		param_dict["volume_open_edge"] =150
		param_dict["limit_sd"] =25
		param_dict["open_interest_edge"] =0
		param_dict["band_open_edge1"] =0
		param_dict["band_open_edge2"] =0.5
		param_dict["band_loss_edge"] =0.5
		param_dict["limit_sd_close_edge"] =1
		param_dict["spread"] =100
	elif "pb" in filename:
		param_dict["volume_open_edge"] =20
		param_dict["limit_sd"] =25
		param_dict["open_interest_edge"] =1
		param_dict["band_open_edge1"] =0
		param_dict["band_open_edge2"] =0.5
		param_dict["band_loss_edge"] =0.5
		param_dict["limit_sd_close_edge"] =1
		param_dict["spread"] =100
	elif "zn" in filename:
		param_dict["volume_open_edge"] =50
		param_dict["limit_sd"] =25
		param_dict["open_interest_edge"] =1
		param_dict["band_open_edge1"] =0
		param_dict["band_open_edge2"] =0.5
		param_dict["band_loss_edge"] =0.5
		param_dict["limit_sd_close_edge"] =1
		param_dict["spread"] =100
	elif "cu" in filename:
		param_dict["volume_open_edge"] =100
		param_dict["band_loss_edge"] =0
		param_dict["limit_sd"] =40
		param_dict["open_interest_edge"] =1
		param_dict["band_open_edge1"] =0
		param_dict["band_open_edge2"] =0.5
		param_dict["band_loss_edge"] =0.5
		param_dict["limit_sd_close_edge"] =1
		param_dict["spread"] =100
	elif "hc" in filename:
		param_dict["volume_open_edge"] =200
		param_dict["band_loss_edge"] =0
		param_dict["limit_sd"] =4
		param_dict["open_interest_edge"] =1
		param_dict["band_open_edge1"] =0
		param_dict["band_open_edge2"] =0.5
		param_dict["band_loss_edge"] =0.5
		param_dict["limit_sd_close_edge"] =1
		param_dict["spread"] =100
	elif "i" in filename and "ni" not in filename:
		param_dict["volume_open_edge"] =1000
		param_dict["limit_sd"] =2
		param_dict["open_interest_edge"] =1
		param_dict["band_open_edge1"] =0.5
		param_dict["band_open_edge2"] =1
		param_dict["band_loss_edge"] =0.5
		param_dict["limit_sd_close_edge"] =1
		param_dict["spread"] =100
	elif "ni" in filename:
		param_dict["volume_open_edge"] =100
		param_dict["band_loss_edge"] =0
		param_dict["limit_sd"] =60
		param_dict["open_interest_edge"] =1
		param_dict["band_open_edge1"] =0
		param_dict["band_open_edge2"] =0.5
		param_dict["band_loss_edge"] =0.5
		param_dict["limit_sd_close_edge"] =1
		param_dict["spread"] =100
	else:
		print "the instrument is not in the parm " + filename
		return
	create_band_obj(csv_data,param_dict)
	file.close()



if __name__=='__main__': 
	# main("ru1709_20170622")
	# data1 = [20170724,20170725,20170726,20170727,20170728]
	# data =[20170731,20170801,20170802,20170803,20170804,20170807,20170808,20170809,20170810]
	# data = data+data1
	# file_dir = "../zn"
	# for root, dirs, files in os.walk(file_dir):
	#     for file in files:
	#     	if "band_data" in file:
	#     		tmp_path = os.path.join(root,file)
	#     		tmp_path = tmp_path.split('/')[2]
	#     		print tmp_path
	#     		main(tmp_path)
	# data = [20170817,20170818,20170821,20170822]
	data = [20170821,20170822,20170823,20170824,20170825,20170828,20170829,20170830]
	# instrumentid = ["rb1801","ru1801","zn1710","pb1710","hc1801","i1801","cu1710","ni1801"]
	instrumentid = ["rb1801"]
	for item in data:
		for instrument in instrumentid:
			path = instrument + "_"+ str(item)
			print path
			main(path)	
		# print WRITETOFILE