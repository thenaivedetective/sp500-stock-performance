from pulp import *

N = 4
D = [35000, 50000, 30000, 60000]
I0 = 10000
cost_Regular = 200
cost_OT = 250
cost_Inventory = 50
UB_RP = 40000

model = LpProblem('Inventory_Planning', LpMinimize)

x = [LpVariable(f'x_{i+1}', lowBound=0, upBound=UB_RP) for i in range(N)]
y = [LpVariable(f'y_{i+1}', lowBound=0) for i in range(N)]
I = [LpVariable(f'I_{i+1}', lowBound=0) for i in range(N)]

model += lpSum(cost_Regular * x[i] + cost_OT * y[i] + cost_Inventory * I[i] for i in range(N))

model += (I[0] == I0 + x[0] + y[0] - D[0])
for i in range(1, N):
    model += (I[i] == I[i-1] + x[i] + y[i] - D[i])

model.solve(PULP_CBC_CMD(msg=0))

x_sol = {i+1: value(x[i]) for i in range(N)}
y_sol = {i+1: value(y[i]) for i in range(N)}
I_sol = {i+1: value(I[i]) for i in range(N)}

print("=" * 50)
print("INVENTORY PLANNING - OPTIMAL SOLUTION")
print("=" * 50)
print(f"Status: {LpStatus[model.status]}")
print(f"Optimal Objective Function Value: ${value(model.objective):,.2f}")
print()
print(f"{'Quarter':<10} {'Regular Prod':>14} {'Overtime Prod':>14} {'Inventory':>12}")
print("-" * 52)
for i in range(N):
    print(f"Q{i+1:<9} {x_sol[i+1]:>14,.0f} {y_sol[i+1]:>14,.0f} {I_sol[i+1]:>12,.0f}")
print()
print(f"Value of x (regular production): {x_sol}")
print(f"Value of y (overtime production): {y_sol}")
print(f"Value of I (inventory):           {I_sol}")
