import datetime

import numpy as np
import pandas as pd

import myModule.treatFiles as mf        #csv
import FinanceDataReader as fdr         #주식 가격정보 긁어오기

# 데이터 전처리
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer

from sklearn.preprocessing import PolynomialFeatures
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

# 모델
from sklearn.linear_model import LinearRegression, Ridge, Lasso, RANSACRegressor, ElasticNet
from sklearn.linear_model import LassoCV, ElasticNetCV, RidgeCV
from sklearn.ensemble import GradientBoostingRegressor as GBR
from sklearn.ensemble import RandomForestRegressor as RFR
from sklearn.cross_decomposition import PLSRegression as  PLS
from sklearn.svm import SVR
from sklearn.kernel_ridge import KernelRidge

from sklearn.pipeline import Pipeline

# 평가
from sklearn.metrics import accuracy_score
from sklearn.metrics import mean_squared_error as mse
from sklearn.metrics import r2_score as r2
from sklearn.model_selection import cross_val_score

# 시각화
import matplotlib.pyplot as plt
from mlxtend.plotting import scatterplotmatrix
from mlxtend.plotting import heatmap

def tShift(temps):
    tempDf = pd.concat([temps.shift(3), temps.shift(2), temps.shift(1), temps], axis=1)
    tempDf.columns = ['t-3', 't-2', 't-1', 't']
    return


# 데이터 전처리
def dataPrep(data):
    stock = data
    #stock.fillna(0, inplace=True)  # 해당 칸만 바꾸고 싶은데..ㅠㅠ 우선 이렇게하고

    #print(stock.keys()) #열이름 확인 Index(['Open', 'High', 'Low', 'Close', 'Volume', 'Change'], dtype='object')

    # print(stock.index) # 인덱스 확인 datetime

    # 시계열 데이터를 년,월,일,요일 로 나눔.
    new_data = pd.DataFrame(index=stock.index)
    new_data['year'] = [x.year for x in stock.index]
    new_data['month'] = [x.month for x in stock.index]
    new_data['day'] = [x.day for x in stock.index]
    new_data['wday'] = [x.weekday() for x in stock.index]

    # tempDf = pd.concat([new_data, stock], axis=1)

    # 시각화1 : 산점도
    cols = ['year', 'month', 'day', 'wday', 'Open', 'High', 'Low', 'Close', 'Volume']
    # scatterplotmatrix(tempDf[cols].values, figsize=(20, 15), names=cols, alpha=0.5)
    # plt.tight_layout()
    # plt.show()

    # 시각화2 : 공분산 행렬
    # cm = np.corrcoef(tempDf[cols].values.T)
    # hm = heatmap(cm, row_names=cols, column_names=cols)
    # plt.show()

    # y = stock['Close']    #.... 가격을 모두 y로 넣어야 할거 같음.
    # X = pd.concat([new_data, stock], axis=1).drop(columns='Close')
    y = stock.dropna(axis=1)
    X = new_data
    # 코스피나 코스닥 같은 지수 데이터 추가는 어떨까

    return X, y


# 학습 데이터 전처리
def prepData(data):
    X = data.drop(['Close', 'Change'], axis=1)  # 열제외
    y = data.dropna(axis=0, inplace=True) # 행제외
    y = data['Close']

    print(X, y)
    #print(sum(data.isna().sum())) # na 확인

    X = X.iloc[:-1].values
    y = y.values

    return X, y

def prepDataWithOHE(data):
    years = dataPrep_ohe(data)
    X = data.drop(['Close', 'Change'], axis=1)  # 열제외
    y = data.dropna(axis=0, inplace=True) # 행제외
    y = data['Close']

    print(X, y)
    #print(sum(data.isna().sum())) # na 확인

    X = pd.concat([X, years], axis=1)

    X = X.iloc[:-1].values
    y = y.values

    return X, y

# 원-핫 인코딩
def dataPrep_ohe(data):
    new_data = pd.DataFrame(index=data.index)

    new_data['year'] = [str(x.year) for x in data.index]
    #print(new_data)
    print(new_data)
    date_ote = OneHotEncoder()
    date_ote.fit(new_data[['year']])
    onehot = date_ote.transform(new_data[['year']])
    onehot = pd.DataFrame(onehot.toarray(), index=data.index)
    index = {}
    for key, value in enumerate(new_data['year'].unique()):
        index[key] = value
    onehot.rename(columns=index, inplace=True)
    #print(onehot)

    return onehot

