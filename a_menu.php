<?php
include("session.php");
include("aa_cabecera.php");
?>

<html>
<head>
<style>

<?php
echo $in_css;
?>

body {
  margin: 0px;
  font-family: 'Roboto', sans-serif;
  font-size: 14px;
  }
</style>

<?php
echo $in_head;
?>

</head>
<body>

<?php
echo $show_menu_1;
echo $show_menu_2;
?>

<div style="border-top:1px solid #3fa338;height:25px;background-color: #3fa338; color:white"><div style="margin-left:11px;margin-top:4px;font-size:14px;font-family: Calibri, sans-serif">Editar Variables</div></div>

<br>

<?php
if ($user_perfil == 2){
  echo "<br><br><div style=\"text-align:center; height:100%; width:100%;\"><div style=\"border:1px solid #ddd; height:100px; width:30%; margin-left:35%; background-color:#f2f2f2\"><div style=\"margin-top:40px; color:#3c3c3c\"><b>No tienes permitido el acceso!</b></div></div></div>";
}else{
  echo "<div style='margin:10px;'>
  <form action = 'b_sub_menu.php' method = 'post'>
  <button type = 'submit' name = 'a_opcion' value = 'mgt_area' style=\"width:280px;\"><div class=\"button-menu\">Gestionar Areas</div></button><br>
  <button type = 'submit' name = 'a_opcion' value = 'mgt_despliegue' style=\"width:280px;\"><div class=\"button-menu\">Gestionar Despliegues</div></button><br>
  <button type = 'submit' name = 'a_opcion' value = 'mgt_servicio' style=\"width:280px;\"><div class=\"button-menu\">Gestionar Servicios</div></button><br>
  <button type = 'submit' name = 'a_opcion' value = 'mgt_vendor' style=\"width:280px;\"><div class=\"button-menu\">Gestionar Marcas de Equipos (Vendors)</div></button><br>
  <button type = 'submit' name = 'a_opcion' value = 'mgt_modelo' style=\"width:280px;\"><div class=\"button-menu\">Gestionar Modelos de Equipos</div></button><br>
  <button type = 'submit' name = 'a_opcion' value = 'mgt_plantilla' style=\"width:280px;\"><div class=\"button-menu\">Gestionar Plantillas</div></button><br>
  <button type = 'submit' name = 'a_opcion' value = 'mgt_variable' style=\"width:280px;\"><div class=\"button-menu\">Gestionar Variables</div></button><br>
  </form><br>
  <form action = 'pri_menu.php' method = 'post'><input type = 'submit' value = 'Inicio' style='width:100px; height:20px;'/></form>
  </div>";
}
?>

</body>
</html>
