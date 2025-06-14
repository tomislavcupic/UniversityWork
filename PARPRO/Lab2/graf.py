
import matplotlib.pyplot as plt

# Podaci iz tablice
procesori = [1, 2, 3, 4, 5, 6, 7, 8]
vrijeme = [18.05, 19.42, 13.58, 11.16, 7.96, 7.43, 6.87, 4.71]

# Izračun ubrzanja (Speedup)
idealno_ubrzanje = procesori
izmjereno_ubrzanje = [vrijeme[0] / t for t in vrijeme]

# Izračun učinkovitosti
ucinkovitost = [s / p for s, p in zip(izmjereno_ubrzanje, procesori)]

# Crtanje grafikona
fig, axs = plt.subplots(2, 1, figsize=(8, 8))

# Graf ubrzanja
axs[0].plot(procesori, idealno_ubrzanje, label='idealno', color='steelblue', linewidth=2)
axs[0].plot(procesori, izmjereno_ubrzanje, label='izmjereno', color='darkorange', linewidth=2)
axs[0].set_title("ubrzanje")
axs[0].legend()

# Graf učinkovitosti
axs[1].plot(procesori, ucinkovitost, color='steelblue', linewidth=2)
axs[1].set_title("učinkovitost")

# Prikaz grafova
plt.tight_layout()
plt.show()