#예측할 데이터 전처리
def predPrep_ohe(data, input):

    #print(years)
    return

def drawDataCoef(X, y):

    y = y.dropna()
    cols = list(X.columns) + ['Close']
    tempDf = pd.concat([X, y], axis=1)
    print(tempDf)

    #
    # scatterplotmatrix(tempDf[cols].values, figsize=(20, 15), names=cols, alpha=0.5)
    # plt.tight_layout()
    # plt.show()
    # plt.savefig('./_data/output/scatter.png', dpi=300, bbox_inches='tight')
    #
    # # 히트맵 보니 예전의 주가는...별로 관련이 없음.
    # cm = np.corrcoef(tempDf[:].values.T)
    # hm = heatmap(cm, row_names=cols, column_names=cols)
    # plt.savefig('./_data/output/heatmap.png', dpi=300, bbox_inches='tight')
    # plt.show()

#랜덤 포레스트
def trainForest(stock):

    #X, y = prepDataWithOHE(stock)
    X, y = prepData(stock)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=31)

    from sklearn.ensemble import RandomForestRegressor
    forest = RandomForestRegressor(n_estimators=1000, criterion='mse', random_state=1, n_jobs=-1)
    forest.fit(X_train, y_train)
    y_train_pred = forest.predict(X_train)
    y_test_pred = forest.predict(X_test)
    print(f'훈련 MSE: {mse(y_train,y_train_pred)}, 테스트 MSE: {mse(y_test,y_test_pred)}')
    print(f'훈련 R2: {r2(y_train,y_train_pred)}, 테스트 R2: {r2(y_test,y_test_pred)}')

    #잔차 시각화
    plt.scatter(y_train_pred,
                y_train_pred - y_train,
                c='steelblue',
                edgecolor='white',
                marker='o',
                s=35,
                alpha=0.9,
                label='Training data')
    plt.scatter(y_test_pred,
                y_test_pred - y_test,
                c='red',
                edgecolor='white',
                marker='^',
                s=35,
                alpha=0.9,
                label='Test data')
    plt.xlabel('Predicted values')
    plt.ylabel('Residuals')
    plt.legend(loc='upper left')
    #plt.hlines(y=0, lw=2, color='black')
    #plt.xlim([55000,90000])
    plt.tight_layout()
    plt.show()

    return forest

def closePredict(stock_code, dates):# 종목 코드랑 예측할 날짜[처음,끝]을 입력하면 해당 기간의 종가예측
    close = 0
    # 상장 시장까지 넣어야 되는 줄!
    # condition = stock_list.loc[stock_list['종목코드']==stock_code]
    # market = str(condition['상장시장'])
    end_date = dates[0] # 데이터를 가져올 마지막 날. 적혀있는 날은 포함하지 않음
    start_date = str(int(end_date[:4])-1)+end_date[4:]  #최근 1년의 주가만
    # 예측할 종목의 정보를 가져온다
    # stock = fdr.DataReader(stock_code, start=start_date, end=end_date)
    stock = fdr.DataReader(stock_code, end=end_date)
    # input = (전날의) [Open,High,Low,Volume,datetime]
    #print(stock)
    forest = trainForest(stock)
    # predPrep_ohe(stock, [70200,  70600,  69900,  11503729, datetime.datetime(2021,11,2)])


    #X = stock[''].drop(stock['Close'])

    return close


if __name__ == '__main__':
    # sample = mf.openCSV('sample_submission')
    stock_list = mf.openCSV('stock_list')
    stock_list['종목코드'] = stock_list['종목코드'].apply(lambda x: str(x).zfill(6)) #zfill 숫자만큼 자릿수 맞춰 0 채우기

    #for stock_code in stock_list['종목코드'].unique():
    #    closePredict(stock_code,['20211101','20211105'])
    closePredict('005930',['20211101','20211105'])
    #print(f'shape: {stock_list.shape}')

