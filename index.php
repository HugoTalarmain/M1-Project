<!DOCTYPE html>
<html>
    <head>
        <title>Site de test</title>
        <link rel="stylesheet" href="css/index.css">
        <meta charset="utf-8">
    </head>
    <body>

        <h1 class ="titre">Test de requêtes sur la base de données</h1>

        <!-- Menu de selection -->
        <form method="post">
            <label class="choix" for="choix">Veuillez choisir un groupe </label>
            <select id="choix" name="choix">
                <option value="">-- Choix du groupe --</option>
                <option value="option1">B0900_B-00</option>
            </select>
            <br>
            <br>
            <label for="conso">Nombre d'heures d'utilisation par jour </label>
            <input type="text" id="conso" name="conso" required>
            <br>
            <br>
            <button type="submit" name="formsend" id="formsend">Faire le calcul</button>
            <br>
            <br>
        </form>

        <?php


        if (isset($_POST['choix']) && !empty($_POST['choix'])) {
            include 'database.php';
            global $db;
            $choix = $_POST['choix'];
            $conso = $_POST['conso'];
            if($choix == 'option1'){
                
                try {
                    $bilan_carbone = 0;
                    $element = array('moteur', 'chassis', 'pupitre', 'radiateur', 'alternateur', 'capot');
                    $i = 0;

                    foreach ($element as $element) {
                        $bilan_elem = 0;
                        $bilan_elem = 0;
                                
                        $pourc_moteur = array(0.8, 0.05, 0.1, 0.05);
                        $pourc_chassis = array(0.6, 0.3, 0, 0.1);
                        $pourc_pupitre = array(0.4, 0.2, 0.1, 0.3);
                        $pourc_radiateur = array(0.1, 0.3, 0, 0.6);
                        $pourc_alternateur = array(0.2, 0.2, 0.4, 0.2);
                        $pourc_capot= array(1, 0, 0, 0);
                        
                        //liste de listes
                        $pourcentage = array($pourc_moteur, $pourc_chassis, $pourc_pupitre, $pourc_radiateur, $pourc_alternateur, $pourc_capot);
                        $materiaux = array('acier', 'aluminium', 'cuivre', 'plastique');

                        //tableau associatif
                        $pourc_materiel = array_combine($materiaux, $pourcentage[$i]);

                        foreach ($pourc_materiel as $materiaux => $pourcentage[$i]) {
                            $requete = $db->prepare("SELECT (ROUND((e.poids*:pourcentage),2)/1000 * m.coeff_ademe) FROM element e, matieres m, element_matiere em WHERE e.ref_id = em.ref_id AND m.nom = em.nom AND e.type = :type_elem AND m.nom = :materiel");
                            
                            // Attribution de la valeur du paramètre
                            $requete->bindParam(':materiel', $materiaux);
                            $requete->bindParam(':pourcentage', $pourcentage[$i]);
                            $requete->bindParam(':type_elem', $element);
                            
                            $requete->execute();
                            while($bilan = $requete->fetch())
                            {
                                $carbone = $bilan[0];
                                //echo $carbone . "<br/>";
                            }
                            $bilan_elem += $carbone;
                            //echo " " .$materiaux. " : " . $bilan_elem ."<br/>";
                        }
                        //echo "Bilan carbone de : " .$element. " -> " . $bilan_elem . " kgCO2" . "<br/>";
                        $bilan_carbone += $bilan_elem;
                        $i++;

                    }
                    echo "<div class='bilan_conso'>" . "Bilan carbone du groupe en fabrication" ."<br/>" . "<div class='total'>" .$bilan_carbone . " kgCO2" . "</div>";

                    /****************** Bilan de consommation du moteur ******************/
                    $conso = $_POST["conso"];
                    //echo "La conso saisie est : " . $conso . "<br>";
                    $requete_conso_moteur = $db->prepare("SELECT consommation FROM element  WHERE type ='moteur'");
                    $requete_conso_moteur->execute();
                    while($conso_moteur = $requete_conso_moteur->fetch()){
                        $moteur_conso = $conso_moteur[0];
                    }
                    //echo "Le moteur consomme : " . $moteur_conso . " litre/heure" . "<br/>";

                    $conso_jour = $conso * $moteur_conso;
                    //echo "Le moteur consomme " .$conso_jour . " litre par jour." . "<br/>";

                    $requete_fuel = $db->prepare("SELECT coeff_ademe FROM matieres WHERE nom ='fuel'");
                    $requete_fuel->execute();
                    while($coeff_fuel = $requete_fuel->fetch()){
                        $fuel_coeff = $coeff_fuel[0];
                    }
                    //echo "Le coeff du fuel est de " . $fuel_coeff . " KgCO2/l" . "<br/>";

                    $bilan_conso_moteur = $fuel_coeff * $conso_jour;
                    echo "<div class='bilan_conso'>" . "Bilan carbone de la consommation du groupe électrogène " . "<div class='total'>" . $bilan_conso_moteur . " KgCO2" . "<br/>" . "</div>";

                    $bilan_total = $bilan_carbone + $bilan_conso_moteur;
                    echo "<div class='bilan_total'>" . "Bilan carbone du groupe " . "<br/>" . "<div class='total'>" . $bilan_total . " KgCO2" . "</div>";
                }   
                catch (PDOException $exception) {
                    error_log('Request error: '.$exception->getMessage());
                }
            }
        }  
?>
    </body>
</html>