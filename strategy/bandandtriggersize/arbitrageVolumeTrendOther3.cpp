#include "arbitrageVolumeTrendOther3.h"


void CHyArbitrageVolumeTrendOther3::clearVector()
{
	memset(&new_Price,0,sizeof(mdPrice));
	memset(&last_Price,0,sizeof(mdPrice));
	isTrendOpenTime=false;
	isTrendCloseTime=false;
}

bool CHyArbitrageVolumeTrendOther3::get_fv_less(double &fv)
{
	// 获取最新的价格。问题：这个mdprice对象每一个参数的作用？
	new_Price=getNewPrice(g_arrChannel,less_md_index);

	last_Price=getLastPrice(g_arrChannel,less_md_index);


	if (new_Price.Volume	==0	||	new_Price.OpenInterest	==	0	||	new_Price.Turnover	==0||	new_Price.LastPrice	==	0
	  ||last_Price.Volume	==0	||	last_Price.OpenInterest	==	0	||	last_Price.Turnover	==0||	last_Price.LastPrice	==	0)
	{
		return false;
	}

	//通过 ShortCompXave 来设置band的开仓边界，一般都是0.5,这边除以了10，所以设置的时候，应该在10倍。
	band_open_edge_ = (param->less.ShortCompXave)/10;
	// 通过设置 LongCompXave 来设置band的平仓边界，一般都是2
	band_close_edge_ = (param->less.LongCompXave)/10;

	// 此部分代码主要是用来保存计算cur_middle_value_和sd的price。
	cur_lastprice_ = new_Price.LastPrice;
	if (vector_prices_.size() < param->less.CompXave)
	{
		vector_prices_.push_back(cur_lastprice_);
		double tmp = GetEMAData(cur_lastprice_);
		return false;
	}
	else{
		vector_prices_.push_back(cur_lastprice_);
		// vector<double>::iterator it = vector_prices_.begin();
		// it = vector_prices_.erase(it);
	}
	//已经达到了周期，开始计算middle data和sd的data
	if (param->less.PositionAdj == 0){
		cur_middle_value_ = GetEMAData(cur_lastprice_);
	}
	else
	{
		cur_middle_value_ = GetMAData(vector_prices_);
	}
	cur_sd_val_ = GetSDData(vector_prices_);

	// 根据最新的价格判断已经下的单子是不是需要撤单
	// 问题：我需要一个参数，现在来决定到了这个边界就开始撤单，那么我怎么调用。达到布林带的某一个标准的时候。
	STraderChannel *pTraderInfo_open=&g_arrTraderChannel[less_open_order_index];
	cancelNotMatchOrder(pTraderInfo_open);

	STraderChannel *pTraderInfo_close=&g_arrTraderChannel[less_close_order_index];
	cancelNotMatchOrder(pTraderInfo_close);

	
	// 计算开仓和平仓的时机，通过这个tick的数据，来判断是不是需要进行开仓或者平仓。
	isTrendOpenTime		=	isOpenTrendTime();
	isTrendCloseTime	=	isCloseTrendTime();

	// 如果达到开仓的时机，那么就进行开仓的操作，如果达到平仓的时机，那么就进行平仓的操作？
	//如果到了开仓的时机，但是已经进行开仓了，还会继续开仓吗，还是这个函数会自己判断。
	// 如果已经平仓了也是同样的道理，判断是不是已经平仓了吗。
	if (isTrendOpenTime)
	{
		STraderChannel *pTraderInfo=&g_arrTraderChannel[less_open_order_index];
		less_process_Lock(pTraderInfo);
	}
	else if (isTrendCloseTime)
	{
		STraderChannel *pTraderInfo=&g_arrTraderChannel[less_close_order_index];
		less_process_Lock(pTraderInfo);

	}
	return true;
}
double CHyArbitrageVolumeTrendOther3::calculateEmaFvAdj()
{
	return 0;
}

