
from maze_env import Maze
from RL_brain import QLearningTable
import pandas as pd
from time import sleep

def train():
    df = pd.DataFrame(columns=('state','action_space','reward','Q','action'))

    def set_state(observation):#获得相应位置
        p = []
        p.append(int((observation[0] - 4) / 40))
        p.append(int((observation[1] - 4) / 40))
        return p

    for episode in range(200):
        observation = env.reset()
        print("start")
        observation = set_state(observation)
        while True:
            #'''
            if episode > 140:
                sleep(0.5)
            #'''
            env.update()

            action = RL.choose_action(str(observation))

            observation_, reward, done = env.step(action)

            if observation_ != 'terminal':
                observation_ = set_state(observation_)

            RL.learn(str(observation), action, reward, str(observation_))

            q = RL.q_table.loc[str(observation), action]

            #创建相应dataframe保存q表
            df = df.append(pd.DataFrame(
                {'state': [observation], 'action_space': [env.action_space[action]], 'reward': [reward], 'Q': [q],
                 'action': action}), ignore_index=True)

            observation = observation_

            if done:
                break
        env.delete()

    print('game over')
    #执行过程和最终结果进行输出保存
    df.to_csv('action.csv')
    RL.q_table.to_csv('q_table.csv')
    env.destroy()

def test():
    env = Maze()
    #读取q表加载初始环境
    q_table = pd.read_csv('q_table.csv')
    observation = env.reset()
    sleep(1)
    env.update()
    x = (observation[0] - 5) / 40
    y = (observation[1] - 5) / 40

    #根据csv中的q表，对当前位置选择最大reward的前进方向
    for i in range(0, 22):
        if q_table.iloc[i, 0] == str([int(x), int(y)]):
            max_num = -999
            for j in range(1, 5):
                if q_table.iloc[i, j] > max_num:
                    action = j - 1
                    max_num = q_table.iloc[i, j]

    #前进至下一状态
    observation_, reward, done = env.step(action)

    #未抵达终点前不断重复以上操作
    while(observation_ != 'terminal'):

        sleep(1)
        env.update()
        x = (observation_[0] - 5) / 40
        y = (observation_[1] - 5) / 40

        for i in range(0, 22):
            if q_table.iloc[i, 0] == str([int(x), int(y)]):
                max_num = -999
                for j in range(1, 5):
                    if q_table.iloc[i, j] > max_num:
                        action = j - 1
                        max_num = q_table.iloc[i, j]

        observation_, reward, done = env.step(action)
    env.destroy()


if __name__ == "__main__":
    while(1):
        choice = input('请输入指令，1、训练；2、测试：')
        if choice == '1':
            env = Maze()
            RL = QLearningTable(actions=list(range(env.n_actions)))
            env.after(100, train)
            env.mainloop()
        else:
            test()
