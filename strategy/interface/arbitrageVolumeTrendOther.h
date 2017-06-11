#ifndef ARBITRAGEVOLUMETRENDOTHER_H
#define ARBITRAGEVOLUMETRENDOTHER_H
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

private:

	mdPrice new_Price;
	mdPrice last_Price;

};


#endif