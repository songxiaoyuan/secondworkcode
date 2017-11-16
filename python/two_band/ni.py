# -*- coding:utf8 -*-
import csv
import basic_fun as bf
import os
import shutil

TIME = 0
LASTPRICE = 1
MIDDLE = 2
SD = 3
RSI = 4
DIFF_VOLUME = 5
SPREAD = 6
LONG =1
SHORT =0

def main():
	shutil.copy('../hour_config/config/352', '../hour_config/real_server/540')
	shutil.copy('../hour_config/config/352', '../hour_config/real_server/541')
	shutil.copy('../hour_config/config/352', '../hour_config/config/353')
	shutil.copy('../hour_config/config/352', '../hour_config/config/354')
	shutil.copy('../hour_config/config/352', '../hour_config/config/355')


if __name__=='__main__': 
	main()