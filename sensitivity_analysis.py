# Topic: sensitivity analysis

from docplex.mp.model import Model

# Define the Model ###
mdl = Model(name='telephone_production')

# Variables
# The continuous variable desk represents the production of desk telephones.
# The continuous variable cell represents the production of cell phones.
desk = mdl.continuous_var(name='desk', lb=0)
cell = mdl.continuous_var(name='cell', lb=0)

# Constraints
# Production machines daily availability (8 hours)
# Factory opening hours
ct_machine_1 = mdl.add_constraint(2 * desk + 1 * cell <= 8)
ct_machine_2 = mdl.add_constraint(1 * desk + 2 * cell <= 8)
ct_factory = mdl.add_constraint(3 * desk + 3 * cell <= 24)

# Objective Function
mdl.maximize(300 * desk + 200 * cell)

# Model information
mdl.print_information()

# Solve the model
s = mdl.solve()

# Display solution
s.display()

# Constraints ###
# Get Shadow prices (called dual values in CPLEX)
print(f"The shadow price for constraint of machine 1 is: {ct_machine_1.dual_value} - its basis status is {ct_machine_1.basis_status.name}.")
print(f"The shadow price for constraint of machine 2 is: {ct_machine_2.dual_value} - its basis status is {ct_machine_2.basis_status.name}.")
print(f"The shadow price for constraint of factory is: {ct_factory.dual_value} - its basis status is {ct_factory.basis_status.name}.")

# Accessing slack values
print(f'The slack value for constraint of machine 1 is: {ct_machine_1.slack_value} - its basis status is {ct_machine_1.basis_status.name}.')
print(f'The slack value for constraint of machine 2 is: {ct_machine_2.slack_value} - its basis status is {ct_machine_2.basis_status.name}.')
print(f'The slack value for constraint of factory is: {ct_factory.slack_value} - its basis status is {ct_factory.basis_status.name}.')

# Allowable increase/decrease for RHS of constraints
cpx = mdl.get_engine().get_cplex()
print(cpx.solution.sensitivity.rhs())

# Relaxing constraints
# I want to buy 4 extra hours of machine 1 (the one with greater shadow prices)
# What is the maximum price I can pay? 133.333
# Let's say we pay 100 for each hour, therefore:
overtime = mdl.continuous_var(name='overtime', ub=4)
ct_machine_1.rhs = ct_machine_1.rhs.solution_value + overtime
mdl.maximize(300 * desk + 200 * cell - 100 * overtime)
s1 = mdl.solve()
s1.display()

# Coefficients ###
# Allowable increase/decrease of objective function coefficients.
print(f"We can move the first objective function coefficient in a range of {cpx.solution.sensitivity.objective()[0]} without changing the optimal solution, assuming all other coefficients remain constant.")
print(f"We can move the second objective function coefficient in a range of {cpx.solution.sensitivity.objective()[1]} without changing the optimal solution, assuming all other coefficients remain constant.")
# Let's try
mdl.maximize(300 * desk + 600 * cell)
s2 = mdl.solve()
mdl.maximize(300 * desk + 700 * cell)
s3 = mdl.solve()
s.display()
s2.display()
s3.display()

# Decision variables ###
print('* desk variable has reduced cost: {0}'.format(desk.reduced_cost))
print('* cell variable has reduced cost: {0}'.format(cell.reduced_cost))