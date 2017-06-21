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
def read_data_from_csv(path,obj):
	f = open(path,'rb')
	reader = csv.reader(f)
	for row in reader:
		obj.get_md_data(row)


def main(filename):
	path = "../data/"+filename+".csv"
	band_and_trigger_obj = band_and_trigger.BandAndTrigger()
	read_data_from_csv(path,band_and_trigger_obj)

	profit = band_and_trigger_obj.get_total_profit()
	print profit

	csv_data = band_and_trigger_obj.get_to_csv_data()
	path_new = "../data/"+filename+ "_band_data" +".csv"
	basic_fun.write_data_to_csv(path,csv_data)


if __name__=='__main__': 
	main("rb1710_20170620")