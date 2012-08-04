WARNING This code is a huge security vulnerability
==================================================
 anyone who knows the name of the skype account to which this bot is connected can run arbitrary commands on the host machine,
 while the security of this code could be improved, executing arbitrary user input safely is very difficult to do and Python was not designed with 
 this capability as a goal.

Py-in-the-Sky
=============

A Skype bot that sits in a chat, runs python code and replies with the result

Messages recieved (including those sent by the user the bot is connected as) will be executed as python if they begin with '>' and the output returned

Usage
=====
Put the full skype name of everyone who is allowed to use the bot, each on it's own line, in the file 'allowed'
Put names of people who can add others to the 'allowed' file in the 'ops' file
Run and log into skype
Run the bot
add the bot to chats and use it by prepending python code with a '>'

Example:
...
[22:04:26] User: >print [x**3 for x in range(20)]
[22:04:27] Bot: [0, 1, 8, 27, 64, 125, 216, 343, 512, 729, 1000, 1331, 1728, 2197, 2744, 3375, 4096, 4913, 5832, 6859]
...

Commands
========
>(any valid python)

<auth list : lists the contents of the allowed file
<auth add user1 user2 : adds any number of usernames to the allowed file
<auth remove : removes users
<threadcount : shows the current number of threads
