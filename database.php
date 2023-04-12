<?php

//faire les intéractions de php avec les bases de données

//on importe une seule fois les constantes
require_once('constants.php');

//fonction qui permet la connexion à la bdd :
//function dbConnect (){
try {
    $db = new PDO('mysql:host='.DB_SERVER.';dbname='.DB_NAME, DB_USER, DB_PASSWORD);
    $db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    //echo 'connexion bdd ok'; //test
    //return $db;
}
catch (PDOException $exception) {
    error_log('Connection error: '.$exception->getMessage());
    echo 'Erreur de connexion à la base de données';
    //return false;
}    
//}

?>