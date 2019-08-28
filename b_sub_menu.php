<?php
include("aa_cabecera.php");
include("session.php");
$txt_in_css = $in_css;
$txt_in_head = $in_head;
?>

<html>
<head>
<style>
<?php echo $txt_in_css; ?>
body {
  margin: 0px;
  font-family: 'Roboto', sans-serif;
  font-size: 14px;
  }
</style>
<?php echo $txt_in_head; ?>
</head>
<body>
<?php echo $show_menu_1; echo $show_menu_2;?>

<br><div style='margin:10px;'>

<?php
if ($_SERVER['REQUEST_METHOD'] == 'POST'){
  if (isset($_POST['a_opcion'])){
    $opcion = $_POST['a_opcion'];
    $valor = split('_',$opcion);
    $adicional = '';
  
    $sec = "";
  
    if ($valor[1] == "plantilla"){
      $sec = "nombre de ";
    }
  
    if ($valor[1] == "variable"){
      echo "<form action = \"editar_variables.py\" method = \"post\">";
      echo "<button type = \"submit\" name = \"b_opcion\" value = \"edita_$valor[1]\" style=\"width:250px;\"><div class=\"button-menu\">Editar $valor[1]s</div></button><br><br>";
    
    }else{
      echo "<form action = \"c_opcion.py\" method = \"post\">
    <button type = \"submit\" name = \"b_opcion\" value = \"agrega_$valor[1]\" style=\"width:250px;\"><div class=\"button-menu\">Agregar $valor[1]s</div></button><br>
    <button type = \"submit\" name = \"b_opcion\" value = \"edita_$valor[1]\" style=\"width:250px;\"><div class=\"button-menu\">Editar $sec$valor[1]s</div></button><br>
    <button type = \"submit\" name = \"b_opcion\" value = \"elimina_$valor[1]\" style=\"width:250px;\"><div class=\"button-menu\">Eliminar $valor[1]s</div></button><br><br>";
      echo "</form>";
    }
    echo "<form action = 'pri_menu.php' method = 'post'>";
    echo "<input type = 'submit' value = 'Inicio' style='width:100px; height:20px;'/>";
    echo "</form>";

  }else{
    echo "Ninguna opcion fue selecionada.<br><br><br>";
  }
}else{
    echo "Ninguna opcion fue selecionada.<br><br><br>";
}
?>

</div>
</body>
</html>
