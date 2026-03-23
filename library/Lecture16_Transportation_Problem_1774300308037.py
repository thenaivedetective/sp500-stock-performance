# -*- coding: utf-8 -*-
"""
Created on Wed March 20 16:52:37 2024

@author: npatankar
"""


# Code 2: Transportation Problem Lecture 16

# Step 1: Add the Basic Packages

from pandas import *
from numpy import *
from gurobipy import *

# Step 2: Setup the parameters for the model

m = 3 # Number of Supply Centers 
n = 4 # Number of Demand Centers 
S = [35,50,40] # Max Supply
D = [45,20,30,30] # Demand requirements
Cost_Vector = [8,6,10,9,9,12,13,7,14,9,16,5] # c_{ij}= Const_Vector[i*n+j]

#Step 3: Setup Indices for Decision Variables

idx_x, c = multidict({(i+1,j+1):Cost_Vector[i*n+j] for i in range(m) for j in range(n)}) # Index for x variable


# Step 4: Setup a LP model 

model = Model('Transportation Problem')

# Step 5: Add Decision Variables to the Model

# General Syntax: addVars(*indices, lb=, ub=, obj=, vtype=GRB.CONTINUOUS, name="" ) 
# Gurobi Url: https://www.gurobi.com/documentation/9.5/refman/py_model_addvars.html 

x = model.addVars(idx_x,obj = c,lb = 0, name = 'x') 


model.update()  # Update the Model

# Step 6: Add Constraints to the Model
# General Syntex: addConstr(constr, name="" ) 
# Gurobi Url: https://www.gurobi.com/documentation/9.5/refman/py_model_addconstr.html

## Supply Constraints

model.addConstrs(x.sum(i+1,'*') <= S[i] for i in range(m))
model.update()  # Update the Model


## Demand Constraints

model.addConstrs(x.sum('*',j+1) >= D[j] for j in range(n))
model.update()  # Update the Model

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

x_sol = {(i+1,j+1): Sol[i*n+j] for i in range(m) for j in range(n)}



## Reduced Cost Calculations
 
RC = []
for var in model.getVars():
    RC.append(var.RC)

x_RC =  {(i+1,j+1): RC[i*n+j] for i in range(m) for j in range(n)} # First N variables are x

    

## Calculation of Dual Variables
## Constraint Attribute Url: https://www.gurobi.com/documentation/9.5/refman/linear_constraint_attribut.html

pi = []
for cons in model.getConstrs():
    pi.append(cons.pi)
    
Dual_Supply_Cons = {i+1: pi[i] for i in range(m)} # First m constraints are Supply Constraints

Dual_Demand_Cons = {j+1: pi[m+j] for j in range(n)} # Next n constraints are Demand Constraints
    
# Step 9: Set up the output file 

import sys

old_stdout = sys.stdout

log_file = open("Transportation_Model_Solution.txt","w")

sys.stdout = log_file

#  Print all important values calculated above
print({"Optimal Objective Function Value": Optimal_Value})
print({"Value of x": x_sol})
print({"RC of x": x_RC})
print({"Dual of Supply Constraints": Dual_Supply_Cons})
print({"Dual of Demand Constraints": Dual_Demand_Cons})

sys.stdout = old_stdout
log_file.close()