double CHyArbitrageVolumeTrendOther3::calculateLessPrice(char OffsetFlag,char Direction,double fv,int perside)
{
	
	// 这个最后的挂单价根本就没有计算啊，还是这个maxprice已经改变了。
	// tirgger 感觉根本就不需要计算挂单价，直接达到下单条件之后，根据选择的下单方式直接下单就好了
	double price=0;
	if (Direction	==	THOST_FTDC_D_Buy)				//买
	{
		price	=	0;
	}
	else if(Direction	==	THOST_FTDC_D_Sell)			//卖
	{
		price	=	MaxPrice;
	}
	return price;


}

bool CHyArbitrageVolumeTrendOther3::isOpenTrendTime()
{
	if (status	==	STATUS_Exit	||	status	==	STATUS_Pause)
	{
		return false;
	}

	// 表示现在交易量之间的差值必须达到一定的数值。
	int diffVolume	=	new_Price.Volume	-	last_Price.Volume;
	if (diffVolume	<	param->less.openEdge)
	{
		return false;
	}

	// 表示现在持仓量之间的差值需要达到一定的数值。
	int diffOpenInterest	=	new_Price.OpenInterest	-	last_Price.OpenInterest;

	if (diffOpenInterest	<=	param->less.index)
	{
		return false;
	}

	// 获取band的信号，判断根据布林带是不是已经达到开仓条件。
	// 如果没有达到的话，直接返回false, 达到的话判断trigger size是不是达到.
	bool bandSignal = IsBandOpenTime();
	if (bandSignal ==false)
	{
		return false;
	}
	double edge =param->less.spread;

	if (arbitrageDirection	==	Direction_long)
	{
		return isUpTime(edge);
	}
	else if (arbitrageDirection	==	Direction_short)
	{
		return isDownTime(edge);
	}
	return false;
}

bool CHyArbitrageVolumeTrendOther3::isCloseTrendTime()
{

	if (status	==	STATUS_Pause)
	{
		return false;
	}

	//现在根据袁总的要求，在判断平仓的时候，只是根据band的平仓条件。
	// 所以trigger size 的平仓条件先忽略。
	return IsBandCloseTime();

	int diffVolume	=	new_Price.Volume	-	last_Price.Volume;
	if (diffVolume	<	param->less.closeEdge)
	{
		return false;
	}

	int diffOpenInterest	=	new_Price.OpenInterest	-	last_Price.OpenInterest;

	if (diffOpenInterest	>=	-	param->less.index)
	{
		return false;
	}


	double edge =param->less.spread;


	if (arbitrageDirection	==	Direction_long)
	{
		return isDownTime(edge);
	}
	else if (arbitrageDirection	==	Direction_short)
	{
		return isUpTime(edge);
	}
	return false;
}

bool CHyArbitrageVolumeTrendOther3::isUpTime(double edge)
{
	int multiple=getVolumeMultiple(g_arrChannel,less_md_index);   //返回合约乘数
	int diffVolume	=	new_Price.Volume	-	last_Price.Volume;  //返回持仓量的变化
	double diffTurnover	=	new_Price.Turnover	-	last_Price.Turnover;  //返回成交金额的变化

	if (diffVolume	==	0	||	diffTurnover	==	0	||	multiple	==	0)
	{
		return false;
	}
	double avePrice	=	diffTurnover/diffVolume/multiple;

	double temp	=	100*(avePrice	-	last_Price.BidPrice1)/(last_Price.AskPrice1-last_Price.BidPrice1);

	if (temp >=	edge)
	{
		return true;

	}
	return false;

}

