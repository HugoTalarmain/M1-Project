<!DOCTYPE html>
<html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0" charset="UTF-8">
        <title>Kohler</title>
        <link rel="icon" href="images/K_kohler.png" type="image/png">
        <link rel="stylesheet" href="style.css">
    </head>
    <body>
        <div class="hero">
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
                <source src="images/lignes-4967.mp4" type="video/mp4">
            </video>
            <div class="ademe_1">
                <h1>La base ADEME <br/></h1>
                <p><br/>La Base Empreinte® est la base de données publique officielle de facteurs d'émission et de jeux de données d'inventaire nécessaires à la réalisation d'exercices de comptabilité carbone des organisations.<br/>
                <br/>Les données utilisées sur ce site et dans sa base de données sont disponibles dans le fichier 'MATIERES.csv'. <br/>
                <br/>Pour mettre à jour ces données, vous pouvez vous rendre sur le site Base Empreinte ® (ademe.fr) : <br/>
                <br/> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; https://base-empreinte.ademe.fr/<br/>
                <br/>Afin d’avoir accès aux données de la Base Empreinte, il est nécessaire de s'identifier sur le site.<br/></p>
            </div> 
            <div class="ademe_2">
                <table class="table_ademe">
                    <thead>
                        <tr>
                            <th>Elément</th>
                            <th>Coeff</th>
                        </tr>
                    </thead>
                    <tbody>
                        <?php
                            include "database.php";
                            global $db;
                            
                            $requete_coeff = $db->prepare("SELECT nom, coeff_ademe FROM matieres");
                            $requete_coeff->execute();
                            $resultats = $requete_coeff->fetchAll(PDO::FETCH_ASSOC);
                            foreach($resultats as $resultat) { ?>
                                <tr>
                                    <td><?php echo $resultat['nom']; ?></td>
                                    <td><?php echo $resultat['coeff_ademe']; ?></td>
                                </tr>                    
                        <?php } ?>
                    </tbody>
                </table> 
            </div>
        </div> 
    </body>
</html>
