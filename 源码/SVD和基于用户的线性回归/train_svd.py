import math
import numpy as np


class UVDecompose:
    def __init__(self):
        self.d = 1
        self.u_dim = 19835
        self.v_dim = 624961
        self.init_val = (49.50 / self.d) ** 0.5
        self.u = np.ones((self.u_dim, self.d)) * self.init_val
        self.v = np.ones((self.d, self.v_dim)) * self.init_val
        self.train_path = r"F:\BigDataLesson\大数据计算及应用-第二次大作业(推荐系统)要求" \
                          r"\大数据计算及应用-第二次大作业(推荐系统)要求\data-202205\train.txt"
        self.train_trans_path = r"F:\BigDataLesson\大数据计算及应用-第二次大作业(推荐系统)要求" \
                                r"\大数据计算及应用-第二次大作业(推荐系统)要求\data-202205\train_trans.txt"
        self.validate_path = r"F:\BigDataLesson\大数据计算及应用-第二次大作业(推荐系统)要求" \
                             r"\大数据计算及应用-第二次大作业(推荐系统)要求\data-202205\_test.txt"
        self.test_path = r"F:\BigDataLesson\大数据计算及应用-第二次大作业(推荐系统)要求" \
                         r"\大数据计算及应用-第二次大作业(推荐系统)要求\data-202205\test.txt"
        self.save_path = r'F:\BigDataLesson\大数据计算及应用-第二次大作业(推荐系统)要求' \
                         r'\大数据计算及应用-第二次大作业(推荐系统)要求\data-202205\save-20run-final.txt'
        self.log_path = r'F:\BigDataLesson\大数据计算及应用-第二次大作业(推荐系统)要求' \
                        r'\大数据计算及应用-第二次大作业(推荐系统)要求\data-202205\log-20run-final.txt'
        self.res_path = r'F:\BigDataLesson\大数据计算及应用-第二次大作业(推荐系统)要求' \
                        r'\大数据计算及应用-第二次大作业(推荐系统)要求\data-202205\res-test-final.txt'

    def calc_rmse(self):
        train = open(self.train_path, mode='r')
        se = 0
        count = 0
        while True:
            line = train.readline()
            if line == '':
                break
            user = int(line.split('|')[0])
            # print(user)
            rate_num = int(line.split('|')[1])
            for _ in range(rate_num):
                line = train.readline()
                item = int(line.split('  ')[0])
                score = int(line.split('  ')[1])
                error = (score - np.dot(self.u[user, :], self.v[:, item])) ** 2
                se += error
                # print("error:{}".format(error))
            count += rate_num
        rmse = (se / count) ** 0.5
        train.close()
        return rmse

    def calc_valid(self):
        valid = open(self.validate_path, mode='r')
        se = 0
        count = 0
        while True:
            line = valid.readline()
            if line == '':
                break
            user = int(line.split('|')[0])
            rate_num = int(line.split('|')[1])
            for _ in range(rate_num):
                line = valid.readline()
                item = int(line.split('  ')[0])
                score = int(line.split('  ')[1])
                error = (score - np.dot(self.u[user, :], self.v[:, item])) ** 2
                se += error
                # print("error:{}".format(error))
            count += rate_num
        rmse = (se / count) ** 0.5
        valid.close()
        return rmse

    def display(self):
        valid = open(self.test_path, mode='r')
        res = open(self.res_path, mode='w')
        while True:
            line = valid.readline()
            if line == '':
                break
            user = int(line.split('|')[0])
            rate_num = int(line.split('|')[1])
            res.write(line)
            for _ in range(rate_num):
                line = valid.readline()
                item = int(line.split('  ')[0])
                score = np.dot(self.u[user, :], self.v[:, item])
                line = "{}  {}\n".format(item, score)
                res.write(line)
                # print("error:{}".format(error))
        valid.close()
        res.close()

    def save_mat(self):
        save = open(self.save_path, mode='w')
        for u_row in range(self.u_dim):
            for u_col in range(self.d):
                save.write("%f|" % self.u[u_row, u_col])
            save.write("\n")
        save.write("\n")
        for v_row in range(self.d):
            for v_col in range(self.v_dim):
                save.write("%f|" % self.v[v_row, v_col])
            save.write("\n")
        save.write("\n")
        save.close()


