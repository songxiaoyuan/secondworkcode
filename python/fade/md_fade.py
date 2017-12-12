# -*- coding:utf8 -*-
import csv
import basic_fun as bf
import os

TIME = 0
LASTPRICE = 1
DIFF_VOLUME = 2
SPREAD = 3
ASKPRICE1 =3
ASKPRICE1VOLUME =4
BIDPRICE1 = 5
BIDPRICE1VOLUME = 6
LONG =1
SHORT =0
class BandAndTrigger(object):
	"""docstring for BandAndTrigger"""
	def __init__(self,param_dic):
		super(BandAndTrigger, self).__init__()
		# self.arg = arg
		self._direction = param_dic["direction"]
		self._limit_diff_volume = param_dic["limit_diff_volume"]
		# now we have the cangwei and the limit cangwei
		self._now_interest = 0
		self._limit_interest = 1

		self._profit = 0
		self._open_lastprice = 0

		self._now_open_signal_tick = 0
		self._has_open_tick = -1

		self._file = param_dic["file"]


	# get the md data ,every line;
	def get_md_data(self,md_array,total_obj):
		# tranfer the string to float
		self._time = md_array[TIME]
		self._lastprice = float(md_array[LASTPRICE])
		self._diff_volume = float(md_array[DIFF_VOLUME])
		self._askprice1 = float(md_array[ASKPRICE1])
		self._askprice1volume = float(md_array[ASKPRICE1VOLUME])
		self._bidprice1 = float(md_array[BIDPRICE1])
		self._bidprice1volume = float(md_array[BIDPRICE1VOLUME])

		open_time = self.is_trend_open_time()
		close_time = self.is_trend_close_time()
		# close_time = False
		
		if open_time and self._now_interest < self._limit_interest:
		# if open_time:
			self._open_lastprice = self._lastprice
			self._now_interest +=1
			self._max_profit = 0
			self._has_open_tick = 0
			mesg= "the time of open: "+self._time + ",the price: " + str(self._lastprice)
			self._file.write(mesg+"\n")
			total_obj._nums +=1
			if self._direction == LONG:
				total_obj._long +=1
			elif self._direction == SHORT:
				total_obj._short +=1
			# print "the diff volume is:" + str(self._now_md_price[VOLUME] - self._pre_md_price[VOLUME])
		# elif close_time:
		elif close_time and self._now_interest >0:
			# print "we need to close"
			if self._direction ==LONG:
				self._profit +=(self._lastprice - self._open_lastprice) 
				if (self._lastprice - self._open_lastprice) >0:
					total_obj._profit_num +=1
				else:
					total_obj._loss_num +=1
			elif self._direction ==SHORT:
				self._profit +=(self._open_lastprice - self._lastprice)

				if (self._open_lastprice - self._lastprice) >0:
					total_obj._profit_num +=1
				else:
					total_obj._loss_num +=1
			self._open_lastprice = 0
			self._max_profit = 0
			self._now_interest = 0
			self._has_open_tick =-1
			mesg= "the time of close:"+self._time+ ",the price: " + str(self._lastprice)
			self._file.write(mesg+"\n")

		return True

	def is_trend_open_time(self):

		is_band_open = self.is_triggersize_open_time(self._direction,self._lastprice,
											self._diff_volume,self._askprice1,self._bidprice1)
		return is_band_open


	def is_trend_close_time(self):
		if self._now_interest <=0:
			return False
		if self._has_open_tick >=0:
			self._has_open_tick +=1
			if self._has_open_tick >=600:
				return True	
		return False


	def is_triggersize_open_time(self,direction,lastprice,diff_volume,askprice1,bidprice1):
		# this is used to judge is time to band open
		if direction ==LONG:
			if diff_volume >= self._limit_diff_volume:
				if lastprice >=askprice1:
					self._now_open_signal_tick +=1
					if self._now_open_signal_tick >=2:
						return True
				else:
					self._now_open_signal_tick = 0
			else:
				self._now_open_signal_tick = 0
		elif direction ==SHORT:
			if diff_volume >= self._limit_diff_volume:
				if lastprice <=bidprice1:
					self._now_open_signal_tick +=1
					if self._now_open_signal_tick >=2:
						return True
				else:
					self._now_open_signal_tick = 0
			else:
				self._now_open_signal_tick = 0
		return False

	def is_band_close_time(self,direction,lastprice,middle_val,sd_val,close_edge):
		# this is used to judge is time to band open
		if direction ==LONG:
			upval = middle_val - close_edge*sd_val
			if lastprice > upval:
				return True
		elif direction ==SHORT:
			downval = middle_val + close_edge*sd_val
			if lastprice < downval:
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

