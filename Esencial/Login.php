<?php
session_start();
include "conexion.php";

$email    = $_POST['email'];
$password = $_POST['password'];

// Buscar usuario por email
$sql = "SELECT * FROM usuarios WHERE email='$email' LIMIT 1";
$result = $conn->query($sql);

if ($result->num_rows > 0) {

    $user = $result->fetch_assoc();

    // Verificar contraseña
    if (password_verify($password, $user['password'])) {

        $_SESSION['usuario'] = $user['nombre'];
        $_SESSION['email'] = $user['email'];

        header("Location: Principal.html");
        exit();

    } else {
        header("Location: login.html?error=incorrecto");
        exit();
    }

} else {
    header("Location: login.html?error=usuario_no_existe");
    exit();
}

$conn->close();
?>
