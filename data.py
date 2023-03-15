"""
Created on Tue Mar  7 11:09:58 2023

@author: hugot
"""

import pandas as pd


# -------------- EXTRACTION DES DONNEES DU MOTEUR --------------

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
    with open("C:/Users/hugot/Desktop/MOTEUR.csv","w") as f:
      f.write(csv_data)
      
# ---------------------------------------------------------------
      
# ----------- EXTRACTION DES DONNEES DE L'ALTERNATEUR -----------
     
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
            
# ---------------------------------------------------------------            
            
# ------------ EXTRACTION DES DONNEES DU RADIATEUR --------------   
            
def radiateur(excel_file_radiator_path):
    
    """
    Fonction qui créer un fichier RADIATEUR_CSV.csv à partir du fichier REF_COOLING.xlsx
    Le nouveau fichier CSV contiendra des données selon des entêtes spécifiques du fichier initial
    Prend en paramètre le chemin du fichier Excel et les entêtes chhoisies
    """
    column_name_cooling = ["REF_REFROID\nCooling part number","ID_STATUT\nStatus", "COOL_CAR_42_IN\nRadiator Weight (kg)"] #"ID_MOT\nEngine type", "ENC_TYPE\nEnclosure",
    #Lecture du fichier
    dfr = pd.read_excel(excel_file_radiator_path)

    #Séléction des colonnes que l'on souhaite traiter 
    df = dfr[column_name_cooling]
    
    #Boucle de tri : seulement les élements ACTIF
    i=0
    while i<=(len(dfr)-1):
        #if df["ID_STATUT\nStatus"][i] != "ACTIF" or df["ID_REFROID\nType of Cooling"][i] != "RADIA" or df["ENC_TYPE\nEnclosure"][i] != "BASE":
        if df["ID_STATUT\nStatus"][i] != "ACTIF":
            df = df.drop(labels=i,axis=0)
        i+=1

    #ajout des colonnes conso et type 
    df['conso'] = 0
    df['type'] = 'radiateur'
    #df = df.drop("ID_REFROID\nType of Cooling", axis=1)
    #df = df.drop("ENC_TYPE\nEnclosure", axis=1)

    #Conversion des données au format CSV 
    csv_data = df.to_csv(header=False, index=False)

    #Enregistrement des données dans le fichier CSV RADIATEUR_CSV.csv
    with open("C:/Users/hugot/Desktop/RADIATEUR.csv","w") as f:
        f.write(csv_data)

        
# ---------------------------------------------------------------         
        
# ------------ EXTRACION DES DONNEES DU CAPOT -------------------   

def capot(excel_file_capot_path):
    
    #Colonnes que l'on souhaite traiter 
    column_name_radiator = ["IDENT\nItem","ID_STATUT\nStatus","ENC_TYPE\nEnclosure","GEN_ORD\nOrder Number","ENC_PDSBRT_IN\nGross weight (kg)"]

    #Lecture du fichier
    dfg = pd.read_excel(excel_file_capot_path)

    #Séléction des colonnes que l'on souhaite traiter 
    df = dfg[column_name_radiator]
    df.rename(columns={'IDENT\nItem': 'ID', 'ID_STATUT\nStatus': 'Status','ENC_PDSBRT_IN\nGross weight (kg)': 'pds','ENC_TYPE\nEnclosure' : 'capot',"GEN_ORD\nOrder Number":'nb'}, inplace=True)
    i=0
    while i<=(len(dfg)-1):
        if df["Status"][i] != "ACTIF":
            df = df.drop(labels=i,axis=0)
        i+=1
        
    df_filtre = df[~df['capot'].str.contains('DW')]
    df_filtre = df_filtre.reset_index(drop=True)
    liste_nom_capot = []
    liste_poids_capot = []
    j=0
    while j<len(df_filtre):
        
        if df_filtre['nb'][j] == 2.0 and df_filtre['nb'][j+1] == 1.0:
            liste_nom_capot.append(df_filtre['capot'][j])
            liste_poids_capot.append(df_filtre['pds'][j]-df_filtre['pds'][j+1])

        if df_filtre['nb'][j] == 2.0 and df_filtre['nb'][j+1] != 1.0:
            if df_filtre['nb'][j+2] == 1.0:
               liste_nom_capot.append(df_filtre['capot'][j])
               liste_poids_capot.append(df_filtre['pds'][j]-df_filtre['pds'][j+2])
        j+=1
        
    dataframe = pd.DataFrame({'id': liste_nom_capot, 'poids': liste_poids_capot})

    status = []
    element = 'ACTIF' 
    for i in range(len(dataframe)):
        status.append(element)
        
    conso = []
    cons = 0 
    for i in range(len(dataframe)):
        conso.append(cons)
        
    typ = []
    ty = 'capot'
    for i in range(len(dataframe)):
        typ.append(ty)
    
    dataframe.insert(loc=1, column='Status', value=status)
    dataframe = dataframe.assign(conso=conso)
    dataframe = dataframe.assign(type=typ)
    dataframe = dataframe.drop_duplicates('id')
    
    #Conversion des données au format CSV 
    csv_data = dataframe.to_csv(header=False, index=False)

    #Enregistrement des données CSV dans un fichier
    with open("C:/Users/hugot/Desktop/CAPOT.csv","w") as f:
        f.write(csv_data)

