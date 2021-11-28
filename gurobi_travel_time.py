import gurobipy as gp
from gurobipy import GRB
import numpy as np
import map_travel_time as mtt
import taxi_dataset
import taxi_dataset as td


# W是一个嵌套列表
# 全局变量
lam = 1
T_od = []

# 选择模型
Model = gp.Model("SOCP_Model")

# 选择参数
taxi_data = taxi_dataset.taxi_data
pickup_datetime = taxi_data.pickup_datatime  # 乘客上出租车的时刻
dropoff_datetime = taxi_data.dropoff_datetime  # 乘客离开出租车的时刻
Time_od = dropoff_datetime - pickup_datetime   # 乘客在出租车上花费的时间，即旅行时间

# 添加变量
T_od_Estimation = Model.addVar(vtype=GRB.CONTINUOUS,name='T_od_Estimation')  # 旅行时间的估计量
t_ij = Model.addVar(vtype=GRB.CONTINUOUS,name="t_ij") # 每一小段弧旅行时间的估计量
t_kl = Model.addVar(vtype=GRB.CONTINUOUS,name="t_kl") # 每一小段弧旅行时间的估计量
x_od = Model.addVar(vtype=GRB.CONTINUOUS,name="x_od") # 旅行时间的估计量与真实旅行时间的比
a_ij = Model.addVar(vtype=GRB.CONTINUOUS,name='a_ij') # 边界
n_od = Model.addVar(vtype=GRB.CONTINUOUS,name="n_od") # 从o点到d点的可行路径的数量
d_ij = Model.addVar(vtype=GRB.CONTINUOUS,name="d_ij") # 每一小段弧的长度
d_kl = Model.addVar(vtype=GRB.CONTINUOUS,name="d_kl") # 每一小段弧的长度

# 添加目标函数
Model.setObjective(np.sum(n_od * x_od) + lam * np.sum(np.abs(t_ij/d_ij-t_kl/d_kl)*2/(d_ij+d_kl)), GRB.MINIMIZE)

# 添加约束
Model.addConstr(T_od_Estimation == np.sum(t_ij),"c0")
Model.addConstr(T_od_Estimation >= np.sum(t_ij),"c1")
Model.addConstr(x_od >= T_od_Estimation/T_od,"c2")
Model.addConstr(t_ij >= a_ij,"c3")
Model.addConstr([T_od_Estimation-x_od]@[4*np.power(T_od,2)]<=(x_od+T_od_Estimation)*(x_od+T_od_Estimation))

# 求解
Model.optimize()
for v in Model.getVars():
    print('%s %g'%(v.varName,v.x))
print('Obj: %g' % Model.objVal)