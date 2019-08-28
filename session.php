<?php
   include('config.php');
   session_start();
   
   $user_check = $_SESSION['login_user'];
   
   $ses_sql = mysqli_query($db,"select username,perfil from $db_table where username = '$user_check' ");
   
   $row = mysqli_fetch_array($ses_sql,MYSQLI_ASSOC);
   
   $login_session = $row['username'];
   $user_perfil = $row['perfil'];
   
   if(!isset($_SESSION['login_user'])){
      echo "stop";
      header("location:login.php");
      die();
   }
?>
