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
AVG_SUM = 12
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

		self._limit_max_draw_down = param_dic["limit_max_draw_down"]
		self._limit_max_loss = param_dic["limit_max_loss"]
		self._limit_max_profit = param_dic["limit_max_profit"]

		self._profit = 0
		self._max_profit = 0
		self._open_lastprice = 0

		# band param
		self._param_open_edge = param_dic["band_open_edge"]		

		# trigger param

		self._ris_data = 0

		self._now_interest = 0
		self._limit_interest = 5
		self._band_add_edge = 1
		self._close_band_num =2

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

		open_time = self.is_trend_open_time()
		close_time = self.is_trend_close_time()
		# close_time = False
		
		if open_time and self._now_interest < self._limit_interest:
		# if open_time:
			self._open_lastprice = ((self._open_lastprice * self._now_interest) + self._lastprice)/(self._now_interest + 1)
			self._now_interest +=1
			self._max_profit = 0
			mesg= "the time of open: "+self._time + ",the price: " + str(self._lastprice)
			self._file.write(mesg+"\n")
			# print "the diff volume is:" + str(self._now_md_price[VOLUME] - self._pre_md_price[VOLUME])
		# elif close_time:
		elif close_time and self._now_interest >0:
			# print "we need to close"
			if self._direction ==LONG:
				self._profit +=(self._lastprice - self._open_lastprice) *self._now_interest
			elif self._direction ==SHORT:
				self._profit +=(self._open_lastprice - self._lastprice) *self._now_interest
			self._open_lastprice = 0
			self._max_profit = 0
			self._now_interest = 0
			mesg= "the time of close:"+self._time+ ",the price: " + str(self._lastprice)
			self._file.write(mesg+"\n")

		return True

	def is_trend_open_time(self):

		open_val = self._param_open_edge + self._band_add_edge*self._now_interest

		is_band_open = self.is_band_open_time(self._direction,self._lastprice,
											self._now_middle_value,open_val,self._now_sd_val,
											self._ris_data,self._limit_rsi_data)
		return is_band_open


	def is_trend_close_time(self):
		if self._now_interest <=0:
			return False
		# base the max draw down
		# 达到最大盈利之后，或者最大亏损之后，就开始平仓。这个是系统自带的。
		# 现在根据李总的说法，添加了maxdrawdown的功能。！！！！！
		if self._direction ==LONG:
			tmp_profit = self._lastprice - self._open_lastprice
		elif self._direction ==SHORT:
			tmp_profit = self._open_lastprice - self._lastprice
		else:
			return False
		if tmp_profit < (0 - self._limit_max_loss) or tmp_profit > self._limit_max_profit:
			# print "the profit is bigger or loss"
			return True

		is_drawdown = self.is_max_draw_down(self._direction,self._lastprice,self._open_lastprice
			,self._max_profit,self._limit_max_draw_down)
		self._max_profit = is_drawdown[1]
		if is_drawdown[0]:
			mesg= 'this is the max draw down ' + str(self._max_profit)
			self._file.write(mesg +"\n")
			return True

		close_band = self._param_open_edge + self._now_interest - self._close_band_num -1

		is_band_close = self.is_band_close_time(self._direction,self._lastprice,
											self._now_middle_value,self._now_sd_val,close_band)
		
		return is_band_close


	def is_band_open_time(self,direction,lastprice,middle_val,open_edge,sd_val,rsi_data,limit_rsi_data):
		# this is used to judge is time to band open
		if direction ==LONG:
			downval = middle_val - open_edge*sd_val
			rsi_data = 100 - rsi_data
			if lastprice < downval  and rsi_data > limit_rsi_data:
				return True
		elif direction ==SHORT:
			upval = middle_val + open_edge*sd_val
			if lastprice > upval and rsi_data > limit_rsi_data:
				return True
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

	def is_max_draw_down(self,direction,cur_price,open_price,max_profit,limit_max_draw_down):
		if open_price ==0 or limit_max_draw_down ==0:
			return (False,max_profit)
		if direction ==LONG:
			tmp_profit = cur_price - open_price;
		elif direction ==SHORT:
			tmp_profit = open_price - cur_price;
		else :
			return (False,0)
		tmp_profit = tmp_profit
		if max_profit < tmp_profit:
			max_profit = tmp_profit
		# f = open("rsidata.txt","a")
		# f.write(str(time)+","+str(cur_price)+","+str(open_price)+","+str(max_profit)+","+str(tmp_profit)+"\n")
		if (max_profit - tmp_profit) >= limit_max_draw_down :
			return (True,max_profit)
		else:
			return (False,max_profit)
		

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
			# param_dict["limit_max_draw_down"] =0
			band_and_trigger_obj = BandAndTrigger(param_dict)
			print "方向是short的交易情况:"
			file.write("方向是short的交易情况:\n")
			start_to_run_md(band_and_trigger_obj,data)
			profit = band_and_trigger_obj.get_total_profit()
			file.write(str(profit)+"\n")
		else:
			print "方向是long的交易情况："
			# param_dict["limit_max_draw_down"] =0
			band_and_trigger_obj = BandAndTrigger(param_dict)
			file.write("方向是long的交易情况：:\n")
			start_to_run_md(band_and_trigger_obj,data)
			profit = band_and_trigger_obj.get_total_profit()
			file.write(str(profit)+"\n")



def main(filename):
	path = "../data/"+filename+"_band_data.csv"
	# path = "../zn/"+filename
	csv_data = read_data_from_csv(path)
	path = "../outdata/"+filename+"_trade_Fade.txt"
	file = open(path,"w")

	# 这个是螺纹钢的 tick 1
	param_dict = {"limit_rsi_data":80,"band_open_edge":3,"limit_max_profit":100000,
				 "file":file,"limit_max_draw_down":100000}
	if "rb" in filename:
		param_dict["band_open_edge"] =3
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
	data = [20170828]
	# instrumentid = ["ru1801","rb1801","zn1710","pb1710","cu1710","hc1801","i1801","ni1801","al1710","au1712","ag1712","bu1712"]
	instrumentid = ["cu1710"]
	for item in data:
		for instrument in instrumentid:
			path = instrument + "_"+ str(item)
			print path
			main(path)	
		# print WRITETOFILE