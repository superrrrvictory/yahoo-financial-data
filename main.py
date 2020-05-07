import requests
import json
import pandas as pd


print('请输入你要查询的股票代码:')
company = input()
print('该公司为US or CN ？')
region = input()
# 设定想要查找的财务指标元素
print('请选择查询年度数据or季度数据（输入季度or年度):')
type_choice = input()

if type_choice == '年度':
    type1 = '''annualEbitda,
                 trailingEbitda,annualDilutedAverageShares,trailingDilutedAverageShares,annualBasicAverageShares,
             trailingBasicAverageShares,annualDilutedEPS,trailingDilutedEPS,annualBasicEPS,trailingBasicEPS,
             annualNetIncomeCommonStockholders,trailingNetIncomeCommonStockholders,annualNetIncome,
             trailingNetIncome,annualNetIncomeContinuousOperations,trailingNetIncomeContinuousOperations,
             annualTaxProvision,trailingTaxProvision,annualPretaxIncome,trailingPretaxIncome,
             annualOtherIncomeExpense,trailingOtherIncomeExpense,annualInterestExpense,trailingInterestExpense,
             annualOperatingIncome,trailingOperatingIncome,annualOperatingExpense,trailingOperatingExpense,
             annualSellingGeneralAndAdministration,trailingSellingGeneralAndAdministration,annualResearchAndDevelopment,
             trailingResearchAndDevelopment,annualGrossProfit,trailingGrossProfit,annualCostOfRevenue,trailingCostOfRevenue,
             annualTotalRevenue,trailingTotalRevenue'''
else:
    type1= '''quarterlyEbitda,trailingEbitda,quarterlyDilutedAverageShares,
          trailingDilutedAverageShares,quarterlyBasicAverageShares,
          trailingBasicAverageShares,quarterlyDilutedEPS,trailingDilutedEPS,
          quarterlyBasicEPS,trailingBasicEPS,quarterlyNetIncomeCommonStockholders,trailingNetIncomeCommonStockholders,quarterlyNetIncome,
          trailingNetIncome,quarterlyNetIncomeContinuousOperations,trailingNetIncomeContinuousOperations,quarterlyTaxProvision,
          trailingTaxProvision,quarterlyPretaxIncome,trailingPretaxIncome,quarterlyOtherIncomeExpense,trailingOtherIncomeExpense,
          quarterlyInterestExpense,trailingInterestExpense,quarterlyOperatingIncome,trailingOperatingIncome,
          quarterlyOperatingExpense,trailingOperatingExpense,quarterlySellingGeneralAndAdministration,trailingSellingGeneralAndAdministration,
          quarterlyResearchAndDevelopment,trailingResearchAndDevelopment,quarterlyGrossProfit,
          trailingGrossProfit,quarterlyCostOfRevenue,trailingCostOfRevenue,quarterlyTotalRevenue,trailingTotalRevenue'''


params = {
'lang': 'en-US',
'region':'US',
'symbol':company,
'padTimeSeries': 'true',
'type':type1,
'merge':'false',
'period1':'493590046',
'period2': '1588221158',
'corsDomain':'finance.yahoo.com'}

# 定义需要抓取的网页
url = 'https://query2.finance.yahoo.com/ws/fundamentals-timeseries/v1/finance/timeseries/'+str(company)+'?'
header = {'user-agent':
              'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36'}
# 抓取数据
respond = requests.get(url,params=params,headers=header)
content = json.loads(respond.content)
stock_financial_data = content['timeseries']['result']


type_time_value_lists = []
for i in range(len(stock_financial_data)):
    try:
        type2 = stock_financial_data[i]['meta']['type'][0]
        data = stock_financial_data[i][type2]
        lists = []
        for m in range(len(data)):
            time_period = data[m]['asOfDate']
            periodType  = data[m]['periodType']
            value = data[m]['reportedValue']['fmt']
            unit = data[m]['currencyCode']
            stock_dict = {'typeriod':time_period,'type':type2,'periodtype':periodType,'value':value,'unit':unit}
            lists.append(stock_dict)
        type_time_value_lists.extend(lists)
    except:
        data = None
        pass

stock = pd.DataFrame(type_time_value_lists)

# 转换数字格式，将307.5M转换成数字类型
def transfer_to_data(x):
    if type(x)==float:
        return x
    else:
        if 'M' in x:
            x_float = float(x.strip('M'))
            x_base = 100000
            return x_float * x_base
        elif 'B' in x:
            x_float = float(x.strip('B'))
            x_base = 1000000000
            return x_float * x_base
        else:
            return float(x)

stock2 = stock
for i in range(len(stock)):
    stock2['value'][i] = transfer_to_data(stock['value'][i])
stock2 = stock2.sort_values('typeriod',ascending=True)
stock2['value'] = stock2['value'].astype(float)
stock2 = stock2.pivot_table(index='type',values='value',columns='typeriod')



stock2.to_csv('stock.csv')
