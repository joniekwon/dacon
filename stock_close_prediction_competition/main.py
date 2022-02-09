import datetime

import numpy as np
import pandas as pd

import myModule.treatFiles as mf        #csv
import FinanceDataReader as fdr         #주식 가격정보 긁어오기

# 데이터 전처리
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder

# 모델
from sklearn.ensemble import RandomForestRegressor

# 학습 데이터 전처리
def prepData(data):
    data.dropna(axis=1, inplace=True)     # Change열 삭제
    f = pd.read_csv(f"./_data/kosdaq_kospi1.csv",
                    encoding='CP949', engine='python', index_col=0)  # 0번째 열을 index로 지정
    f.index = f.index.map(lambda x: datetime.datetime.strptime(str(x), "%Y. %m. %d"))
    f.fillna(method='pad', axis=0, inplace=True)

    #print(f[f.index==end_date])
    data.reset_index(inplace=True)
    f.reset_index(inplace=True)

    # X 데이터 프레임에 없는 데이터 삭제
    condition = []
    for value in f['Date'].values:
        c = value in data['Date'].unique()
        condition.append(c)

    condition = pd.Series(condition)
    f['condition'] = condition
    index = f[f['condition'] == False].index
    f.drop(index, inplace=True)
    f.drop(['condition'], axis=1, inplace=True)

    data.index = data['Date']
    f.index = f['Date']

    if min(data['Date'].values) < min(f['Date'].values):
        condition = data['Date'] >= min(f['Date'].values)
        data = data[condition]
    else:
        f = f[f['Date'] >= min(data['Date'].values)]

    #df.drop(colums=[], axis=0) #행제외
    #df.drop(colums=[], axis=0) #열제외
    #print(data, f)

    X = data.drop(['Close', 'Date'], axis=1)
    y = data['Close']
    f = f.drop(columns=['Date'])
    X = pd.concat([X,f], axis=1)

    #print(X, y)
    return X, y


def prprocessing(X,y):
    from sklearn.preprocessing import MinMaxScaler

    return X,y

#랜덤 포레스트
def trainForest(X_train, X_test, y_train, y_test):

    forest = RandomForestRegressor(n_estimators=1000, criterion='mse', random_state=1, n_jobs=-1)
    forest.fit(X_train, y_train)
    y_train_pred = forest.predict(X_train)
    y_test_pred = forest.predict(X_test)
    # print(f'훈련 MSE: {mse(y_train,y_train_pred)}, 테스트 MSE: {mse(y_test,y_test_pred)}')
    # print(f'훈련 R2: {r2(y_train,y_train_pred)}, 테스트 R2: {r2(y_test,y_test_pred)}')

    #잔차 시각화
    # plt.scatter(y_train_pred,
    #             y_train_pred - y_train,
    #             c='steelblue',
    #             edgecolor='white',
    #             marker='o',
    #             s=35,
    #             alpha=0.9,
    #             label='Training data')
    # plt.scatter(y_test_pred,
    #             y_test_pred - y_test,
    #             c='red',
    #             edgecolor='white',
    #             marker='^',
    #             s=35,
    #             alpha=0.9,
    #             label='Test data')
    # plt.xlabel('Predicted values')
    # plt.ylabel('Residuals')
    # plt.legend(loc='upper left')
    #plt.hlines(y=0, lw=2, color='black')
    #plt.xlim([55000,90000])
    # plt.tight_layout()
    #plt.show()

    return forest

def setInputX(X):
    inputX = X.iloc[-1].values
    #print(inputX)
    return inputX


def predictClose(result, stock_code, dates):# 종목 코드랑 예측할 날짜[처음,끝]을 입력하면 해당 기간의 종가예측
    # condition = stock_list.loc[stock_list['종목코드']==stock_code]
    # market = str(condition['상장시장'])
    predict_date = datetime.datetime.strptime(dates[0], '%Y%m%d')
    end_date = predict_date - datetime.timedelta(days=1) # 데이터를 가져올 마지막 날
    end_date = str(end_date.year) + str(end_date.month) + str(end_date.day)
    start_date = str(int(end_date[:4])-1)+end_date[4:]  #최근 1년의 주가만
    print(f"start_date: {start_date}, end_date:{end_date}")
    # 예측할 종목의 정보를 가져온다
    # stock = fdr.DataReader(stock_code, start=start_date, end=end_date)
    stock = fdr.DataReader(stock_code, end=end_date, start=start_date)
    # input = (전날의) [Open,High,Low,Volume,]
    #print(stock)
    X, y = prepData(stock, dates[0])
    print('-' * 50)
    #print(f'종목: {stock_list[stock_list["종목코드"]==stock_code]}')
    stock_name = stock_list[stock_list['종목코드'] == stock_code]['종목명']
    #stock_code = stock_list[stock_list['종목명'] == '삼성전자']['종목코드']
    #predict_stock = str(stock_code)+ '('+ stock_name + ')' #한글이 깨지네여^^...
    #
    _X = X[:-5]
    _y = y[5:]

    forest = RandomForestRegressor(n_estimators=1000, criterion='mse', random_state=1, n_jobs=-1)
    inputX = X[-5:].values
    forest.fit(_X, _y)
    prediction = forest.predict(inputX)
   # str_date = str(predict_date.year)+'-'+str(predict_date.month)+'-'+str(predict_date.day)
    for i in range(5):
        result.loc[i, stock_code] = prediction[i]

    print(f"{predict_date.year}-{predict_date.month}-{predict_date.day} 부터 5일간 예상 종가: {prediction} 원")
    #print(result)
    print('='*50)
    # sample_submission = pd.read_csv('./_data/sample_submission.csv')
    # sample_submission.loc[:,stock_code] = predictions
    #X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    return result


if __name__ == '__main__':
    # sample = mf.openCSV('sample_submission')
    stock_list = mf.openCSV('stock_list')
    stock_list['종목코드'] = stock_list['종목코드'].apply(lambda x: str(x).zfill(6)) #zfill 숫자만큼 자릿수 맞춰 0 채우기
    #종가
    result1 = pd.DataFrame()
    result2 = pd.DataFrame()
    for stock_code in stock_list['종목코드']:
        print(f"{stock_list[stock_list['종목코드']==stock_code]}")
        result1 = predictClose(result1, stock_code,['20211101'])
        result2 = predictClose(result2, stock_code,['20211129'])

    result = pd.concat([result1,result2], axis=0)

    mf.sortStockName(result, 'result_final(RS=42,est=1500)')
    # result = predictClose(result, '352820', ['20211101', '20211105'])
    # result = predictClose(result, '005930', ['20211101', '20211105'])
    # mf.saveCSV(result, 'sample')
    print("*" * 60)
    #closePredict('005930',['20211101','20211105'])
    #print(f'shape: {stock_list.shape}')

