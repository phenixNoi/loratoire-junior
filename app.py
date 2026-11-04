import streamlit as st
import sqlite3
import pandas as pd
from pathlib import Path
from datetime import datetime

st.set_page_config(
    page_title="L'ORATOIRE – L'Orateur Junior",
    page_icon="🎤",
    layout="centered"
)

DB_PATH = Path("inscriptions.db")

NAVY = "#101B35"
GOLD = "#D4AF37"
RED = "#A62632"

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS inscriptions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date_inscription TEXT NOT NULL,
                enfant TEXT NOT NULL,
                age INTEGER NOT NULL,
                ecole TEXT NOT NULL,
                parent TEXT NOT NULL,
                telephone TEXT NOT NULL,
                email TEXT,
                formule TEXT NOT NULL,
                frais_formation INTEGER NOT NULL,
                frais_inscription INTEGER NOT NULL,
                total INTEGER NOT NULL,
                statut_inscription TEXT NOT NULL
            )
        """)
        conn.commit()

def enregistrer(data):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            INSERT INTO inscriptions (
                date_inscription, enfant, age, ecole, parent, telephone,
                email, formule, frais_formation, frais_inscription, total,
                statut_inscription
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, data)
        conn.commit()

init_db()

st.markdown(f"""
<style>
.stApp {{ background: #F5F6FA; }}
.main .block-container {{ max-width: 820px; padding-top: 2rem; }}
.brand {{
  background: linear-gradient(120deg, {NAVY}, #26385F);
  color: white; padding: 28px 24px; border-radius: 18px;
  text-align: center; border-bottom: 5px solid {GOLD};
}}
.brand h1 {{ color: {GOLD}; letter-spacing: 2px; margin-bottom: 4px; }}
.brand h2 {{ color: white; font-size: 1.35rem; margin-top: 12px; }}
.brand p {{ color: #F2E7C5; margin-bottom: 0; }}
div.stButton > button {{
  background: {NAVY}; color: white; border: 1px solid {GOLD};
  border-radius: 10px; min-height: 3rem; font-weight: 700; width: 100%;
}}
div.stButton > button:hover {{ background: {RED}; color: white; border-color: {RED}; }}
.total {{
  background: #101B35; color: white; border-left: 6px solid {GOLD};
  padding: 18px; border-radius: 12px; margin: 12px 0;
}}
.total strong {{ color: {GOLD}; font-size: 1.8rem; }}
.small-note {{ color: #555; font-size: .9rem; }}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="brand">
  <h1>L’ORATOIRE</h1>
  <p>HAUTE FORMATION À L’ART DE DIRE</p>
  <h2>L’ORATEUR JUNIOR</h2>
  <p><b>FORMONS LES ORATEURS DE DEMAIN !</b></p>
</div>
""", unsafe_allow_html=True)

st.write("")
st.write("Une formation pratique destinée aux enfants et adolescents de **9 à 18 ans**.")
st.info("📅 Rentrée : samedi 28 novembre 2026  \n🕒 Horaires : 15h30 – 17h30  \n📍 Lieu : Lycée Technique d’Abidjan, Cocody")

st.header("1. Informations sur l’enfant")
with st.form("formulaire_inscription"):
    enfant = st.text_input("Nom et prénoms de l’enfant *")
    c1, c2 = st.columns(2)
    with c1:
        age = st.number_input("Âge (9 à 18 ans) *", min_value=9, max_value=18, step=1, value=9)
    with c2:
        ecole = st.text_input("Établissement scolaire *")

    st.header("2. Parent ou tuteur")
    parent = st.text_input("Nom et prénoms du parent/tuteur *")
    telephone = st.text_input("Numéro WhatsApp / téléphone *")
    email = st.text_input("Adresse e-mail (facultatif)")

    st.header("3. Choix de la formule")
    formule = st.radio(
        "Sélectionnez une formule *",
        ["Formule intensive – 2 mois", "Formule progressive – 3 mois"],
        format_func=lambda x: (
            "FORMULE 1 – INTENSIVE | 120 000 FCFA/mois pendant 2 mois"
            if x.startswith("Formule intensive")
            else "FORMULE 2 – PROGRESSIVE | 70 000 FCFA/mois pendant 3 mois"
        )
    )

    if formule.startswith("Formule intensive"):
        frais_formation = 240000
        total = 250000
        mensualite = 120000
        duree = "2 mois"
    else:
        frais_formation = 210000
        total = 220000
        mensualite = 70000
        duree = "3 mois"

    st.markdown(f"""
    <div class="total">
      <div><b>RÉCAPITULATIF FINANCIER</b></div>
      <p>Durée : {duree}</p>
      <p>Paiement mensuel : {mensualite:,} FCFA</p>
      <p>Total des frais de formation : {frais_formation:,} FCFA</p>
      <p>Frais d’inscription (une seule fois) : 10 000 FCFA</p>
      <hr style="border-color:#65708A">
      <div>MONTANT TOTAL À PAYER</div>
      <strong>{total:,} FCFA</strong>
      <p style="font-size:.85rem;margin-bottom:0">Frais d’inscription inclus dans le total.</p>
    </div>
    """.replace(",", " "), unsafe_allow_html=True)

    st.caption("Les frais d’inscription de 10 000 FCFA sont payables à l’inscription pour confirmer la place de l’enfant. Les frais de formation sont ensuite réglés mensuellement selon la formule choisie.")

    st.header("4. Confirmation")
    consentement = st.checkbox(
        "Je confirme avoir pris connaissance de la formule choisie, des modalités de paiement et du montant total. J’autorise L’ORATOIRE à utiliser ces informations uniquement pour gérer cette inscription."
    )

    submitted = st.form_submit_button("ENVOYER MON INSCRIPTION")

if submitted:
    if not enfant.strip() or not ecole.strip() or not parent.strip() or not telephone.strip():
        st.error("Merci de remplir tous les champs obligatoires.")
    elif not consentement:
        st.error("Merci de confirmer votre accord avant l’envoi.")
    else:
        statut = "À confirmer – frais d'inscription non vérifiés"
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data = (
            date, enfant.strip(), int(age), ecole.strip(), parent.strip(),
            telephone.strip(), email.strip(), formule, frais_formation,
            10000, total, statut
        )
        enregistrer(data)
        st.success("Votre demande d’inscription a bien été enregistrée. Merci pour votre confiance !")
        st.markdown(
            "Pour confirmer la place de votre enfant, veuillez contacter L’ORATOIRE et régler les frais d’inscription de **10 000 FCFA**."
        )
        st.markdown("**WhatsApp :** 05 74 51 46 79 / 07 20 32 67 94  \n**Téléphone :** 01 01 10 54 19")

st.divider()
st.subheader("Programme de formation")
st.markdown("""
- Prise de parole en public
- Confiance en soi et gestion du stress
- Articulation et expression orale
- Construction et présentation d’un discours
- Éloquence et leadership
- Exercices pratiques
""")
st.markdown("""
<div style="text-align:center;color:#101B35;padding:12px">
  <b>L’ORATOIRE</b><br><i>L’art de dire, le pouvoir de convaincre.</i><br><br>
  WhatsApp : 05 74 51 46 79 / 07 20 32 67 94<br>
  Téléphone : 01 01 10 54 19
</div>
""", unsafe_allow_html=True)

st.divider()
with st.expander("Espace administration – réservé à l’équipe L’ORATOIRE"):
    st.warning("Configurez un mot de passe administrateur dans les paramètres Secrets de Streamlit avant de publier. Ne laissez pas cet espace sans protection.")
    admin_password = st.text_input("Mot de passe administrateur", type="password")
    expected = st.secrets.get("ADMIN_PASSWORD", "")
    if expected and admin_password == expected:
        with sqlite3.connect(DB_PATH) as conn:
            df = pd.read_sql_query("SELECT * FROM inscriptions ORDER BY id DESC", conn)
        st.success(f"{len(df)} inscription(s) enregistrée(s).")
        st.dataframe(df, use_container_width=True)
        st.download_button(
            "Télécharger les inscriptions (CSV)",
            df.to_csv(index=False).encode("utf-8-sig"),
            file_name="inscriptions_loratoire_junior.csv",
            mime="text/csv"
        )
    elif admin_password:
        st.error("Mot de passe incorrect.")

st.caption("Confidentialité : les informations demandées concernent un mineur. Elles doivent être utilisées uniquement pour gérer son inscription et ne doivent pas être partagées publiquement.")
