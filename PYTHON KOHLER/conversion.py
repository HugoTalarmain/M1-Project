# -*- coding: utf-8 -*-
"""
Created on Tue Mar  7 11:09:58 2023

@author: hugot
"""

import pandas as pd


# -------------- EXTRACTION DES DONNEES DU MOTEUR --------------

def moteur(excel_file_motor_path, CSV_file_motor_path):
    column_name_motor = ["IDENT\nItem","ID_STATUT\nStatus","MOT_GN_46_IN\nWet weight (kg)","MOT_H5_07_IN\nFuel consumption @ ESP Max Power (l/h)"]

    #Lecture du fichier
    dfm = pd.read_excel(excel_file_motor_path)

    #Séléction des colonnes que l'on souhaite traiter 
    df = dfm[column_name_motor]
    
    #Boucle de tri 
    i=0
    while i<=(len(df)-1):
        if df["ID_STATUT\nStatus"][i] != "ACTIF" and df["ID_STATUT\nStatus"][i] != "PRILIMINARY":
            df = df.drop(labels=i,axis=0)
        i+=1
    
    #Ajout de la colonne type 
    df['type'] = 'moteur'
    #Conversion des données au format CSV 
    csv_data = df.to_csv(header=False, index=False)
    
    #Enregistrement des données CSV dans un fichier
    with open(CSV_file_motor_path,"w") as f:
      f.write(csv_data)
      
# ---------------------------------------------------------------
      
# ----------- EXTRACTION DES DONNEES DE L'ALTERNATEUR -----------
     
def alternateur(excel_file_alternator_path,CSV_file_alternator_path):

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
        with open(CSV_file_alternator_path,"w") as f:
            f.write(csv_data)
            
# ---------------------------------------------------------------            
            
# ------------ EXTRACTION DES DONNEES DU RADIATEUR --------------   
            
def radiateur(excel_file_radiator_path,CSV_file_radiator_path):
    
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
    df = df.drop_duplicates("REF_REFROID\nCooling part number")
    #df = df.drop("ENC_TYPE\nEnclosure", axis=1)

    #Conversion des données au format CSV 
    csv_data = df.to_csv(header=False, index=False)

    #Enregistrement des données dans le fichier CSV RADIATEUR_CSV.csv
    with open(CSV_file_radiator_path,"w") as f:
        f.write(csv_data)

        
# ---------------------------------------------------------------         
        
# ------------ EXTRACION DES DONNEES DU CAPOT -------------------   

def capot(excel_file_capot_path,CSV_file_capot_path):
    
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
    with open(CSV_file_capot_path,"w") as f:
        f.write(csv_data)

# ---------------------------------------------------------------         
        
# --------- AJOUT D'UNE MATIERE A CHAQUE ELEMENT ---------------- 

