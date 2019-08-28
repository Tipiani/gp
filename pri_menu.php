<?php
include("session.php");
include("aa_cabecera.php");
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

<div style='margin:10px;'>

<table style="width:100%;">
<tr>
<td style="height:200px; text-align: right;">
<div style="margin-top:7%; margin-right:20px">
<form action = "generar_config.py" method = "post">
<button type = "submit" name = "pri_opcion" value = "generar" style="width:300px;height:70px"><img align="left" src="http://190.12.64.140:81/gespl/imagenes/gen_conf_4.png" onerror="this.onerror=null; this.src='http://192.168.20.31/gespl/imagenes/gen_conf_4.png'" style="margin-top:5px;width:50px;height:50px;"/><div class="button-menu" style="margin-top:18px">Generar Configuracion</div></button> 
</form>
</div>
</td>
<td style="height:200px; text-align: left;">
<div style="margin-top:7%; margin-left:20px">
<form action = "a_menu.php" method = "post">
<button type = "submit" name = "pri_opcion" value = "gestionar" style="width:300px;height:70px"><img align="left" src="http://190.12.64.140:81/gespl/imagenes/editar_elementos.png" onerror="this.onerror=null; this.src='http://192.168.20.31/gespl/imagenes/editar_elementos.png'" style="margin-top:5px;width:50px;height:50px;"/><div class="button-menu" style="margin-top:18px">Gestionar Elementos</div></button>
</form>
</div>
</td>
</tr>
</table>

</div>

</body></html>
