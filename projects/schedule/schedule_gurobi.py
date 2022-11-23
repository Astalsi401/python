import pandas as pd
import gurobipy as gp
from gurobipy import GRB
from os.path import dirname, abspath

pwd = dirname(abspath(__file__)).replace('\\', '/')
pd.set_option('display.max_columns', 500)


def main():
    df = pd.read_excel(f'{pwd}/媒合會TEMP.xlsx').fillna('').query('`回覆` == ""')
    df = df[['單位名稱', '台灣公司名稱']]
    foreign_tw_num = {f'{row["單位名稱"]}': f'{row["num"]}' for i, row in df.groupby(['單位名稱']).size().reset_index(name='num').iterrows()}
    roles = list(set(df['單位名稱'].values.tolist()))
    courses, courseRequirements = gp.multidict(foreign_tw_num)
    availability = []
    for i, row in df.iterrows():
        ava = (row['台灣公司名稱'], row['單位名稱'])
        if ava not in availability:
            availability.append(ava)

    m = gp.Model("媒合時間表")

    # 加入Decision Variable:
    x = m.addVars(availability, vtype=GRB.BINARY, name="x")

    # 加入Auxiliary Variable:
    totalCourses = m.addVars(roles, name="TotalCourses")  # totalCourses計算每位幹部出席的社課數量
    minCourse = m.addVar(name='minCourse')                # minCourse是被分配到的最少社課數量
    maxCourse = m.addVar(name='maxCourse')                # maxCourse是被分配到的最多社課數量
    # 加入限制式：每堂社課都需有一定數量幹部出席，以維持社課品質
    course_requirement = m.addConstrs((x.sum('*', c) == courseRequirements[c] for c in courses), name='courseRequirement')

    # 加入限制式：計算每位幹部出席的社課總數
    num_courses = m.addConstrs((totalCourses[r] == x.sum(r, '*') for r in roles), name='totalCourses')

    min_constr = m.addGenConstrMin(minCourse, totalCourses, name='minCourse')  # addGenConstrMin()會找出變數中的最小值
    max_constr = m.addGenConstrMax(maxCourse, totalCourses, name='maxCourse')  # addGenConstrMax()會找出變數中的最大值

    # 加入目標式：在符合每堂社課所需幹部數量下，依照各幹部可出席時段，安排一個盡量公平的排班表，平衡每位幹部的出席次數
    m.setObjective(maxCourse - minCourse, GRB.MINIMIZE)

    m.write('assignment.lp')  # 儲存此排班表

    # Optimize
    m.optimize()


if __name__ == '__main__':
    main()
