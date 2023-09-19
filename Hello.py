import streamlit as st
from datetime import datetime

# Function to calculate days between two dates
def calculate_days(start_date, end_date):
    delta = end_date - start_date
    return delta.days

# Function to calculate each roommate's share of the bills
def calculate_share(bill_details, coloc_details):
    shares = {}
    for bill_type, bill_info in bill_details.items():
        billing_amount = bill_info['amount']
        billing_start_date = bill_info['start_date']
        billing_end_date = bill_info['end_date']
        total_days = 0
        coloc_days = {}

        for name, dates in coloc_details.items():
            start_date = max(dates[0], billing_start_date)
            end_date = min(dates[1], billing_end_date)

            days = calculate_days(start_date, end_date)
            total_days += days
            coloc_days[name] = days

        bill_share = {}
        for name, days in coloc_days.items():
            share = (days / total_days) * billing_amount
            bill_share[name] = round(share, 2)

        shares[bill_type] = bill_share
    return shares

# Function to calculate how much each roommate owes to the others
def calculate_owe(shares, payers):
    owe_details = {}

    for name in payers.values():
        owe_details[name] = 0

    for bill_type, payer in payers.items():
        for name, amount in shares[bill_type].items():
            if name not in owe_details:
                owe_details[name] = 0
            if name == payer:
                owe_details[name] += amount
            else:
                owe_details[name] -= amount
    return owe_details

# Streamlit App
st.title("Répartition de Facture entre Colocataires 💰🏠")

# Navigation
page = st.selectbox("Étape :", ["Montant des Factures", "Détails des Colocataires", "Qui a payé les factures?", "Résultats"])

# Initialize variables
bill_details = {}
coloc_details = {}
payers = {}

if page == "Montant des Factures":
    st.header("Étape 1: Montant des Factures 💵")
    # Your code here for this step, e.g.
    eau_amount = st.number_input("Montant de la Facture d'Eau 💧", min_value=0.0)
    eau_start_date = st.date_input("Date de Début de Facturation Eau 🗓️", format="DD/MM/YYYY")
    eau_end_date = st.date_input("Date de Fin de Facturation Eau 🗓️", format="DD/MM/YYYY")

    edf_amount = st.number_input("Montant de la Facture EDF ⚡", min_value=0.0)
    edf_start_date = st.date_input("Date de Début de Facturation EDF 🗓️", format="DD/MM/YYYY")
    edf_end_date = st.date_input("Date de Fin de Facturation EDF 🗓️", format="DD/MM/YYYY")

    if st.button("Valider Étape 1"):
        bill_details = {
            "Eau": {"amount": eau_amount, "start_date": eau_start_date, "end_date": eau_end_date},
            "EDF": {"amount": edf_amount, "start_date": edf_start_date, "end_date": edf_end_date}
        }

elif page == "Détails des Colocataires":
    st.header("Étape 2: Détails des Colocataires 👥")
    coloc_count = st.number_input("Nombre de Colocataires 👫", min_value=1, value=4)
    coloc_details = {}

    for i in range(1, coloc_count + 1):
        name = st.text_input(f"Nom du Colocataire {i}")
        start_date = st.date_input(f"Date d'arrivée du Colocataire {i} 📆", format="DD/MM/YYYY")
        end_date = st.date_input(f"Date de départ du Colocataire {i} 📆", format="DD/MM/YYYY")
        coloc_details[name] = [start_date, end_date]

    if st.button("Valider Étape 2"):
        # Validate and store roommate details
        # Allow the user to proceed to the next step

        pass  # Replace with your validation and data storing logic

elif page == "Qui a payé les factures?":
    st.header("Étape 3: Qui a payé les factures? 💳")
    eau_payer = st.selectbox("Payer de la Facture d'Eau 💧", list(coloc_details.keys()))
    edf_payer = st.selectbox("Payer de la Facture EDF ⚡", list(coloc_details.keys()))

    if st.button("Valider Étape 3"):
        payers = {
            "Eau": eau_payer,
            "EDF": edf_payer
        }

        shares = calculate_share(bill_details, coloc_details)
        owe_details = calculate_owe(shares, payers)

elif page == "Résultats":
    st.header("Étape 4: Résultats 📊")

    shares = calculate_share(bill_details, coloc_details)
    owe_details = calculate_owe(shares, payers)

    st.subheader("Répartition des Factures")
    st.write(shares)
    st.subheader("Combien chacun doit à qui")
    st.write(owe_details)
