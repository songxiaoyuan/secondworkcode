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
LONG =1
SHORT =0

class BandAndSeries(object):
	"""docstring for BandAndSeries"""
	def __init__(self,param_dic):
		super(BandAndSeries, self).__init__()
		# self.arg = arg
		self._direction = param_dic["direction"]
		self._limit_rsi_data = param_dic["limit_rsi_data"]

		self._moving_theo = "EMA"
		# now we have the cangwei and the limit cangwei
		self._now_interest = 0
		self._limit_interest = 1
		self._profit = 0

		# band param
		self._param_close_edge =param_dic["band_profit_edge"]	

		self._limit_sd = param_dic["limit_sd"]
		self._limit_sd_close_edge = param_dic["limit_sd_close_edge"]	

		# series param
		self._limit_series_lastprice = param_dic["limit_series_lastprice"]
		self._limit_multiple = param_dic["limit_multiple"]
		self._limit_large_period = param_dic["limit_large_period"]
		self._limit_bar_volume_tick = param_dic["limit_bar_volume_tick"]
		self._diff_volume_array = []
		self._lastprice_array = []
		self._tmp_sum_diff_volume = 0
		self._now_bar_volume_tick = 0

		self._rsi_data = 0
		self._tmp_profit = 0
		self._open_lastprice = 0
		self._ris_status = 0
		self._limit_max_loss = param_dic["max_loss"]
		self._limit_max_profit = param_dic["max_profit"]

		self._has_interest_tick = 0
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
		self._rsi_data = float(md_array[RSI])
		self._diff_volume = float(md_array[DIFF_VOLUME])

		self._tmp_sum_diff_volume += self._diff_volume
		self._now_bar_volume_tick +=1
		if self._now_bar_volume_tick >= self._limit_bar_volume_tick:
			self._diff_volume_array.append(self._tmp_sum_diff_volume)
			self._lastprice_array.append(self._lastprice)
			self._tmp_sum_diff_volume = 0
			self._now_bar_volume_tick = 0


		open_time = self.is_trend_open_time()
		close_time = self.is_trend_close_time()
		# close_time = False
		
		if open_time and self._now_interest < self._limit_interest:
		# if open_time:
			self._now_interest +=1
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

	def is_trend_open_time(self):
		# "'this is used to jude the time used to open return bool'"
		# first base the sd,find is time to open band 
		# is_band_open = bf.is_band_open_time(self._direction,self._lastprice,
		# 									self._now_middle_value,self._now_sd_val,self._param_open_edge1,self._param_open_edge2,
		# 									self._limit_sd,self._limit_sd_open_edge)
		# # return is_band_open
		# if is_band_open ==False:
		# 	return False

		is_diff_volume_open = bf.is_diff_volume_open_time(self._tmp_sum_diff_volume,self._diff_volume_array,
												self._limit_multiple,self._limit_large_period)

		# return is_diff_volume_open
		if is_diff_volume_open ==False:
			return False

		# is_series_open = bf.is_lastprice_series_open_time(self._direction,self._series_lastprice,self._limit_series_lastprice)
		is_lastprice_open = bf.is_lastprice_open_time(self._direction,self._lastprice,self._lastprice_array,self._limit_large_period)

		return is_lastprice_open
		# return is_series_open

	def is_trend_close_time(self):
		# this is used to jude the time to close return bool
		# first base band, if the sd is too small ,wo need to bigger
		# current the close signal is only band
		if self._now_interest <=0:
			return False

		# exit when profit
		close_val = self._param_close_edge
		if self._now_sd_val < self._limit_sd:
			close_val = self._limit_sd_close_edge
		is_band_close = bf.is_band_close_time(self._direction,self._lastprice,
											self._now_middle_value,self._now_sd_val,close_val
											,self._rsi_data,self._limit_rsi_data)
		if is_band_close == True:
			return True


		# base the max loss to leave and close
		if self._open_lastprice != 0:
			if self._direction ==LONG:
				tmp = self._lastprice - self._open_lastprice
			elif self._direction ==SHORT:
				tmp = self._open_lastprice - self._lastprice
			if tmp <0 and ((0 - tmp) > self._limit_max_loss):
				return True
			# if tmp > self._limit_max_profit:
			# 	return True
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
			band_and_trigger_obj = BandAndSeries(param_dict)
			print "方向是short的交易情况:"
			file.write("方向是short的交易情况:\n")
			start_to_run_md(band_and_trigger_obj,data)
			profit = band_and_trigger_obj.get_total_profit()
			file.write(str(profit)+"\n")
		else:
			print "方向是long的交易情况："
			# param_dict["open_interest_edge"] =1
			band_and_trigger_obj = BandAndSeries(param_dict)
			file.write("方向是long的交易情况：:\n")
			start_to_run_md(band_and_trigger_obj,data)
			profit = band_and_trigger_obj.get_total_profit()
			file.write(str(profit)+"\n")



