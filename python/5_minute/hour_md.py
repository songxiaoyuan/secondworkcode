# -*- coding:utf8 -*-
import csv
import basic_fun as bf
import os

TIME = 0
LASTPRICE = 1
MIDDLE_60 = 2
MIDDLE_5 = 3
MIDDLE_1 = 4
LONG =1
SHORT =0

class BandAndTrigger(object):
	"""docstring for BandAndTrigger"""
	def __init__(self,param_dic):
		super(BandAndTrigger, self).__init__()
		# self.arg = arg
		self._direction = param_dic["direction"]

		# now we have the cangwei and the limit cangwei
		self._now_interest = 0
		self._limit_interest = 1
		self._min_lastprice = 1000000
		self._max_lastprice = 0

		self._range = param_dic["range"]

		# band param
		self._param_open_edge1 = param_dic["band_open_edge1"]
		self._param_open_edge2 = param_dic["band_open_edge2"]
		self._param_loss_edge = param_dic["band_loss_edge"]
		self._param_profit_edge =param_dic["band_profit_edge"]	

		self._price_tick = param_dic["price_tick"]

		self._open_status = 0
		self._pre_open_status = 0

		self._quick_exit =0

		self._profit =0

		self._file = param_dic["file"]

	# get the md data ,every line;
	def get_md_data(self,md_array,total_obj):
		# tranfer the string to float
		self._time = md_array[TIME]
		self._lastprice = float(md_array[LASTPRICE])
		self._now_middle_value_60 = float(md_array[MIDDLE_60])
		self._now_middle_value_5 = float(md_array[MIDDLE_5])
		self._now_middle_value_1 = float(md_array[MIDDLE_1])

		if self._quick_exit ==0:
			self._quick_exit = self._lastprice
		self._quick_exit = bf.get_ema_data(self._lastprice,self._quick_exit,20)

		if self._min_lastprice >= self._lastprice:
			self._min_lastprice = self._lastprice
		if self._max_lastprice <= self._lastprice:
			self._max_lastprice = self._lastprice

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
			total_obj._nums +=1
			# print "the diff volume is:" + str(self._now_md_price[VOLUME] - self._pre_md_price[VOLUME])
		# elif close_time:
		elif close_time and self._now_interest >0:
			self._now_interest -=1
			# print "we need to close"
			if self._direction ==LONG:
				total_obj._long +=1
				self._profit +=(self._lastprice - self._open_lastprice)
				if self._profit >0:
					total_obj._profit_num +=1
				else:
					total_obj._loss_num +=1
			elif self._direction ==SHORT:
				total_obj._short +=1
				self._profit +=(self._open_lastprice - self._lastprice)
				if self._profit >0:
					total_obj._profit_num +=1
				else:
					total_obj._loss_num +=1
			self._open_lastprice = 0
			self._open_status = 0
			total_obj._profit += self._profit
			mesg= "the time of close:"+self._time+ ",the price: " + str(self._lastprice)
			self._file.write(mesg+"\n")

		return True


	def is_band_open_time(self,direction,lastprice,middle_val5,bigger_edge1,bigger_edge_increase,middle_val1):
		# this is used to judge is time to band open
		if direction ==LONG:
			upval = middle_val5 + (bigger_edge_increase+bigger_edge1)*self._price_tick
			downval = middle_val5 + bigger_edge1*self._price_tick
			if lastprice < downval:
				self._pre_open_status = 1
				return False
			elif lastprice > upval:
				self._pre_open_status = -1
				return False
			elif lastprice >= downval:
				if self._pre_open_status ==1 and lastprice >= middle_val1:
				# if self._pre_open_status ==1:
					return True
				else:
					return False
		elif direction ==SHORT:
			downval = middle_val5 - (bigger_edge_increase+bigger_edge1)*self._price_tick
			upval = middle_val5 - bigger_edge1*self._price_tick
			if lastprice > upval:
				self._pre_open_status = 1
				return False
			elif lastprice < downval:
				self._pre_open_status = -1
				return False
			elif lastprice <= upval:
				if self._pre_open_status ==1 and lastprice <= middle_val1:
				# if self._pre_open_status ==1:

					return True
				else:
					return False
		return False

	def is_trend_open_time(self):

		hour = int(self._time.split(":")[0])
		minute = int(self._time.split(":")[1])
		if hour ==14 and minute >=58:
			return False
		if hour ==9 and minute <=3:
			return False

		# if (self._max_lastprice - self._min_lastprice) >= 80 * self._price_tick:
		# 	return False

		is_band_open = self.is_band_open_time(self._direction,self._lastprice,
											self._now_middle_value_60,
											self._param_open_edge1,self._param_open_edge2,self._now_middle_value_1)
		return is_band_open

	def is_band_close_time(self,direction,lastprice,middle_val,close_edge,profit_edge):
	# this is used to judge is time to band is close time
		if direction ==LONG:
			loss_val = middle_val - close_edge*self._price_tick
			profit_val = middle_val + profit_edge*self._price_tick
			if lastprice < loss_val:
				return True
			if lastprice > profit_val:
				self._open_status = 1
				# return True
		elif direction ==SHORT:
			loss_val = middle_val + close_edge*self._price_tick
			profit_val = middle_val - profit_edge*self._price_tick
			if lastprice > loss_val:
				return True
			if lastprice < profit_val:
				self._open_status = 1
				# return True
		return False

	def is_middle_cross_close_time(self,direction,lastprice,middle_value_1):
		if direction ==LONG:
			if lastprice <= middle_value_1 and self._open_status ==1:
				return True
		elif direction ==SHORT:
			if lastprice >= middle_value_1 and self._open_status ==1:
				return True
		return False

	def is_triggersize_series_close_time(self,profit_edge):
		if self._direction == LONG:
			profit_val = self._now_middle_value_60 + profit_edge*self._price_tick
			if self._lastprice < profit_val:
				return False
			if self._diff_volume >= self._limit_diff_volume and self._spread<=0:
				self._limit_triggersize_series +=1
				if self._limit_triggersize_series >= self._limit_triggersize_num:
					return True
			else:
				self._limit_triggersize_series = 0
				return False
		elif self._direction == SHORT:
			profit_val = self._now_middle_value_60 - profit_edge*self._price_tick
			if self._lastprice > profit_val:
				return False
			if self._diff_volume >= self._limit_diff_volume and self._spread>=100:
				self._limit_triggersize_series +=1
				if self._limit_triggersize_series >= self._limit_triggersize_num:
					return True
			else:
				self._limit_triggersize_series = 0
				return False
		return False
	def is_trend_close_time(self):
		# this is used to jude the time to close return bool
		# first base band, if the sd is too small ,wo need to bigger
		# current the close signal is only band
		if self._now_interest <=0:
			return False

		tmp_time =self._time.split(":")
		tmp_time_str = tmp_time[0]+":"+tmp_time[1]
		if "14:58" in tmp_time_str:
			return True
		# //base the max loss
		if self._direction == LONG:
			if self._lastprice < self._open_lastprice - 10*self._price_tick:
				return True
		if self._direction == SHORT:
			if self._lastprice > self._open_lastprice + 10 *self._price_tick:
				return True

		if self._direction == LONG:
			if self._lastprice > self._open_lastprice + 30*self._price_tick:
				return True
		if self._direction == SHORT:
			if self._lastprice < self._open_lastprice - 30 *self._price_tick:
				return True
		return False

		# is_band_close = self.is_band_close_time(self._direction,self._lastprice,
		# 									self._now_middle_value_60,self._param_loss_edge,self._param_profit_edge)
		# if is_band_close ==True :
		# 	return True
		# # if self._direction == LONG and self._open_lastprice !=0:
		# # 	profit_val = (self._min_lastprice + self._range* self._price_tick)
		# # 	if self._lastprice >= profit_val:
		# # 		return True
		# # if self._direction == SHORT and self._open_lastprice !=0:
		# # 	profit_val = (self._max_lastprice - self._range* self._price_tick)
		# # 	if self._lastprice <= profit_val:
		# # 		return True

		# is_middle_cross_close = self.is_middle_cross_close_time(self._direction,self._lastprice,self._quick_exit)
		# return is_middle_cross_close

	def get_total_profit(self):
		return  self._profit
		

