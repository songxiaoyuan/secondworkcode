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
		self._limit_diff_volume = param_dic["limit_diff_volume"]
		# now we have the cangwei and the limit cangwei
		self._now_interest = 0
		self._limit_interest = 1
		self._direction = 0

		self._profit = 0
		self._open_lastprice = 0

		self._now_open_signal_tick = 0
		self._has_open_tick = -1
		self._diff_volume_array = []

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
		self._diff_volume_array.append(self._diff_volume)

		open_time = self.is_trend_open_time()
		close_time = self.is_trend_close_time()
		# close_time = False
		
		if open_time and self._now_interest < self._limit_interest:
		# if open_time:
			self._open_lastprice = self._lastprice
			self._now_interest +=1
			self._has_open_tick = 0
			mesg= "the time of open: "+self._time + ",the price: " + str(self._lastprice)
			self._file.write(mesg+"\n")
			total_obj._nums +=1
			# print "the diff volume is:" + str(self._now_md_price[VOLUME] - self._pre_md_price[VOLUME])
		# elif close_time:
		elif close_time and self._now_interest >0:
			self._now_interest -=1
			if self._lastprice - self._open_lastprice >0:
				total_obj._long +=1
			else:
				total_obj._short +=1
			self._has_open_tick =-1
			mesg= "the time of close:"+self._time+ ",the price: " + str(self._lastprice)
			self._file.write(mesg+"\n")

		return True

	def is_trend_open_time(self):

		hour = int(self._time.split(":")[0])
		minute = int(self._time.split(":")[1])
		if hour ==14 and minute >=58:
			return False
		if hour ==9 and minute <=5:
			return False
		is_band_open = self.is_triggersize_open_time(self._direction,self._lastprice,
											self._diff_volume_array)
		return is_band_open


	def is_trend_close_time(self):
		if self._now_interest <=0:
			return False

		hour = int(self._time.split(":")[0])
		minute = int(self._time.split(":")[1])
		if hour ==14 and minute >=58:
			return True
		if self._has_open_tick >=0:
			self._has_open_tick +=1
			if self._has_open_tick >=600:
				return True	
		return False


	def is_triggersize_open_time(self,direction,lastprice,diff_volume_array):
		# this is used to judge is time to band open
		l = len(diff_volume_array)
		begin = l - 8
		if begin <0:
			begin = 0
		bigger = 0
		for x in xrange(begin,l):
			tmp = self._diff_volume_array[x]
			if tmp > self._limit_diff_volume:
				bigger +=1
		if bigger >=5:
			return True
		else:
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
			continue
			# param_dict["limit_max_draw_down"] =0
			band_and_trigger_obj = BandAndTrigger(param_dict)
			print "方向是short的交易情况:"
			file.write("方向是short的交易情况:\n")
			start_to_run_md(band_and_trigger_obj,data,total_obj)
			profit = band_and_trigger_obj.get_total_profit()
			total_obj._profit += profit
			file.write(str(profit)+"\n")
		else:
			# print "方向是long的交易情况："
			# param_dict["limit_max_draw_down"] =0
			band_and_trigger_obj = BandAndTrigger(param_dict)
			file.write("方向是long的交易情况：:\n")
			start_to_run_md(band_and_trigger_obj,data,total_obj)
			profit = band_and_trigger_obj.get_total_profit()
			total_obj._profit += profit
			file.write(str(profit)+"\n")



def main(filename,total_obj):
	# path = "../tmp/"+filename+"_band_data.csv"
	path = "../tmp/"+filename
	csv_data = read_data_from_csv(path)
	path = "../outdata/"+filename+"_trade_Fade.txt"
	file = open(path,"w")
	total_obj._name = filename
	# 这个是螺纹钢的 tick 1
	param_dict = {"limit_rsi_data":80,"band_open_edge":3,"limit_max_profit":100000,
				 "file":file,"limit_max_draw_down":100000}
	if "rb" in filename:
		param_dict["limit_diff_volume"] =1500
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
		param_dict["limit_diff_volume"] =150
		# param_dict["limit_max_draw_down"] =50
		param_dict["limit_max_profit"] =100
		param_dict["limit_max_loss"] =100
	elif "cu" in filename:
		param_dict["limit_diff_volume"] =150
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
		self._open = 0
		self._close = 0
		self._name = "0"

if __name__=='__main__': 
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
	# data13 =[20171030,20171031,20171101,20171102,20171103]
	# data14 = [20171106,20171107,20171108,20171109,20171110]
	# data15 = [20171113,20171114,20171115,20171116,20171117]
	# data16 = [20171120,20171121,20171122,20171123,20171124]
	# data = data1+data2+data3+data4+data5+data6+data7+data8+data9+data10+data11+data12+data13+data14+data15+data16

	total_obj = total(0,0)
	total_path = "../tmp/"
	instrumentid = "rb"
	for file in os.listdir(total_path):
		tmp =  os.path.join(total_path,file)
		if os.path.isdir(tmp):
			print "this is dir"
		else:
			if instrumentid in file:
				# print file
				main(file,total_obj)
		# print WRITETOFILE

	print total_obj._nums
	print total_obj._profit
	print total_obj._long
	print total_obj._short
	print total_obj._profit_num
	print total_obj._loss_num


