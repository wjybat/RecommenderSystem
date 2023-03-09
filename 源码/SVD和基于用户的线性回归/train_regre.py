import numpy as np
from matplotlib import pyplot as plt


class LinearRegressionForUsers:

    def __init__(self):
        self.coef_ = None
        self.intercept_ = None
        self._theta = None
        self.MSE = []
        self.theta_list = []
        self.train_path = r"F:\BigDataLesson\大数据计算及应用-第二次大作业(推荐系统)要求" \
                          r"\大数据计算及应用-第二次大作业(推荐系统)要求\data-202205\train.txt"
        self.validate_path = r"F:\BigDataLesson\大数据计算及应用-第二次大作业(推荐系统)要求" \
                             r"\大数据计算及应用-第二次大作业(推荐系统)要求\data-202205\test.txt"
        self.feature_path = r"F:\BigDataLesson\大数据计算及应用-第二次大作业(推荐系统)要求" \
                            r"\大数据计算及应用-第二次大作业(推荐系统)要求\data-202205\itemAttribute.txt"
        self.res_path = r'F:\BigDataLesson\大数据计算及应用-第二次大作业(推荐系统)要求' \
                        r'\大数据计算及应用-第二次大作业(推荐系统)要求\data-202205\res-test-regre-final.txt'

    def fit_normal(self, X_train, y_train):
        assert X_train.shape[0] == y_train.shape[0], \
            "the size of X_train must be equal to the size of y_train"

        X_b = np.hstack([np.ones((len(X_train), 1)), X_train])
        self._theta = np.linalg.inv(X_b.T.dot(X_b)).dot(X_b.T).dot(y_train)

        self.intercept_ = self._theta[0]
        self.coef_ = self._theta[1:]

        return self

    def fit_gd(self, X_train, y_train, eta=0.01, n_iters=1e4):
        assert X_train.shape[0] == y_train.shape[0], \
            "the size of X_train must be equal to the size of y_train"

        def J(theta, X_b, y):
            try:
                return np.sum((y - X_b.dot(theta)) ** 2) / len(y)
            except:
                return float('inf')

        def dJ(theta, X_b, y):
            return X_b.T.dot(X_b.dot(theta) - y) * 2. / len(X_b)

        def gradient_descent(X_b, y, inital_theta, eta, n_iters=1e4, epsilon=1e-8):

            theta = inital_theta
            cur_iter = 0

            while cur_iter < n_iters:
                gradient = dJ(theta, X_b, y)
                last_theta = theta
                theta = theta - eta * gradient
                yPred = X_b.dot(theta)
                num = (yPred - y).dot(yPred - y)
                d = y.size
                self.MSE.append(num / d)
                self.theta_list.append((cur_iter + 1))
                if (abs(J(theta, X_b, y) - J(last_theta, X_b, y)) < epsilon):
                    break
                cur_iter += 1

            return theta

        X_b = np.hstack([np.ones((len(X_train), 1)), X_train])
        initial_theta = np.zeros(X_b.shape[1])
        self._theta = gradient_descent(X_b, y_train, initial_theta, eta, n_iters)

        self.intercept_ = self._theta[0]
        self.coef_ = self._theta[1:]

        return self

    def predict(self, X_predict):
        assert self.intercept_ is not None and self.coef_ is not None, \
            "must fit before predict!"
        assert X_predict.shape[1] == len(self.coef_), \
            "the feature number of X_predict must be equal to X_train"

        X_b = np.hstack([np.ones((len(X_predict), 1)), X_predict])

        return X_b.dot(self._theta)

    def __repr__(self):
        return "LinearRegression()"


# 按间距中的绿色按钮以运行脚本。
if __name__ == '__main__':
    LR = LinearRegressionForUsers()
    feature = open(LR.feature_path, mode='r')
    feature_mat = np.zeros((624961,2))
    for line in feature:
        item = int(line.split('|')[0])
        attr1 = line.split('|')[1]
        attr2 = line.split('|')[2].strip()
        attr1 =int(attr1) if attr1!='None' else 0
        attr2 =int(attr2) if attr2!='None' else 0
        feature_mat[item,0]=attr1
        feature_mat[item,1]=attr2
    feature.close()
    min = [np.min(feature_mat[..., i]) for i in range(feature_mat.shape[1])]
    max = [np.max(feature_mat[..., i]) for i in range(feature_mat.shape[1])]
    #print(feature_mat.shape[1])
    feature_mat = np.array([[(ele - min[i]) / (max[i] - min[i]) for ele in feature_mat[..., i]] for i in range(feature_mat.shape[1])])
    feature_mat=feature_mat.transpose()
    #print(feature_mat)

    train = open(LR.train_path, mode='r')
    LR_set=[]
    while True:
        line = train.readline()
        if line == '':
            break
        user = int(line.split('|')[0])
        print("current user:{}".format(user))
        rate_num = int(line.split('|')[1])
        current_x=np.ones((rate_num,2))
        current_y=np.ones(rate_num)
        for i in range(rate_num):
            line = train.readline()
            item = int(line.split('  ')[0])
            score = int(line.split('  ')[1])
            current_y[i]=score
            current_x[i,0]=feature_mat[item,0]
            current_x[i, 1] = feature_mat[item, 1]
        LR.fit_gd(current_x, current_y, eta=0.005)
        LR_set.append(LR)
        LR=LinearRegressionForUsers()
        # if user==0:
        #     break
    train.close()

    valid = open(LR.validate_path, mode='r')
    res=open(LR.res_path,mode='a')
    # se=0
    # count=0
    while True:
        line = valid.readline()
        if line == '':
            break
        user = int(line.split('|')[0])
        print("current test_user:{}".format(user))
        rate_num = int(line.split('|')[1])
        test_x =np.ones((rate_num,2))
        # test_y = np.ones(rate_num)
        LR=LR_set[user]
        items=[]
        for i in range(rate_num):
            line = valid.readline()
            item = int(line.split('  ')[0])
            # score = int(line.split('  ')[1])
            items.append(item)
            # test_y[i]=score
            test_x[i, 0] = feature_mat[item, 0]
            test_x[i, 1] = feature_mat[item, 1]
        y_predT = LR.predict(test_x)
        # se += (y_predT - test_y).dot(y_predT - test_y)
        # count+=rate_num
        res.write("{}|{}\n".format(user,rate_num))
        for ele0,ele1 in zip(y_predT,items):
            if ele0==LR.intercept_:
                ele0=-1
            res.write("{}  {}\n".format(ele1,ele0))
        # print(LR.intercept_)
        # if user==0:
        #     break
    valid.close()
    res.close()

    # print("迭代次数为%d" % len(LR.MSE))
    # plt.subplot(2, 2, 1)
    # plt.xticks([])
    # plt.plot(LR.theta_list, LR.MSE)
    # plt.title("iteration %d" % len(LR.MSE))
    # plt.show()
    # print((se/count)**0.5)
