# -*- coding: utf-8 -*-
"""
Created on Wed March 20 13:53:10 2024

@author: npatankar
"""


# Code 1: Inventory Planning Problem Lecture 15 

# Step 1: Add the Basic Packages

from pandas import *
from numpy import *
from gurobipy import *

import sys

# Step 2: Setup the parameters for the model

N = 3 # Number of quarters (Q3 removed)
D = [35000,50000,60000] # Demand for each Quarter (Q1, Q2, Q4)
I0 = 10000 #Starting or initial Inventory
cost_Regular = 200 # Cost of Regular Production
cost_OT = 250 # Cost of Overtime Production
cost_Inventory = 100 # Cost of Inventory holding cost/quarter (updated from 50)
UB_RP = 40000 # Upper Bound in Regular Production


def solve_model(cost_Inventory):

    #Step 3: Setup Indices for Decision Variables

    idx_x, c_x = multidict({(i+1):cost_Regular for i in range(N)}) # Index for x variable
    idx_y, c_y = multidict({(i+1):cost_OT for i in range(N)}) # Index for y variable
    idx_I, c_I = multidict({(i+1):cost_Inventory for i in range(N)}) # Index for I variable

    # Step 4: Setup a LP model

    model = Model('Inventory Planning')
    model.Params.OutputFlag = 0

    # Step 5: Add Decision Variables to the Model

    x = model.addVars(idx_x, obj=c_x, lb=0, name='x')
    y = model.addVars(idx_y, obj=c_y, lb=0, name='y')
    I = model.addVars(idx_I, obj=c_I, lb=0, name='I')

    model.update()

    # Step 6: Add Constraints to the Model

    ## Constraint: I_1 = I_0 + x_1 + y_1 - Demand_1
    model.addConstr(I[1] == I0 + x[1] + y[1] - D[0])
    model.update()

    ## Constraint: I_2 = I_1 + x_2 + y_2 - Demand_2
    model.addConstr(I[2] == I[1] + x[2] + y[2] - D[1])
    model.update()

    ## Constraint: I_3 = I_2 + x_3 + y_3 - Demand_3 (was Q4)
    model.addConstr(I[3] == I[2] + x[3] + y[3] - D[2])
    model.update()

    ## Constraint: x_1 <= UB_RP
    model.addConstr(x[1] <= UB_RP)
    model.update()

    ## Constraint: x_2 <= UB_RP
    model.addConstr(x[2] <= UB_RP)
    model.update()

    ## Constraint: x_3 <= UB_RP
    model.addConstr(x[3] <= UB_RP)
    model.update()

    # Step 7: Solve the LP
    model.Params.Method = 0
    model.update()
    model.optimize()

    # Step 8: Determine Optimal Solution and other values

    Optimal_Value = model.ObjVal

    Sol = []
    for var in model.getVars():
        Sol.append(var.x)

    x_sol = {i+1: Sol[i] for i in range(N)}
    y_sol = {i+1: Sol[N+i] for i in range(N)}
    I_sol = {i+1: Sol[2*N+i] for i in range(N)}

    RC = []
    for var in model.getVars():
        RC.append(var.RC)

    x_RC = {i+1: RC[i] for i in range(N)}
    y_RC = {i+1: RC[N+i] for i in range(N)}
    I_RC = {i+1: RC[2*N+i] for i in range(N)}

    pi = []
    for cons in model.getConstrs():
        pi.append(cons.pi)

    Dual_inventory = {i+1: pi[i] for i in range(N)}
    Dual_RP_UB = {i+1: pi[N+i] for i in range(N)}

    total_units = sum(x_sol[i+1] + y_sol[i+1] for i in range(N))
    avg_cost_per_unit = Optimal_Value / total_units if total_units > 0 else 0

    return {
        "Optimal_Value": Optimal_Value,
        "x_sol": x_sol,
        "y_sol": y_sol,
        "I_sol": I_sol,
        "x_RC": x_RC,
        "y_RC": y_RC,
        "I_RC": I_RC,
        "Dual_inventory": Dual_inventory,
        "Dual_RP_UB": Dual_RP_UB,
        "total_units": total_units,
        "avg_cost_per_unit": avg_cost_per_unit
    }


# Solve for both scenarios
results_before = solve_model(cost_Inventory=50)   # Original inventory cost
results_after  = solve_model(cost_Inventory=100)  # Updated inventory cost

# Step 9: Set up the output file

old_stdout = sys.stdout
log_file = open("Inventory_Model_Solution.txt", "w")
sys.stdout = log_file

print("===== BEFORE (Inventory Cost = $50) =====")
print({"Optimal Objective Function Value": results_before["Optimal_Value"]})
print({"Value of x": results_before["x_sol"]})
print({"Value of y": results_before["y_sol"]})
print({"Value of I": results_before["I_sol"]})
print({"RC of x": results_before["x_RC"]})
print({"RC of y": results_before["y_RC"]})
print({"RC of I": results_before["I_RC"]})
print({"Dual of Inventory Constraints": results_before["Dual_inventory"]})
print({"Dual of UB on x": results_before["Dual_RP_UB"]})
print({"Total Units Produced": results_before["total_units"]})
print({"Average Cost Per Unit (Before)": round(results_before["avg_cost_per_unit"], 2)})

print()
print("===== AFTER (Inventory Cost = $100) =====")
print({"Optimal Objective Function Value": results_after["Optimal_Value"]})
print({"Value of x": results_after["x_sol"]})
print({"Value of y": results_after["y_sol"]})
print({"Value of I": results_after["I_sol"]})
print({"RC of x": results_after["x_RC"]})
print({"RC of y": results_after["y_RC"]})
print({"RC of I": results_after["I_RC"]})
print({"Dual of Inventory Constraints": results_after["Dual_inventory"]})
print({"Dual of UB on x": results_after["Dual_RP_UB"]})
print({"Total Units Produced": results_after["total_units"]})
print({"Average Cost Per Unit (After)": round(results_after["avg_cost_per_unit"], 2)})

sys.stdout = old_stdout
log_file.close()
