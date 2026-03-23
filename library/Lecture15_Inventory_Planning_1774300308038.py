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

# Step 2: Setup the parameters for the model

N = 4 # Number of quarters
D = [35000,50000,30000,60000] # Demand for each Quarter 
I0 = 10000 #Starting or initial Inventory
cost_Regular = 200 # Cost of Regular Production
cost_OT = 250 # Cost of Overtime Production
cost_Inventory = 100 # Cost of Inventory holding cost/quarter
UB_RP = 40000 # Upper Bound in Regular Production

#Step 3: Setup Indices for Decision Variables

idx_x, c_x =multidict({(i+1):cost_Regular  for i in range(N)}) # Index for x variable
idx_y, c_y =multidict({(i+1):cost_OT  for i in range(N)}) # Index for y variable
idx_I, c_I =multidict({(i+1):cost_Inventory  for i in range(N)}) # Index for y variable


# Step 4: Setup a LP model 

model = Model('Inventory Planning')

# Step 5: Add Decision Variables to the Model

# General Syntax: addVars(*indices, lb=, ub=, obj=, vtype=GRB.CONTINUOUS, name="" ) 
# Gurobi Url: https://www.gurobi.com/documentation/9.5/refman/py_model_addvars.html 

x = model.addVars(idx_x,obj = c_x,lb = 0,name = 'x') 
y = model.addVars(idx_y,obj = c_y,lb = 0, name = 'y') 
I = model.addVars(idx_I,obj = c_I,lb = 0, name = 'I') 

model.update()  # Update the Model

# Step 6: Add Constraints to the Model
# General Syntex: addConstr(constr, name="" ) 
# Gurobi Url: https://www.gurobi.com/documentation/9.5/refman/py_model_addconstr.html

## Constraint: I_1 = I_0 + x_1 + y_1 - Demand_1;

model.addConstr(I[1] == I0 + x[1] + y[1]-D[0])
model.update()  # Update the Model


## Constraint: I_2 = I_1 + x_2 + y_2 - Demand_2;
model.addConstr(I[2] == I[1] + x[2] + y[2]-D[1])
model.update()  # Update the Model

## Constraint: I_3 = I_2 + x_3 + y_3 - Demand_3;
model.addConstr(I[3] == I[2] + x[3] + y[3]-D[2])
model.update()  # Update the Model

## Constraint: I_4 = I_3 + x_4 + y_4 - Demand_4;
model.addConstr(I[4] == I[3] + x[4] + y[4]-D[3])
model.update()  # Update the Model

### We may add previous three constraints using a single Command using model.addConstrs
# General Syntax: addConstrs(generator, name="" )
# Gurobi Url: https://www.gurobi.com/documentation/9.5/refman/py_model_addconstrs.html 


#model.addConstrs(I[j+1] == I[j] + x[j+1] + y[j+1]-D[j] for j in range(1,N))
#model.update() 


## Constraint: x_1 <= UB_RP 
model.addConstr(x[1] <= UB_RP)
model.update() 


## Constraint: x_2 <= UB_RP 
model.addConstr(x[2] <= UB_RP)
model.update() 


## Constraint: x_3 <= UB_RP 
model.addConstr(x[3] <= UB_RP)
model.update() 


## Constraint: x_4 <= UB_RP 
model.addConstr(x[4] <= UB_RP)
model.update() 

### We may add the previous 4 constraints using a single command using model.addConstrs
#model.addConstrs(x[j+1] <= UB_RP for j in range(N))
#model.update() 

# Step 7: Solve the LP

## May Declare the Method to solve LP: Primal Simplex
## Gurobi Parameters Url: https://www.gurobi.com/documentation/9.5/refman/parameters.html

model.Params.Method = 0 # Optional Command
model.update() 

# Uncomment the following if we would like to Maximize

#model.ModelSense = -1 


model.optimize() # Optimize the model - Min is default



# Step 8: Determine Optimal Solution and other values

## Optimal Objective Function Value
## Gurobi Model Attributes Url: https://www.gurobi.com/documentation/9.5/refman/attributes.html

Optimal_Value = model.ObjVal


## Optimal Solution 
## Variable Attribute Url: https://www.gurobi.com/documentation/9.5/refman/variable_attributes.html
Sol = []
for var in model.getVars():
    Sol.append(var.x)

x_sol = {i+1: Sol[i] for i in range(N)} # First N variables are x

y_sol = {i+1: Sol[N+i] for i in range(N)} #  N+1:2N variables are y

I_sol = {i+1: Sol[2*N+i] for i in range(N)} #  2N+1:3N variable are I


## Reduced Cost Calculations
 
RC = []
for var in model.getVars():
    RC.append(var.RC)

x_RC = {i+1: RC[i] for i in range(N)} # First N variables are x

y_RC = {i+1: RC[N+i] for i in range(N)} #  N+1:2N variables are y

I_RC = {i+1: RC[2*N+i] for i in range(N)} #  2N+1:3N variable are I

    

## Calculation of Dual Variables
## Constraint Attribute Url: https://www.gurobi.com/documentation/9.5/refman/linear_constraint_attribut.html

pi = []
for cons in model.getConstrs():
    pi.append(cons.pi)
    
Dual_inventory = {i+1: pi[i] for i in range(N)} # First N constraints are inventory balance constraints

Dual_RP_UB = {i+1: pi[N+i] for i in range(N)} # Second N constraints are UB Constraints on Regular Production
    
# Step 9: Set up the output file 

import sys

old_stdout = sys.stdout

log_file = open("Inventory_Model_Solution.txt","w")

sys.stdout = log_file

#  Print all important values calculated above
print({"Optimal Objective Function Value": Optimal_Value})
print({"Value of x": x_sol})
print({"Value of y": y_sol})
print({"Value of I": I_sol})
print({"RC of x": x_RC})
print({"RC of y": y_RC})
print({"RC of I": I_RC})
print({"Dual of Inventory Constraints": Dual_inventory})
print({"Dual of UB on x": Dual_RP_UB})

sys.stdout = old_stdout
log_file.close()




