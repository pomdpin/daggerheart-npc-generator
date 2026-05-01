# app.py
import streamlit as st
import random
import json
from pathlib import Path
import namemaker

# Load your data
app_folder = Path("files")

# Streamlit UI
st.title("Daggerheart")
st.header("Générateur de PNJs / NPC Generator")
on = st.toggle("Toggle to switch to English")

if on:
    nombre_pnj = st.number_input("How many NPCs ?", min_value=1, value=1)
else :
    nombre_pnj = st.number_input("Combien de PNJs ?", min_value=1, value=1)

# Load data based on language
file_name = "heritage_en.json" if on else "heritage_fr.json"
file_descr = "description_en.json" if on else "description_fr.json"
age_terme = "years old" if on else "ans"

with open(app_folder/"prenoms_noms.json", encoding="utf-8") as names:
    names = json.load(names)
with open(app_folder/file_name, encoding="utf-8") as heritage:
    heritages = json.load(heritage)
with open(app_folder/file_descr, encoding="utf-8") as description:
    descriptions = json.load(description)

option_ancestry = heritages["Ascendance"]
if on :
    ascendance = st.pills("Choose one or several ancestries to generate from:", option_ancestry)
else:
    ascendance = st.pills("Choisissez une ou plusieurs ascendances à partir desquelles générer:", option_ancestry)

if st.button("Générer / Generate"):
    set_prenoms = namemaker.make_name_set(names["Prénoms"], order=3, name_len_func=len, clean_up=True)
    set_noms = namemaker.make_name_set(names["Noms de famille"], order=3, name_len_func=len, clean_up=True)

    pnjs = []
    for _ in range(nombre_pnj):
        name = set_prenoms.make_name()
        surname = set_noms.make_name()
        descr_general = []
        descr_asc = []
        classe = random.choice(heritages["Classe"])
        ascendance = random.choice(list(heritages["Ascendance"].keys()))
        age = random.randint(heritages["Ascendance"][ascendance]["age_min"], heritages["Ascendance"][ascendance]["age_max"])
        taille = random.randint(heritages["Ascendance"][ascendance]["taille_min"], heritages["Ascendance"][ascendance]["taille_max"])
        community = random.choice(list(heritages["Communauté"].keys()))
        personnality = random.choice(heritages["Communauté"][community])

        for categorie in descriptions["General"]:
            descr_general.append(random.choice(descriptions["General"][categorie]))

        for categorie in descriptions["Ascendance"][ascendance]:
            valeur = random.choice(descriptions["Ascendance"][ascendance][categorie])
            descr_asc.append(valeur)
            if categorie == "Style" and ("chauve" in valeur or "bald" in valeur):
                continue

        phrase_descr_asc = " ".join(descr_asc)

        if on:
            pnj_name = f"{name} {surname}"
            pnj_desc = f"""{community} {classe},
{name} is a {personnality} {age} {age_terme} / {taille} cm {ascendance} with {descr_general[0]} eyes, wearing {descr_general[1]} {descr_general[2]}.
\n{name} {phrase_descr_asc}.
{descr_general[3]}."""
        else :
            pnj_name = f"{name} {surname}"
            pnj_desc = f"""{classe} faisant partie de la {community},
{name} est un(e) {ascendance} {personnality} de {age}{age_terme} aux yeux {descr_general[0]} mesurant {taille}cm, vêtu {descr_general[1]} {descr_general[2]}.
\n{name} {phrase_descr_asc}.
{descr_general[3]}"""

        pnjs.append((pnj_name, pnj_desc))

cols = st.columns(2)
for i, pnj in enumerate(pnjs):
    with cols[i % 2]:
        # Display all PNJs
        for name, desc in pnjs:
            st.subheader(name)
            st.write(desc)

st.write("""
         ________________________________________
         **Copyright/Attribution: Daggerheart**
         \r*This project is unofficial fan content and is not approved or endorsed in any way by Critical Role.*
         \r*This product includes materials from the **Daggerheart System Reference Document 1.0**, **© Critical Role, LLC.** under the terms of the **Darrington Press Community Gaming (DPCGL) License**. More information can be found at https://www.daggerheart.com. There are no previous modifications by others.*
         \r*All Rights Reserved. Sous licence **Black Book Editions**, tous droits réservés.*""")
