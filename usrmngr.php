<?php
   include("aa_cabecera.php");
   $txt_in_css = $in_css;
   $txt_in_head = $in_head;
   $txt_menu_1 = $show_menu_1;
   $txt_menu_2 = $show_menu_2;
   
   include("config_2.php");
   #include("session.php");
   
   $error = "";

function creauser(){
}

function creaperf(){
}

function creasecc(){
}
  
if($_SERVER["REQUEST_METHOD"] == "POST") {
  #$myusername = mysqli_real_escape_string($db,$_POST['username']);
  #$mypassword = mysqli_real_escape_string($db,$_POST['password']);
  $mypassword = hash('sha256', $mypassword);
  $sql = "SELECT id FROM $db_table WHERE username = '$myusername' and password = '$mypassword'";
  $result = mysqli_query($db,$sql);
  $row = mysqli_fetch_array($result,MYSQLI_ASSOC);
  ///$active = $row['active'];

  $count = mysqli_num_rows($result);

  // If result matched $myusername and $mypassword, table row must be 1 row

  if($count == 1) {
    ///session_register("myusername");
    $_SESSION['login_user'] = $myusername;
    header("location: pri_menu.php");
  }else {
    $error = "Your Login Name or Password is invalid";
  }
}
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
    <?php
      echo $show_menu_1; echo $show_menu_2;
    ?>
    <div style="margin-left:7px">
      <?php
        $opciones = array("secciones","perfiles","usuarios");
        $menu_1 = '';
        for ($a = 0; $a < count($opciones); $a++) {
          $menu_1 = "$menu_1<input type = 'radio' name = 'mgropc' value = '$opciones[$a]'/>".ucfirst($opciones[$a])."<br>";
        }#
      ?>
      <br><br>
      <span>Editar:</span><br><br>
      <form action = 'usrmngr.php' method = 'post'>
        <?php echo $menu_1;?><br><br>
        <input type = 'submit' value = 'Continuar' style='width:100px; height:20px;'/>
      </form>
      <form action = 'pri_menu.php' method = 'post'>
        <input type = 'submit' value = 'Inicio' style='width:100px; height:20px;'/>
      </form>
    </div>
  </body>
</html>

