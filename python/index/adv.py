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

class ADV(object):
	"""docstring for ADV"""
	def __init__(self,param_dic):
		super(ADV, self).__init__()
		# self.arg = arg
		self._period = param_dic["period"]
		self._pre_adv = param_dic["pre_adv"]
		self._now_tick_num = 0
		self._min_lastprice = 0
		self._max_lastprice = 0
		self._pre_volume = 0


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

		clv = 0
		if self._min_lastprice == self._max_lastprice:
			clv = 0
		else:
			clv = (2*lastprice - self._min_lastprice - self._max_lastprice)/(self._max_lastprice - self._min_lastprice)
		
		adv = self._pre_adv + clv*(volume - self._pre_volume)


		if self._now_tick_num >= self._period:
			self._pre_adv = adv
			self._min_lastprice = 0
			self._max_lastprice = 0
			self._pre_volume = volume
			self._now_tick_num = 0
		
		return adv


if __name__=='__main__': 

	print "this is the adv"