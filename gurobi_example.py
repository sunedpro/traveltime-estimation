import gurobipy as gp
from gurobipy import GRB


m = gp.Model("lp")
x = m.addVar(vtype=GRB.CONTINUOUS,name="x")
y = m.addVar(vtype=GRB.CONTINUOUS,name="y")
z = m.addVar(vtype=GRB.CONTINUOUS,name="z")

m.setObjective(x + y + 2*z, GRB.MAXIMIZE)
m.addConstr(x + 2*y + 3*z <=4,"c0")
m.addConstr(x + y >= 1, "c1")
m.optimize()

for v in m.getVars():
    print('%s %g'%(v.varName,v.x))
print('Obj: %g' % m.objVal)

# except gp.GurobiError as e:
#     print('Error code' + str(e.error) + 'e.errno' + ':'+ str(e))
# except AttributeError:
#     print('Encountered an attribute error')