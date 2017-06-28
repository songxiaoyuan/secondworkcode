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

def create_band_obj(data,filename,ris_add,ris_period,loss_band,open_edge):
	if ris_add ==True:
		limit_ris_val = 80
	else:
		limit_ris_val = 0
	for i in xrange(0,2):
		band_and_trigger_obj = band_and_trigger.BandAndTrigger(i,limit_ris_val,ris_period,loss_band,open_edge)
		if i==1:
			print "方向是long的交易情况："
			start_to_run_md(band_and_trigger_obj,data)
			profit = band_and_trigger_obj.get_total_profit()
			print profit
		else:
			# continue
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
			# print "正常根据0.5开，然后3平的交易情况： 没有添加rsi的情况"
			# create_band_obj(csv_data,5000,0,filename,True,False)
			print "正常根据0.5开，0.5退出 然后3平的交易情况：了添加rsi的情况"
			create_band_obj(csv_data,filename,True,10,0.5,120)
		elif band_type ==1:
			# print "当sd小于4倍的最小变动价位时，平仓变成4倍的sd的交易情况：没有添加ris的情况 "
			# create_band_obj(csv_data,5000,20,filename,False,False)
			print "正常根据0.5开，1退出 然后3平的交易情况：开仓是900的情况。"
			create_band_obj(csv_data,filename,True,14,1,120)
			# print "正常根据0.5开，1退出 然后3平的交易情况：开仓是120的情况。"
			# create_band_obj(csv_data,filename,True,10,1,120)
			# print "正常根据0.5开，1退出 然后3平的交易情况：开仓是150的情况。"
			# create_band_obj(csv_data,filename,True,10,1,150)
			# print "正常根据0.5开，1退出 然后3平的交易情况：开仓是180的情况。"
			# create_band_obj(csv_data,filename,True,10,1,180)
			# print "当sd小于4倍的最小变动价位时，平仓变成4倍的sd的交易情况：添加了ris的情况 bar是120，然后period是10 "
			# create_band_obj(csv_data,10,4,filename,False,True,120,10)
		else:
			# continue
			print "根据最大回撤平仓的交易情况，现在最大回撤设置的是20个最小变动价位："
			create_band_obj(csv_data,filename,True,10,1)



if __name__=='__main__': 
	# main("ru1709_20170622")
	# data = [20170623,20170622,20170621,20170620,20170619,20170616]
	data = [20170628]
	for item in data:
		path = "ru1709_"+ str(item)
		# print path
		main(path)	
	# print WRITETOFILE