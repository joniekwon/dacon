import pandas as pd
import numpy as np
import datetime

def openCSV(fileName):
    data = pd.read_csv(f"./_data/{fileName}.csv",
                       encoding='UTF-8', engine='python')
    return data

def openCSVwoidx(fileName):
    data = pd.read_csv(f"./_data/{fileName}.csv",
                       encoding='UTF-8', index_col=0, engine='python')
    return data

def saveCSV(data, fileName):
    result = data.to_csv(f"./_data/output/{fileName}.csv", encoding='UTF-8')
    return result

def sortStockName(result, fileName):
    sample_submission = pd.read_csv('./_data/sample_submission.csv')

    result = result.transpose()
    result = result.reset_index()
    #result.drop(columns=[])

    result = result.astype({'index': 'int'})
    result.index = result['index']
    result = result.drop(columns=['index'], axis=0)

    result = result.sort_index(key=lambda x: x)
    result = result.transpose()
    # sort 완료
    # 데이 추가
    print(result)
    result.insert(0, 'Day', sample_submission['Day'])   #0번째 열에 Day열 추가
    result['Day'] = sample_submission['Day']
    columns = list(sample_submission.columns[1:])
    result.columns = ['Day'] + [str(x).zfill(6) for x in columns]

    result = result.to_csv(f"./_data/output/{fileName}.csv", index=False)
    return result

if __name__=='__main__':
    # f = pd.read_csv(f"../_data/kosdaq_kospi1.csv",
    #                    encoding='CP949', engine='python', index_col=0)  # 0번째 열을 index로 지정
    #
    # f.index = f.index.map(lambda x:datetime.datetime.strptime(str(x),"%Y. %m. %d"))
    # #f.drop('거래대금(주식시장  잠정치) (억원)', inplace=True)
    #
    # print(f)

    # stock_list = pd.read_csv("../_data/stock_list.csv",
    #                    encoding='UTF-8', engine='python')
    # result = pd.DataFrame()
    # stock_name = stock_list[stock_list['종목코드']==5930]['종목명']
    # stock_code = stock_list[stock_list['종목명']=='삼성전자']['종목코드']
    # print(stock_name)
    # print(stock_code)
    # result['삼성전자'] = {'D':'D'}
    # for i in range(1,6):
    #     result.loc['D','삼성전자'] = [i]

    stock_list = pd.read_csv(f"../_data/stock_list.csv")
    result = pd.read_csv(f"../_data/output/result_final.csv")
    stock_list['종목코드'] = stock_list['종목코드'].apply(lambda x: str(x).zfill(6))  # zfill 숫자만큼 자릿수 맞춰 0 채우기
    sample_submission = pd.read_csv(f"../_data/sample_submission.csv")

    sortStockName(result,'fffinal')
    print(result)
    result = result.to_csv(f"../_data/output/o_result_final.csv", index=False)

   #  print(sample_submission['Day'])
   #  rere.set_index(sample_submission['Day'], inplace=True)
   #
   #  rere.drop(columns=['Day'],inplace=True)
   #  rere = rere.reset_index()
   #  print(rere)
   #  rere.to_csv(f"../_data/output/a.csv", index=False)