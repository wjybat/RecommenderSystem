# 推荐系统算法实现

### 小组成员

王隽毅  1911475

包烜濚 1911392

杨坤     1911504

### 可执行文件说明

运行recommend.exe即可运行程序。
exe文件同级目录下，需要存在res-test-uv-final.txt和res-test-regre-final.txt两个文件。
运行生成res-test-combine-final.txt文件，该文件保存了最终结果。

### 源码文件说明

#### SVD和基于用户的线性回归

SVD和基于用户的线性回归 文件目录下包括

train_split.py： 用于将数据集中的train.txt文件划分为训练集和测试集。

train_transpose.py： 用于生成SVD所需的转置矩阵数据集。

train_svd.py： SVD算法的具体实现代码，用于SVD推荐系统的训练和预测。

train_regre.py： 线性回归算法的具体实现代码，用于线性回归推荐系统的训练和预测。使用了itemAttribute.txt来提高预测性能。

combine.py： 用于整合SVD和线性回归的结果。

#### 基于用户的协同过滤

fasterCofiltering.py： 基于用户的协同过滤算法的具体实现代码，用于协同过滤推荐系统的训练和预测。

### 生成的预测结果

结果使用的是整合SVD模型+线性回归模型的推荐系统的结果。
结果保存在res-test-combine-final.txt中，使用了itemAttribute.txt来提高预测性能。
结果的格式如下：
`
<user id>|<numbers of rating items>
<item id>   <score>
`