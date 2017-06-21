#ifndef ARBITRAGEVOLUMETRENDOTHER3_H
#define ARBITRAGEVOLUMETRENDOTHER3_H
#include <vector>
#include <math.h>
#include <string>
#include <string.h>
#include <fstream>
#include "hyArbitrage_Interface.h"
#include "func.h"
using namespace std;

#define MaxPrice 100000
class CHyArbitrageVolumeTrendOther3:public CHyArbitrageBase
{
public:
	CHyArbitrageVolumeTrendOther3(Parameter* Param):CHyArbitrageBase(Param){}
	~CHyArbitrageVolumeTrendOther3(){};
public:
	virtual bool get_fv_less(double &fv);
	virtual void clearVector();
	virtual double calculateEmaFvAdj();
	virtual double calculateLessPrice(char OffsetFlag,char Direction,double fv,int perside);
	virtual void   closeTraded(char direction,double price);
	virtual void   openTraded(char direction,double price);

private:

	void cancelNotMatchOrder(STraderChannel* pTraderInfo);

	bool isOpenTrendTime();
	bool isCloseTrendTime();

	bool isUpTime(double edge);
	bool isDownTime(double edge);


	// 判断是不是达到了布林带的开仓和平仓条件
	bool IsBandCloseTime();
	bool IsBandOpenTime();
	//根据现在的price的一个列表，计算列表里面的ma数据。
	double GetMAData(vector<double> &prices);
	// 根据现在的price的一个列表，计算列表里面的标准差
	double GetSDData(vector<double> &prices);
	// 根据传入的这个lastprice，计算返回的ema的值。
	double GetEMAData(double price);

	// 将想要的信息写入到本地。
	void WriteMesgToFile(string path,string mesg);

private:

	mdPrice new_Price;
	mdPrice last_Price;
	vector<double> vector_prices_;
	double cur_lastprice_;
	double last_mea_val_;
	int current_ema_tick_num_;
	double band_open_edge_;
	double band_close_edge_;
	double cur_middle_value_;
	double cur_sd_val_;
	double cur_spread_price_val_;

};


#endif