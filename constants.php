<?php

//afficher les détails des erreurs à l'écran :
ini_set('display_errors', 1);
error_reporting(E_ALL);

//saisir des constantes de connexion à la bdd :
define('DB_USER', 'root');
define('DB_PASSWORD', '');
define('DB_NAME', 'application');
define('DB_SERVER', 'localhost');

?>