if __name__ == '__main__':
    uv = UVDecompose()
    # print(uv.v[0,0])

    print(uv.calc_rmse())
    # uv.u = np.ones((uv.u_dim, uv.d))
    # uv.v = np.ones((uv.d, uv.v_dim))
    # print(uv.calc_rmse())
    RMSE0 = math.inf

    epochs = 0
    while True:
        train = open(uv.train_path, mode='r')
        train.seek(0, 0)
        while True:
            line = train.readline()
            if line == '':
                break
            try:
                user = int(line.split('|')[0])
            except ValueError:
                print(line)
                print(user)
                exit(0)
            print("current u_row:{}".format(user))
            rate_num = int(line.split('|')[1])
            u_line = user
            cur_pos = train.tell()
            for u_col in range(uv.d):
                up = 0
                down = 0
                for _ in range(rate_num):
                    line = train.readline()
                    item = int(line.split('  ')[0])
                    score = int(line.split('  ')[1])
                    up += uv.v[u_col, item] * (score - (
                            np.dot(uv.u[u_line, :], uv.v[:, item]) - uv.u[u_line, u_col] * uv.v[u_col, item]))
                    down += uv.v[u_col, item] ** 2
                if down != 0:
                    z_point = up / down
                    if z_point > uv.u[u_line, u_col]:
                        uv.u[u_line, u_col] += abs(z_point - uv.u[u_line, u_col]) * 1
                    else:
                        uv.u[u_line, u_col] -= abs(z_point - uv.u[u_line, u_col]) * 1
                if u_col != uv.d - 1:
                    train.seek(cur_pos, 0)

        train_trans = open(uv.train_trans_path, mode='r')
        train_trans.seek(0, 0)
        while True:
            line = train_trans.readline()
            if line == '':
                break
            try:
                v_col = int(line.split('|')[0])
            except ValueError:
                print(line)
                print(v_col)
                exit(0)
            print("current v_col:{}".format(v_col))
            user_num = int(line.split('|')[1])
            up = [0 for _ in range(uv.d)]
            down = [0 for _ in range(uv.d)]
            user = 0
            for _ in range(user_num):
                line = train_trans.readline()
                user = int(line.split('  ')[0])
                score = int(line.split('  ')[1])
                for v_line in range(uv.d):
                    up[v_line] += uv.u[user, v_line] * (score - (
                            np.dot(uv.u[user, :], uv.v[:, v_col]) - uv.u[user, v_line] * uv.v[v_line, v_col]))
                    down[v_line] += uv.u[user, v_line] ** 2
            for v_line in range(uv.d):
                if down[v_line] == 0:
                    continue
                z_point = up[v_line] / down[v_line]
                if z_point > uv.v[v_line, v_col]:
                    uv.v[v_line, v_col] += abs(z_point - uv.v[v_line, v_col]) * 1
                else:
                    uv.v[v_line, v_col] -= abs(z_point - uv.v[v_line, v_col]) * 1
                # uv.v[v_line, v_col] = up[v_line] / down[v_line]

        train.close()
        train_trans.close()
        RMSE = uv.calc_rmse()
        print("RMSE:{}".format(RMSE))
        # valid_rmse = uv.calc_valid()
        epochs += 1
        print("current epochs:{}".format(epochs))
        log = open(uv.log_path, mode='a')
        # log.write("epochs:{}\nRMSE:{}\nvalid_rmse:{}\n".format(epochs, RMSE, valid_rmse))
        log.write("epochs:{}\nRMSE:{}\n".format(epochs, RMSE))
        log.close()
        # if RMSE0 - RMSE < 0.001:
        #     print("total epochs:{}".format(epochs))
        #     break
        if epochs >= 25:
            break

    uv.display()
    uv.save_mat()
