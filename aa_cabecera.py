#!/usr/bin/env python

import sys
reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')

def mostrar_cabecera():

#https://mocah.org/uploads/posts/5399393-architecture-building-minimal-wallpaper-desktop-wallpapers-desktop-background-desktop-backgrounds-wallpapers-amazing-wallpaper-office-corner-mist-dense-mist-misty-black-and-white-corner-buildi.jpg
#https://soprema.us/wp-content/uploads/2017/06/luca-bravo-198061.jpg
#https://mocah.org/uploads/posts/5399393-architecture-building-minimal-wallpaper-desktop-wallpapers-desktop-background-desktop-backgrounds-wallpapers-amazing-wallpaper-office-corner-mist-dense-mist-misty-black-and-white-corner-buildi.jpg
#https://visme.co/blog/wp-content/uploads/2017/07/50-Beautiful-and-Minimalist-Presentation-Backgrounds-031.jpg
  in_css = '''@charset "UTF-8";

body {
   color: #333333;
   /*background-image: url(https://visme.co/blog/wp-content/uploads/2017/07/50-Beautiful-and-Minimalist-Presentation-Backgrounds-031.jpg);*/
   background-size: cover;
}

div.lista-ele {
  background-color:#e8e8e8;
  width:304px;border:1px solid #a9a9a9;
  border-radius:3px
}

div.lista-cont {
  width:100%;
  margin-left:5px
}

div div {
  border-radius: 3px;
}

select {
  padding: 7px 10px;
  /*border: none;*/
  border-radius: 3px;
}

.button-menu {
  margin-top: 2px;
  margin-right: 10px;
}

input[type=text] {
  /*border: none;*/
  padding: 7px 10px;
  border: 1px solid #a9a9a9;
  border-radius: 3px;
}

button[type=submit], input[type=submit]{
        margin-top: 4px;
        width:130px;
        height:30px;
	-moz-box-shadow:inset 0px 1px 0px 0px #ffffff;
	-webkit-box-shadow:inset 0px 1px 0px 0px #ffffff;
	box-shadow:inset 0px 1px 0px 0px #ffffff;
	background:-webkit-gradient(linear, left top, left bottom, color-stop(0.05, #ededed), color-stop(1, #dfdfdf));
	background:-moz-linear-gradient(top, #ededed 5%, #dfdfdf 100%);
	background:-webkit-linear-gradient(top, #ededed 5%, #dfdfdf 100%);
	background:-o-linear-gradient(top, #ededed 5%, #dfdfdf 100%);
	background:-ms-linear-gradient(top, #ededed 5%, #dfdfdf 100%);
	background:linear-gradient(to bottom, #ededed 5%, #dfdfdf 100%);
	filter:progid:DXImageTransform.Microsoft.gradient(startColorstr='#ededed', endColorstr='#dfdfdf',GradientType=0);
	background-color:#ededed;
	-moz-border-radius:6px;
	-webkit-border-radius:6px;
	border-radius:6px;
	border:1px solid #dcdcdc;
	display:inline-block;
	cursor:pointer;
	color:#333333;
	font-family:Calibri;
	font-size:13.5px;
	font-weight:bold;
	padding:4px 24px 22px;
	text-decoration:none;
	text-shadow:0px 1px 0px #ffffff;
}

button[type=submit]:hover,input[type=submit]:hover {
	background:-webkit-gradient(linear, left top, left bottom, color-stop(0.05, #dfdfdf), color-stop(1, #ededed));
	background:-moz-linear-gradient(top, #dfdfdf 5%, #ededed 100%);
	background:-webkit-linear-gradient(top, #dfdfdf 5%, #ededed 100%);
	background:-o-linear-gradient(top, #dfdfdf 5%, #ededed 100%);
	background:-ms-linear-gradient(top, #dfdfdf 5%, #ededed 100%);
	background:linear-gradient(to bottom, #dfdfdf 5%, #ededed 100%);
	filter:progid:DXImageTransform.Microsoft.gradient(startColorstr='#dfdfdf', endColorstr='#ededed',GradientType=0);
	background-color:#dfdfdf;
}

/* Base Styles */

#cssmenu > ul,
#cssmenu > ul li,
#cssmenu > ul ul {

  list-style: none;
  margin: 0;
  padding: 0;

}


#cssmenu > ul {

  position: relative;
  z-index: 597;

}


#cssmenu > ul li {

  float: left;
  min-height: 1px;
  line-height: 1.3em;
  vertical-align: middle;

}


#cssmenu > ul li.hover,#cssmenu > ul li:hover {

  position: relative;
  z-index: 599;
  cursor: default;

}


#cssmenu > ul ul {
  visibility: hidden;
  position: absolute;
  top: 100%;
  left: 0;
  z-index: 598;
  width: 100%;
}

#cssmenu > ul ul li {
  float: none;
}

#cssmenu > ul ul ul {
  top: 1px;
  left: 99%;
}

#cssmenu > ul li:hover > ul {
  visibility: visible;
}

/* Align last drop down RTL */

#cssmenu > ul > li.last ul ul {
  left: auto !important;
  right: 99%;
}

#cssmenu > ul > li.last ul {
  left: auto;
  right: 0;
}

#cssmenu > ul > li.last {
  text-align: right;
}

/* Theme Styles */

#cssmenu > ul {
  border-top: 4px solid #3fa338;
  font-family: Calibri, Tahoma, Arial, sans-serif;
  font-size: 14px;
  background: #1e1e1e;
  background: -moz-linear-gradient(top, #1e1e1e 0%, #040404 100%);
  background: -webkit-gradient(linear, left top, left bottom, color-stop(0%, #1e1e1e), color-stop(100%, #040404));
  background: -webkit-linear-gradient(top, #1e1e1e 0%, #040404 100%);
  background: linear-gradient(top, #1e1e1e 0%, #040404 100%);
  width: auto;
  zoom: 1;
}

#cssmenu > ul:before {
  content: '';
  display: block;
}

#cssmenu > ul:after {
  content: '';
  display: table;
  clear: both;
}

#cssmenu > ul li a {
  display: inline-block;
  padding: 10px 22px;
}

#cssmenu > ul > li.active,
#cssmenu > ul > li.active:hover {
  background-color: #3fa338;
}

#cssmenu > ul > li > a:link,
#cssmenu > ul > li > a:active,
#cssmenu > ul > li > a:visited {
  color: #ffffff;
}

#cssmenu > ul > li > a:hover {
  color: #ffffff;
}

#cssmenu > ul ul ul {
  top: 0;
}
#cssmenu > ul li li {
  background-color: #ffffff;
  border-bottom: 1px solid #ebebeb;
  font-size: 12px;
}
#cssmenu > ul li.hover,
#cssmenu > ul li:hover {
  background-color: #F5F5F5;
}

#cssmenu > ul > li.hover,
#cssmenu > ul > li:hover {
  background-color: #3fa338;
  -webkit-box-shadow: inset 0 -3px 0 rgba(0, 0, 0, 0.15);
  -moz-box-shadow: inset 0 -3px 0 rgba(0, 0, 0, 0.15);
  box-shadow: inset 0 -3px 0 rgba(0, 0, 0, 0.15);
}
#cssmenu > ul a:link,
#cssmenu > ul a:visited {
  color: #9a9a9a;
  text-decoration: none;
}
#cssmenu > ul a:hover {
  color: #9a9a9a;
}
#cssmenu > ul a:active {
  color: #9a9a9a;
}
#cssmenu > ul ul {
  border: 1px solid #CCC \9;
  -webkit-box-shadow: 0 0px 2px 1px rgba(0, 0, 0, 0.15);
  -moz-box-shadow: 0 0px 2px 1px rgba(0, 0, 0, 0.15);
  box-shadow: 0 0px 2px 1px rgba(0, 0, 0, 0.15);
  width: 150px;
}

div.principal-1 {
    font-family: 'Roboto', sans-serif;
    font-size: 20px;
    background-color: black;
    height: 15px;
}

div.principal-2 {
    font-family: 'Roboto', sans-serif;
    font-size: 15px;
    background-color: black;
    height: 25px;
}

.se-pre-con {
        position: fixed;
        left: 0px;
        top: 0px;
        width: 100%;
        height: 100%;
        z-index: 9999;
        background: url(https://static-steelkiwi-dev.s3.amazonaws.com/media/filer_public/f5/2d/f52dbbc7-f0fe-4ef7-9192-1580de2da276/543aa75c-67ff-4b98-b1b9-12054ef3fbe9.gif) center no-repeat #fff;
}

.principal {
    font-family: 'Roboto', sans-serif;
    font-size: 40px;
    color: white;
    background-color: black;
    height: 80px;
}

/* The sticky class is added to the header with JS when it reaches its scroll position */
.sticky {
  position: fixed;
  top: 0;
  width: 100%;
  z-index:1;
}

/* Add some top padding to the page content to prevent sudden quick movement (as the header gets a new position at the top of the page (position:fixed and top:0) */

.sticky + .content {
  padding-top: 500px;
}

a#salida {
  margin-right: 20px;
  margin-bottom: 5px;
  text-decoration: none;
}

a#salida:link {
  color: white;
}

/* visited link */
a#salida:visited {
  color: white;
}

/* mouse over link */
a#salida:hover {
  color: #3fa338;
}

/* selected link */
a#salida:active {
  color: white;
}
'''

  in_head = '''<meta charset='utf-8'>

<meta http-equiv="X-UA-Compatible" content="IE=edge">

<meta name="viewport" content="width=device-width, initial-scale=1">

<script src="http://code.jquery.com/jquery-latest.min.js" type="text/javascript">
</script>

<title>Gestor de Plantillas</title>
  '''

  show_menu = '''
<div class="se-pre-con"></div>
<div class="principal-1"></div>
<div style="background-color:black">
  <table style="background-color:black;border-collapse:collapse;border:0px solid black">
    <tr>
      <td style="width:10%; border:0px solid black">
        <img style="margin-left:60px" width="120%" src="http://190.12.64.140:81/gespl/imagenes/logo_on.png" onerror='this.onerror=null; this.src="http://192.168.20.31/gespl/imagenes/logo_on.png"'/>
      </td>
      <td style="width:80%; text-align:center; border:0px solid black">
        <span class="principal">Gestor de Plantillas</span>
      </td>
      <td style="width:10%; border:0px solid black">
      </td>
    </tr>
  </table>
</div>

<div class='principal-2' style="text-align:right;font-size:12px;"><a id="salida" href="logout.php">Logout</a></div>

<div id='cssmenu'>
  <ul style="diplay:inline-block;">
    <li id="lilogo" style="float:right;display:none;"><a href="javascript:void(0)" onclick="yourFunction()"><span id="logopic" style="display:none"><img src="http://190.12.64.140:81/gespl/imagenes/logo_on.png" onerror='this.onerror=null; this.src="http://192.168.20.31/gespl/imagenes/logo_on.png"' width="50px"></span></a></li>

    <li><a href='pri_menu.php'><span>Inicio</span></a></li>

    <li><a href='a_menu.php'><span>Gestionar Elementos</span></a></li>

    <li class='has-sub'><a href='generar_config.py'><span>Generar Config.</span></a>

<!--
      <ul>

        <li class='has-sub'><a href='#'><span>Product 1</span></a>

          <ul>

            <li><a href='#'><span>Sub Product</span></a></li>

            <li class='last'><a href='#'><span>Sub Product</span></a></li>

          </ul>

        </li>

        <li class='has-sub'><a href='#'><span>Product 2</span></a>

          <ul>
            
<li><a href='#'><span>Sub Product</span></a></li>

            <li class='last'><a href='#'><span>Sub Product</span></a></li>

          </ul>

        </li>

      </ul>

-->
    </li>

    <li><a href='ver_plantillas.py' target="_blank"><span>Ver Todas las Plantillas</span></a></li>

    <li class='last'><a href='manual_plantillas.php'><span>Manual de Usuario</span></a></li>

  </ul>

</div>

<script>
// When the user scrolls the page, execute myFunction 
window.onscroll = function() {myFunction()};

// Get the header
var header = document.getElementById("cssmenu");

// Get the offset position of the navbar
var sticky = header.offsetTop;

// Add the sticky class to the header when you reach its scroll position. Remove "sticky" when you leave the scroll position
function myFunction() {
  if (window.pageYOffset > sticky) {
    header.classList.add("sticky");
    document.getElementById('logopic').style.display = 'inline';
    document.getElementById('lilogo').style.cssFloat = 'left';
    document.getElementById('lilogo').style.display = 'inline';
  } else {
    header.classList.remove("sticky");
    document.getElementById('logopic').style.display = 'none';
    document.getElementById('lilogo').style.cssFloat = 'right';
    document.getElementById('lilogo').style.display = 'none';
  }
}
</script>

<script>
  //paste this code under the head tag or in a separate js file.
  // Wait for window load
  $(window).load(function() {
    // Animate loader off screen
    $(".se-pre-con").fadeOut("slow");;
  });
</script>
  '''

  return in_css, in_head, show_menu