def start_to_run_md(band_obj,data,total_obj):
	for row in data:
		band_obj.get_md_data(row,total_obj)

def create_band_obj(data,param_dict,total_obj):
	file = param_dict["file"]
	for i in xrange(0,2):
		param_dict["direction"] = i
		if i==0:
			# continue
			# param_dict["limit_max_draw_down"] =0
			band_and_trigger_obj = BandAndTrigger(param_dict)
			print "方向是short的交易情况:"
			file.write("方向是short的交易情况:\n")
			start_to_run_md(band_and_trigger_obj,data,total_obj)
			profit = band_and_trigger_obj.get_total_profit()
			total_obj._profit += profit
			file.write(str(profit)+"\n")
		else:
			print "方向是long的交易情况："
			# param_dict["limit_max_draw_down"] =0
			band_and_trigger_obj = BandAndTrigger(param_dict)
			file.write("方向是long的交易情况：:\n")
			start_to_run_md(band_and_trigger_obj,data,total_obj)
			profit = band_and_trigger_obj.get_total_profit()
			total_obj._profit += profit
			file.write(str(profit)+"\n")



def main(filename,total_obj):
	path = "../tmp/"+filename+"_band_data.csv"
	# path = "../zn/"+filename
	csv_data = read_data_from_csv(path)
	path = "../outdata/"+filename+"_trade_Fade.txt"
	file = open(path,"w")

	# 这个是螺纹钢的 tick 1
	param_dict = {"limit_rsi_data":80,"band_open_edge":3,"limit_max_profit":100000,
				 "file":file,"limit_max_draw_down":100000}
	if "rb" in filename:
		param_dict["limit_diff_volume"] =1000
		# param_dict["limit_max_draw_down"] =10
		param_dict["limit_max_profit"] =20
		param_dict["limit_max_loss"] =20
	elif "ru" in filename:
		param_dict["band_open_edge"] =3
		# param_dict["limit_max_draw_down"] =5000
		param_dict["limit_max_profit"] =1000
		param_dict["limit_max_loss"] =200
	elif "pb" in filename:
		param_dict["band_open_edge"] =3
		# param_dict["limit_max_draw_down"] =50
		param_dict["limit_max_profit"] =100
		param_dict["limit_max_loss"] =100
	elif "zn" in filename:
		param_dict["band_open_edge"] =3
		# param_dict["limit_max_draw_down"] =50
		param_dict["limit_max_profit"] =100
		param_dict["limit_max_loss"] =100
	elif "cu" in filename:
		param_dict["band_open_edge"] =3
		# param_dict["limit_max_draw_down"] =100
		param_dict["limit_max_profit"] =200
		param_dict["limit_max_loss"] =200
	elif "hc" in filename:
		param_dict["band_open_edge"] =3
		# param_dict["limit_max_draw_down"] =10
		param_dict["limit_max_profit"] =20
		param_dict["limit_max_loss"] =20
	elif "i" in filename and "ni" not in filename:
		param_dict["band_open_edge"] =3
		# param_dict["limit_max_draw_down"] =5000
		param_dict["limit_max_profit"] =10
		param_dict["limit_max_loss"] =10
	elif "ni" in filename:
		param_dict["band_open_edge"] =3
		# param_dict["limit_max_draw_down"] =100
		param_dict["limit_max_profit"] =200
		param_dict["limit_max_loss"] =100
	elif "al" in filename:
		param_dict["band_open_edge"] =3
		# param_dict["limit_max_draw_down"] =100
		# param_dict["limit_max_profit"] =200
		param_dict["limit_max_loss"] =100
	elif "au" in filename:
		param_dict["band_open_edge"] =3
		# param_dict["limit_max_draw_down"] =100
		# param_dict["limit_max_profit"] =200
		param_dict["limit_max_loss"] =1
	elif "ag" in filename:
		param_dict["band_open_edge"] =3
		# param_dict["limit_max_draw_down"] =100
		# param_dict["limit_max_profit"] =200
		param_dict["limit_max_loss"] =20
	elif "bu" in filename:
		param_dict["band_open_edge"] =3
		# param_dict["limit_max_draw_down"] =100
		# param_dict["limit_max_profit"] =200
		param_dict["limit_max_loss"] =40
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
	data13 =[20171030]
	data = data1+data2+data3+data4+data5+data6+data7+data8+data9+data10+data11+data12+data13

	instrumentid_array = ["rb1801"]
	total_obj = total(0,0)
	for item in data:
		for instrument in instrumentid_array:
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