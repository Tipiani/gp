<?php
   include("aa_cabecera.php");
   $txt_in_css = $in_css;
   $txt_in_head = $in_head;
   include("config.php");
   session_start();
   
   $error = "";

   if($_SERVER["REQUEST_METHOD"] == "POST") {
      // username and password sent from form 
      
      $myusername = mysqli_real_escape_string($db,$_POST['username']);
      $mypassword = mysqli_real_escape_string($db,$_POST['password']); 
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
      <style type = "text/css">
         <?php echo $txt_in_css; ?>
         body {
            margin: 0px;
            font-family: 'Roboto', sans-serif;
            font-size: 14px;
            /*font-family:Arial, Helvetica, sans-serif;*/
         }
         label {
            font-weight:bold;
            width:100px;
            font-size:14px;
         }
         .box {
            border:#666666 solid 1px;
         }
      </style>
      <?php echo $txt_in_head; ?>
   </head>
   <?php echo $show_menu_login;?>
   <body bgcolor = "#FFFFFF">
   <br><br><br>	
      <div align = "center">
         <div style = "width:300px; border: solid 1px #333333; " align = "left">
            <div style = "height:25px; border-bottom-right-radius:0px; border-bottom-left-radius:0px; background-color:black; color:#FFFFFF; padding:3px;"><div style="margin-top:4px;"><b>Login</b></div></div>
				
            <div style = "margin:30px">
               
               <form action = "" method = "post">
                  <label>Usuario  :</label><input type = "text" name = "username" class = "box"/><br /><br />
                  <label>Contraseña  :</label><input type = "password" name = "password" class = "box" /><br/><br />
                  <input style="margin-left:110px" type = "submit" value = " Ingresar "/><br />
               </form>
               
               <div style = "font-size:11px; color:#cc0000; margin-top:10px"><?php echo $error; ?></div>
					
            </div>
				
         </div>
			
      </div>

   </body>
</html>
