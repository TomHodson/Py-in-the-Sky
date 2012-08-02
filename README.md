*WARNING* This code in it's current implentation is a huge security vulnerability,
 anyone who knows the name of the skype account to which this bot is connected can run arbitrary commands on the host machine,
 while the security of this code could be improved, executing arbitrary user input safely is very difficult to do and Python was not designed with 
 this capability as a goal.

Py-in-the-Sky
=============

A Skype bot that sits in a chat, runs python code and replies with the result

Messages recieved (including those sent by the user the bot is connected as) will be executed as python if they begin with '>' and the output returned
