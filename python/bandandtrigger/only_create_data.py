# -*- coding:utf8 -*-
import csv
import band_and_trigger
import basic_fun as bf

LASTPRICE = 4
VOLUME = 11
OPENINTEREST = 13
TURNONER = 12
BIDPRICE1 = 22
ASKPRICE1 =24
TIME = 20


class BandAndTrigger(object):
	"""docstring for BandAndTrigger"""
	def __init__(self):
		super(BandAndTrigger, self).__init__()
		# self.arg = arg
		self._pre_md_price = []
		self._now_md_price = []
		self._lastprice_array = []
		self._pre_ema_val = 0
		self._now_middle_value =0
		self._now_sd_val = 0

		self._rsi_array = []
		self._pre_rsi_lastprice =0
		self._now_bar_rsi_tick = 0
		self._rsi_bar_period = 120
		self._rsi_period = 14

		self._rsi_array_3 = []
		self._pre_rsi_lastprice_3 =0
		self._now_bar_rsi_tick_3 = 0
		self._rsi_period_3 = 20
		self._ris_data_3 = 0

		self._moving_theo = "EMA"
		self._param_period = 3600

		self._write_to_csv_data = []


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
		self._lastprice_array.append(lastprice)
		# print lastprice

		if len(self._pre_md_price) ==0:
			self._rsi_array.append(0)
			self._pre_rsi_lastprice = lastprice
			self._ris_data = -1
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

			if self._now_bar_rsi_tick_3 >= self._rsi_bar_period:
				# 表示已经到了一个bar的周期。
				tmpdiff1 = lastprice - self._pre_rsi_lastprice_3		
				self._pre_rsi_lastprice_3 = lastprice
				self._now_bar_rsi_tick_3 = 1
				self._ris_data_3 =bf.get_rsi_data2(tmpdiff1,self._rsi_array_3,self._rsi_period_3)
				self._rsi_array_3.append(tmpdiff1)
			else:
				self._now_bar_rsi_tick_3 +=1
				tmpdiff1 = lastprice - self._pre_rsi_lastprice_3
				self._ris_data_3 =bf.get_rsi_data2(tmpdiff1,self._rsi_array_3,self._rsi_period_3)
				# self._ris_data_3 = 0
				# self._ris_data = -1
		# self._now_bar_rsi_tick +=1
		# if self._now_bar_rsi_tick >= self._rsi_period:
		# 	self._ris_data =bf.get_rsi_data(self._rsi_array,self._rsi_period)
		# 	self._now_bar_rsi_tick =0
		# else:
		# 	self._ris_data =0
		# print self._ris_data	

		if len(self._lastprice_array)-1 < self._param_period:
			# this is we dont start the period.
			ema_period = len(self._lastprice_array)
			pre_ema_val = bf.get_ema_data(lastprice,self._pre_ema_val,ema_period)
			self._pre_ema_val = pre_ema_val
			# save the pre_ema_val and return
			return True

		# start the judge
		if self._moving_theo =="EMA":
			self._now_middle_value = bf.get_ema_data(lastprice,self._pre_ema_val,self._param_period)
			self._pre_ema_val = self._now_middle_value
		else:
			self._now_middle_value = bf.get_ma_data(self._lastprice_array,self._param_period)
		

		
		# self._ris_data = bf.get_rsi_data(self._rsi_array,self._rsi_period)
		self._now_sd_val =bf.get_sd_data(self._now_md_price[TIME], self._lastprice_array,self._param_period)
		diff_volume = self._now_md_price[VOLUME] - self._pre_md_price[VOLUME]

		tmpsd_lastprice = 1000*self._now_sd_val/self._now_md_price[LASTPRICE]
		tmp_to_csv = [self._now_md_price[TIME],self._now_md_price[LASTPRICE],self._now_middle_value,
					self._now_sd_val,self._ris_data,diff_volume,self._ris_data_3,tmpsd_lastprice]
		self._write_to_csv_data.append(tmp_to_csv)

		return True

	def get_to_csv_data(self):
		return self._write_to_csv_data


def main(filename):
	path = "../data/"+filename+".csv"
	# read_data_from_csv(pth)
	f = open(path,'rb')
	reader = csv.reader(f)
	bt = BandAndTrigger()
	for row in reader:
		bt.get_md_data(row)
		# tranfer the string to float
	f.close()
	
	data = bt.get_to_csv_data()
	path_new = "../data/"+filename+ "_band_data"+".csv"
	bf.write_data_to_csv(path_new,data)


if __name__=='__main__':
	# data = [20170623,20170622,20170621,20170620,20170619,20170616]
	data = [20170703]
	for item in data:
		path = "pb1708_"+ str(item)
		print path
		main(path)	