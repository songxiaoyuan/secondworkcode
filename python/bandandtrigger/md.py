# -*- coding:utf8 -*-
import csv
import basic_fun as bf

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
		self._param_open_edge = param_dic["band_open_edge"]
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

		self._file = param_dic["file"]


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
		self._ema_diff_volume = self._diff_volume
		self._ema_diff_openinterest = self._diff_openinterest
		self._ema_spread = self._spread



		open_time = self.is_trend_open_time()
		close_time = self.is_trend_close_time()
		# close_time = False
		
		if open_time and self._now_interest < self._limit_interest:
		# if open_time:
			self._now_interest +=1
			# print "we start to open"
			self._open_lastprice = self._lastprice
			mesg= "the time of open: "+self._time + ",the price: " + str(self._lastprice)
			mesg1 = "the diff volume: "+str(self._ema_diff_volume)+", the interest: " + str(self._ema_diff_openinterest) + ", the spread: "+ str(self._ema_spread)
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

		open_val = self._param_open_edge
		is_band_open = bf.is_band_open_time(self._direction,self._lastprice,
											self._now_middle_value,self._now_sd_val,open_val,
											self._limit_sd,self._limit_sd_open_edge)
		# return is_band_open
		if is_band_open ==False:
			return False
		# return True
		is_trigger_open = self.is_trigger_size_open_time(self._direction,self._param_volume_open_edge,
													self._param_open_interest_edge,self._param_spread)
		return is_trigger_open

	def is_trigger_size_open_time(self,direction,volume_open_edge,
								openinterest_edge,spread_edge):

		if self._ema_diff_volume < volume_open_edge:
			return False
		if openinterest_edge != 0 and self._ema_diff_openinterest <= openinterest_edge:
			return False
		if self._direction ==SHORT:
			self._ema_spread = 100 - self._ema_spread
		if self._ema_spread < spread_edge:
			return False
		return True


	def is_trend_close_time(self):
		# this is used to jude the time to close return bool
		# first base band, if the sd is too small ,wo need to bigger
		# current the close signal is only band
		if self._now_interest <=0:
			return False
		
		loss_val = self._param_loss_edge
		close_val = self._param_close_edge
		is_band_close = bf.is_band_close_time(self._direction,self._lastprice,
											self._now_middle_value,self._now_sd_val,loss_val,close_val
											,self._ris_data,self._limit_rsi_data,self._limit_sd,self._limit_sd_close_edge)
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
		band_and_trigger_obj = BandAndTrigger(param_dict)
		if i==0:
			# continue
			print "方向是short的交易情况:"
			file.write("方向是short的交易情况:\n")
			start_to_run_md(band_and_trigger_obj,data)
			profit = band_and_trigger_obj.get_total_profit()
			file.write(str(profit)+"\n")
		else:
			print "方向是long的交易情况："
			file.write("方向是long的交易情况：:\n")
			start_to_run_md(band_and_trigger_obj,data)
			profit = band_and_trigger_obj.get_total_profit()
			file.write(str(profit)+"\n")



def main(filename):
	path = "../data/"+filename+"_band_data.csv"
	csv_data = read_data_from_csv(path)
	path = "../outdata/"+filename+"_trade.txt"
	file = open(path,"w")

	# 这个是螺纹钢的 tick 1
	param_dict = {"limit_rsi_data":80,
				"band_open_edge":0.5,"band_loss_edge":1,"band_profit_edge":3,
				 "file":file
				,"open_interest_edge":0,"spread":100,"volume_open_edge":0
				,"limit_sd":4,"limit_sd_open_edge":1,"limit_sd_close_edge":3}
	if "rb" in filename:
		param_dict["volume_open_edge"] =900
		param_dict["limit_sd"] =5
	elif "ru" in filename:
		param_dict["volume_open_edge"] =100
		param_dict["limit_sd"] =20
	elif "pb" in filename:
		param_dict["volume_open_edge"] =20
		param_dict["limit_sd"] =20
	elif "zn" in filename:
		param_dict["volume_open_edge"] =100
		param_dict["limit_sd"] =25
	elif "cu" in filename:
		param_dict["volume_open_edge"] =100
		param_dict["band_loss_edge"] =0.5
		param_dict["limit_sd"] =40
	elif "i" in filename:
		param_dict["volume_open_edge"] =900
		param_dict["band_loss_edge"] =0.5
		param_dict["limit_sd"] =2
	else:
		print "the instrument is not in the parm " + filename
		return
	create_band_obj(csv_data,param_dict)
	file.close()



if __name__=='__main__': 
	# main("ru1709_20170622")
	# data1 = [20170630,20170629,20170628,20170627,20170623,20170622,20170621,20170620,20170619,20170616]
	# data =[20170711,20170712,20170713,20170714,20170717,20170718,20170719,20170720,20170721,20170724,20170725,20170726,20170727,20170728]
	# data = data1+data2
	data = [20170808]
	# instrumentid = ["rb1710","ru1801","zn1709","pb1709"]
	instrumentid = ["cu1710"]
	for item in data:
		for instrument in instrumentid:
			path = instrument + "_"+ str(item)
			print path
			main(path)	
		# print WRITETOFILE