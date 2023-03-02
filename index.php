<!DOCTYPE html>
<html>
    <head>
        <title>Site de test</title>
        <meta charset="utf-8">
    </head>
    <body>
        <h1>Test de requêtes sur la base de données</h1>

        <!-- Menu de selection -->
        <form method="post">
            <label for="choix">Veuillez choisir un groupe :</label>
            <br>
            <br>
            <select id="choix" name="choix">
                <option value="">-- Choix du groupe --</option>
                <option value="option1">B0900_B-00</option>
            </select>
            <br>
            <br>
            <label for="conso">Nombre d'heure d'utilisation par jour :</label>
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
                
                /*
                *****************  Requete et affichage generale *****************
                //Poids du groupe
                $requete1 = $db->prepare("SELECT poids FROM groupe");
                $requete1->execute();
                while($poids_groupe = $requete1->fetch())
                {
                    echo "Poids du groupe : " . $poids_groupe['poids'] . "kg" . "<br/>";
                }
                */

                /*****************  Bilan carbone du moteur  *****************/

                $requete_acier_moteur = $db->prepare("SELECT (ROUND((e.poids*0.8),2)/1000 * m.coeff_ademe) FROM element e, matieres m, element_matiere em WHERE e.ref_id = em.ref_id AND m.nom = em.nom AND e.type ='moteur' AND m.nom = 'acier'");
                $requete_acier_moteur->execute();
                while($acier_moteur = $requete_acier_moteur->fetch()){
                    $moteur_acier = $acier_moteur[0];
                }

                $requete_alu_moteur = $db->prepare("SELECT (ROUND((e.poids*0.05),2)/1000 * m.coeff_ademe) FROM element e, matieres m, element_matiere em WHERE e.ref_id = em.ref_id AND m.nom = em.nom AND e.type ='moteur' AND m.nom = 'aluminium'");
                $requete_alu_moteur->execute();
                while($alu_moteur = $requete_alu_moteur->fetch()){
                    $moteur_alu = $alu_moteur[0];
                }

                $requete_plastique_moteur = $db->prepare("SELECT (ROUND((e.poids*0.05),2)/1000 * m.coeff_ademe) FROM element e, matieres m, element_matiere em WHERE e.ref_id = em.ref_id AND m.nom = em.nom AND e.type ='moteur' AND m.nom = 'plastique'");
                $requete_plastique_moteur->execute();
                while($plastique_moteur = $requete_plastique_moteur->fetch()){
                    $moteur_plastique = $plastique_moteur[0];
                }

                $requete_cuivre_moteur = $db->prepare("SELECT (ROUND((e.poids*0.1),2)/1000 * m.coeff_ademe) FROM element e, matieres m, element_matiere em WHERE e.ref_id = em.ref_id AND m.nom = em.nom AND e.type ='moteur' AND m.nom = 'cuivre'");
                $requete_cuivre_moteur->execute();
                while($cuivre_moteur = $requete_cuivre_moteur->fetch()){
                    $moteur_cuivre = $cuivre_moteur[0];
                }

                //echo "Bilan acier moteur : " . $moteur_acier . "<br/>";
                //echo "Bilan alu moteur : " . $moteur_alu . "<br/>";
                //echo "Bilan plastique moteur : " . $moteur_plastique . "<br/>";
                //echo "Bilan cuivre moteur : " . $moteur_cuivre . "<br/>";
                $bilan_moteur = $moteur_acier + $moteur_alu + $moteur_cuivre + $moteur_plastique;
                //echo "Bilan carbon du moteur en fabrication : " . $bilan_moteur . " kgCO2" . "<br/>";

                /****************** Bilan carbone de l'alternateur ******************/

                $requete_acier_alternateur = $db->prepare("SELECT (ROUND((e.poids*0.2),2)/1000 * m.coeff_ademe) FROM element e, matieres m, element_matiere em WHERE e.ref_id = em.ref_id AND m.nom = em.nom AND e.type ='alternateur' AND m.nom = 'acier'");
                $requete_acier_alternateur->execute();
                while($acier_alternateur = $requete_acier_alternateur->fetch()){
                    $alternateur_acier = $acier_alternateur[0];
                }

                $requete_alu_alternateur = $db->prepare("SELECT (ROUND((e.poids*0.2),2)/1000 * m.coeff_ademe) FROM element e, matieres m, element_matiere em WHERE e.ref_id = em.ref_id AND m.nom = em.nom AND e.type ='alternateur' AND m.nom = 'aluminium'");
                $requete_alu_alternateur->execute();
                while($alu_alternateur = $requete_alu_alternateur->fetch()){
                    $alternateur_alu = $alu_alternateur[0];
                }

                $requete_plastique_alternateur = $db->prepare("SELECT (ROUND((e.poids*0.2),2)/1000 * m.coeff_ademe) FROM element e, matieres m, element_matiere em WHERE e.ref_id = em.ref_id AND m.nom = em.nom AND e.type ='alternateur' AND m.nom = 'plastique'");
                $requete_plastique_alternateur->execute();
                while($plastique_alternateur = $requete_plastique_alternateur->fetch()){
                    $alternateur_plastique = $plastique_alternateur[0];
                }

                $requete_cuivre_alternateur = $db->prepare("SELECT (ROUND((e.poids*0.4),2)/1000 * m.coeff_ademe) FROM element e, matieres m, element_matiere em WHERE e.ref_id = em.ref_id AND m.nom = em.nom AND e.type ='alternateur' AND m.nom = 'cuivre'");
                $requete_cuivre_alternateur->execute();
                while($cuivre_alternateur = $requete_cuivre_alternateur->fetch()){
                    $alternateur_cuivre = $cuivre_alternateur[0];
                }
                $bilan_alternateur = $alternateur_acier + $alternateur_alu + $alternateur_cuivre + $alternateur_plastique;
                //echo "Bilan carbon de l'alternateur en fabrication : " . $bilan_alternateur . " kgCO2" . "<br/>";

                /****************** Bilan carbone du radiateur ******************/

                $requete_acier_radiateur = $db->prepare("SELECT (ROUND((e.poids*0.1),2)/1000 * m.coeff_ademe) FROM element e, matieres m, element_matiere em WHERE e.ref_id = em.ref_id AND m.nom = em.nom AND e.type ='radiateur' AND m.nom = 'acier'");
                $requete_acier_radiateur->execute();
                while($acier_radiateur = $requete_acier_radiateur->fetch()){
                    $radiateur_acier = $acier_radiateur[0];
                }

                $requete_alu_radiateur = $db->prepare("SELECT (ROUND((e.poids*0.3),2)/1000 * m.coeff_ademe) FROM element e, matieres m, element_matiere em WHERE e.ref_id = em.ref_id AND m.nom = em.nom AND e.type ='radiateur' AND m.nom = 'aluminium'");
                $requete_alu_radiateur->execute();
                while($alu_radiateur = $requete_alu_radiateur->fetch()){
                    $radiateur_alu = $alu_radiateur[0];
                }

                $requete_plastique_radiateur = $db->prepare("SELECT (ROUND((e.poids*0.6),2)/1000 * m.coeff_ademe) FROM element e, matieres m, element_matiere em WHERE e.ref_id = em.ref_id AND m.nom = em.nom AND e.type ='radiateur' AND m.nom = 'plastique'");
                $requete_plastique_radiateur->execute();
                while($plastique_radiateur = $requete_plastique_radiateur->fetch()){
                    $radiateur_plastique = $plastique_radiateur[0];
                }
                /*
                $requete_cuivre_radiateur = $db->prepare("SELECT (ROUND((e.poids*0.4),2)/1000 * m.coeff_ademe) FROM element e, matieres m, element_matiere em WHERE e.ref_id = em.ref_id AND m.nom = em.nom AND e.type ='radiateur' AND m.nom = 'cuivre'");
                $requete_cuivre_radiateur->execute();
                while($cuivre_radiateur = $requete_cuivre_radiateur->fetch()){
                    $radiateur_cuivre = $cuivre_radiateur[0];
                }
                */
                $bilan_radiateur = $radiateur_acier + $radiateur_alu + $radiateur_plastique;
                //echo "Bilan carbon du radiateur en fabrication : " . $bilan_radiateur . " kgCO2" . "<br/>";

                /****************** Bilan carbone du pupitre ******************/

                $requete_acier_pupitre = $db->prepare("SELECT (ROUND((e.poids*0.2),2)/1000 * m.coeff_ademe) FROM element e, matieres m, element_matiere em WHERE e.ref_id = em.ref_id AND m.nom = em.nom AND e.type ='pupitre' AND m.nom = 'acier'");
                $requete_acier_pupitre->execute();
                while($acier_pupitre = $requete_acier_pupitre->fetch()){
                    $pupitre_acier = $acier_pupitre[0];
                }

                $requete_alu_pupitre = $db->prepare("SELECT (ROUND((e.poids*0.2),2)/1000 * m.coeff_ademe) FROM element e, matieres m, element_matiere em WHERE e.ref_id = em.ref_id AND m.nom = em.nom AND e.type ='pupitre' AND m.nom = 'aluminium'");
                $requete_alu_pupitre->execute();
                while($alu_pupitre = $requete_alu_pupitre->fetch()){
                    $pupitre_alu = $alu_pupitre[0];
                }

                $requete_plastique_pupitre = $db->prepare("SELECT (ROUND((e.poids*0.3),2)/1000 * m.coeff_ademe) FROM element e, matieres m, element_matiere em WHERE e.ref_id = em.ref_id AND m.nom = em.nom AND e.type ='pupitre' AND m.nom = 'plastique'");
                $requete_plastique_pupitre->execute();
                while($plastique_pupitre = $requete_plastique_pupitre->fetch()){
                    $pupitre_plastique = $plastique_pupitre[0];
                }

                $requete_cuivre_pupitre = $db->prepare("SELECT (ROUND((e.poids*0.1),2)/1000 * m.coeff_ademe) FROM element e, matieres m, element_matiere em WHERE e.ref_id = em.ref_id AND m.nom = em.nom AND e.type ='pupitre' AND m.nom = 'cuivre'");
                $requete_cuivre_pupitre->execute();
                while($cuivre_pupitre = $requete_cuivre_pupitre->fetch()){
                    $pupitre_cuivre = $cuivre_pupitre[0];
                }
                $bilan_pupitre = $pupitre_acier + $pupitre_alu + $pupitre_cuivre + $pupitre_plastique;
                //echo "Bilan carbon du pupitre en fabrication : " . $bilan_pupitre . " kgCO2" . "<br/>";
            }

                /****************** Bilan carbone du chassis ******************/

                $requete_acier_chassis = $db->prepare("SELECT (ROUND((e.poids*0.6),2)/1000 * m.coeff_ademe) FROM element e, matieres m, element_matiere em WHERE e.ref_id = em.ref_id AND m.nom = em.nom AND e.type ='chassis' AND m.nom = 'acier'");
                $requete_acier_chassis->execute();
                while($acier_chassis = $requete_acier_chassis->fetch()){
                    $chassis_acier = $acier_chassis[0];
                }

                $requete_alu_chassis = $db->prepare("SELECT (ROUND((e.poids*0.3),2)/1000 * m.coeff_ademe) FROM element e, matieres m, element_matiere em WHERE e.ref_id = em.ref_id AND m.nom = em.nom AND e.type ='chassis' AND m.nom = 'aluminium'");
                $requete_alu_chassis->execute();
                while($alu_chassis = $requete_alu_chassis->fetch()){
                    $chassis_alu = $alu_chassis[0];
                }

                $requete_plastique_chassis = $db->prepare("SELECT (ROUND((e.poids*0.1),2)/1000 * m.coeff_ademe) FROM element e, matieres m, element_matiere em WHERE e.ref_id = em.ref_id AND m.nom = em.nom AND e.type ='chassis' AND m.nom = 'plastique'");
                $requete_plastique_chassis->execute();
                while($plastique_chassis = $requete_plastique_chassis->fetch()){
                    $chassis_plastique = $plastique_chassis[0];
                }
                /*
                $requete_cuivre_chassis = $db->prepare("SELECT (ROUND((e.poids*0.1),2)/1000 * m.coeff_ademe) FROM element e, matieres m, element_matiere em WHERE e.ref_id = em.ref_id AND m.nom = em.nom AND e.type ='chassis' AND m.nom = 'cuivre'");
                $requete_cuivre_chassis->execute();
                while($cuivre_chassis = $requete_cuivre_chassis->fetch()){
                    $chassis_cuivre = $cuivre_chassis[0];
                }
                */
                $bilan_chassis = $chassis_acier + $chassis_alu + $chassis_plastique;
                //echo "Bilan carbon du pupitre en fabrication : " . $bilan_chassis . " kgCO2" . "<br/>";

                /****************** Bilan carbone du capot ******************/

                $requete_acier_capot = $db->prepare("SELECT (ROUND((e.poids),2)/1000 * m.coeff_ademe) FROM element e, matieres m, element_matiere em WHERE e.ref_id = em.ref_id AND m.nom = em.nom AND e.type ='capot' AND m.nom = 'acier'");
                $requete_acier_capot->execute();
                while($acier_capot = $requete_acier_capot->fetch()){
                    $capot_acier = $acier_capot[0];
                }
                $bilan_capot = $capot_acier;
                //echo "Bilan carbon du pupitre en fabrication : " . $bilan_capot . " kgCO2" . "<br/>";

                /****************** Bilan carbone du capot ******************/

                $bilan_groupe = $bilan_moteur + $bilan_radiateur + $bilan_alternateur + $bilan_chassis + $bilan_pupitre + $bilan_capot;
                echo "Bilan carbone du groupe électrogène en fabrication : " . $bilan_groupe ." KgCO2" . "<br/>";


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
                echo "Le bilan carbone de la consommation du groupe électrogène est de : " . $bilan_conso_moteur . " KgCO2" . "<br/>";

                $bilan_total = $bilan_groupe + $bilan_conso_moteur;
                echo "Le bilan carbone du groupe du groupe est de " . $bilan_total . " KgCO2";




        }   
        else {
            echo "Veuillez sélectionner une option.";
        }
?>
    </body>
</html>