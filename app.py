import streamlit as st
import pandas as pd
import time

# === CONSTANTES SECTORIELLES ===
CA_ANNUEL_PAR_POSTE = 74078  # € par salarié/an (source : Cerfrance 2024-2025)
JOURS_TRAVAIL_ETP = 220      # jours travaillés/an par ETP
CA_JOUR = CA_ANNUEL_PAR_POSTE / JOURS_TRAVAIL_ETP  # ≈ 337 €/jour/ETP

VACANCE_MOYENNE_SANS = 45
VACANCE_AVEC_AGENCE = 10
COUT_PRESTATION = 2000
FIABILITE_BONUS_ZONE_EURO = 1.10

# === CONFIG PAGE ===
st.set_page_config(page_title="Calculateur économies recrutement", layout="wide")

# === HEADER ===
st.title("Calculateur d’économies – Restauration (France)")
st.markdown("Estimez l'impact financier d’un poste vacant et les économies réalisées "
            "grâce au **recrutement délégué à une agence spécialisée partout en Europe**.")

# === INPUTS ===
st.sidebar.header("Paramètres")
nb_postes = st.sidebar.number_input("Nombre de postes à pourvoir", min_value=1, step=1, value=1)
deja_vacant = st.sidebar.number_input("Depuis combien de jours les postes sont déjà vacants", min_value=0, step=1, value=0)

# === PARAMÈTRES & SOURCES ===
st.header("Paramètres utilisés et sources")
st.markdown(f"""
- **CA annuel moyen par salarié (ETP)** : {CA_ANNUEL_PAR_POSTE} €  
  Source : [Cerfrance 2024-2025](https://www.cerfrance.fr/actualites/les-chiffres-cles-de-la-restauration-en-2024-2025)  
- **Jours travaillés annuels par ETP** : {JOURS_TRAVAIL_ETP} (base légale 35h/semaine)  
- **CA moyen par jour par ETP** : {CA_JOUR:.0f} €  
- **Vacance moyenne sans agence spécialisée** : {VACANCE_MOYENNE_SANS} jours  
- **Vacance avec recrutement délégué** : {VACANCE_AVEC_AGENCE} jours  
- **Coût prestation fixe** : {COUT_PRESTATION} €  
- **Bonus fiabilité zone euro** : +{int((FIABILITE_BONUS_ZONE_EURO-1)*100)}%
""")

# === BOUTON CALCUL ===
if "calcul_lance" not in st.session_state:
    st.session_state.calcul_lance = False

if st.button("Lancer le calcul des économies"):
    st.session_state.calcul_lance = True

    # Messages marketing affichés pendant la progression
    messages = [
        "🔍 Analyse des pertes actuelles...",
        "📊 Estimation du chiffre d'affaires perdu...",
        "🛠️ Application de notre solution de recrutement...",
        "💸 Calcul des économies réalisées...",
        "✅ Résultats prêts !"
    ]

    # Barre de progression
    progress = st.progress(0)
    status = st.empty()

    # Boucle avec progression + messages
    for i in range(100):
        progress.progress(i + 1)

        # Changement de message tous les 20%
        if i % 20 == 0 and i // 20 < len(messages):
            status.text(messages[i // 20])

        time.sleep(0.06)  # durée totale ~3s

    # Nettoyage du message
    status.text("")


# === CALCULS UNIQUEMENT SI CLIC ===
if st.session_state.calcul_lance:
    vacance_sans = VACANCE_MOYENNE_SANS + deja_vacant
    cout_sans = vacance_sans * CA_JOUR * nb_postes

    cout_avec_vacance = VACANCE_AVEC_AGENCE * CA_JOUR * nb_postes
    cout_avec_total = cout_avec_vacance + (COUT_PRESTATION * nb_postes)

    economies = (cout_sans - cout_avec_total) * FIABILITE_BONUS_ZONE_EURO
    jours_ca_sauves = economies / CA_JOUR

    # === AFFICHAGE DES RÉSULTATS ===
    st.header("Résultats")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Sans agence spécialisée")
        st.metric("Durée vacance", f"{vacance_sans} jours")
        st.metric("Perte estimée", f"{cout_sans:,.0f} €")

    with col2:
        st.subheader("Avec recrutement délégué")
        st.metric("Durée vacance", f"{VACANCE_AVEC_AGENCE} jours")
        st.metric("Coût total (vacance + prestation)", f"{cout_avec_total:,.0f} €")

    st.success(f"Économie nette réalisée : {economies:,.0f} €")
    st.info(f"Équivalent à {jours_ca_sauves:,.0f} jours de chiffre d’affaires sauvés")

    # Comparatif prestation vs économies
    st.subheader("Analyse du rapport coût / gain")
    st.write(f"- **Coût de la prestation** : {COUT_PRESTATION * nb_postes:,.0f} €")
    st.write(f"- **Économies générées grâce à cette prestation** : {economies:,.0f} €")
    st.write(f"- Chaque euro investi dans la prestation génère environ "
             f"**{economies / (COUT_PRESTATION * nb_postes):.1f} €** d’économies nettes.")

    # === CHART COMPARATIF ===
    data = pd.DataFrame({
        "Scénario": ["Sans agence spécialisée", "Avec recrutement délégué"],
        "Montant (€)": [cout_sans, cout_avec_total]
    })
    st.bar_chart(data.set_index("Scénario"))