# ---------------------------------------------------------------         
        
# --------- AJOUT D'UNE MATIERE A CHAQUE ELEMENT ---------------- 

def element_matiere(CSV_file_motor_path,CSV_file_alternator_path,CSV_file_radiator_path,CSV_file_capot_path):
    
    #Lecture du fichier CSV
    data_frame_motor = pd.read_csv(CSV_file_motor_path, header=None)
    data_frame_alt = pd.read_csv(CSV_file_alternator_path, header=None)
    data_frame_radiator = pd.read_csv(CSV_file_radiator_path, header=None)
    data_frame_capot = pd.read_csv(CSV_file_capot_path, header=None)
    
    
    #Recuperation de la colonne des identifiants
    donnees_colonnes_motor = data_frame_motor.iloc[:, 0].tolist()
    donnees_colonnes_alt = data_frame_alt.iloc[:, 0].tolist()
    donnees_colonnes_radiator = data_frame_radiator.iloc[:, 0].tolist()
    donnees_colonnes_capot = data_frame_capot.iloc[:, 0].tolist()
    
    
    #Liste vide
    lst_motor = [x for x in donnees_colonnes_motor for _ in range(4)]
    lst_alt = [x for x in donnees_colonnes_alt for _ in range(4)]
    lst_radia = [x for x in donnees_colonnes_radiator for _ in range(4)]
    lst_capot = [x for x in donnees_colonnes_capot for _ in range(4)]
    
    matieres = ['acier','aluminium','cuivre','plastique']
    lst_matieres_motor = []
    lst_matieres_alt = []
    lst_matieres_radia = []
    lst_matieres_capot = []
    
    
    #Ajout des 4 matieres pour chaque element dans motor
    i = 0
    for i in range(int(len(lst_motor)/4)):
        lst_matieres_motor += matieres
        
    j = 0
    for j in range(int(len(lst_alt)/4)):
        lst_matieres_alt += matieres

    k = 0
    for k in range(int(len(lst_radia)/4)):
        lst_matieres_radia += matieres
        
    l = 0
    for l in range(int(len(lst_capot)/4)):
        lst_matieres_capot += matieres
    
    
    #Création d'une dataframe 
    elem_mat_motor = {'elements' : lst_motor, 'matieres' : lst_matieres_motor}
    frame_elem_mat_motor = pd.DataFrame(elem_mat_motor)
    
    elem_mat_alt = {'elements' : lst_alt, 'matieres' : lst_matieres_alt}
    frame_elem_mat_alt = pd.DataFrame(elem_mat_alt)
    
    elem_mat_radia = {'elements' : lst_radia, 'matieres' : lst_matieres_radia}
    frame_elem_mat_radia = pd.DataFrame(elem_mat_radia)
    
    elem_mat_capot = {'elements' : lst_capot, 'matieres' : lst_matieres_capot}
    frame_elem_mat_capot = pd.DataFrame(elem_mat_capot)
    
    dataframe_elem_matiere =  pd.concat([frame_elem_mat_motor, frame_elem_mat_alt, frame_elem_mat_radia, frame_elem_mat_capot])
    
    #Conversion des données au format CSV 
    csv_data = dataframe_elem_matiere.to_csv(header=False, index=False)

    #Enregistrement des données CSV dans un fichier
    with open("C:/Users/hugot/Desktop/ELEMENTS_MATIERES.csv","w") as f:
        f.write(csv_data)
            
# ---------------------------------------------------------------         
        
# ----------- EXTRACTION DES DONNEES DU GROUPE ------------------ 
        
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

# ---------------------------------------------------------------         
        
# ------ MISE EN RELATION DU GROUPE ET DES ELEMENTS ------------- 

