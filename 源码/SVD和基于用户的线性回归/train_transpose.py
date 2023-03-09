if __name__ == '__main__':
    for_train = open(r"F:\BigDataLesson\大数据计算及应用-第二次大作业(推荐系统)要求"
                     r"\大数据计算及应用-第二次大作业(推荐系统)要求\data-202205\train.txt", encoding='utf-8', mode='r')
    transpose = open(r"F:\BigDataLesson\大数据计算及应用-第二次大作业(推荐系统)要求"
                     r"\大数据计算及应用-第二次大作业(推荐系统)要求\data-202205\train_trans.txt", encoding='utf-8', mode='w')
    for i in range(7):
        l = [[] for _ in range(100000)]
        for_train.seek(0,0)
        while True:
            line = for_train.readline()
            if line == '':
                break
            item_num = int(line.split('|')[1])
            user = int(line.split('|')[0])
            print("current user:{}".format(user))
            for _ in range(item_num):
                line=for_train.readline()
                item=int(line.split('  ')[0])
                score=int(line.split('  ')[1])
                if item in range(i*100000,(i+1)*100000):
                    l[item%100000].append((user,score))
        for index in range(len(l)):
            if i==6 and index>24960:
                break
            if len(l[index])!=0:
                transpose.write("{}|{}\n".format(index+i*100000,len(l[index])))
                for ele in l[index]:
                    transpose.write("{}  {}\n".format(ele[0],ele[1]))
            else:
                transpose.write("{}|{}\n".format(index+i*100000, 0))
    for_train.close()
    transpose.close()