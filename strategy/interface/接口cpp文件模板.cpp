#include "arbitrageXXXX.h"

void CHyArbitrageXXXX::clearVector()
{
	//m_less_theo.clear();
	//m_main_theo.clear();
	//m_less_emaTheo.clear();
	//m_main_emaTheo.clear();
	//m_fv.clear();
	//m_fv_ema_fast.clear();
	//m_fv_ema_slow.clear();
	//m_atr_diff.clear();
	//atrValue	=	0;
}
bool CHyArbitrageXXXX::get_fv_less(double &fv)
{
	mdPrice md_main=getNewPrice(g_arrChannel,main_md_index);
	mdPrice md_less=getNewPrice(g_arrChannel,less_md_index);
	double theo_main=get_theo(param->main.Theo,md_main);
	double theo_less=get_theo(param->less.Theo,md_less);
	if (theo_main	==	0	||	theo_less	==	0)
	{
		return false;
	}

	m_main_theo.push_back(theo_main);
	m_less_theo.push_back(theo_less);

	double ema_main=get_emaTheo(m_main_theo,m_main_emaTheo,param->main.compXave);
	double ema_less=get_emaTheo(m_less_theo,m_less_emaTheo,param->less.compXave);

	m_main_emaTheo.push_back(ema_main);
	m_less_emaTheo.push_back(ema_less);


	double WeightAve_main	=	get_theo(P_T_WeightAve,md_main);
	double WeightAve_less	=	get_theo(P_T_WeightAve,md_less);

	if (WeightAve_main	!=	0	&&	WeightAve_less	!=	0)
	{
		double atr_diff	=	(WeightAve_less	*	param->less.volMultiplier)	-	(WeightAve_main*param->less.volMultiplier);

		atr_diff	=	fabs(atr_diff);

		m_atr_diff.push_back(atr_diff);

		atrValue	=	calAtrValue();

	}
	if (ema_main	==	0	||	ema_less	==	0)
	{
		return false;
	}
	fv=get_compTheo(theo_main,theo_less,ema_main,ema_less,param->less.index);
	return true;

}

double CHyArbitrageXXXX::calculateLessPrice(char OffsetFlag,char Direction,double fv,int perside)
{
	double priceTick=getPriceTick(g_arrChannel,less_md_index);
	double positionAdj=0;
	double emaAdj=0;

	double price=0;
	if (Direction	==	THOST_FTDC_D_Buy)				//买
	{
		if (OffsetFlag	==	THOST_FTDC_OF_Open)
		{
			price= fv	-	param->less.openEdge*priceTick	-	(perside-1)*param->less.orderSpacingOpen*priceTick	-	positionAdj	-	emaAdj;

		}
		else if (OffsetFlag	==	THOST_FTDC_OF_Close)
		{
			price= fv	-param->less.closeEdge*priceTick	-	(perside-1)*param->less.orderSpacingClose*priceTick	-	positionAdj	-	emaAdj;

		}
	}
	else if(Direction	==	THOST_FTDC_D_Sell)			//卖
	{
		if (OffsetFlag	==	THOST_FTDC_OF_Open)
		{
			price= fv	+	param->less.openEdge*priceTick	+	(perside-1)*param->less.orderSpacingOpen*priceTick	-	positionAdj	-	emaAdj;

		}
		else if (OffsetFlag	==	THOST_FTDC_OF_Close)
		{
			price= fv	+	param->less.closeEdge*priceTick	+	(perside-1)*param->less.orderSpacingClose*priceTick	-	positionAdj	-	emaAdj;

		}

	}
	price	=((int)(price/priceTick+0.500001))*priceTick;

	price	=	ChangePrice(Direction,OffsetFlag,price);

	return price;

}

double  CHyArbitrageXXXX::calAtrValue()
{

	int tickSize	=		param->less.AdjEmaFast; //参数借用:ShortCompXave
	int tickDiffSize	=	param->less.AdjEmaSlow;	//参数借用:LongComXave

	if (tickSize	<=0	||	tickDiffSize<=0)
	{
		return 0;
	}

	int size	=	m_atr_diff.size();
	if (size	<	tickSize	+	tickDiffSize)
	{
		return 0;
	}
	double nowHight	=	getMaxValue(m_atr_diff,size	-tickSize,size-1);
	double nowLow	=	getMinValue(m_atr_diff,size	-tickSize,size-1);
	double preLast	=	m_atr_diff[size	-	tickDiffSize	-	1];

	double tr1	=	fabs(nowHight	-	nowLow);
	double tr2	=	fabs(preLast	-	nowHight);
	double tr3	=	fabs(preLast	-	nowLow);
	
	double atrValue	=	max(tr1,tr2);
	atrValue	=		max(atrValue,tr3);
	return atrValue;
}
double CHyArbitrageXXXX::getMaxValue(vector <double> &m_src,int nStartIndex,int nStopIndex)
{
	int size	=	m_src.size();
	if (nStartIndex	>=	size	||	nStopIndex>=size)
	{
		return 0;
	}

	double maxValue	=	m_src[nStartIndex];
	for (int i=nStartIndex;i<nStopIndex;i++)
	{
		if (m_src[i]	>	maxValue)
		{
			maxValue	=	m_src[i];
		}
	}
	return maxValue;
}
double CHyArbitrageXXXX::getMinValue(vector <double> &m_src,int nStartIndex,int nStopIndex)
{
	int size	=	m_src.size();
	if (nStartIndex	>=	size	||	nStopIndex>=size)
	{
		return 0;
	}

	double minValue	=	m_src[nStartIndex];
	for (int i=nStartIndex;i<nStopIndex;i++)
	{
		if (m_src[i]	<	minValue)
		{
			minValue	=	m_src[i];
		}
	}
	return minValue;
}
double CHyArbitrageXXXX::ChangePrice(char Direction,char OffsetFlag,double price)
{
	double changePrice	=	price;
	if (atrValue	==	0)
	{
		return changePrice;
	}
	double edge	=	0;
	if (OffsetFlag	==	THOST_FTDC_OF_Open)
	{
		edge	=	param->less.openEdge;
	}
	else if (OffsetFlag	==	THOST_FTDC_OF_Close)
	{
		edge	=	param->main.closeEdge;
	}

	double bias	=	(double)param->less.PositionAdj;		//参数借用:PositionAdj
	double weight	=	(double)param->less.PositionNormal/(double)100;	//参数借用: PositionNormal/100
	double cmp_atrValue	=	weight	*	(edge	+	bias);

	if (Direction	==	THOST_FTDC_D_Buy)
	{
		
		if (atrValue	>	cmp_atrValue)	//不发单
		{
			changePrice	=	0;
		}
	}
	else if (Direction	==	THOST_FTDC_D_Sell)
	{
		if (atrValue	>	cmp_atrValue)	//不发单
		{
			changePrice	=	MaxPrice;
		}
	}
	return changePrice;
}

void CHyArbitrageXXXX::closeTraded()
{


}

void CHyArbitrageXXXX::openTraded()
{

}