def main(filename):
	path = "../create_data/"+filename+"_band_data.csv"
	# path = "../zn/"+filename
	csv_data = read_data_from_csv(path)
	path = "../outdata/"+filename+"_trade_series_noband.txt"
	file = open(path,"w")

	param_dict = {"limit_rsi_data":80,"band_profit_edge":3,
				"limit_bar_volume_tick":20,"limit_series_lastprice":5,"limit_sd_close_edge":1,
				"file":file,}
	if "rb" in filename:
		param_dict["limit_sd"] =10
		param_dict["limit_sd_close_edge"] =5
		param_dict["limit_multiple"] =3
		param_dict["limit_large_period"] =5
		param_dict["max_loss"] =10
		param_dict["max_profit"] =2000
	elif "ru" in filename:
		param_dict["limit_sd"] =25
		param_dict["band_open_edge1"] =0
		param_dict["band_open_edge2"] =0.5
		param_dict["band_loss_edge"] =0.5
		param_dict["limit_sd_close_edge"] =1
		param_dict["limit_sd_open_edge"] =2
		param_dict["limit_multiple"] =3
		param_dict["limit_large_period"] =5
		param_dict["max_loss"] =50
		param_dict["max_profit"] =20
	elif "pb" in filename:
		param_dict["volume_open_edge"] =30
		param_dict["limit_sd"] =25
		param_dict["open_interest_edge"] =0
		param_dict["band_open_edge1"] =0
		param_dict["band_open_edge2"] =0.5
		param_dict["band_loss_edge"] =0.5
		param_dict["limit_sd_close_edge"] =1
		param_dict["limit_sd_open_edge"] =2
		param_dict["spread"] =100
		param_dict["limit_wvad"] =200
	elif "zn" in filename:
		param_dict["volume_open_edge"] =50
		param_dict["limit_sd"] =50
		param_dict["open_interest_edge"] =0
		param_dict["band_open_edge1"] =0
		param_dict["band_open_edge2"] =0.5
		param_dict["band_loss_edge"] =0.5
		param_dict["limit_sd_close_edge"] =1
		param_dict["limit_sd_open_edge"] =2
		param_dict["spread"] =100
		param_dict["limit_wvad"] =500
	elif "cu" in filename:
		param_dict["volume_open_edge"] =100
		param_dict["limit_sd"] =40
		param_dict["open_interest_edge"] =0
		param_dict["band_open_edge1"] =0
		param_dict["band_open_edge2"] =0.5
		param_dict["band_loss_edge"] =0.5
		param_dict["limit_sd_close_edge"] =1
		param_dict["limit_sd_open_edge"] =2
		param_dict["spread"] =100
		param_dict["limit_wvad"] =600
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
	# data = [20171012]
	data =[20171009,20171010,20171011,20171012,20171013]
	# instrumentid = ["ru1801","rb1801","zn1710","pb1710","cu1710","hc1801","i1801","ni1801","al1710","au1712","ag1712","bu1712"]
	instrumentid = ["rb1801"]
	for item in data:
		for instrument in instrumentid:
			path = instrument + "_"+ str(item)
			print path
			main(path)	
		# print WRITETOFILE