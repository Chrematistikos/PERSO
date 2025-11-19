import numpy as np
import matplotlib.pyplot as plt

# =============================================================================
# PARAMÈTRES GÉNÉRAUX
# =============================================================================
r = 0.025          # taux d'intérêt
g = 0.018          # taux de croissance
s0 = -0.032        # solde primaire initial
x0 = 1.15          # dette initiale (% du PIB)
t = 5              # nombre d'années pour la simulation courte
a0 = 2025          # année de départ
effort = 0.005     # effort annuel maximum pour lissage
n = 10             # durée pour atteindre l'objectif de dette
x_Obj = 1          # objectif de dette (% du PIB)

# =============================================================================
# FONCTIONS UTILES
# =============================================================================
def d(x, s):
    """Évolution de la dette selon le solde primaire."""
    return ((1 + r) / (1 + g)) * x - s

def s_stable(x):
    """Solde primaire stabilisant la dette pour un niveau de dette x."""
    return ((r - g) / (1 + g)) * x

def x_stable(s):
    """Dette stable correspondant à un solde primaire donné."""
    return s / ((1 + r) / (1 + g) - 1)

# =============================================================================
# 1. SITUATION ACTUELLE (SANS AJUSTEMENT)
# =============================================================================
print("\n" + "="*50)
print("SITUATION ACTUELLE")
print("="*50)

x_star1 = x_stable(s0)
y_star1 = x_star1

print(f"Point fixe calculé: {x_star1*100:.4f}% du PIB")

# Définition du domaine autour du point fixe pour le graphique
delta = abs(x_star1) * 2 if x_star1 != 0 else 1
x_vals = np.linspace(x_star1 - delta, x_star1 + delta, 500)
y_vals = d(x_vals, s0)

# --- Tracé des fonctions et point fixe ---
plt.figure(figsize=(10,7))
plt.plot(x_vals, y_vals, label=r'$y = \frac{1 + r}{1 + g}x - s$', color='red', linewidth=1)
plt.plot(x_vals, x_vals, label=r'$y = x$', color='blue', linewidth=1)
plt.scatter(x_star1, y_star1, color='red', s=60, zorder=5, label=f'Point fixe ({x_star1:.4f})')
plt.plot([x_star1, x_star1], [0, y_star1], color='gray', linestyle='--', linewidth=1)
plt.plot([0, x_star1], [y_star1, y_star1], color='gray', linestyle='--', linewidth=1)
plt.axhline(y=0, color='black', linewidth=1)
plt.axvline(x=0, color='black', linewidth=1)
plt.xlim(x_star1 - delta, x_star1 + delta)
plt.ylim(y_star1 - delta, y_star1 + delta)
plt.title('Dynamique de la dette - Situation actuelle')
plt.xlabel('x')
plt.ylabel('y')
plt.grid(True, linestyle=':')
plt.legend()

# --- Simulation de la dynamique ---
dette_prev1 = []
s_star_prev = []
xn = x0
dette_prev1.append(xn*100)
s_star_prev.append(s_stable(xn)*100)

for _ in range(t):
    yn = d(xn, s0)
    dette_prev1.append(yn*100)
    plt.plot([xn, xn], [xn, yn], color='green', linewidth=1)
    plt.plot([xn, yn], [yn, yn], color='green', linewidth=1)
    xn = yn
    s_star_prev.append(s_stable(xn)*100)

plt.scatter(x0, x0, color='black', s=60, zorder=5, label=f'Dette actuelle ({x0:.4f})')
plt.show()

# --- Trajectoire de la dette et du solde ---
annee1 = [a0 + j for j in range(len(dette_prev1))]

plt.figure(figsize=(10,6))
plt.plot(annee1, dette_prev1, marker='o', linestyle='-')
plt.xlabel('Années')
plt.ylabel('Dette en % du PIB')
plt.title('Trajectoire de la dette')
plt.grid(True, linestyle=':')
plt.show()

plt.figure(figsize=(10,6))
plt.plot(annee1, s_star_prev, marker='o', linestyle='-')
plt.xlabel('Années')
plt.ylabel('Solde stabilisant la dette en % du PIB')
plt.title('Trajectoire du solde stabilisant')
plt.grid(True, linestyle=':')
plt.show()

# =============================================================================
# 2. AVEC AJUSTEMENT BUDGÉTAIRE PERMANENT
# =============================================================================
print("\n" + "="*50)
print("AVEC AJUSTEMENT")
print("="*50)

s_star2 = s_stable(x0)
print(x0,s_star2)
print(f"Solde primaire stabilisant: {s_star2*100:.4f}% du PIB")

x_star2 = x_stable(s_star2)
y_star2 = x_star2
print(f"Nouveau point fixe: {x_star2*100:.4f}% du PIB")

delta = abs(x_star2) * 2 if x_star2 != 0 else 1
x_vals = np.linspace(x_star2 - delta, x_star2 + delta, 500)
y_vals = d(x_vals, s_star2)

plt.figure(figsize=(10,7))
plt.plot(x_vals, y_vals, label=r'$y = \frac{1 + r}{1 + g}x - s$', color='red', linewidth=1)
plt.plot(x_vals, x_vals, label=r'$y = x$', color='blue', linewidth=1)
plt.scatter(x_star2, y_star2, color='red', s=60, zorder=5, label=f'Point fixe ({x_star2:.4f})')
plt.plot([x_star2, x_star2], [0, y_star2], color='gray', linestyle='--', linewidth=1)
plt.plot([0, x_star2], [y_star2, y_star2], color='gray', linestyle='--', linewidth=1)
plt.axhline(y=0, color='black', linewidth=1)
plt.axvline(x=0, color='black', linewidth=1)
plt.xlim(x_star2 - delta, x_star2 + delta)
plt.ylim(y_star2 - delta, y_star2 + delta)

