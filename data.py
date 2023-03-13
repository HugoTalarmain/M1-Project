# -*- coding: utf-8 -*-
"""
Created on Tue Mar  7 11:09:58 2023

@author: hugot
"""

import pandas as pd

def moteur(excel_file_motor_path):
    column_name_motor = ["IDENT\nItem","ID_STATUT\nStatus","MOT_GN_46_IN\nWet weight (kg)","MOT_H5_07_IN\nFuel consumption @ ESP Max Power (l/h)"]

    #Lecture du fichier
    dfm = pd.read_excel(excel_file_motor_path)

    #Séléction des colonnes que l'on souhaite traiter 
    df = dfm[column_name_motor]
    
    #Boucle de tri 
    i=0
    while i<=(len(df)-1):
        if df["ID_STATUT\nStatus"][i] != "ACTIF":
            df = df.drop(labels=i,axis=0)
        i+=1
    
    #Ajout de la colonne type 
    df['type'] = 'moteur'
    #Conversion des données au format CSV 
    csv_data = df.to_csv(header=False, index=False)
    
    #Enregistrement des données CSV dans un fichier
    with open("C:/Users/hugot/Desktop/CAT_MOTEUR.csv","w") as f:
      f.write(csv_data)
     
def alternateur(excel_file_alternator_path):

    # ouvrir le fichier CSV d'origine
    with open(excel_file_alternator_path, newline='') as csvfile_origine:
        reader = pd.read_csv(csvfile_origine, delimiter=';')
    
        # récupérer les colonnes que l'on souhaite
        colonne1 = []
        colonne2 = []
        colonne3 = []
        colonneff2 = []

        colonne1.append(reader["ID_ALT Alternator type"])
        colonne2.append(reader["ID_STATUT Status"])
        colonne3.append(reader["ALT_GN_POIDS_MO Net Weight of the alternator with single bearing config (kg)"])
    
        colonnef1 = list(set(colonne1[0]))
        colonnef2 = list(set(colonne2[0]))
        for i in range(len(colonnef1)):
            colonneff2.append(colonnef2[0])
        colonnef3 = list(set(colonne3[0]))
      
        type_element = "alternateur"  
        consommation = 0
        colonnef4 = []  
        colonnef5=[]
    
        for i in range(len(colonnef1)):
            colonnef4.append(type_element)
            colonnef5.append(consommation)
    
        df = pd.DataFrame({'ID': colonnef1, 'Status': colonneff2, 'Poids': colonnef3, 'Conso': colonnef5, 'Type': colonnef4})
    
        #Conversion des données au format CSV 
        csv_data = df.to_csv(header=False, index=False)
    
        #Enregistrement des données CSV dans un fichier
        with open("C:/Users/hugot/Desktop/ALTERNATEUR.csv","w") as f:
            f.write(csv_data)
            
def radiateur(excel_file_radiator_path):


    #Colonnes que l'on souhaite traiter 
    column_name_radiator = ["IDENT_GE\nGenset model","ID_STATUT\nStatus","ID_REFROID\nType of Cooling", "ENC_TYPE\nEnclosure","COOL_CAR_42_IN\nRadiator Weight (kg)"]

    #Lecture du fichier
    dfr = pd.read_excel(excel_file_radiator_path)

    #Séléction des colonnes que l'on souhaite traiter 
    df = dfr[column_name_radiator]

    i=0
    while i<=(len(dfr)-1):
        if df["ID_STATUT\nStatus"][i] != "ACTIF" or df["ID_REFROID\nType of Cooling"][i] != "RADIA" or df["ENC_TYPE\nEnclosure"][i] != "BASE":
            df = df.drop(labels=i,axis=0)
        i+=1

    #ajout de la colonne type 
    df['conso'] = 0
    df['type'] = 'radiateur'
    df = df.drop("ID_REFROID\nType of Cooling", axis=1)
    df = df.drop("ENC_TYPE\nEnclosure", axis=1)

    #Conversion des données au format CSV 
    csv_data = df.to_csv(header=False, index=False)

    #Enregistrement des données CSV dans un fichier
    with open("C:/Users/hugot/Desktop/REF_COOLING.csv","w") as f:
        f.write(csv_data)

def element_matiere(CSV_file_motor_path):
    
    #Lecture du fichier CSV
    data_frame = pd.read_csv(CSV_file_motor_path, header=None)
    
    #Recuperation de la colonne des identifiants
    donnees_colonnes = data_frame.iloc[:, 0].tolist()
    
    #Liste vide
    lst_elements = [x for x in donnees_colonnes for _ in range(4)]
    matieres = ['acier','aluminium','cuivre','plastique']
    lst_matieres = []
    
    #Ajout des 4 matieres pour chaque element
    i = 0
    for i in range(int(len(lst_elements)/4)):
        lst_matieres += matieres
    
    #Création d'une dataframe 
    elem_mat = {'elements' : lst_elements, 'matieres' : lst_matieres}
    frame_elem_mat = pd.DataFrame(elem_mat)
    
    #Conversion des données au format CSV 
    csv_data = frame_elem_mat.to_csv(header=False, index=False)

    #Enregistrement des données CSV dans un fichier
    with open("C:/Users/hugot/Desktop/ELEMENTS_MATIERES.csv","w") as f:
        f.write(csv_data)
            
        
