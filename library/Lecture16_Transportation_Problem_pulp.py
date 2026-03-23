from pulp import *

m = 3
n = 4
S = [35, 50, 40]
D = [45, 20, 30, 30]
Cost = [
    [8,  6, 10, 9],
    [9, 12, 13, 7],
    [14,  9, 16, 5]
]

model = LpProblem('Transportation_Problem', LpMinimize)

x = [[LpVariable(f'x_{i+1}_{j+1}', lowBound=0) for j in range(n)] for i in range(m)]

model += lpSum(Cost[i][j] * x[i][j] for i in range(m) for j in range(n))

for i in range(m):
    model += (lpSum(x[i][j] for j in range(n)) <= S[i])

for j in range(n):
    model += (lpSum(x[i][j] for i in range(m)) >= D[j])

model.solve(PULP_CBC_CMD(msg=0))

x_sol = {(i+1, j+1): value(x[i][j]) for i in range(m) for j in range(n)}

print("=" * 55)
print("TRANSPORTATION PROBLEM - OPTIMAL SOLUTION")
print("=" * 55)
print(f"Status: {LpStatus[model.status]}")
print(f"Optimal Objective Function Value: {value(model.objective):.2f}")
print()
print("Shipment Plan (from Plant i to City j):")
print(f"{'':10}", end="")
for j in range(n):
    print(f"{'City '+str(j+1):>10}", end="")
print(f"{'Supply Used':>12}")
print("-" * 55)
for i in range(m):
    print(f"Plant {i+1}   ", end="")
    supply_used = 0
    for j in range(n):
        val = x_sol[(i+1, j+1)]
        print(f"{val:>10.1f}", end="")
        supply_used += val
    print(f"{supply_used:>12.1f}  (max {S[i]})")
print("-" * 55)
print(f"{'Demand Met':10}", end="")
for j in range(n):
    met = sum(x_sol[(i+1, j+1)] for i in range(m))
    print(f"{met:>10.1f}", end="")
print()
print()
print(f"Full solution: {x_sol}")