def element_matiere(CSV_file_motor_path, CSV_file_alternator_path, CSV_file_radiator_path, CSV_file_capot_path,CSV_file_elem_mat_path):
    
    #Lecture du fichier CSV
    data_frame_motor = pd.read_csv(CSV_file_motor_path, header=None)
    data_frame_alt = pd.read_csv(CSV_file_alternator_path, header=None)
    data_frame_radiator = pd.read_csv(CSV_file_radiator_path, header=None)
    data_frame_capot = pd.read_csv(CSV_file_capot_path, header=None)
    
    lst_df = [data_frame_motor, data_frame_alt, data_frame_radiator, data_frame_capot]
    mes_variables = {}
    matieres = ['acier','aluminium','cuivre','plastique']
    
    for i, element in enumerate(lst_df):
        nom_variable_1 = f"donnees_colonnes_{i}"
        mes_variables[nom_variable_1] = element.iloc[:, 0].tolist()
        nom_variable_2 = f"lst_{i}"
        mes_variables[nom_variable_2] = [x for x in mes_variables[nom_variable_1] for _ in range(4)]
        nom_variable_3 = f"lst_matieres_{i}"
        mes_variables[nom_variable_3] = []
        
        #Ajout des 4 matieres pour chaque element
        for j in range(len(mes_variables[nom_variable_1])):
            mes_variables[nom_variable_3] += matieres
            
        
        #Création d'une dataframe
        nom_variable_4 = f"elem_mat_{i}"
        mes_variables[nom_variable_4] = {'elements' : nom_variable_2, 'matieres' : nom_variable_3}
        nom_variable_4 = f"frame_elem_mat_{i}"
        mes_variables[nom_variable_4] = pd.DataFrame({'elements': mes_variables[nom_variable_2], 'matieres': mes_variables[nom_variable_3]})
    
    
    ma_liste = [] # Définition d'une liste vide

    for k in range(4):
        ma_liste.append("PUPITRE") # Ajoute "pupitre" à la liste 4 fois
    #print(ma_liste) # Affiche la liste ["pupitre", "pupitre", "pupitre", "pupitre"]
        
    datapupitre = pd.DataFrame({'elements': ma_liste, 'matieres': matieres})
    #print(datapupitre)
    
        
    dataframe_elem_matiere = pd.concat([mes_variables['frame_elem_mat_0'], mes_variables['frame_elem_mat_1'], mes_variables['frame_elem_mat_2'], mes_variables['frame_elem_mat_3'],datapupitre])
    
    #print(dataframe_elem_matiere)
    # inversion des données dans chaque ligne
    dataframe_elem_matiere = dataframe_elem_matiere.apply(lambda x: x[::-1], axis=1)
    
    #Conversion des données au format CSV 
    csv_data = dataframe_elem_matiere.to_csv(header=False, index=False)

    #Enregistrement des données CSV dans un fichier
    with open(CSV_file_elem_mat_path,"w") as f:
        f.write(csv_data)

            
# ---------------------------------------------------------------         
        
# ----------- EXTRACTION DES DONNEES DU GROUPE ------------------ 
        
def groupe(excel_file_group_path,CSV_file_group_path):
    
    #Colonnes que l'on souhaite traiter 
    column_name_radiator = ["IDENT\nItem","ID_STATUT\nStatus",'ENC_PDSBRT_IN\nGross weight (kg)','ENC_TYPE\nEnclosure']

    #Lecture du fichier
    dfg = pd.read_excel(excel_file_group_path)

    #Séléction des colonnes que l'on souhaite traiter 
    df = dfg[column_name_radiator]
    df.rename(columns={'IDENT\nItem': 'ID', 'ID_STATUT\nStatus': 'Status','ENC_PDSBRT_IN\nGross weight (kg)': 'pds','ENC_TYPE\nEnclosure' : 'capot'}, inplace=True)
    i=0
    while i<=(len(dfg)-1):
        if df["Status"][i] != "ACTIF":
            df = df.drop(labels=i,axis=0)
        i+=1
    df_filtre = df[~df['capot'].str.contains('BASE|DW|ISO20|SSI', na=False)]
    df_filtre = df_filtre.drop('capot',axis=1)
    #Conversion des données au format CSV 
    csv_data = df_filtre.to_csv(header=False, index=False)

    #Enregistrement des données CSV dans un fichier
    with open(CSV_file_group_path,"w") as f:
        f.write(csv_data)        

# ---------------------------------------------------------------         
        
# ------ MISE EN RELATION DU GROUPE ET DES ELEMENTS ------------- 

