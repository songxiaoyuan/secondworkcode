# coding: utf-8
import sys, csv , operator  
#!/usr/bin/python
# -*- coding:utf8 -*-
import os
LASTPRICE = 4
VOLUME = 11
OPENINTEREST = 13
TURNONER = 12
BIDPRICE1 = 22
ASKPRICE1 =24
TIME = 20
LONG =1
SHORT =0

class WVAD(object):
	"""docstring for WVAD"""
	def __init__(self,param_dic):
		super(WVAD, self).__init__()
		# self.arg = arg
		self._period = param_dic["period"]
		self._bar_num = param_dic["bar_num"]
		self._now_tick_num = 0
		self._min_lastprice = 0
		self._max_lastprice = 0
		self._open_price = 0
		self._pre_volume = 0
		self._wavd_array =[]


	def __del__(self):
		print "this is the over function"

	# get the md data ,every line;
	def get_md_data(self,md_array):
		# tranfer the string to float
		md_array[LASTPRICE] = float(md_array[LASTPRICE])
		md_array[VOLUME] = float(md_array[VOLUME])
		if self._pre_volume ==0:
			self._pre_volume = md_array[VOLUME]

		lastprice = md_array[LASTPRICE]
		volume = md_array[VOLUME]
		if self._min_lastprice ==0 or self._min_lastprice > lastprice:
			self._min_lastprice = lastprice
		if self._max_lastprice ==0 or self._max_lastprice < lastprice:
			self._max_lastprice = lastprice
		if self._open_price ==0:
			self._open_price = lastprice

		diff_min_max = self._max_lastprice - self._min_lastprice
		diff_close_open = lastprice - self._open_price
		diff_volume = volume - self._pre_volume
		tmp_wvad = 0
		if diff_min_max ==0:
			tmp_wvad = 0
		else:
			tmp_wvad = (diff_close_open/diff_min_max) * (diff_volume)

		self._now_tick_num +=1
		ret = self.get_sum_ema(tmp_wvad,self._wavd_array,self._bar_num)
		if self._now_tick_num >= self._period:
			self._wavd_array.append(tmp_wvad)
			self._now_tick_num = 0
			self._pre_volume = volume
			self._open_price = lastprice
			self._min_lastprice = lastprice
			self._max_lastprice = lastprice

		
		return ret

	def get_sum(self,tmp_wvad,num_array,period):
		period -=1
		ret = tmp_wvad
		l = len(num_array)
		for i in xrange(l-1,-1,-1):
			if i >= (l - period):
				ret +=num_array[i]
		return ret

	def get_sum_ema(self,tmp_wvad,num_array,period):
		if period ==1:
			return tmp_wvad
		perod_sum = (period * (period+1))/2
		ret = tmp_wvad * period
		period -=1
		tmp = period
		l = len(num_array)
		for i in xrange(l-1,-1,-1):
			if i >= (l - period):
				ret +=(num_array[i]*tmp)
				tmp -=1
		return ret/perod_sum


if __name__=='__main__': 

	print "this is the adv"