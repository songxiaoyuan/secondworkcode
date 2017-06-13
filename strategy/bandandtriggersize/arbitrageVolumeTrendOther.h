#ifndef ARBITRAGEVOLUMETRENDOTHER_H
#define ARBITRAGEVOLUMETRENDOTHER_H
#include <vector>
#include <math.h>
#include <string>
#include <string.h>
#include "hyArbitrage_Interface.h"
#include "func.h"
using namespace std;

#define MaxPrice 100000
class CHyArbitrageVolumeTrendOther:public CHyArbitrageBase
{
public:
	CHyArbitrageVolumeTrendOther(Parameter* Param):CHyArbitrageBase(Param){}
	~CHyArbitrageVolumeTrendOther(){};
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

	// 通过每一个tick传入的lastprice来判断band是不是达到开仓或者平仓条件。
	// 开多仓后者开空仓都是返回1，
	// 平多仓或者平空仓返回2
	// 如果不做操作的话，那么返回0
	bool isBandCloseTime();
	bool isBandOpenTime();
	//根据现在的price的一个列表，计算列表里面的ma数据。
	double getMAData(vector<double> prices);
	// 根据现在的price的一个列表，计算列表里面的标准差
	double getSDData(vector<double> prices);
	// 根据传入的这个lastprice，计算返回的ema的值。
	double getEMAData(double price);
	bool isLongOpenTime(double price,double middleval,double upval);
	bool isLongCloseTime(double price,double profitval,double lossval);
	bool isShortOpenTime(double price,double middleval,double downval);
	bool isShortCloseTime(double price,double profitval,double lossval);

private:

	mdPrice new_Price;
	mdPrice last_Price;
	vector<double> prices;
	double lastPrice;
	int emaTickNum;
	double bandOpenEdge;
	double bandCloseEdge;
	double middleData;
	double sdData;

};


#endif