<?php
include "conexion.php";

$nombre   = $_POST['nombre'];
$email    = $_POST['email'];
$password = $_POST['password'];

if (empty($nombre) || empty($email) || empty($password)) {
    die("Faltan datos");
}

// Encriptar contraseña
$passwordHash = password_hash($password, PASSWORD_DEFAULT);

// Guardar en la base
$sql = "INSERT INTO usuarios (nombre, email, password) VALUES ('$nombre', '$email', '$passwordHash')";

if ($conn->query($sql) === TRUE) {
    header("Location: login.html?msg=registrado");
    exit();
} else {
    echo "Error: " . $conn->error;
}

$conn->close();
?>