def groupe(excel_file_group_path):
    
    #Colonnes que l'on souhaite traiter 
    column_name_radiator = ["IDENT\nItem","ID_STATUT\nStatus",'ENC_PDSBRT_IN\nGross weight (kg)','ENC_TYPE\nEnclosure']

    #Lecture du fichier
    dfg = pd.read_excel(excel_file_group_path)

    #Séléction des colonnes que l'on souhaite traiter 
    df = dfg[column_name_radiator]
    df.rename(columns={'IDENT\nItem': 'ID', 'ID_STATUT\nStatus': 'Status','ENC_PDSBRT_IN\nGross weight (kg)': 'pds','ENC_TYPE\nEnclosure' : 'capot'}, inplace=True)
    i=0
    while i<=(len(dfg)-1):
        if df["Status"][i] != "ACTIF" :
            df = df.drop(labels=i,axis=0)
        i+=1

    
    #Conversion des données au format CSV 
    csv_data = df.to_csv(header=False, index=False)

    #Enregistrement des données CSV dans un fichier
    with open("C:/Users/hugot/Desktop/GROUPE.csv","w") as f:
        f.write(csv_data)        

def groupe_element(excel_file_group_elem_path):
    
    #Colonnes que l'on souhaite traiter 
    column_name_groupe_moteur = ["IDENT\nItem",'ID_MOT\nEngine type']
    colomn_name_groupe_alternateur = ["IDENT\nItem","ID_ALT\nAlternator type"]
    colomn_name_groupe_radiateur = ["IDENT\nItem","ID_REFROID\nType of Cooling"]
    colomn_name_groupe_pupitre = ["IDENT\nItem"]

    #Lecture du fichier pour le moteur 
    dfg = pd.read_excel(excel_file_group_elem_path)

    #Séléction des colonnes que l'on souhaite traiter 
    df1 = dfg[column_name_groupe_moteur]
    df1.rename(columns={'IDENT\nItem': 'ID', 'ID_MOT\nEngine type': 'element'}, inplace=True)
    
    #Pour l'altérnateur
    dfa = pd.read_excel(excel_file_group_elem_path)
    df2 = dfa[colomn_name_groupe_alternateur]
    df2.rename(columns={'IDENT\nItem': 'ID', 'ID_ALT\nAlternator type': 'element'}, inplace=True)
    
    
    #Pour le radiateur
    dfr = pd.read_excel(excel_file_group_elem_path)
    df3 = dfr[colomn_name_groupe_radiateur]
    df3.rename(columns={'IDENT\nItem': 'ID', 'ID_REFROID\nType of Cooling': 'element'}, inplace=True)
    
    #Pour le pupitre
    dfr = pd.read_excel(excel_file_group_elem_path)
    df4 = dfr[colomn_name_groupe_pupitre]
    df4.rename(columns={'IDENT\nItem': 'ID'}, inplace=True)
    pupitre = []
    element = 'PUPITRE'
    for i in range(len(df4)):
        pupitre.append(element)
    df4 = df4.assign(element=pupitre)
    
    #Pour le chassis
    dfr = pd.read_excel(excel_file_group_elem_path)
    df5 = dfr[colomn_name_groupe_pupitre]
    df5.rename(columns={'IDENT\nItem': 'ID'}, inplace=True)
    chassis = []
    element = 'CHASSIS'
    for i in range(len(df5)):
        chassis.append(element)
    df5 = df5.assign(element=chassis)
    
    nouvelle_dataframe =  pd.concat([df1, df2, df3, df4, df5])
    
    #Conversion des données au format CSV 
    csv_data = nouvelle_dataframe.to_csv(header=False, index=False)

    #Enregistrement des données CSV dans un fichier
    with open("C:/Users/hugot/Desktop/GROUPE_ELEMENT.csv","w") as f:
        f.write(csv_data)
    
def main(): 
    
    #Chemin des fichiers
    excel_file_motor_path = "C:/Users/hugot/Desktop/BBDSDMO/CAT_MOTEUR.xlsx" 
    excel_file_alternator_path = "C:/Users/hugot/Desktop/BBDSDMO/alternateur.csv"
    excel_file_radiator_path = "C:/Users/hugot/Desktop/BBDSDMO/REF_COOLING.xlsx" 
    excel_file_group_path = 'C:/Users/hugot/Desktop/BBDSDMO/TD_ENCOMBREMENT.xlsx'
    excel_file_group_elem_path = "C:/Users/hugot/Desktop/BBDSDMO/CAT_GROUPE.xlsx"
    
    
    #Chemin des fichiers CSV
    CSV_file_motor_path = 'C:/Users/hugot/Desktop/CAT_MOTEUR.csv'
    
    #Activation des fonctions
    moteur(excel_file_motor_path)
    alternateur(excel_file_alternator_path)
    radiateur(excel_file_radiator_path)
    element_matiere(CSV_file_motor_path)
    groupe(excel_file_group_path)
    groupe_element(excel_file_group_elem_path)
    print('Conversion réalisée avec succès')

if __name__ == '__main__':
    main()
