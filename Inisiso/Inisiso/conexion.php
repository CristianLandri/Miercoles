<?php

$host = "localhost";
$User = "root";
$pass = "";

$db = "iniciosesiondb";

$conexion = mysqli_connect($host, $User, $pass, $db);

if (!$scan) {
    echo "Conexion_fallida";
}