if __name__ == '__main__':
    uv_path = r'F:\BigDataLesson\大数据计算及应用-第二次大作业(推荐系统)要求' \
              r'\大数据计算及应用-第二次大作业(推荐系统)要求\data-202205\res-test-final.txt'
    regre_path = r'F:\BigDataLesson\大数据计算及应用-第二次大作业(推荐系统)要求' \
                 r'\大数据计算及应用-第二次大作业(推荐系统)要求\data-202205\res-test-regre-final.txt'
    test_path = r'F:\BigDataLesson\大数据计算及应用-第二次大作业(推荐系统)要求' \
                r'\大数据计算及应用-第二次大作业(推荐系统)要求\data-202205\test.txt'
    res_path = r'F:\BigDataLesson\大数据计算及应用-第二次大作业(推荐系统)要求' \
               r'\大数据计算及应用-第二次大作业(推荐系统)要求\data-202205\res-test-combine-final.txt'
    res1 = open(uv_path, mode='r')
    res2 = open(regre_path, mode='r')
    res0 = open(res_path, mode='w')
    res3 = open(test_path, mode='r')
    # se=0
    # count=0
    while True:
        line1 = res1.readline()
        line2 = res2.readline()
        # line3=res3.readline()
        if line1 == '':
            break
        if line1.find('|') != -1:
            res0.write(line1)
        else:
            item = int(line1.split('  ')[0])
            score1 = float(line1.split('  ')[1].strip())
            score2 = float(line2.split('  ')[1].strip())
            if score2 == -1.0:
                if score1 < 0:
                    score1 = 0.0
                if score1 > 100:
                    score1 = 100.0
                score = int(score1)
            else:
                if score2 < 0:
                    score2 = 0.0
                if score2 > 100:
                    score2 = 100.0
                score = int(score2)
            res0.write("{}  {}\n".format(item, score))
            # real_score=int(line3.split('  ')[1])
            # se+=(-sreal_scorecore)**2
            # count+=1
    # rmse=(se/count)**0.5
    # print(rmse)
    res0.close()
    res1.close()
    res2.close()
    res3.close()