def groupe_element(excel_file_group_elem_path, excel_file_radiator_path,CSV_file_group_elem_path):
    
    #Colonnes que l'on souhaite traiter 
    column_name_groupe_moteur = ['ID_MOT\nEngine type',"IDENT\nItem"]
    colomn_name_groupe_alternateur = ["ID_ALT\nAlternator type","IDENT\nItem"]
    colomn_name_groupe_capot = ["ID_CAPOT\nCanopy","IDENT\nItem"]
    colomn_name_groupe_pupitre = ["IDENT\nItem"]
    colomn_name_groupe_radiateur = ["REF_REFROID\nCooling part number","IDENT\nItem"]

    #Lecture du fichier pour le moteur 
    dfg = pd.read_excel(excel_file_group_elem_path)

    #Séléction des colonnes que l'on souhaite traiter 
    df1 = dfg[column_name_groupe_moteur]
    df1.rename(columns={ 'ID_MOT\nEngine type': 'element','IDENT\nItem': 'ID'}, inplace=True)
    
    #Pour l'altérnateur
    dfa = pd.read_excel(excel_file_group_elem_path)
    df2 = dfa[colomn_name_groupe_alternateur]
    df2.rename(columns={'ID_ALT\nAlternator type': 'element','IDENT\nItem': 'ID'}, inplace=True)
    
    #Pour le capot
    dfr = pd.read_excel(excel_file_group_elem_path)
    df3 = dfr[colomn_name_groupe_capot]
    df3.rename(columns={"ID_CAPOT\nCanopy": 'element','IDENT\nItem': 'ID'}, inplace=True)
    df3 = df3.dropna(subset=['element'])
    
    #Pour le pupitre
    dfr = pd.read_excel(excel_file_group_elem_path)
    df4 = dfr[colomn_name_groupe_pupitre]
    df4.rename(columns={'IDENT\nItem': 'ID'}, inplace=True)
    pupitre = []
    element = 'PUPITRE'
    for i in range(len(df4)):
        pupitre.append(element)
    df4 = df4.assign(element=pupitre)
    
    #Pour le radiateur
    dfv = pd.read_excel(excel_file_group_elem_path)
    dfc = pd.read_excel(excel_file_radiator_path)
    
    # Suppression des lignes où la colonne "ID_STATUT\nStatus" a une valeur différente de 'ACTIF'
    dfc = dfc[dfc['ID_STATUT\nStatus'] == 'ACTIF']
    
    # Fusionner les deux dataframes en utilisant les colonnes "DESC_GEN\nDescription" et "IDENT_GE\nGenset model" comme colonnes communes
    merged_df = pd.merge(dfv, dfc, left_on='DESC_GEN\nDescription', right_on='IDENT_GE\nGenset model')
           
    df6 = merged_df[colomn_name_groupe_radiateur]
    df6.rename(columns={ "REF_REFROID\nCooling part number": 'element','IDENT\nItem': 'ID'}, inplace=True)
    df6 = df6.drop_duplicates()
    
    nouvelle_dataframe =  pd.concat([df1, df2, df3, df4, df6])
    
    # inversion des données dans chaque ligne
    nouvelle_dataframe = nouvelle_dataframe.apply(lambda x: x[::-1], axis=1)
    
    
    #Conversion des données au format CSV 
    csv_data = nouvelle_dataframe.to_csv(header=False, index=False)

    #Enregistrement des données CSV dans un fichier
    with open(CSV_file_group_elem_path,"w") as f:
        f.write(csv_data)
    
    
def type_element(CSV_file_type_path):
    """
    Fonction qui créer un fichier CSV TYPE.csv
    Le fichier CSV contiendra les 6 éléments qui composent un GE
    """
    #création d'un DataFrame avec une seule colonne de données
    df = pd.DataFrame({'Colonne': ['alternateur', 'capot', 'moteur', 'pupitre', 'radiateur']})

    #écriture du DataFrame dans un fichier CSV
    df.to_csv(CSV_file_type_path, header=False, index=False)
    
