# 와인 분류 경진대회를 통해 배운 것

## EDA 

### 시각화 - 다양한 그래프를 그리고 해석하는 방법을 알게 됨

[seabron api](https://seaborn.pydata.org/api.html) <br>
* displot, distplot, catplot, boxplot 등<br>
* 시각화를 통해 이상치 및 특성간의 관계를 빠르게 파악할 수 있다.

### 이상치 제거
[참고]<br>
[https://hungryap.tistory.com/69](https://hungryap.tistory.com/69)
https://datascienceschool.net/03%20machine%20learning/05.03%20%EB%A0%88%EB%B2%84%EB%A6%AC%EC%A7%80%EC%99%80%20%EC%95%84%EC%9B%83%EB%9D%BC%EC%9D%B4%EC%96%B4.html

## 공부해야하는 것

### bagging, stacking ...등 모델과 하이퍼파라미터에 대한 공부
* https://dacon.io/competitions/official/235840/codeshare/3834?page=1&dtype=recent

### 하이퍼파라미터 튜닝
* https://optuna.org/
* https://dacon.io/codeshare/2704
* https://dacon.io/competitions/official/235840/codeshare/3794?page=1&dtype=recent

*** 

## 아쉬운 점
레드와인 / 화이트와인 데이터셋을 나누어서 해보면 어떨지, 각 특성마다 품질과의 관계를 시각화 했을때 품질 4등급의 데이터만 이상하게 튀는것을 확인하였는데 4등급만 제외한 나머지를 훈련하고 4등급은 따로 해보면 어떨지 궁금하다. 시간이 되면 모델을 만들어서 정확도 비교 해봐야겠다 ㅎㅎ<br>
그리고 하이퍼파라미터라던가, 어떤 데이터에는 어떤 모델이 성능이 괜찮게 나온다던가 하는 모델에 대한 경험이 많이 부족해서 더 열공 해야겠다는 다짐을 하게 되었다..ㅠ
