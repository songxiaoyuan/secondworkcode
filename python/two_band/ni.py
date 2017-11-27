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
	# ni
	shutil.copy('../hour_config/config/352', '../hour_config/real_server/540')
	shutil.copy('../hour_config/config/352', '../hour_config/real_server/541')
	shutil.copy('../hour_config/config/352', '../hour_config/config/353')
	shutil.copy('../hour_config/config/352', '../hour_config/config/354')
	shutil.copy('../hour_config/config/352', '../hour_config/config/355')
	# pp
	shutil.copy('../hour_config/config/382', '../hour_config/real_server/544')
	shutil.copy('../hour_config/config/382', '../hour_config/real_server/545')
	shutil.copy('../hour_config/config/382', '../hour_config/config/383')
	shutil.copy('../hour_config/config/382', '../hour_config/config/384')
	shutil.copy('../hour_config/config/382', '../hour_config/config/385')
	# m
	shutil.copy('../hour_config/config/512', '../hour_config/real_server/564')
	shutil.copy('../hour_config/config/512', '../hour_config/real_server/565')
	shutil.copy('../hour_config/config/512', '../hour_config/config/513')
	shutil.copy('../hour_config/config/512', '../hour_config/config/514')
	shutil.copy('../hour_config/config/512', '../hour_config/config/515')
	# p
	shutil.copy('../hour_config/config/482', '../hour_config/real_server/558')
	shutil.copy('../hour_config/config/482', '../hour_config/real_server/559')
	shutil.copy('../hour_config/config/482', '../hour_config/config/483')
	shutil.copy('../hour_config/config/482', '../hour_config/config/484')
	shutil.copy('../hour_config/config/482', '../hour_config/config/485')

	# bu
	shutil.copy('../hour_config/config/422', '../hour_config/real_server/542')
	shutil.copy('../hour_config/config/422', '../hour_config/real_server/543')
	shutil.copy('../hour_config/config/422', '../hour_config/config/423')
	shutil.copy('../hour_config/config/422', '../hour_config/config/424')
	shutil.copy('../hour_config/config/422', '../hour_config/config/425')

	# jm
	shutil.copy('../hour_config/config/462', '../hour_config/real_server/554')
	shutil.copy('../hour_config/config/462', '../hour_config/real_server/555')
	shutil.copy('../hour_config/config/462', '../hour_config/config/463')
	shutil.copy('../hour_config/config/462', '../hour_config/config/464')
	shutil.copy('../hour_config/config/462', '../hour_config/config/465')

	# j
	shutil.copy('../hour_config/config/452', '../hour_config/real_server/552')
	shutil.copy('../hour_config/config/452', '../hour_config/real_server/553')
	shutil.copy('../hour_config/config/452', '../hour_config/config/453')
	shutil.copy('../hour_config/config/452', '../hour_config/config/454')
	shutil.copy('../hour_config/config/452', '../hour_config/config/455')

if __name__=='__main__': 
	main()