# Game tool - Week 1 

## Team
- Alan CHAUCHET 15129189
- Florian GUERIN 15129095

## Problem / Goal

To understand how online game works, we have made a little chat using socket to send and receive different kind of data between lots of client.
So the client can send a message for all other client or on a unique channel without set up a configuration but how to make that ?

## Architecture

For the project, we used python as programming language. You have to install **python 3.4**. By default, the port is 5000.
The project only use two file, one is the client and one the server. 

## How to use the program

First, you have to launch the server :

> python server.py

Now, you can launch many clients : 

> python client.py [server's hostname] [port=5000]

That's it :)

