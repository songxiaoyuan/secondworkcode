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
LONG =1
SHORT =0

class BandAndTrigger(object):
	"""docstring for BandAndTrigger"""
	def __init__(self,param_dic):
		super(BandAndTrigger, self).__init__()
		# self.arg = arg
		self._direction = param_dic["direction"]
		self._limit_rsi_data = param_dic["limit_rsi_data"]

		# now we have the cangwei and the limit cangwei
		self._now_interest = 0
		self._limit_interest = 1

		self._profit = 0

		# band param
		self._param_open_edge1 = param_dic["band_open_edge1"]
		self._param_open_edge2 = param_dic["band_open_edge2"]
		self._param_loss_edge = param_dic["band_loss_edge"]
		self._param_close_edge =param_dic["band_profit_edge"]
		self._limit_sd = param_dic["limit_sd"]
		self._limit_sd_close_edge = param_dic["limit_sd_close_edge"]		

		# trigger param
		self._param_volume_open_edge = param_dic["volume_open_edge"]
		self._param_open_interest_edge = param_dic["open_interest_edge"]
		self._param_spread = param_dic["spread"]

		self._now_interest = 0
		self._limit_interest = 1

		self._current_hour =0
		self._has_open = 0
		self._limit_open =1

		self._file = param_dic["file"]


	def __del__(self):
		print "this is the over function"
		# bf.write_config_info(self._pre_ema_val,self._lastprice_array
		# 	,self._rsi_array,self._rsi_period,self._lastprice,self._config_file)

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
		# print self._time
		self._spread = float(md_array[SPREAD])


		open_time = self.is_trend_open_time()
		close_time = self.is_trend_close_time()
		# close_time = False
		
		if open_time and self._now_interest < self._limit_interest:
		# if open_time:
			self._now_interest +=1
			# self._has_open +=1
			# print "we start to open"
			self._open_lastprice = self._lastprice
			mesg= "the time of open: "+self._time + ",the price: " + str(self._lastprice)
			self._file.write(mesg+"\n")
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

	
	def is_time_open_time(self):
		hour = self._time.split(':')[0]
		hour = int(hour)
		if hour == self._current_hour:
			if self._has_open >= self._limit_open:
				return False
			else:
				self._has_open +=1
				return True
		else:
			self._current_hour = hour
			if hour != 13:
				self._has_open = 0
		return False

	def is_trend_open_time(self):

		is_band_open = bf.is_band_open_time(self._direction,self._lastprice,
											self._now_middle_value,
											self._param_open_edge1,self._param_open_edge2)
		# return is_band_open
		if is_band_open ==False:
			return False

		if self._diff_volume < self._param_volume_open_edge:
			return False
		if self._diff_openinterest != 0 and self._diff_openinterest < self._param_open_interest_edge:
			return False
		# return True
		if self._direction ==LONG:
			if self._spread <self._param_spread:
				return False
		elif self._direction ==SHORT:
			tmp = 100 - self._spread
			if tmp < self._param_spread:
				return False
		is_time_open = self.is_time_open_time()
		return is_time_open


	def is_trend_close_time(self):
		# this is used to jude the time to close return bool
		# first base band, if the sd is too small ,wo need to bigger
		# current the close signal is only band
		if self._now_interest <=0:
			return False

		# base the max draw down
		# 达到最大盈利之后，或者最大亏损之后，就开始平仓。这个是系统自带的。
		# if self._direction ==LONG:
		# 	tmp_profit = self._lastprice - self._open_lastprice
		# elif self._direction ==SHORT:
		# 	tmp_profit = self._open_lastprice - self._lastprice
		# else:
		# 	return False
		# if tmp_profit < (0 - self._limit_max_loss) or tmp_profit > self._limit_max_profit:
		# 	# print "the profit is bigger or loss"
		# 	return True
		

		loss_val = self._param_loss_edge
		close_val = self._param_close_edge
		if self._now_sd_val < self._limit_sd:
			close_val = self._limit_sd_close_edge
		is_band_close = bf.is_band_close_time(self._direction,self._lastprice,
											self._now_middle_value,self._now_sd_val,loss_val,close_val
											,self._ris_data,self._limit_rsi_data)
		return is_band_close

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
	path = "../create_data/"+filename+"_band_data.csv"
	# path = "../zn/"+filename
	csv_data = read_data_from_csv(path)
	path = "../outdata/"+filename+"_trade_limit_time.txt"
	file = open(path,"w")

	# 这个是螺纹钢的 tick 1
	param_dict = {"limit_rsi_data":90,"band_open_edge1":0.5,"band_open_edge2":1,
				"band_loss_edge":0,"band_profit_edge":3,
				"limit_sd":50,"limit_sd_close_edge":5,
				"open_interest_edge":0,"spread":80,"volume_open_edge":0,
				"file":file}
	if "rb" in filename:
		param_dict["volume_open_edge"] =200
		param_dict["limit_sd"] =10
		param_dict["band_open_edge1"] = 5
		param_dict["band_open_edge2"] = 7
	elif "ru" in filename:
		param_dict["volume_open_edge"] =20
		param_dict["limit_sd"] =10
		param_dict["band_open_edge1"] = 25
		param_dict["band_open_edge2"] = 35
	elif "pb" in filename:
		param_dict["volume_open_edge"] =10
		param_dict["limit_sd"] =10
		param_dict["band_open_edge1"] = 25
		param_dict["band_open_edge2"] = 35
	elif "zn" in filename:
		param_dict["volume_open_edge"] =10
		param_dict["limit_sd"] =10
		param_dict["band_open_edge1"] = 25
		param_dict["band_open_edge2"] = 35
	elif "cu" in filename:
		param_dict["volume_open_edge"] =20
		param_dict["limit_sd"] =10
		param_dict["band_open_edge1"] = 25
		param_dict["band_open_edge2"] = 35
	elif "hc" in filename:
		param_dict["volume_open_edge"] =400
		param_dict["band_open_edge1"] =0
		param_dict["band_open_edge2"] =0.5
		param_dict["band_loss_edge"] =0.5
		param_dict["limit_sd"] =4
		param_dict["open_interest_edge"] =0
		param_dict["limit_sd_close_edge"] =1
		param_dict["limit_sd_open_edge"] =2
		param_dict["spread"] =90
		param_dict["limit_wvad"] =2000
	elif "i" in filename and "ni" not in filename:
		param_dict["volume_open_edge"] =900
		param_dict["limit_sd"] =4
		param_dict["open_interest_edge"] =0
		param_dict["band_open_edge1"] =0
		param_dict["band_open_edge2"] =0.5
		param_dict["band_loss_edge"] =0.5
		param_dict["limit_sd_close_edge"] =1
		param_dict["limit_sd_open_edge"] =2
		param_dict["spread"] =100
		param_dict["limit_wvad"] =5000
	elif "ni" in filename:
		param_dict["volume_open_edge"] =100
		param_dict["limit_sd"] =60
		param_dict["open_interest_edge"] =0
		param_dict["band_open_edge1"] =0
		param_dict["band_open_edge2"] =0.5
		param_dict["band_loss_edge"] =0.5
		param_dict["limit_sd_close_edge"] =1
		param_dict["limit_sd_open_edge"] =2
		param_dict["spread"] =100
		param_dict["limit_wvad"] =2000
	elif "al" in filename:
		param_dict["volume_open_edge"] =100
		param_dict["limit_sd"] =30
		param_dict["open_interest_edge"] =0
		param_dict["band_open_edge1"] =0
		param_dict["band_open_edge2"] =0.5
		param_dict["band_loss_edge"] =0.5
		param_dict["limit_sd_close_edge"] =1
		param_dict["limit_sd_open_edge"] =2
		param_dict["spread"] =100
		param_dict["limit_wvad"] =500
	elif "au" in filename:
		param_dict["volume_open_edge"] =20
		param_dict["limit_sd"] =0.3
		param_dict["open_interest_edge"] =0
		param_dict["band_open_edge1"] =0
		param_dict["band_open_edge2"] =0.5
		param_dict["band_loss_edge"] =0.5
		param_dict["limit_sd_close_edge"] =1
		param_dict["spread"] =100
		param_dict["limit_wvad"] =2000
	elif "ag" in filename:
		param_dict["volume_open_edge"] =300
		param_dict["limit_sd"] =6
		param_dict["open_interest_edge"] =0
		param_dict["band_open_edge1"] =0
		param_dict["band_open_edge2"] =0.5
		param_dict["band_loss_edge"] =0.5
		param_dict["limit_sd_close_edge"] =1
		param_dict["spread"] =100
		param_dict["limit_wvad"] =2000
	elif "bu" in filename:
		param_dict["volume_open_edge"] =500
		param_dict["limit_sd"] =12
		param_dict["open_interest_edge"] =0
		param_dict["band_open_edge1"] =0
		param_dict["band_open_edge2"] =0.5
		param_dict["band_loss_edge"] =0.5
		param_dict["limit_sd_close_edge"] =1
		param_dict["limit_sd_open_edge"] =2
		param_dict["spread"] =100
		param_dict["limit_wvad"] =2200
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
	data1 =[20170918,20170919,20170920,20170921,20170922]
	data2 =[20170925,20170926,20170927,20170928,20170929]
	data3 =[20171009,20171010,20171011,20171012,20171013]
	data4 =[20171016,20171017,20171018,20171019,20171020]
	data = data1 + data2 + data3 +data4
	# data = [20171020]
	# instrumentid = ["ru1801","rb1801","zn1710","pb1710","cu1710","hc1801","i1801","ni1801","al1710","au1712","ag1712","bu1712"]
	instrumentid = ["rb1801","zn1712","ru1801"]
	for item in data:
		for instrument in instrumentid:
			path = instrument + "_"+ str(item)
			print path
			main(path)	
		# print WRITETOFILE