dette_prev2 = []
xn = x0
dette_prev2.append(xn*100)
for _ in range(t):
    yn = d(xn, s_star2)
    dette_prev2.append(yn*100)
    plt.plot([xn, xn], [xn, yn], color='green', linewidth=1)
    plt.plot([xn, yn], [yn, yn], color='green', linewidth=1)
    xn = yn

plt.scatter(x0, x0, color='black', s=60, zorder=5, label=f'Dette actuelle ({x0:.4f})')
plt.title(f'Avec un solde primaire permanent de {s_star2*100:.2f}% du PIB')
plt.xlabel('x')
plt.ylabel('y')
plt.grid(True, linestyle=':')
plt.legend()
plt.show()

annee2 = [a0 + j for j in range(len(dette_prev2))]

plt.figure(figsize=(10,6))
plt.plot(annee2, dette_prev2, marker='o', linestyle='-')
plt.xlabel('Années')
plt.ylabel('Dette en % du PIB')
plt.title('Trajectoire de la dette avec ajustement permanent')
plt.grid(True, linestyle=':')
plt.ylim(0, max(dette_prev2) * 1.1)
plt.show()

# =============================================================================
# 3. AJUSTEMENT LISSÉ
# =============================================================================
print("\n" + "="*50)
print("AVEC AJUSTEMENT LISSÉ")
print("="*50)

x = x0
s3 = s0
i = 0
dette_prev3 = [x*100]
solde_traj3 = [s3*100]
solde_star3 = [s_stable(x)*100]

while s_stable(x) > s3:
    s_target = s_stable(x)
    if s_target - s3 > effort:
        s3 += effort
    else:
        s3 = s_target
    x = d(x, s3)
    dette_prev3.append(x*100)
    solde_traj3.append(s3*100)
    solde_star3.append(s_stable(x)*100)
    i += 1

annee3 = [a0 + j for j in range(len(solde_traj3))]

plt.figure(figsize=(10,6))
plt.plot(annee3, solde_traj3, color='blue', marker='o', linestyle='-', label='Solde appliqué')
plt.plot(annee3, solde_star3, color='red', marker='o', linestyle='-', label='Solde stabilisant')
plt.xlabel('Années')
plt.ylabel('Solde en % du PIB')
plt.title('Trajectoire du solde avec ajustement lissé')
plt.grid(True, linestyle=':')
plt.legend()
plt.show()

# =============================================================================
# 4. RÉDUCTION DE DETTE VERS OBJECTIF
# =============================================================================
print("\n" + "="*50)
print("AVEC RÉDUCTION DE DETTE")
print("="*50)

x4 = x0
s4 = s0
delta4 = (x0 - x_Obj)/n
dette_prev4 = [x4*100]
solde_star4 = [s4*100]

for _ in range(n):
    s4 = ((1+r)/(1+g)-1)*x4 + delta4  # formule corrigée pour réduction linéaire
    x4 = d(x4, s4)
    solde_star4.append(s4*100)
    dette_prev4.append(x4*100)

annee4 = [a0 + j for j in range(len(dette_prev4))]

plt.figure(figsize=(10,6))
plt.plot(annee4, solde_star4, color='blue', marker='o', linestyle='-')
plt.xlabel('Années')
plt.ylabel('Solde en % du PIB')
plt.title('Trajectoire du solde stabilisant objectif de dette')
plt.grid(True, linestyle=':')
plt.show()

plt.figure(figsize=(10,6))
plt.plot(annee4, dette_prev4, color='blue', marker='o', linestyle='-')
plt.xlabel('Années')
plt.ylabel('Dette en % du PIB')
plt.title('Trajectoire de la dette vers objectif')
plt.grid(True, linestyle=':')
plt.show()

# =============================================================================
# 5. RÉDUCTION DE DETTE AVEC SOLDE CONSTANT
# =============================================================================
print("\n" + "="*50)
print("RÉDUCTION DE DETTE - SOLDE CONSTANT")
print("="*50)

# Calcul du solde constant nécessaire
alpha = (1 + r) / (1 + g)
s_const = (alpha**n * x0 - x_Obj) * (1 - alpha) / (1 - alpha**n)
print(f"Solde primaire constant nécessaire : {s_const*100:.4f}% du PIB")

# Simulation de la trajectoire de la dette
x = x0
dette_const = [x * 100]
solde_const = [s_const * 100]

for _ in range(n):
    x = d(x, s_const)
    dette_const.append(x * 100)
    solde_const.append(s_const * 100)

# Axe des années
annee_const = [a0 + i for i in range(len(dette_const))]

# Tracé du solde constant
plt.figure(figsize=(10,6))
plt.plot(annee_const, solde_const, color='blue', marker='o', linestyle='-')
plt.xlabel('Années')
plt.ylabel('Solde en % du PIB')
plt.title('Trajectoire du solde primaire constant')
plt.grid(True, linestyle=':')
plt.show()

# Tracé de la dette associée
plt.figure(figsize=(10,6))
plt.plot(annee_const, dette_const, color='red', marker='o', linestyle='-')
plt.xlabel('Années')
plt.ylabel('Dette en % du PIB')
plt.title('Trajectoire de la dette avec solde constant')
plt.grid(True, linestyle=':')
plt.show()

# Résumé final
print(f"Dette initiale : {dette_const[0]:.2f}% du PIB")
print(f"Dette finale après {n} ans : {dette_const[-1]:.2f}% du PIB")