def matieres(CSV_file_matieres_path):
    nom_matieres = ['acier', 'aluminium', 'cuivre', 'fuel','hvo', 'plastique']
    coeff_matieres = [2211,7803,1445,2.93,0.712,1870]
    
    ademe = {'nom' : nom_matieres, 'coeff' : coeff_matieres}
    frame_ademe = pd.DataFrame(ademe)
    
    #Conversion des données au format CSV 
    csv_data = frame_ademe.to_csv(header=False, index=False)

    #Enregistrement des données CSV dans un fichier
    with open(CSV_file_matieres_path,"w") as f:
        f.write(csv_data)

def pupitre(CSV_file_pupitre_path):
    ref_id = ['PUPITRE']
    statut = ['ACTIF']
    poids = [50]
    conso = [0]
    typee = ['pupitre']
    
    pupitre = {'ref_id' : ref_id, 'statut' : statut, 'poids' : poids, 'consommation' : conso, 'type' : typee}
    frame_pupitre = pd.DataFrame(pupitre)
    
    csv_data = frame_pupitre.to_csv(header=False, index=False)
    #Enregistrement des données CSV dans un fichier
    with open(CSV_file_pupitre_path,"w") as f:
        f.write(csv_data)
    
# ---------------------------------------------------------------         
        
        
# --------------IMPORT DES DONNEES DANS PHPMYADMIN---------------     
        
import pymysql
import csv

def import_data(csv_file, db_host, db_user, db_pass, db_name, db_table, db_col1, db_col2, db_col3, db_col4, db_col5):
    # Ouvrir le fichier CSV
    with open(csv_file, 'r') as file:
        # Créer un lecteur CSV
        reader = csv.reader(file)
        # Se connecter à la base de données
        db = pymysql.connect(host=db_host, user=db_user, password=db_pass, db=db_name)
        # Créer un curseur pour exécuter les requêtes SQL
        cursor = db.cursor()
        if db_col5 == '' and db_col4 == '' and db_col3 == '' and db_col2 == '':
            # Parcourir les lignes restantes du CSV
            for row in reader:
                # Créer une requête SQL pour insérer les données dans la table de la base de données
                sql = "INSERT IGNORE {0} ({1}) VALUES ('{2}')".format(db_table, db_col1, row[0])
                # Exécuter la requête SQL
                cursor.execute(sql)
        
        if db_col5 == '' and db_col4 == '' and db_col3 == '':
            # Parcourir les lignes restantes du CSV
            for row in reader:
                # Créer une requête SQL pour insérer les données dans la table de la base de données
                sql = "INSERT IGNORE {0} ({1}, {2}) VALUES ('{3}', '{4}')".format(db_table, db_col1, db_col2, row[0], row[1])
                # Exécuter la requête SQL
                cursor.execute(sql)
        if db_col5 == '' and db_col4 == '':
            for row in reader:
                sql = "INSERT IGNORE {0} ({1}, {2}, {3}) VALUES ('{4}', '{5}', '{6}')".format(db_table, db_col1, db_col2, db_col3, row[0], row[1], row[2])
                cursor.execute(sql)
        if db_col5 == '' : 
            for row in reader:
                sql = "INSERT IGNORE {0} ({1}, {2}, {3}, {4}) VALUES ('{5}', '{6}', '{7}', '{8}')".format(db_table, db_col1, db_col2, db_col3, db_col4, row[0], row[1], row[2], row[3])
                cursor.execute(sql)
        if db_col5 != '': 
            for row in reader:
                sql = "INSERT IGNORE {0} ({1}, {2}, {3}, {4}, {5}) VALUES ('{6}', '{7}', '{8}', '{9}', '{10}')".format(db_table, db_col1, db_col2, db_col3, db_col4, db_col5, row[0], row[1], row[2], row[3], row[4])
                cursor.execute(sql)
        # Fermer le curseur et la connexion à la base de données
        cursor.close()
        db.commit()
        db.close()

        
# ---------------------------------------------------------------        
        
# --------------------- FONTION MAIN ---------------------------- 
    
