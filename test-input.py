#!/usr/bin/python

import cgi, cgitb
print "Content-type:text/html\r\n\r\n"

print '''<html>
<form action = "plantilla_prev.py" method = "post" target = "_blank">
<textarea name = "textcontent" cols = "60" rows = "20">
Type your text here...
</textarea>
<input type = "submit" value = "Submit" />
</form>
</html>'''
