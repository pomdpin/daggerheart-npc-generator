# app.py
import streamlit as st
import random
import json
from pathlib import Path
import namemaker

# Load your data
app_folder = Path("C:/Users/yoann/OneDrive/Documents/Jeux de Rôles/Daggerheart/Applications/NPC-Generator/files")

# Streamlit UI
st.title("Daggerheart")
st.header("Générateur de PNJs / NPC Generator")
language = st.selectbox("Langue / Language", ["Français", "English"])
nombre_pnj = st.number_input("Nombre de PNJs / How many NPCs", min_value=1, value=1)

if st.button("Générer / Generate"):
    # Load data based on language
    file_name = "heritage_fr.json" if language == "Français" else "heritage_en.json"
    file_descr = "description_fr.json" if language == "Français" else "description_en.json"
    age_terme = "ans" if language == "Français" else "years old"

    with open(app_folder/"prenoms_noms.json", encoding="utf-8") as names:
        names = json.load(names)
    with open(app_folder/file_name, encoding="utf-8") as heritage:
        heritages = json.load(heritage)
    with open(app_folder/file_descr, encoding="utf-8") as description:
        descriptions = json.load(description)

    prenoms = namemaker.make_name_set(names["Prénoms"], order=3, name_len_func=len, clean_up=True)
    noms = namemaker.make_name_set(names["Noms de famille"], order=3, name_len_func=len, clean_up=True)

    pnjs = []
    for _ in range(nombre_pnj):
        name = random.choice(prenoms)
        surname = random.choice(noms)
        descr_general = []
        descr_asc = []
        classe = random.choice(heritages["Classe"])
        ascendance =random.choice(list(heritages["Ascendance"].keys()))
        age = random.randint(heritages["Ascendance"][ascendance]["age_min"],heritages["Ascendance"][ascendance]["age_max"])
        taille = random.randint(heritages["Ascendance"][ascendance]["taille_min"],heritages["Ascendance"][ascendance]["taille_max"])
        community = random.choice(list(heritages["Communauté"].keys()))
        personnality = random.choice(heritages["Communauté"][community])
        for categorie in descriptions["General"]:
            descr_general.append(random.choice(descriptions["General"][categorie])) 
        for categorie in descriptions["Ascendance"][ascendance]:
            valeur = random.choice(descriptions["Ascendance"][ascendance][categorie])
            descr_asc.append(valeur)
            if categorie == "Style" and "chauve" in valeur or "bald" in valeur :
                continue 

        phrase_descr_asc = " ".join(descr_asc)
        
        pnjs.append(f"""{name} {surname}\n
        {classe} faisant parti de la {community}, {name} est un(e) {ascendance} de {age}{age_terme} aux yeux {descr_general[0]} mesurant {taille}cm, vêtue {descr_general[1]} {descr_general[2]}.
        \r{descr_general[3]} 
        \r{name} {phrase_descr_asc}.""")

    for pnj in pnjs:
        st.write(pnj)
