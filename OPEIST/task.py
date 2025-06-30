import pulp
import matplotlib.pyplot as plt
import numpy as np

prob = pulp.LpProblem("Minimalna_cijena_mjesavine_po_vreci", pulp.LpMaximize)

x1 = pulp.LpVariable("x1", lowBound=0, cat='Continuous')
x2 = pulp.LpVariable("x2", lowBound=0, cat='Continuous')

prob += 1 * x1 + 2 * x2, "Ukupna cijena"
prob += -1 * x1 + 1 * x2 <= 2, "Nutritivni element A"
prob += 0 * x1 + 1 * x2 <= 4, "Nutritivni element B"
prob += 1 * x1 + 1 * x2 <= 8, "Nutritivni element C"
prob += 2 * x1 - 1 * x2 <= 10, "Nutritivni element D"
prob.solve()

print("Status:", pulp.LpStatus[prob.status])
print(f"Optimalan broj vrećica P je: {pulp.value(x1)}, a vrećica Q je: {pulp.value(x2)}")
print("Minimalna cijena mješavine po vrećici:", pulp.value(prob.objective))

for name, c in prob.constraints.items():
    print(f"{name}: Sjena (shadow price) {c.pi} - Dodatna  {c.slack}")

x_vals = np.linspace(0, 20, 400)

A_constraint = (18 - 3 * x_vals) / 1.5
B_constraint = (45 - 2.5 * x_vals) / 11.25
C_constraint = (24 - 2 * x_vals) / 3

plt.figure(figsize=(10, 8))

plt.plot(x_vals, A_constraint, label=r'$3x_1 + 1.5x_2 \geq 18$', color='blue')
plt.plot(x_vals, B_constraint, label=r'$2.5x_1 + 11.25x_2 \geq 45$', color='green')
plt.plot(x_vals, C_constraint, label=r'$2x_1 + 3x_2 \geq 24$', color='red')

plt.fill_between(x_vals, np.maximum(A_constraint, 0), 20, color='blue', alpha=0.1)
plt.fill_between(x_vals, np.maximum(B_constraint, 0), 20, color='green', alpha=0.1)
plt.fill_between(x_vals, np.maximum(C_constraint, 0), 20, color='red', alpha=0.1)

plt.xlim((0, 20))
plt.ylim((0, 20))

plt.plot(pulp.value(x1), pulp.value(x2), 'ro', label="Optimalna tocka")
plt.annotate(f'Optimalna točka\n(x1={pulp.value(x1):.2f}, x2={pulp.value(x2):.2f})', xy=(pulp.value(x1), pulp.value(x2)))

plt.xlabel(r'$x_1$ (Broj vrecica marke P)')
plt.ylabel(r'$x_2$ (Broj vrecica marke Q)')
plt.title("Graficko rjesenje LP problema")
plt.legend()
plt.grid(True)
plt.show()