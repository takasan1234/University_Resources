from docplex.mp.model import Model

# Create a model
model = Model(name='simple_lp')

# Variable definition
x = model.continuous_var(name='x')
y = model.continuous_var(name='y')

# Objective function: Maximize 3x + 4y 
model.maximize(3 * x + 4 * y)

# Constraints
model.add_constraint(x + 2 * y <= 14)
model.add_constraint(3 * x - y >= 0)
model.add_constraint(x - y <= 2)

# Solve
solution = model.solve()

# Display the result
if solution:
    print(f"x = {x.solution_value}")
    print(f"y = {y.solution_value}")
    print(f"Maximum value: {solution.objective_value}")
else:
    print("No solution was found")