def groupe_element(excel_file_group_elem_path, excel_file_radiator_path):
    
    #Colonnes que l'on souhaite traiter 
    column_name_groupe_moteur = ["IDENT\nItem",'ID_MOT\nEngine type']
    colomn_name_groupe_alternateur = ["IDENT\nItem","ID_ALT\nAlternator type"]
    colomn_name_groupe_capot = ["IDENT\nItem","ID_CAPOT\nCanopy"]
    colomn_name_groupe_pupitre = ["IDENT\nItem"]
    colomn_name_groupe_radiateur = ["IDENT\nItem", "REF_REFROID\nCooling part number"]

    #Lecture du fichier pour le moteur 
    dfg = pd.read_excel(excel_file_group_elem_path)

    #Séléction des colonnes que l'on souhaite traiter 
    df1 = dfg[column_name_groupe_moteur]
    df1.rename(columns={'IDENT\nItem': 'ID', 'ID_MOT\nEngine type': 'element'}, inplace=True)
    
    #Pour l'altérnateur
    dfa = pd.read_excel(excel_file_group_elem_path)
    df2 = dfa[colomn_name_groupe_alternateur]
    df2.rename(columns={'IDENT\nItem': 'ID', 'ID_ALT\nAlternator type': 'element'}, inplace=True)
    
        #Pour le capot
    dfr = pd.read_excel(excel_file_group_elem_path)
    df3 = dfr[colomn_name_groupe_capot]
    df3.rename(columns={'IDENT\nItem': 'ID', "ID_CAPOT\nCanopy": 'element'}, inplace=True)
    
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
    
    #Pour le radiateur
    dfv = pd.read_excel(excel_file_group_elem_path)
    dfc = pd.read_excel(excel_file_radiator_path)
    
    # Suppression des lignes où la colonne "ID_STATUT\nStatus" a une valeur différente de 'ACTIF'
    dfc = dfc[dfc['ID_STATUT\nStatus'] == 'ACTIF']
    
    # Fusionner les deux dataframes en utilisant les colonnes "DESC_GEN\nDescription" et "IDENT_GE\nGenset model" comme colonnes communes
    merged_df = pd.merge(dfv, dfc, left_on='DESC_GEN\nDescription', right_on='IDENT_GE\nGenset model')
           
    df6 = merged_df[colomn_name_groupe_radiateur]
    df6.rename(columns={'IDENT\nItem': 'ID', "REF_REFROID\nCooling part number": 'element'}, inplace=True)
    
    
    nouvelle_dataframe =  pd.concat([df1, df2, df3, df4, df5, df6])
    
    #Conversion des données au format CSV 
    csv_data = nouvelle_dataframe.to_csv(header=False, index=False)

    #Enregistrement des données CSV dans un fichier
    with open("C:/Users/hugot/Desktop/GROUPE_ELEMENT.csv","w") as f:
        f.write(csv_data)
    
    
# ---------------------------------------------------------------         
        
# --------------------- FONTION MAIN ---------------------------- 
    
def main(): 
    
    #Chemin des fichiers
    excel_file_motor_path = "C:/Users/hugot/Desktop/BBDSDMO/CAT_MOTEUR.xlsx" 
    excel_file_alternator_path = "C:/Users/hugot/Desktop/BBDSDMO/alternateur.csv"
    excel_file_radiator_path = "C:/Users/hugot/Desktop/BBDSDMO/REF_COOLING.xlsx" 
    excel_file_group_path = 'C:/Users/hugot/Desktop/BBDSDMO/TD_ENCOMBREMENT.xlsx'
    excel_file_group_elem_path = "C:/Users/hugot/Desktop/BBDSDMO/CAT_GROUPE.xlsx"
    excel_file_capot_path = "C:/Users/hugot/Desktop/BBDSDMO/TD_ENCOMBREMENT.xlsx"
    
    
    #Chemin des fichiers CSV
    CSV_file_motor_path = 'C:/Users/hugot/Desktop/MOTEUR.csv'
    CSV_file_alternator_path = 'C:/Users/hugot/Desktop/ALTERNATEUR.csv'
    CSV_file_radiator_path = 'C:/Users/hugot/Desktop/RADIATEUR.csv'
    CSV_file_capot_path = 'C:/Users/hugot/Desktop/CAPOT.csv'
    
    #Activation des fonctions
    moteur(excel_file_motor_path)
    alternateur(excel_file_alternator_path)
    radiateur(excel_file_radiator_path)
    capot(excel_file_capot_path)
    element_matiere(CSV_file_motor_path,CSV_file_alternator_path,CSV_file_radiator_path,CSV_file_capot_path)
    groupe(excel_file_group_path)
    groupe_element(excel_file_group_elem_path,excel_file_radiator_path)
    
    print('Conversion réalisée avec succès')

if __name__ == '__main__':
    main()
    
# ---------------------------------------------------------------  
