# -*- coding:utf8 -*-
import basic_fun as bf

LASTPRICE = 4
VOLUME = 11
OPENINTEREST = 13
TURNONER = 12
BIDPRICE1 = 22
ASKPRICE1 =24
TIME = 20
LONG =1
SHORT =0

class BandAndTrigger(object):
	"""docstring for BandAndTrigger"""
	def __init__(self,param_dic):
		super(BandAndTrigger, self).__init__()
		# self.arg = arg
		self._pre_md_price = []
		self._now_md_price = []
		self._lastprice_array = []
		self._pre_ema_val = 0
		self._now_middle_value =0
		self._now_sd_val = 0

		self._max_profit = 0
		self._limit_max_draw_down = param_dic["limit_max_draw_down"]
		self._limit_max_profit = param_dic["limit_max_profit"]
		self._limit_max_loss = param_dic["limit_max_loss"]

		self._multiple = param_dic["multiple"]

		self._rsi_array = []
		self._rsi_period = param_dic["rsi_period"]
		self._pre_rsi_lastprice =0 
		self._now_bar_rsi_tick = 0
		self._rsi_bar_period = param_dic["rsi_bar_period"]
		self._limit_rsi_data = param_dic["limit_rsi_data"]


		# self._limit_twice_sd = 2

		self._direction = param_dic["direction"]
		self._moving_theo = "EMA"
		# now we have the cangwei and the limit cangwei
		self._now_interest = 0
		self._limit_interest = 1

		# band param
		self._param_open_edge = param_dic["band_open_edge"]
		self._param_loss_edge = param_dic["band_loss_edge"]
		self._param_close_edge =param_dic["band_profit_edge"]
		self._param_period = param_dic["band_period"]
		
		# if the sd is too small like is smaller than _param_limit_sd_value,
		# the open edge and close edge will bigger 
		# self._param_limit_sd_value = limit_sd_val
		# self._param_limit_bigger = 0

		# trigger param
		self._param_volume_open_edge = param_dic["volume_open_edge"]
		self._param_open_interest_edge = param_dic["open_interest_edge"]
		self._param_spread = param_dic["spread"]

		self._open_lastprice = 0
		self._profit = 0
		self._ris_data = 0

		self._sd_lastprice = param_dic["sd_lastprice"]

		self._file = param_dic["file"]


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
			# self._rsi_array.append(0)
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
		
		self._now_sd_val =bf.get_sd_data(self._now_md_price[TIME], self._lastprice_array,self._param_period)	
		
		diff_volume = self._now_md_price[VOLUME] - self._pre_md_price[VOLUME]
		diff_openinterest = self._now_md_price[OPENINTEREST] - self._pre_md_price[OPENINTEREST]

		# self.f.write(str(self._now_md_price[TIME])+","+str(lastprice)+","+str(self._now_middle_value)+","+str(self._now_sd_val)+","+str(self._ris_data)+"\n")
		diff_volume = self._now_md_price[VOLUME] - self._pre_md_price[VOLUME]

		diff_interest = self._now_md_price[OPENINTEREST] - self._pre_md_price[OPENINTEREST]

		diff_turnover = self._now_md_price[TURNONER] - self._pre_md_price[TURNONER]
		if diff_volume ==0:
			return True
		avg_price = float(diff_turnover)/diff_volume/self._multiple
		spread = 100*(self._pre_md_price[ASKPRICE1] - avg_price)/(self._pre_md_price[ASKPRICE1] - self._pre_md_price[BIDPRICE1])

		open_time = self.is_trend_open_time()
		close_time = self.is_trend_close_time()
		# close_time = False


		if open_time and self._now_interest < self._limit_interest:
		# if open_time:
			self._now_interest +=1
			# print "we start to open"
			self._open_lastprice = self._now_md_price[LASTPRICE]
			self._max_profit = 0
			mesg= "the time of open: "+self._now_md_price[TIME] + ",the price: " + str(self._now_md_price[LASTPRICE])
			mesg1 = "the diff volume: "+str(diff_volume)+", the interest: " + str(diff_interest) + ", the spread: "+ str(spread)
			self._file.write(mesg+"\n")
			self._file.write(mesg1+"\n")
			# print "the diff volume is:" + str(self._now_md_price[VOLUME] - self._pre_md_price[VOLUME])
		# elif close_time:
		elif close_time and self._now_interest >0:
			self._now_interest -=1
			# print "we need to close"
			if self._direction ==LONG:
				self._profit +=(self._now_md_price[LASTPRICE] - self._open_lastprice)
			elif self._direction ==SHORT:
				self._profit +=(self._open_lastprice - self._now_md_price[LASTPRICE])
			self._open_lastprice = 0
			self._max_profit = 0
			mesg= "the time of close:"+self._now_md_price[TIME] + ",the price: " + str(self._now_md_price[LASTPRICE])
			self._file.write(mesg+"\n")

		return True

	def is_trend_open_time(self):
		# "'this is used to jude the time used to open return bool'"
		# first base the sd,find is time to open band 
		# if self._now_sd_val < self._param_limit_sd_value:
		# 	# open_val = self._param_limit_bigger*self._param_open_edge
		# 	open_val = self._param_open_edge
		# else:
		open_val = self._param_open_edge
		is_band_open = bf.is_band_open_time(self._direction,self._now_md_price[LASTPRICE],
											self._now_middle_value,self._now_sd_val,open_val)
		# return is_band_open
		if is_band_open ==False:
			return False
		is_trigger_open = bf.is_trigger_size_open_time(self._direction,self._now_md_price,self._pre_md_price,
													self._param_volume_open_edge,self._param_open_interest_edge,
													self._param_spread,self._multiple)
		return is_trigger_open

	def is_trend_close_time(self):
		# this is used to jude the time to close return bool
		# first base band, if the sd is too small ,wo need to bigger
		# current the close signal is only band
		if self._now_interest <=0:
			return False

		# base the max draw down
		# 达到最大盈利之后，或者最大亏损之后，就开始平仓。这个是系统自带的。
		# 现在根据李总的说法，添加了maxdrawdown的功能。！！！！！
		if self._direction ==LONG:
			tmp_profit = self._now_md_price[LASTPRICE] - self._open_lastprice
		elif self._direction ==SHORT:
			tmp_profit = self._open_lastprice - self._now_md_price[LASTPRICE]
		else:
			return False
		if tmp_profit < (0 - self._limit_max_loss) or tmp_profit > self._limit_max_profit:
			# print "the profit is bigger or loss"
			return True

		is_drawdown = bf.is_max_draw_down(self._direction,self._now_md_price[LASTPRICE],self._open_lastprice
			,self._multiple,self._max_profit,self._limit_max_draw_down)
		self._max_profit = is_drawdown[1]
		if is_drawdown[0]:
			mesg= 'this is the max draw down ' + str(self._max_profit)
			self._file.write(mesg +"\n")
			return True
		
		# if tmp_profit >= self._max_profit:
		# 	self._max_profit = tmp_profit
		# # 如果达到最大回撤之后，也开始平仓，这个可以自己添加
		# tmp_draw_down = self._max_profit - tmp_profit
		# # print tmp_draw_down
		# if tmp_draw_down > self._draw_down:
		# 	print "the max draw down!!"
		# 	return True


		# if self._now_sd_val < self._param_limit_sd_value and self._now_sd_val > self._limit_twice_sd:
		# 	# open_val = self._param_limit_bigger*self._param_open_edge
		# 	open_val = self._param_loss_edge
		# 	# close_val = self._param_limit_bigger*self._param_close_edge
		# 	close_val = self._param_close_edge + self._param_limit_bigger
		# elif self._now_sd_val <= self._limit_twice_sd:
		# 	open_val = self._param_loss_edge
		# 	close_val = self._param_close_edge + self._param_limit_bigger
		# else:
		loss_val = self._param_loss_edge
		close_val = self._param_close_edge
		is_band_close = bf.is_band_close_time(self._direction,self._now_md_price[LASTPRICE],
											self._now_middle_value,self._now_sd_val,loss_val,close_val
											,self._ris_data,self._limit_rsi_data,self._sd_lastprice)
		return is_band_close
		

	def get_total_profit(self):
		return self._profit

if __name__=='__main__': 
	print "this is the band and trigger size"