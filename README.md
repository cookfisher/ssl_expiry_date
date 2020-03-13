# ssl_expiry_date
To validate the SSL certificate expiry date for local server and remote server

For validate your local server, you can choose {your_hostname} or 127.0.0.1 as your hostname in the host = 'your_hostname'. If it is a self signed certificate, it will return `<Verify return code: 18 (self signed certificate)>`. If this is the case, you can use the following code  
```` python 
import socket, ssl
import OpenSSL
import os
from subprocess import call
call('openssl x509 -startdate -enddate -noout -in /path/to/the certificate file end with .pem or .crt', shell=True)
````
the sample output will like this:
````
notBefore=Mar 10 18:44:00 2020 GMT
notAfter=Mar 10 18:44:00 2021 GMT
````

If you are sit in the same local network with your web server, you can use the local ip address of the web server or the web site name of the web server, like host = '192.168.1.103', the output should be the same as you test the ssl certificate expiry date for the remote server.
