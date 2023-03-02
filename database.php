<?php 
    //Information de connexion au serveur
    define('HOST','localhost');
    define('DB_NAME','sitweb');
    define('USER','root');
    define('PASS','');

    try{
        //URL de connexion
        $db = new PDO("mysql:host=" . HOST . ";dbname=" . DB_NAME, USER, PASS);
        //Affichage des erreurs 
        $db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    } catch(PDOException $e){
        echo $e;
    }

?>