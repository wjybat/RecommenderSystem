import numpy as np
import math

def takeFirst(elem):
    return elem[0]

class CoFiltering:
    def __init__(self):
        self.userRateVectors =[]
        self.userNum = 0
        self.rateSum=0 #所有评值之和
        self.rateNum = 0 #评分总数目
        self.rateMean = 0#所有评分均值
        self.itemDeviation = 0#item偏差
        self.userDeviation = 0#user偏差
        self.allSame =False
        self.sameRate=0
        self.N = 2 #相似用户集合大小
        self.dataFilePath = ".\_train.txt"
        self.testFilePath = ".\_test.txt"
        self.resultFilePath = r".\resFile.txt"
        self.calcMean()
        self.similarityTable = np.zeros(self.userNum**2//2)

    def getSimilarity(self,uidx,uidy):
        #print('res type :',type(uidx*(uidx-1)//2+uidy-1))
        return self.similarityTable[uidx*(uidx-1)//2+uidy-1]

    def sim(self,x,y,uidx,uidy):
        '计算cosine相似度'
        #print('uid type:',type(uidx))
        if uidx<uidy:
            temp = uidx
            uidx = uidy
            udiy =temp
        if self.getSimilarity(uidx,uidy)!=0:
            return self.getSimilarity(uidx,uidy)
        else:
            x = dict(x)
            y = dict(y)
            s=0
            for index1 in x.keys():
                for index2 in y.keys():
                    if index1==index2:
                        s+=x[index1]*y[index2]
            sum1,sum2=0,0
            for i in x.keys():
                sum1+=x[i]**2
            for i in y.keys():
                sum2+=y[i]**2
            self.similarityTable[uidx*(uidx-1)//2+uidy-1] = s/(math.sqrt(sum1)*math.sqrt(sum2))
            return self.similarityTable[uidx*(uidx-1)//2+uidy-1]

    def getUserVector(self,uID):
        return self.userRateVectors[int(uID)]
        # dataFile = open(self.dataFilePath,'r')
        # userVector = dict()
        # res = list()
        # data = dataFile.readline()
        # #print('data file line:',data)
        # while(data!=''):
        #     uid,count = data.strip().split('|')
        #     if uid !=uID:
        #         for i in range(int(count)):
        #             a = dataFile.readline()
        #     elif uid == uID:
        #         for i in range(int(count)):
        #             item = dataFile.readline().strip().split()
        #             userVector[item[0]] = int(item[1])
        #             #print(len(userVector))
        #         #print(str(userVector))
        #         break
        #     data = dataFile.readline()
        # dataFile.close()
        # return userVector
        
    def getSimUsers(self,userid,userVector,itemID):
        '获取与uID最为相似的user集合N'
        res = list()
        Sum,num=0,0
        for i in range(len(self.userRateVectors)):
            if itemID in self.userRateVectors[i].keys():
                Sum+=self.userRateVectors[i][itemID]
                num+=1
                itemTemp = self.userRateVectors[i].copy()
                #归一化
                m = sum(list(itemTemp.values()))/len(itemTemp)
                for j in itemTemp.keys():
                    itemTemp[j]-=m
                #print(temp)
                userTemp = userVector.copy()
                #归一化
                m=sum(list(userTemp.values()))/len(userTemp)
                self.userDeviation = m-self.rateMean
                for j in userTemp.keys():
                    userTemp[j]-=m
                if sum(itemTemp.values())!= 0 and sum(userTemp.values())!=0:
                    s = self.sim(userTemp,itemTemp,int(userid),int(i))
                    res.append((s,self.userRateVectors[i][itemID]))
                    res.sort(key=takeFirst,reverse=True)
                    if len(res)>self.N:
                        res.pop()
                elif sum(userTemp.values())==0:
                    self.allSame=True
                    self.sameRate = sum(userVector.values())/len(userVector)
        try:
            self.itemDeviation = Sum/num - self.rateMean
        except ZeroDivisionError :
            print('Sum:',Sum)
            print('Num',num)

        return res
        
    def calcMean(self):
        '计算所有打分的均值'
        dataFile = open(self.dataFilePath,'r')
        lines = dataFile.readlines()
        lineNum = 0
        while lineNum<len(lines):
            self.userNum+=1
            #print(lines[lineNum].strip().split())
            uid,count = lines[lineNum].strip().split('|')
            temp =dict()
            for i in range(int(count)):
                item = lines[i+lineNum+1].strip().split()
                temp[item[0]]=int(item[1])
            lineNum+=(int(count)+1)
            self.rateNum+=len(temp)
            self.rateSum+=sum(list(temp.values()))
            self.userRateVectors.append(temp)
        self.rateMean = self.rateSum/self.rateNum
        dataFile.close()
        #print(self.userNum)

    def calcRMSE(self):
        Sum =0
        num =0
        resFile = open(self.resultFilePath,'r')
        testFile = open(self.testFilePath,'r')
        data1 = testFile.readline()
        data2 = resFile.readline()
        while(data1!='' and data2!=''):
            count = data1.strip().split('|')[1]
            num+=int(count)
            for i in range(int(count)):
                item1=testFile.readline().strip().split()[1]
                item2=resFile.readline().strip().split()[1]
                Sum+=(float(item2)-float(item1))**2
            data1=testFile.readline()
            data2 = resFile.readline()
        rmse = math.sqrt(Sum/num)
        resFile.close()
        testFile.close()
        return rmse

    def predict(self):
        '对_test.txt中item进行打分预测'
        #self.calcMean()#计算所有评分均值
        testFile = open(self.testFilePath,'r')
        resFile = open(self.resultFilePath,'w+')
        data = testFile.readline()
        time = 0
        while(data!=''):
              time+=1
              resFile.write(data)
              uid,count = data.strip().split('|')
              #print(int(count))
              userVector = self.getUserVector(uid)
              for i in range(int(count)):
                  item = testFile.readline().strip().split(' ')[0]
                  #output itemid to resuslt file
                  print('to predict:',uid,item)
                  simList = self.getSimUsers(uid,userVector,item)
                  #print(simList)
                  if(self.allSame):
                      rate = self.sameRate
                      self.allSame=False
                  else:
                      weightsum ,Sum=0,0
                      for i in range(len(simList)):
                          Sum+=simList[i][0]*simList[i][1]
                          weightsum+=simList[i][0]
                          #rate =self.rateMean+self.userDeviation+self.itemDeviation+ Sum/weightsum
                          rate = Sum/weightsum
                  if rate>100:
                      rate = 100
                  if rate<=0:
                      rate = 0  
                  resFile.write(item+'  '+str(rate)+'\n')
              data = testFile.readline()
            #   if time == 2:
            #       break
            #  break #只测试第一组数据
        testFile.close()
        resFile.close()

if __name__ == '__main__':
    cf = CoFiltering()
    cf.predict()
    print('RMSE :',cf.calcRMSE())





