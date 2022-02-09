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

# 원-핫 인코딩
def dataPrep_ohe(year):
    new_data = pd.DataFrame(index=year.index)

    new_data['year'] = [str(x.year) for x in year.index]
    month = {1: 'jan', 2: 'feb', 3: 'mar', 4: 'apr', 5: 'may', 6: 'jun', 7: 'jul', 8: 'aug', 9: 'sep', 10: 'oct',
             11: 'nov', 12: 'dec'}
    new_data['month'] = [month[x.month] for x in year.index]
    new_data['day'] = [str(x.day) for x in year.index]

    for i in new_data['year'].unique():
        new_data[i] = pd.Series([lambda x: 1 if x==i else 0 for i in new_data['year'].values])
    print(new_data)

    index = list(new_data['year'].unique()) + list(new_data['month'].unique()) + list(new_data['day'].unique())
    id_dict = {}
    for i, id in enumerate(index):
        id_dict[i]=id

    date_ote = OneHotEncoder()
    date_ote.fit(new_data[['year', 'month', 'day']])
    onehot = date_ote.transform(new_data[['year', 'month', 'day']])
    onehot = pd.DataFrame(onehot.toarray(), index=year.index)
    onehot.rename(columns=id_dict, inplace=True)

    #print(onehot)

    # 시각화2 - 산점도
    # years = list(new_data['year'].unique())
    # month = list(month.values())
    # days = [str(x) for x in range(1, 32)]
    # wdays = list(new_data['wday'].unique())
    # years = years + month + days + wdays
    # cols = years.extend(['Open', 'High', 'Low', 'Close', 'Volume'])
    # tempDf = pd.concat([onehot, data], axis=1)

    # 히트맵 보니 예전의 주가는...별로 관련이 없음.
    # cm = np.corrcoef(tempDf[:].values.T)
    # hm = heatmap(cm, row_names=cols, column_names=cols)
    # plt.savefig('./_data/output/heatmap.png', dpi=300, bbox_inches='tight')
    # plt.show()

    y = year.dropna(axis=1)
    X = onehot

    return X, y

# 인풋을 원핫 인코딩으로
def input_ohe(X, date):
    d = datetime.datetime.strptime(date, '%Y%m%d')
    df = pd.DataFrame(index=[d], columns=X.columns)
    df = df.fillna(0)
    print(df)
    # year = d.year
    # months = {1: 'jan', 2: 'feb', 3: 'mar', 4: 'apr', 5: 'may', 6: 'jun', 7: 'jul', 8: 'aug', 9: 'sep', 10: 'oct',
    #          11: 'nov', 12: 'dec'}
    # month = months[int(d.month)]
    # day = d.day
    # weekdays = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat']
    # wday = weekdays[d.weekday()]
    #
    # X = pd.DataFrame({'year':[year], 'month':[month], 'day': [day], 'wday': [wday]})
    # print(X)

    # date_ote = OneHotEncoder()
    # date_ote.fit(X[['year', 'month', 'day', 'wday']])
    # onehot = date_ote.transform(X[['year', 'month', 'day', 'wday']])
    # onehot = pd.DataFrame(onehot.toarray(), index=X.index)
    # print(onehot)
    return