def start_to_run_md(band_obj,data,total_obj):
	for row in data:
		band_obj.get_md_data(row,total_obj)

def create_band_obj(data,param_dict,total_obj):
	file = param_dict["file"]
	for i in xrange(0,2):
		param_dict["direction"] = i
		if i==0:
			# continue
			# param_dict["open_interest_edge"] =1
			band_and_trigger_obj = BandAndTrigger(param_dict)
			print "方向是short的交易情况:"
			file.write("方向是short的交易情况:\n")
			start_to_run_md(band_and_trigger_obj,data,total_obj)
			profit = band_and_trigger_obj.get_total_profit()
			total_obj._profit += profit
			file.write(str(profit)+"\n")
		else:
			print "方向是long的交易情况："
			# param_dict["open_interest_edge"] =1
			band_and_trigger_obj = BandAndTrigger(param_dict)
			file.write("方向是long的交易情况：:\n")
			start_to_run_md(band_and_trigger_obj,data,total_obj)
			profit = band_and_trigger_obj.get_total_profit()
			total_obj._profit += profit
			file.write(str(profit)+"\n")


def main(filename,total_obj):
	# path = "../create_data/"+filename+"_band_data.csv"
	path = "../tmp/"+filename+"_band_data.csv"
	# path = "../everydayoutdata/"+filename+"_band_data.csv"
	csv_data = bf.read_data_from_csv(path)
	path = "../outdata/"+filename+"_trade_limit_time_volume.txt"
	file = open(path,"w")

	# 这个是螺纹钢的 tick 1
	param_dict = {"band_loss_edge":3,"band_profit_edge":40,"band_open_edge1":3,
				"band_open_edge2":2,"file":file}
	if "rb" in filename:
		param_dict["price_tick"] = 1
		param_dict["range"] = 80
		param_dict["band_loss_edge"] = 7
	elif "ru" in filename:
		param_dict["price_tick"] = 5
		param_dict["band_open_edge1"] = 0
		param_dict["band_open_edge2"] = 50
		param_dict["band_loss_edge"] = 25
		param_dict["max_loss"] =50
		param_dict["max_profit"] = 150
	elif "pb" in filename:
		param_dict["volume_open_edge"] =20
		param_dict["band_open_edge1"] = 0
		param_dict["band_open_edge2"] = 50
		param_dict["band_loss_edge"] = 25
		param_dict["max_loss"] =50
		param_dict["max_profit"] = 150
	elif "zn" in filename:
		param_dict["price_tick"] = 5
		param_dict["range"] = 80
		param_dict["band_loss_edge"] = 5
	elif "cu" in filename:
		param_dict["price_tick"] = 10
		param_dict["range"] = 60
		param_dict["band_loss_edge"] = 5
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
		param_dict["volume_open_edge"] =200
		param_dict["band_open_edge1"] = 0
		param_dict["band_open_edge2"] = 100
		param_dict["band_loss_edge"] = 50
	elif "al" in filename:
		param_dict["volume_open_edge"] =100
		param_dict["band_open_edge1"] = 0
		param_dict["band_open_edge2"] = 50
		param_dict["band_loss_edge"] = 25
		param_dict["max_loss"] = 50
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
		param_dict["volume_open_edge"] =600
		param_dict["band_open_edge1"] = 0
		param_dict["band_open_edge2"] = 10
		param_dict["band_loss_edge"] = 5
		param_dict["max_loss"] =10
		param_dict["max_profit"] = 30
	elif "j" in filename and "m" not in filename:
		param_dict["volume_open_edge"] =100
		param_dict["band_open_edge1"] = 0
		param_dict["band_open_edge2"] = 5
		param_dict["band_loss_edge"] = 2.5
		param_dict["max_loss"] =5
		param_dict["max_profit"] = 20
	elif "jm" in filename:
		param_dict["volume_open_edge"] =100
		param_dict["band_open_edge1"] = 0
		param_dict["band_open_edge2"] = 5
		param_dict["band_loss_edge"] = 2.5
		param_dict["max_loss"] =5
		param_dict["max_profit"] = 20
	elif "pp" in filename:
		param_dict["volume_open_edge"] =80
		param_dict["band_open_edge1"] = 0
		param_dict["band_open_edge2"] = 10
		param_dict["band_loss_edge"] = 5
		param_dict["max_loss"] =10
		param_dict["max_profit"] = 30
	elif "v" in filename:
		param_dict["volume_open_edge"] =80
		param_dict["band_open_edge1"] = 0
		param_dict["band_open_edge2"] = 50
		param_dict["band_loss_edge"] = 25
		param_dict["max_loss"] =25
		param_dict["max_profit"] = 100
	elif "y" in filename:
		param_dict["volume_open_edge"] =100
		param_dict["band_open_edge1"] = 0
		param_dict["band_open_edge2"] = 20
		param_dict["band_loss_edge"] = 10
		param_dict["max_loss"] =10
		param_dict["max_profit"] = 140
	elif "p" in filename and "pp" not in filename:
		param_dict["volume_open_edge"] =100
		param_dict["band_open_edge1"] = 0
		param_dict["band_open_edge2"] = 20
		param_dict["band_loss_edge"] = 10
		param_dict["max_loss"] =20
		param_dict["max_profit"] = 100
	elif "c1801" in filename:
		param_dict["volume_open_edge"] =40
		param_dict["band_open_edge1"] = 0
		param_dict["band_open_edge2"] = 5
		param_dict["band_loss_edge"] = 3
		param_dict["max_loss"] =5
		param_dict["max_profit"] = 30
	elif "a1801" in filename:
		param_dict["volume_open_edge"] =40
		param_dict["band_open_edge1"] = 0
		param_dict["band_open_edge2"] = 10
		param_dict["band_loss_edge"] = 3
		param_dict["max_loss"] =5
		param_dict["max_profit"] = 30
	elif "m1801" in filename:
		param_dict["volume_open_edge"] =100
		param_dict["band_open_edge1"] = 0
		param_dict["band_open_edge2"] = 10
		param_dict["band_loss_edge"] = 3
		param_dict["max_loss"] =5
		param_dict["max_profit"] = 20
	elif "jd1801" in filename:
		param_dict["volume_open_edge"] =30
		param_dict["band_open_edge1"] = 0
		param_dict["band_open_edge2"] = 10
		param_dict["band_loss_edge"] = 5
		param_dict["max_loss"] =10
		param_dict["max_profit"] = 20
	else:
		print "the instrument is not in the parm " + filename
		return
	create_band_obj(csv_data,param_dict,total_obj)
	file.close()


