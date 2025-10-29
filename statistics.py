import matplotlib.pyplot as plt

# Podaci
elitism_sizes = [1, 10, 30]

# Easy Sudoku
time_sa_easy = [14.15, 6.15, 15.9]
fitness_easy_no_sa = [-8, -4, -7]

# World's Most Difficult Sudoku
time_sa_hard = [20, 5.9, 16]
fitness_hard_no_sa = [-10, -10, -10]

# Kreiranje figure i osa
fig, ax1 = plt.subplots(figsize=(10,6))

# Leva osa - vreme
ax1.set_xlabel('Elitism Size')
ax1.set_ylabel('Vreme izvršavanja (s)', color='tab:blue')
ax1.plot(elitism_sizes, time_sa_easy, marker='o', label='Easy Sudoku SA', color='tab:blue')
ax1.plot(elitism_sizes, time_sa_hard, marker='o', label='World Most Difficult SA', color='tab:cyan')
ax1.tick_params(axis='y', labelcolor='tab:blue')
ax1.set_xticks(elitism_sizes)

# Desna osa - fitness
ax2 = ax1.twinx()
ax2.set_ylabel('Fitness bez SA (konflikti)', color='tab:green')
ax2.plot(elitism_sizes, fitness_easy_no_sa, marker='x', linestyle='--', label='Easy Sudoku no SA', color='tab:green')
ax2.plot(elitism_sizes, fitness_hard_no_sa, marker='x', linestyle='--', label='World Most Difficult no SA', color='tab:olive')
ax2.tick_params(axis='y', labelcolor='tab:green')

# Legenda
lines, labels = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines + lines2, labels + labels2, loc='upper center')

plt.title('Poređenje vremena i fitness vrednosti za različite elitismSize')
plt.grid(True)
plt.show()
