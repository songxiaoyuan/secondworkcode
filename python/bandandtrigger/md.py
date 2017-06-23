# -*- coding:utf8 -*-
import csv
import band_and_trigger
import basic_fun

LASTPRICE = 4
VOLUME = 11
OPENINTEREST = 13
TURNONER = 12
BIDPRICE1 = 22
ASKPRICE1 =24
TIME = 20

# read the md data from csv, it uesd to like the csv
def read_data_from_csv(path):
	f = open(path,'rb')
	reader = csv.reader(f)
	ret = []
	for row in reader:
		# obj.get_md_data(row)
		ret.append(row)
	return ret

def start_to_run_md(band_obj,data):
	for row in data:
		band_obj.get_md_data(row)

def create_band_obj(data,max_drawdown,limit_sd_val,filename,write_to_file,ris_add,ris_bar_period,ris_period):
	if ris_add ==True:
		limit_ris_val = 80
	else:
		limit_ris_val = 0
	for i in xrange(0,2):
		band_and_trigger_obj = band_and_trigger.BandAndTrigger(i,max_drawdown,limit_sd_val,limit_ris_val,ris_bar_period,ris_period)
		if i==1:
			print "方向是long的交易情况："
			start_to_run_md(band_and_trigger_obj,data)
			profit = band_and_trigger_obj.get_total_profit()
			print profit
		else:
			print "方向是short的交易情况"
			start_to_run_md(band_and_trigger_obj,data)
			profit = band_and_trigger_obj.get_total_profit()
			print profit
			# if write_to_file ==True:
			# 	print "start to write the file"
			# 	csv_data = band_and_trigger_obj.get_to_csv_data()
			# 	path_new = "../data/"+filename+ "_band_data" +".csv"
			# 	basic_fun.write_data_to_csv(path_new,csv_data)


def main(filename):
	path = "../data/"+filename+".csv"
	csv_data = read_data_from_csv(path)
	print filename
	for band_type in xrange(0,2):
		if band_type ==0:
			continue
			print "正常根据0.5开，然后2平的交易情况： 没有添加rsi的情况"
			create_band_obj(csv_data,5000,0,filename,True,False)
			print "正常根据0.5开，然后2平的交易情况： 了添加rsi的情况"
			create_band_obj(csv_data,5000,0,filename,False,True)
		elif band_type ==1:
			# print "当sd小于4倍的最小变动价位时，平仓变成4倍的sd的交易情况：没有添加ris的情况 "
			# create_band_obj(csv_data,5000,20,filename,False,False)
			# print "当sd小于4倍的最小变动价位时，平仓变成4倍的sd的交易情况：添加了ris的情况 bar是1，然后period是25 "
			# create_band_obj(csv_data,10,4,filename,False,True,1,25)
			print "当sd小于4倍的最小变动价位时，平仓变成4倍的sd的交易情况：添加了ris的情况 bar是120，然后period是10 "
			create_band_obj(csv_data,10,4,filename,False,True,120,10)
		else:
			print "根据最大回撤平仓的交易情况，现在最大回撤设置的是5个最小变动价位："
			create_band_obj(csv_data,5,0,filename,False)



if __name__=='__main__': 
	main("rb1710_20170622")
	# print WRITETOFILE