class total(object):
	"""docstring for total"""
	def __init__(self, profit,nums):
		super(total, self).__init__()
		self._profit = profit
		self._nums = nums
		self._long = 0
		self._short = 0
		self._profit_num = 0
		self._loss_num = 0

if __name__=='__main__': 
	# data1 =[20170801,20170802,20170803,20170804]
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
	data13 =[20171030,20171031,20171101,20171102,20171103]
	data14 = [20171106,20171107,20171108,20171109,20171110]
	data15 = [20171113,20171114,20171115,20171116,20171117]
	data16 = [20171120,20171121,20171122,20171123,20171124]
	# data = data1+data2+data3+data4+data5+data6+data7+data8+data9+data10+data11+data12+data13+data14+data15+data16
	data = data2+data3+data4+data5+data6+data7+data8+data9+data10+data11+data12+data13+data14+data15+data16

	# data =[20171024]
	# instrumentid = ["rb1801","ru1801","zn1801","pb1712"]
	instrumentid = ["zn1801"]
	total_obj = total(0,0)
	for item in data:
		for instrument in instrumentid:
			# path = instrument
			path = instrument + "_"+ str(item)
			print path
			main(path,total_obj)	
		# print WRITETOFILE

	print total_obj._nums
	print total_obj._profit
	print total_obj._long
	print total_obj._short
	print total_obj._profit_num
	print total_obj._loss_num