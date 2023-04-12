<!DOCTYPE html>
<html>
<style>
		table {
			border-collapse: collapse;
			width: 100%;
		}
		td {
			border: 1px solid black;
			padding: 10px;
			text-align: center;
		}
	</style>
    <head>
        <title>Bilan carbone</title>
        <link rel="icon" href="images/K_kohler.png" type="image/png">
        <link rel="stylesheet" href="style.css">
        <meta charset="utf-8">
    </head>
    <body>
        <nav>
            <img src="images/KOHLER_white.png" class="logo">
            <ul>
                <li><a href="index.html">Page d'accueil</a></li>
                <li><a href="index.php">Bilan carbone</a></li>
                <li><a href="ademe.php">ADEME</a></li>
                <li><a href="propos.html">À propos</a></li>
            </ul>
        </nav>
        
        <video autoplay loop muted plays-inline class="back-video">
            <source src="images/fibre-121470.mp4" type="video/mp4">
        </video>

        <!-- FORMULAIRE DE SELECTION -->
        <section class="index">
            <div class="form-box">
                <div class="form-value"></div>
                    <form method="post">
                        <div class="selected">
                            <label class="choix">Veuillez sélectionner un groupe</label>
                            <br/>
                            <select name="groupe" id="groupe">
                                <!-- PARTIE PHP -->
                                <?php
                                    include "database.php";
                                    global $db;

                                    // Requête pour récupérer toutes les valeurs de la colonne "id"
                                    $req = $db->query('SELECT identifiant FROM groupe');

                                    // Affichage des résultats dans une balise select
                                    while ($donnees = $req->fetch())
                                    {
                                        echo '<option value="' . $donnees['identifiant'] . '">' . $donnees['identifiant'] . '</option>';
                                    }
                                ?>
                                <!-- FIN PHP -->
                            </select>
                        </div>
                        <div class="radio">
                            <!-- OPTION DU CAPOT -->
                            <p class ="capot">Voulez-vous ajouter un capot ?</p>
                            <input type="radio" name="radio" value="radio1_valeur"> 
                            <label for="option1">Oui</label>
                            <input type="radio" name="radio" value="radio2_valeur">
                            <label for="option2">Non</label>
                            
                            <br/>
                            <br/>
                            <!-- OPTION DU CAPOT -->
                            <p class ="carbu">Quel type de carburant voulez-vous utiliser ?</p>
                            <input type="radio" name="carbu" value="radio1_valeur_fuel">
                            <label for="option1">Fuel</label>
                            <input type="radio" name="carbu" value="radio2_valeur_hvo"> 
                            <label for="option2">HVO</label>
                            <br/>
                            <br/>
                        </div>
                        
                        <!-- HEURE D'UTILISATION -->  
                        <div class="inputbox">
                            <label for="conso">Nombre d'heure(s) d'utilisation par an</label>
                            <br/>
                            <input type="text" id="conso" name="conso" required>
                        </div> 
                        
                        <br/>
                        <br/>

                        <!-- BOUTON D'ENVOI -->
                        <input type="submit" value="Envoyer">
                    </form>
                </div>
            </div>

            <!-- AFFICHAGE DU GROUPE -->
            </table>
            <?php
            // Vérification que le formulaire a bien été soumis
            if ($_SERVER['REQUEST_METHOD'] == 'POST')
            {
                // Récupération de la valeur sélectionnée dans le select

                if(!empty($_POST['groupe']) && !empty($_POST['radio']) && !empty($_POST['conso'] && !empty($_POST['carbu']))) {

                    //Création des variables 
                    $identifiant = $_POST['groupe'];
                    $radio1 = $_POST['radio'];
                    $conso = $_POST['conso'];
                    $radio2 = $_POST['carbu'];

                    // Affichage de la valeur sélectionnée
                    echo "<div class='reponse_groupe'>" . "Bilan pour le groupe " . $identifiant . "." . "<br/>" . "</div>";
                    
                    //Affichage de la séléction du capot 
                    if($radio1 == 'radio1_valeur'){
                        echo "<div class='reponse_capot'>" . "Vous avez sélectionné un capot pour ce groupe." . "<br/>". "</div>";
                    } 
                    else if($radio1 == 'radio2_valeur'){
                        echo "<div class='reponse_capot'>" . "Vous n'avez pas sélectionné de capot pour ce groupe." . "<br/>". "</div>";
                        
                    }

                    $bilan_carbone = 0;
                    $element = array('moteur', 'pupitre', 'radiateur', 'alternateur', 'capot');
                    $i = 0;
                    $j = 0;
                    $counter = 0;
                    $counter_er = 0;
                    $css_er_elem = array("<div class='er_elem_1'>", "<div class='er_elem_2'>", "<div class='er_elem_3'>", "<div class='er_elem_4'>", "<div class='er_elem_5'>");
                    $poids_chassis = 0;
                    $pourc_chassis = array(0.6, 0.3, 0, 0.1);
                
                    //Liste vide des poids qui va s'incrementer, nécessaire au chassis après
                    $poids = array();
                    //Récupération du poids des groupes pour calculer celui du chassis
                    $requete_poids_groupe = $db->prepare("SELECT g.poids FROM groupe g WHERE g.identifiant = '$identifiant'");
                    $requete_poids_groupe->execute();
                    $result = $requete_poids_groupe->fetch(PDO::FETCH_ASSOC);
                
                    // Si la requête a retourné au moins une ligne de résultat
                    if ($result) {
                        //On récupère la première valeur du premier résultat
                        $poids[0] = $result;
                        //echo  "<div class='er_pds_group'>" . "Erreur, le groupe " .$identifiant . " n'a pas de poids." . "<br/>" . "</div>"; //test affichage

                    } else {
                        //Si la requête n'a retourné aucun résultat
                        echo "<div class='er_pds_group'>" . "Erreur, le groupe " .$identifiant . " n'a pas de poids." . "<br/>" . "</div>";
                        //Si le résultat est de 0
                        if($poids[0] == 0){
                            echo  "<div class='er_pds_group'>" . "Erreur, le groupe " .$identifiant . " n'a pas de poids." . "<br/>" . "</div>";
                        }
                    }
                    
                    foreach ($element as $element) {
                        $bilan_elem = 0;
                        $erreur_element = False;
                                
                        $pourc_moteur = array(0.8, 0.05, 0.1, 0.05);
                        $pourc_pupitre = array(0.4, 0.2, 0.1, 0.3);
                        $pourc_radiateur = array(0.1, 0.3, 0, 0.6);
                        $pourc_alternateur = array(0.2, 0.2, 0.4, 0.2);
                        $pourc_capot= array(1, 0, 0, 0);

                        $materiaux = array('acier', 'aluminium', 'cuivre', 'plastique');
                        //liste de listes
                        $pourcentage = array($pourc_moteur, $pourc_pupitre, $pourc_radiateur, $pourc_alternateur, $pourc_capot);
                        //tableau associatif
                        $pourc_materiel = array_combine($materiaux, $pourcentage[$i]);

                        foreach ($pourc_materiel as $materiaux => $pourcentage[$i]) {
                            $requete = $db->prepare("SELECT (ROUND((e.poids*:pourcentage),2)/1000 * m.coeff_ademe) FROM groupe_element ge, element e, matieres m, element_matiere em WHERE ge.ref_id = e.ref_id AND e.ref_id = em.ref_id AND m.nom = em.nom AND ge.identifiant = '$identifiant' AND e.type = :type_elem AND m.nom = :materiel");
                            
                            // Attribution de la valeur du paramètre
                            $requete->bindParam(':materiel', $materiaux);
                            $requete->bindParam(':pourcentage', $pourcentage[$i]);
                            $requete->bindParam(':type_elem', $element);
                            
                            $requete->execute();
                            $resultats1 = $requete->fetchAll();

                            //Gestion de l'erreur du manque de l'élément
                            if ($resultats1) {
                                $carbone = $resultats1[0][0];
                            } else {
                                $carbone = null;
                                $erreur_element = True;
                            }

                            //Si on choisi 'non' pour le capot
                            if($radio1 == 'radio2_valeur' && $element == 'capot'){
                                $bilan_elem += 0;
                            }
                            else{
                                $bilan_elem += $carbone; //avec capot (oui)
                            }                            
                            //echo " " .$materiaux. " : " . $carbone ."<br/>";
                        }            
                        //echo "Bilan carbone de : " .$element. " -> " . $bilan_elem . " kgCO2" . "<br/>"; 
                        
                        //on gère l'erreur suite à un ou plusieurs bilans vides (sauf pour 'non' capot car forcément égal à 0) ou élément manquant(s)
                        if($bilan_elem != 0 || ($radio1 == 'radio2_valeur' && $element == 'capot')){
                            $counter++;
                        }
                        if($erreur_element == True || ($bilan_elem == 0 && $element != 'capot')){
                            echo $css_er_elem[$counter_er] ."Erreur, les données du : " .$element. " sont manquantes ou à 0." . "<br/>". "</div>";
                            $counter_er++;
                        }

                        $bilan_carbone += $bilan_elem;
                        $i++;

                        //Récupération des poids des éléments pour calculer celui du chassis
                        $requete_poids_elem = $db->prepare("SELECT e.poids FROM groupe_element ge, element e WHERE ge.ref_id = e.ref_id AND ge.identifiant = '$identifiant' AND e.type = :type_elem");
                        $requete_poids_elem->bindParam(':type_elem', $element);             
                        $requete_poids_elem->execute();
                        $result = $requete_poids_elem->fetch(PDO::FETCH_ASSOC);
                        if ($result !== false) {
                            $poids[$i] = $result;
                        }
                        //s'il y a un poids manquant
                        else {
                            //pour ne pas avoir d'erreur d'indice et de liste, on met par défaut le poids à 0
                            $poids[$i]['poids'] = 0;
                        }    
                    }
                    
                    //Calculs pour le chassis en déduction des autres éléments
                    $poids_chassis = $poids[0]['poids'] - ($poids[1]['poids'] + $poids[2]['poids'] + $poids[3]['poids'] + $poids[4]['poids'] + $poids[5]['poids']);
                    $coeff_ademe = array();
                    $materiaux = array('acier', 'aluminium', 'cuivre', 'plastique');

                    foreach ($materiaux as $materiaux) {
                        //récupération des coeff ADEME
                        $requete_coeff = $db->prepare("SELECT m.coeff_ademe FROM matieres m WHERE m.nom = :materiel");
                        $requete_coeff->bindParam(':materiel', $materiaux);
                        $requete_coeff->execute();
                        $coeff_ademe[$j] = $requete_coeff->fetch(PDO::FETCH_ASSOC);
                        $j++;
                    }
                    $bilan_chassis = (($poids_chassis*$pourc_chassis[0])/1000)*$coeff_ademe[0]['coeff_ademe'] + (($poids_chassis*$pourc_chassis[1])/1000)*$coeff_ademe[1]['coeff_ademe'] + (($poids_chassis*$pourc_chassis[2])/1000)*$coeff_ademe[2]['coeff_ademe'] + (($poids_chassis*$pourc_chassis[3])/1000)*$coeff_ademe[3]['coeff_ademe'];
                    
                    if($bilan_chassis != 0){
                        $counter++;
                    }
                    $bilan_carbone += $bilan_chassis;
                    
                    //Affichage d'un tableau avec les résultats
                    echo "<table class='table_bilan'>";
                    echo "<tr>";
                    echo "<td>"."Bilan en fabrication"."</td>";
                    echo "<td>"."Bilan en consommation"."</td>";
                    echo "<td>"."Bilan carbone total"."</td>";
                    echo "</tr>";

                    echo "<tr>";
                    //Affichage du bilan du groupe seulement si on a le bilan pour les 6 éléments
                    if($counter!=6){                      
                        echo "<td>"."Par manque de données, nous ne pouvons pas vous donner le bilan en fabrication."."</td>";
                    }
                    else{
                        echo "<td>"."Bilan carbone du groupe en fabrication : " . round($bilan_carbone) . " kg CO2."."</td>";
                    }

                    if(!is_numeric($conso)){
                        echo "Veuillez choisir un nombre entre 0 et 8760." . "<br/>";
                    }
                    else{
                        if($conso <= 8760){
                            echo "<div class='reponse_heures'>" ."Vous avez sélectionné une utilisation de " . $conso . " heure(s) / an." . "<br/>". "</div>"; 
                            
                            $requete_conso_moteur = $db->prepare("SELECT consommation FROM element e, groupe_element ge 
                            WHERE e.ref_id = ge.ref_id
                            AND ge.identifiant = '$identifiant' 
                            AND e.type = 'moteur'");
                            $requete_conso_moteur->execute();
                            while($conso_moteur = $requete_conso_moteur->fetch()){
                                $moteur_conso = $conso_moteur[0];
                            }

                            if($moteur_conso != 0){
                            
                                $conso_jour = $conso * $moteur_conso;

                                if($radio2 == 'radio1_valeur_fuel'){
                                    $requete_fuel = $db->prepare("SELECT coeff_ademe FROM matieres WHERE nom ='fuel'");
                                    $requete_fuel->execute();
                                    while($coeff_fuel = $requete_fuel->fetch()){
                                        $fuel_coeff = $coeff_fuel[0];
                                    }
                                    echo "<div class='reponse_carbu'>" . "Vous avez sélectionné du fuel pour ce groupe." . "<br/>" . "</div>";
                                    $bilan_conso_moteur = $fuel_coeff * $conso_jour;
                                }
                                else{
                                    $requete_hvo = $db->prepare("SELECT coeff_ademe FROM matieres WHERE nom ='hvo'");
                                    $requete_hvo->execute();
                                    while($coeff_hvo = $requete_hvo->fetch()){
                                        $hvo_coeff = $coeff_hvo[0];
                                    }
                                    echo "<div class='reponse_carbu'>" . "Vous avez sélectionné du HVO pour ce groupe." . "<br/>" . "</div>";
                                    $bilan_conso_moteur = $hvo_coeff * $conso_jour;
                                }
                                echo "<td>" . round($bilan_conso_moteur) . " Kg CO2."."</td>";

                                if($counter!=6){
                                    echo "<td>"."Par manque de données, nous ne pouvons pas vous donner le bilan total."."</td>";
                                }
                                else{
                                    $bilan_total = $bilan_carbone + $bilan_conso_moteur;
                                    echo "<td>". round($bilan_total) . " Kg CO2."."</td>";
                                }
                            }
                            else{
                                echo "<div class='er_conso'>" . "Erreur, il manque des données sur la consommation du moteur." . "<br/>". "</div>";
                                echo "<td>"."Par manque de données, nous ne pouvons pas vous donner le bilan en consommation."."</td>";
                            }
                        }
                        else{
                            echo "<div class='reponse_heures'>" ."Veuillez choisir un nombre entre 0 et 8760." . "<br/>". "</div>";
                        }
                    }
                    echo "</tr>";
                    echo "</table>";
                    
                }
                else{
                    echo "<div class='remplir'>" ." Veuillez remplir tous les champs." . "</div>";
                }
            }
            ?>
            </table>
        </section>
    </body>

</html>
