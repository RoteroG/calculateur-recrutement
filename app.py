import streamlit as st
import pandas as pd

# === CONSTANTES SECTORIELLES ===
CA_ANNUEL_PAR_POSTE = 74078  # € par salarié/an (source : Cerfrance 2024-2025)
JOURS_TRAVAIL_ETP = 220      # jours travaillés/an par ETP (35h/semaine, congés inclus)
CA_JOUR = CA_ANNUEL_PAR_POSTE / JOURS_TRAVAIL_ETP  # ≈ 337 €/jour

VACANCE_MOYENNE_SANS = 45    # jours moyens sans prestation
VACANCE_AVEC_PRESTATION = 10 # jours avec prestation express
COUT_PRESTATION = 2000       # € (paiement unique par recrutement)
FIABILITE_BONUS_ZONE_EURO = 1.10  # +10% (moins de turnover zone euro)

# === CONFIG PAGE ===
st.set_page_config(page_title="Calculateur économies recrutement", layout="wide")

# === HEADER ===
st.title("Calculateur d’économies – Restauration (France)")
st.markdown("Estimez l'impact financier d’un poste vacant et les économies réalisées "
            "grâce à notre recrutement express en Europe.")

# === INPUTS ===
st.sidebar.header("Paramètres")
nb_postes = st.sidebar.number_input("Nombre de postes à pourvoir", min_value=1, step=1, value=1)
deja_vacant = st.sidebar.number_input("Depuis combien de jours les postes sont déjà vacants", min_value=0, step=1, value=0)

# === CALCULS ===
vacance_sans = VACANCE_MOYENNE_SANS + deja_vacant
cout_sans = vacance_sans * CA_JOUR * nb_postes

cout_avec_vacance = VACANCE_AVEC_PRESTATION * CA_JOUR * nb_postes
cout_avec_total = cout_avec_vacance + (COUT_PRESTATION * nb_postes)

economies = (cout_sans - cout_avec_total) * FIABILITE_BONUS_ZONE_EURO
jours_ca_sauves = economies / CA_JOUR

# === AFFICHAGE COMPARATIF ===
col1, col2 = st.columns(2)

with col1:
    st.subheader("Sans prestation")
    st.metric("Durée vacance", f"{vacance_sans} jours")
    st.metric("Perte estimée", f"{cout_sans:,.0f} €")

with col2:
    st.subheader("Avec notre prestation")
    st.metric("Durée vacance", f"{VACANCE_AVEC_PRESTATION} jours")
    st.metric("Coût total (vacance + prestation)", f"{cout_avec_total:,.0f} €")

st.success(f"Économie nette réalisée : {economies:,.0f} €")
st.info(f"Équivalent à {jours_ca_sauves:,.0f} jours de chiffre d’affaires sauvés")

# === CHART COMPARATIF ===
data = pd.DataFrame({
    "Scénario": ["Sans prestation", "Avec prestation"],
    "Montant (€)": [cout_sans, cout_avec_total]
})
st.bar_chart(data.set_index("Scénario"))

# === PARAMÈTRES & SOURCES ===
st.markdown("---")
st.header("Paramètres utilisés et sources")
st.markdown(f"""
- CA annuel moyen par salarié (ETP) : **{CA_ANNUEL_PAR_POSTE} €**  
  Source : [Cerfrance 2024-2025](https://www.cerfrance.fr/actualites/les-chiffres-cles-de-la-restauration-en-2024-2025)  
- Jours travaillés annuels par ETP : **{JOURS_TRAVAIL_ETP}** (base légale 35h/semaine)  
- CA moyen par jour : **{CA_JOUR:.0f} €**  
- Vacance moyenne sans prestation : **{VACANCE_MOYENNE_SANS} jours**  
- Vacance avec prestation express : **{VACANCE_AVEC_PRESTATION} jours**  
- Coût prestation fixe : **{COUT_PRESTATION} €**  
- Bonus fiabilité zone euro : **+{int((FIABILITE_BONUS_ZONE_EURO-1)*100)}%**
""")