def main(): 
    
    
    import configparser
    config = configparser.ConfigParser()
    config.read('config.ini')
    
    #Base de données 
    db_host = config['database']['db_host']
    db_user = config['database']['db_user']
    db_pass = config['database']['db_pass']
    db_name = config['database']['db_name']

    #Chemin des fichiers
    excel_file_motor_path = config['excel file']['excel_file_motor_path']
    excel_file_alternator_path = config['excel file']['excel_file_alternator_path']
    excel_file_radiator_path = config['excel file']['excel_file_radiator_path']
    excel_file_group_path = config['excel file']['excel_file_group_path']
    excel_file_group_elem_path = config['excel file']['excel_file_group_elem_path']
    excel_file_capot_path = config['excel file']['excel_file_capot_path']
    
    #Chemin des fichiers CSV
    CSV_file_motor_path = config['CSV file']['CSV_file_motor_path']
    CSV_file_alternator_path = config['CSV file']['CSV_file_alternator_path']
    CSV_file_radiator_path = config['CSV file']['CSV_file_radiator_path']
    CSV_file_capot_path = config['CSV file']['CSV_file_capot_path']
    CSV_file_elem_mat_path = config['CSV file']['CSV_file_elem_mat_path']
    CSV_file_group_path = config['CSV file']['CSV_file_group_path']
    CSV_file_group_elem_path = config['CSV file']['CSV_file_group_elem_path']
    CSV_file_matieres_path = config['CSV file']['CSV_file_matieres_path']
    CSV_file_type_path = config['CSV file']['CSV_file_type_path']
    CSV_file_pupitre_path = config['CSV file']['CSV_file_pupitre_path']
    
    #Activation des fonctions
    moteur(excel_file_motor_path,CSV_file_motor_path)
    alternateur(excel_file_alternator_path,CSV_file_alternator_path)
    radiateur(excel_file_radiator_path,CSV_file_radiator_path)
    capot(excel_file_capot_path,CSV_file_capot_path)
    element_matiere(CSV_file_motor_path,CSV_file_alternator_path,CSV_file_radiator_path,CSV_file_capot_path,CSV_file_elem_mat_path)
    groupe(excel_file_group_path,CSV_file_group_path)
    groupe_element(excel_file_group_elem_path,excel_file_radiator_path,CSV_file_group_elem_path)
    matieres(CSV_file_matieres_path)
    type_element(CSV_file_type_path)
    pupitre(CSV_file_pupitre_path)
    
    #Import base de données
    import_data(CSV_file_type_path,db_host,db_user,db_pass,db_name,'type_element','type','','','','')
    import_data(CSV_file_matieres_path,db_host,db_user,db_pass,db_name,'matieres','nom','coeff_ademe','','','')
    import_data(CSV_file_motor_path,db_host,db_user,db_pass,db_name,'element','ref_id','statut','poids','consommation','type')
    import_data(CSV_file_alternator_path,db_host,db_user,db_pass,db_name,'element','ref_id','statut','poids','consommation','type')
    import_data(CSV_file_radiator_path,db_host,db_user,db_pass,db_name,'element','ref_id','statut','poids','consommation','type')
    import_data(CSV_file_pupitre_path,db_host,db_user,db_pass,db_name,'element','ref_id','statut','poids','consommation','type')
    import_data(CSV_file_capot_path,db_host,db_user,db_pass,db_name,'element','ref_id','statut','poids','consommation','type')
    import_data(CSV_file_group_path,db_host,db_user,db_pass,db_name,'groupe','identifiant','statut','poids','','')
    import_data(CSV_file_group_elem_path,db_host,db_user,db_pass,db_name,'groupe_element','ref_id','identifiant','','','')
    import_data(CSV_file_elem_mat_path,db_host,db_user,db_pass,db_name,'element_matiere','nom','ref_id','','','')
    
    
    print('Conversion réalisée avec succès')
    
    
if __name__ == '__main__':
    main()
    
# ---------------------------------------------------------------  