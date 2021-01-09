# Online English Dictionary TCP Server and Client

This is a online English dictionary implemented in Python which supports high concurrent access from clients through multiprocessing


# About the code

## Server:
![scrcpy](image_help/img_server_port.png) 

Claim your IP and port to build connection with client here. Now the default ones should be fine to play around in a local network.

![scrcpy](image_help/image_md5.png) 
the server will use MySQL to store and read most of the data, including user account and password. Right now I'm using MD5 to hash the passwd. Change it if you like.


==== 这部分应该用实际的页面效果 ====
User can request his/her word checking history, either displayed in the console or downloaded in a txt file. 

User can also update modify the dictionary and upload to the server to replace the current one.

## Client
===== register image ====
User can register their username and password

==== check image ===
check for word and definition


# Create database for dictionary

I'm using mysql so the two tables will be used and they should be created as:

==== place holder for tables image =====
