# Online English Dictionary TCP Server and Client

This is a online English dictionary implemented in Python which supports high concurrent access from clients through multiprocessing


# About the code

## Server:
![Alt text](https://github.com/GuanzhaoLi/Online-Dictionary-TCP_Server-and-Client/blob/main/image_help/img_server_port%20.png)

Claim your IP and port to build connection with client here. Now the default ones should be fine to play around in a local network.

![Alt text](https://github.com/GuanzhaoLi/Online-Dictionary-TCP_Server-and-Client/blob/main/image_help/%20image_md5.png)
the server will use MySQL to store and read most of the data, including user account and password. Right now I'm using MD5 to hash the passwd. Change it if you like.


![Alt text](https://github.com/GuanzhaoLi/Online-Dictionary-TCP_Server-and-Client/blob/main/image_help/user_history.png)
User can request his/her word checking history, either displayed in the console or downloaded in a txt file. 

User can also update modify the dictionary and upload to the server to replace the current one.

## Client
![Alt text](https://github.com/GuanzhaoLi/Online-Dictionary-TCP_Server-and-Client/blob/main/image_help/register.png)
User can register their username and password

![Alt text](https://github.com/GuanzhaoLi/Online-Dictionary-TCP_Server-and-Client/blob/main/image_help/check_word.png)
check for word and definition


# Create database for dictionary

I'm using mysql so the two tables will be used and they should be created as:

![Alt text](https://github.com/GuanzhaoLi/Online-Dictionary-TCP_Server-and-Client/blob/main/image_help/sqltable.png)
