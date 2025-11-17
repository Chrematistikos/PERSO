# Dette_Streamlit.py
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# =============================================================================
# INTERFACE UTILISATEUR
# =============================================================================
st.title("Simulation de la dette publique")

# Paramètres ajustables
r = st.sidebar.number_input("Taux d'intérêt (r)", value=0.025, step=0.001)
g = st.sidebar.number_input("Taux de croissance (g)", value=0.018, step=0.001)
x0 = st.sidebar.number_input("Dette initiale (% PIB)", value=1.15, step=0.01)
s0 = st.sidebar.number_input("Solde primaire initial (% PIB)", value=-0.032, step=0.01)
x_Obj = st.sidebar.number_input("Objectif de dette (% PIB)", value=1.0, step=0.01)
t = st.sidebar.number_input("Durée courte (années)", value=5, step=1)
n = st.sidebar.number_input("Durée pour objectif de dette (années)", value=10, step=1)
effort = st.sidebar.number_input("Effort annuel max pour lissage", value=0.005, step=0.001)
a0 = st.sidebar.number_input("Année de départ", value=2025, step=1)

# =============================================================================
# FONCTIONS
# =============================================================================
def d(x, s):
    return ((1 + r) / (1 + g)) * x - s

def s_stable(x):
    return ((r - g) / (1 + g)) * x

def x_stable(s):
    return s / ((1 + r) / (1 + g) - 1)

# =============================================================================
# 1. SITUATION ACTUELLE
# =============================================================================
st.header("1️⃣ Situation actuelle (sans ajustement)")
x_star1 = x_stable(s0)
y_star1 = x_star1
st.write(f"Point fixe calculé : {x_star1*100:.4f}% du PIB")

delta = abs(x0) * 2 if x0 != 0 else 1
x_vals = np.linspace(x0 - delta, x0 + delta, 500)
y_vals = d(x_vals, s0)

fig, ax = plt.subplots(figsize=(10,7))
ax.plot(x_vals, y_vals, label=r'$y = \frac{1 + r}{1 + g}x - s$', color='red', linewidth=1)
ax.plot(x_vals, x_vals, label=r'$y = x$', color='blue', linewidth=1)
ax.scatter(x_star1, y_star1, color='red', s=60, zorder=5, label=f'Point fixe ({x_star1:.4f})')
ax.plot([x_star1, x_star1], [0, y_star1], color='gray', linestyle='--', linewidth=1)
ax.plot([0, x_star1], [y_star1, y_star1], color='gray', linestyle='--', linewidth=1)
ax.axhline(y=0, color='black', linewidth=1)
ax.axvline(x=0, color='black', linewidth=1)

ax.set_xlim(x0 - delta, x0 + delta)
ax.set_ylim(x0 - delta, x0 + delta)

dette_prev1 = []
solde_prev1 = []
xn = x0
dette_prev1.append(xn*100)
solde_prev1.append(s_stable(xn)*100)

for n_iter in range(t):
    yn = d(xn, s0)
    dette_prev1.append(yn*100)
    solde_prev1.append(s_stable(xn)*100)
    # verticale : de (xn, xn) à (xn, yn)
    ax.plot([xn, xn], [xn, yn], color='green', linewidth=1)
    # horizontale : de (xn, yn) à (yn, yn)
    ax.plot([xn, yn], [yn, yn], color='green', linewidth=1)
    xn = yn

ax.scatter(x0, x0, color='black', s=60, zorder=5, label=f'Dette actuelle ({x0:.4f})')

ax.set_title('Dynamique de la dette')
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.grid(True, linestyle=':')
ax.legend()
st.pyplot(fig)


annee1 = [a0 + i for i in range(len(dette_prev1))]

# Graphiques
st.subheader("Trajectoire de la dette")
fig, ax = plt.subplots(figsize=(10,5))
ax.plot(annee1, dette_prev1, marker='o', linestyle='-')
ax.set_xlabel("Années")
ax.set_ylabel("Dette en % du PIB")
ax.grid(True, linestyle=':')
st.pyplot(fig)

st.subheader("Trajectoire du solde stabilisant la dette")
fig2, ax2 = plt.subplots(figsize=(10,5))
ax2.plot(annee1, solde_prev1, marker='o', linestyle='-')
ax2.set_xlabel("Années")
ax2.set_ylabel("Solde stabilisant (% PIB)")
ax2.grid(True, linestyle=':')
st.pyplot(fig2)

