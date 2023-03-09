if __name__ == '__main__':
    train_file = open(r"F:\BigDataLesson\大数据计算及应用-第二次大作业(推荐系统)要求"
                      r"\大数据计算及应用-第二次大作业(推荐系统)要求\data-202205\train.txt", encoding='utf-8', mode='r')
    for_train = open(r"F:\BigDataLesson\大数据计算及应用-第二次大作业(推荐系统)要求"
                     r"\大数据计算及应用-第二次大作业(推荐系统)要求\data-202205\_train.txt", encoding='utf-8', mode='w')
    for_test = open(r"F:\BigDataLesson\大数据计算及应用-第二次大作业(推荐系统)要求"
                    r"\大数据计算及应用-第二次大作业(推荐系统)要求\data-202205\_test.txt", encoding='utf-8', mode='w')
    while True:
        line=train_file.readline()
        if line=='':
            break
        item_num=int(line.split('|')[1])
        user_num=int(line.split('|')[0])
        test_num=item_num//10
        for_test.write("%d|%d\n" %(user_num,test_num))
        for _ in range(test_num):
            line=train_file.readline()
            for_test.write(line)
        train_num = item_num-test_num
        for_train.write("%d|%d\n" % (user_num, train_num))
        sort_list=[]
        for _ in range(train_num):
            line = train_file.readline()
            item=int(line.split('  ')[0])
            # score=int(line.split('  ')[1])
            sort_list.append((item,line))
        sort_list=sorted(sort_list,key=lambda x:x[0])
        for ele in sort_list:
            line=ele[1]
            for_train.write(line)
    train_file.close()
    for_train.close()
    for_test.close()