bool CHyArbitrageVolumeTrendOther3::isDownTime(double edge)
{
	int multiple=getVolumeMultiple(g_arrChannel,less_md_index);    
	int diffVolume	=	new_Price.Volume	-	last_Price.Volume;   
	double diffTurnover	=	new_Price.Turnover	-	last_Price.Turnover;  

	if (diffVolume	==	0	||	diffTurnover	==	0	||	multiple	==	0)
	{
		return false;
	}

	double avePrice	=	diffTurnover/diffVolume/multiple;

	double temp	=	100*(last_Price.AskPrice1	-	avePrice)/(last_Price.AskPrice1-last_Price.BidPrice1);
	if (temp >=	edge)
	{
		return true;

	}
	return false;

}
void CHyArbitrageVolumeTrendOther3::cancelNotMatchOrder(STraderChannel* pTraderInfo)
{
	pthread_mutex_lock(&pTraderInfo->cs_trader_order);
	for (unsigned int i=0;i<pTraderInfo->trader_order.size();i++)
	{
		orderMsg *ordermsg=&pTraderInfo->trader_order[i];
		if (ordermsg->remainVolume	==	0)
		{
			continue;
		}

		if (ordermsg->status	==	1) //挂单状态，考虑是否撤单
		{
			lessAction_action_Lock(ordermsg);

		}
	}
	pthread_mutex_unlock(&pTraderInfo->cs_trader_order);
}

double CHyArbitrageVolumeTrendOther3::GetMAData(vector<double> &vector_prices_){
	double sum =0;
	if (vector_prices_.size()==0)
	{
		return 0;
	}
	for (int i = vector_prices_.size()-1; i >=0 && i >= vector_prices_.size() - param->less.CompXave; i--)
	{
		sum +=vector_prices_[i];
	}
	return sum/vector_prices_.size();
}

double CHyArbitrageVolumeTrendOther3::GetSDData(vector<double> &vector_prices_){
	int size = vector_prices_.size();
	if (size ==0)
	{
		return 0;
	}
	double sum = 0;
	for (int i = size-1; i >=0 && i >= size - param->less.CompXave; i--)
	{
		sum +=vector_prices_[i];
	}
	double avg = sum/size;
	sum = 0;
	for (int i = size-1; i >=0 && i >= size - param->less.CompXave; i--)
	{
		sum += (vector_prices_[i]-avg)*(vector_prices_[i]-avg);
	}
	return sqrt(sum);
}

double CHyArbitrageVolumeTrendOther3::GetEMAData(double price){
	if (vector_prices_.size()==1)
	{
		current_ema_tick_num_ =1;
		last_mea_val_ = price;
		return last_mea_val_;
	}
	if (current_ema_tick_num_ < param->less.CompXave)
	{
		current_ema_tick_num_ +=1;
	}
	double ret = ((current_ema_tick_num_ - 1)*last_mea_val_ + 2*price)/(current_ema_tick_num_ + 1);
	last_mea_val_ = ret;
	return ret;
}



bool CHyArbitrageVolumeTrendOther3::IsBandOpenTime(){
	if (arbitrageDirection	==	Direction_long)
	{
		double upval = cur_middle_value_ + cur_sd_val_ * band_open_edge_;
		if (cur_lastprice_ > cur_middle_value_ && cur_lastprice_ < upval)
		{
			return true;
		}
	}
	else if (arbitrageDirection	==	Direction_short)
	{
		double downval = cur_middle_value_ - cur_sd_val_ * band_open_edge_;
		if (cur_lastprice_ > downval && cur_lastprice_ < cur_middle_value_)
		{
			return true;
		}
	}
	return false;
}

bool CHyArbitrageVolumeTrendOther3::IsBandCloseTime(){

	if (arbitrageDirection	==	Direction_long)
	{
		double profitval = cur_middle_value_ + cur_sd_val_ * band_close_edge_;
		double lossval = cur_middle_value_ - cur_sd_val_ * band_open_edge_;
		if (cur_lastprice_ > profitval || cur_lastprice_ < lossval)
		{
			return true;
		}
	}
	else if (arbitrageDirection	==	Direction_short)
	{
		double profitval = cur_middle_value_ - cur_sd_val_ * band_close_edge_;
		double lossval = cur_middle_value_ + cur_sd_val_ * band_open_edge_;
		if (cur_lastprice_ < lossval || cur_lastprice_ > profitval)
		{
			return true;
		}
	}
	return false;
}

void CHyArbitrageVolumeTrendOther3::closeTraded(char direction,double price)
{


}

void CHyArbitrageVolumeTrendOther3::openTraded(char direction,double price)
{

}