# =============================================================================
# 2. Ajustement permanent
# =============================================================================
st.header("2️⃣ Ajustement budgétaire permanent")
s_star2 = s_stable(x0)
st.write(f"Solde primaire stabilisant : {s_star2*100:.4f}% du PIB")
x_star2 = x_stable(s_star2)

x = x0
dette_prev2 = [x*100]
for _ in range(t):
    x = d(x, s_star2)
    dette_prev2.append(x*100)

annee2 = [a0 + j for j in range(len(dette_prev2))]
fig3, ax3 = plt.subplots(figsize=(10,5))
ax3.plot(annee2, dette_prev2, marker='o', linestyle='-', color='blue')
ax3.set_xlabel("Années")
ax3.set_ylabel("Dette en % du PIB")
ax3.grid(True, linestyle=':')
st.pyplot(fig3)

# =============================================================================
# 3. Ajustement lissé
# =============================================================================
st.header("3️⃣ Ajustement lissé")
x = x0
s3 = s0
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

annee3 = [a0 + j for j in range(len(dette_prev3))]
fig4, ax4 = plt.subplots(figsize=(10,5))
ax4.plot(annee3, solde_traj3, color='blue', marker='o', linestyle='-', label='Solde appliqué')
ax4.plot(annee3, solde_star3, color='red', marker='o', linestyle='-', label='Solde stabilisant')
ax4.set_xlabel("Années")
ax4.set_ylabel("Solde en % du PIB")
ax4.grid(True, linestyle=':')
ax4.legend()
st.pyplot(fig4)

# =============================================================================
# 4. Réduction de dette vers objectif
# =============================================================================
st.header("4️⃣ Réduction de dette vers objectif")
x4 = x0
s4 = s0
delta4 = (x0 - x_Obj)/n
dette_prev4 = []
solde_star4 = []

for _ in range(n):
    x4 = d(x4, s4)
    s4 = ((1+r)/(1+g)-1)*x4 + delta4
    solde_star4.append(s4*100)
    dette_prev4.append(x4*100)

annee4 = [a0 + j for j in range(len(dette_prev4))]
fig5, ax5 = plt.subplots(figsize=(10,5))
ax5.plot(annee4, dette_prev4, color='blue', marker='o', linestyle='-')
ax5.set_xlabel("Années")
ax5.set_ylabel("Dette en % du PIB")
ax5.grid(True, linestyle=':')
st.pyplot(fig5)

fig6, ax6 = plt.subplots(figsize=(10,5))
ax6.plot(annee4, solde_star4, color='red', marker='o', linestyle='-')
ax6.set_xlabel("Années")
ax6.set_ylabel("Solde en % du PIB")
ax6.grid(True, linestyle=':')
st.pyplot(fig6)

# =============================================================================
# 5. Réduction de dette avec solde constant
# =============================================================================
st.header("5️⃣ Réduction de dette avec solde constant")
alpha = (1 + r) / (1 + g)
s_const = (alpha**n * x0 - x_Obj) * (1 - alpha) / (1 - alpha**n)
st.write(f"Solde primaire constant nécessaire : {s_const*100:.4f}% du PIB")

x = x0
dette_const = [x*100]
solde_const = [s_const*100]

for _ in range(n):
    x = d(x, s_const)
    dette_const.append(x*100)
    solde_const.append(s_const*100)

annee_const = [a0 + i for i in range(len(dette_const))]
fig7, ax7 = plt.subplots(figsize=(10,5))
ax7.plot(annee_const, dette_const, color='red', marker='o', linestyle='-')
ax7.set_xlabel("Années")
ax7.set_ylabel("Dette en % du PIB")
ax7.grid(True, linestyle=':')
st.pyplot(fig7)

fig8, ax8 = plt.subplots(figsize=(10,5))
ax8.plot(annee_const, solde_const, color='blue', marker='o', linestyle='-')
ax8.set_xlabel("Années")
ax8.set_ylabel("Solde en % du PIB")
ax8.grid(True, linestyle=':')
st.pyplot(fig8)

st.write(f"Dette initiale : {dette_const[0]:.2f}% du PIB")
st.write(f"Dette finale après {n} ans : {dette_const[-1]:.2f}% du PIB")

