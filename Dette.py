# Dette_Streamlit.py
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# =============================================================================
# INTERFACE UTILISATEUR
# =============================================================================
st.title("Simulation de la dette publique")

# Paramètres ajustables
r = (st.sidebar.number_input("Taux d'intérêt actuel (r)", value=2.25, step=0.01))/100
g = (st.sidebar.number_input("Taux de croissance actuel (g)", value=1.8, step=0.1))/100
s0 = (st.sidebar.number_input("Solde primaire actuel (% PIB)", value=-3.2, step=0.1))/100
x0 = (st.sidebar.number_input("Dette actuelle (% PIB)", value=115.0, step=0.5))/100
a0 = st.sidebar.number_input("Année actuelle", value=2025, step=1)
x_Obj = (st.sidebar.number_input("Objectif de dette (% PIB)", value=100.0, step=0.5))/100
t = st.sidebar.number_input("Durée de projection pour la trajectoire  (années)", value=5, step=1)
n = st.sidebar.number_input("Durée pour atteindre l'objectif de dette (années)", value=10, step=1)
effort = (st.sidebar.number_input("Effort annuel pour l'ajustement progressif (% PIB)", value=0.5,min_value=0.1, step=0.1))/100


# Menu
menu = st.sidebar.radio(
    "Choisissez une section",
    [
        "Situation actuelle",
        "Ajustement instantané",
        "Ajustement progressif",
        "Réduction de dette (solde variable)",
        "Réduction de dette (solde constant)"
    ]
)

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
# 1️⃣ SITUATION ACTUELLE
# =============================================================================
if menu == "Situation actuelle":
    st.header("1️⃣ Situation actuelle")
    x_star1 = x_stable(s0)
    y_star1 = x_star1
    st.write(f"Point fixe calculé : {x_star1*100:.4f}% du PIB")

    delta = abs(x0) * 2 if x0 != 0 else 1
    x_vals = np.linspace(x0 - delta, x0 + delta, 500)
    y_vals = d(x_vals, s0)

    fig, ax = plt.subplots(figsize=(10,7))
    ax.plot(x_vals, y_vals, label=r'$y = \frac{1 + r}{1 + g}x - s$', color='red')
    ax.plot(x_vals, x_vals, label=r'$y = x$', color='blue')
    ax.scatter(x_star1, y_star1, color='red', s=60)
    ax.plot([x_star1, x_star1], [0, y_star1], color='gray', linestyle='--')
    ax.plot([0, x_star1], [y_star1, y_star1], color='gray', linestyle='--')

    ax.set_xlim(x0 - delta, x0 + delta)
    ax.set_ylim(x0 - delta, x0 + delta)

    dette_prev1 = []
    solde_prev1 = []
    xn = x0
    dette_prev1.append(xn*100)
    solde_prev1.append(s_stable(xn)*100)

    for _ in range(t):
        yn = d(xn, s0)
        ax.plot([xn, xn], [xn, yn], color='green')
        ax.plot([xn, yn], [yn, yn], color='green')
        xn = yn
        dette_prev1.append(yn * 100)
        solde_prev1.append(s_stable(xn) * 100)

    st.pyplot(fig)

    annee1 = [a0 + i for i in range(len(dette_prev1))]

    st.subheader("Trajectoire de la dette")
    fig, ax = plt.subplots(figsize=(10,5))
    ax.plot(annee1, dette_prev1, marker='o')
    st.pyplot(fig)

    st.subheader("Trajectoire du solde stabilisant la dette")
    fig2, ax2 = plt.subplots(figsize=(10,5))
    ax2.plot(annee1, solde_prev1, marker='o')
    st.pyplot(fig2)


# =============================================================================
# 2️⃣ AJUSTEMENT INSTANTANÉ
# =============================================================================
if menu == "Ajustement instantané":
    st.header("2️⃣ Ajustement instantané")

    s_star2 = s_stable(x0)
    st.write(f"Solde primaire stabilisant : {s_star2*100:.4f}% du PIB")

    x = x0
    dette_prev2 = [x*100]

    for _ in range(t):
        x = d(x, s_star2)
        dette_prev2.append(x*100)

    annee2 = [a0 + j for j in range(len(dette_prev2))]

    fig3, ax3 = plt.subplots(figsize=(10,5))
    ax3.plot(annee2, dette_prev2, marker='o')
    st.pyplot(fig3)


# =============================================================================
# 3️⃣ AJUSTEMENT PROGRESSIF
# =============================================================================
if menu == "Ajustement progressif":
    st.header("3️⃣ Ajustement progressif")

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
    ax4.plot(annee3, solde_traj3, marker='o', label='Solde appliqué')
    ax4.plot(annee3, solde_star3, marker='o', label='Solde stabilisant')
    ax4.legend()
    st.pyplot(fig4)


# =============================================================================
# 4️⃣ RÉDUCTION DE DETTE – solde variable
# =============================================================================
if menu == "Réduction de dette (solde variable)":
    st.header("4️⃣ Réduction de dette avec solde variable")

    x4 = x0
    s4 = s0
    delta4 = (x0 - x_Obj)/n
    dette_prev4 = []
    solde_star4 = []
    dette_prev4.append(x4*100)

    for _ in range(n):
        s4 = ((1 + r) / (1 + g) - 1) * x4 + delta4
        solde_star4.append(s4 * 100)
        x4 = d(x4, s4)
        dette_prev4.append(x4*100)

    solde_star4.append(s_stable(x4)*100)

    annee4 = [a0 + j for j in range(len(dette_prev4))]

    st.subheader("Trajectoire de la dette")
    fig5, ax5 = plt.subplots(figsize=(10,5))
    ax5.plot(annee4, dette_prev4, marker='o')
    st.pyplot(fig5)

    st.subheader("Trajectoire du solde")
    fig6, ax6 = plt.subplots(figsize=(10,5))
    ax6.plot(annee4, solde_star4, marker='o')
    st.pyplot(fig6)


# =============================================================================
# 5️⃣ RÉDUCTION DE DETTE – solde constant
# =============================================================================
if menu == "Réduction de dette (solde constant)":
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

    solde_const[-1] = s_stable(dette_const[-1])

    annee_const = [a0 + i for i in range(len(dette_const))]

    st.subheader("Trajectoire de la dette")
    fig7, ax7 = plt.subplots(figsize=(10,5))
    ax7.plot(annee_const, dette_const, marker='o')
    st.pyplot(fig7)

    st.subheader("Trajectoire du solde")
    fig8, ax8 = plt.subplots(figsize=(10,5))
    ax8.plot(annee_const, solde_const, marker='o')
    st.pyplot(fig8)

    st.write(f"Dette initiale : {dette_const[0]:.2f}% du PIB")
    st.write(f"Dette finale après {n} ans : {dette_const[-1]:.2f}% du PIB")


