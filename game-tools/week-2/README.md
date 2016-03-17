# Game tool - Week 2

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

## Protocol

### Client

When asking to enter the room:
> {
> 	"state": 2
> }

When asking to leave the room:
> {
> 	"state": 1
> }

When client selected his object:
> {
> 	"state": 3,
>	"id": `objectId`
> }


### Server

When client accessed the room:
> {
> 	"state": 2
> }

When client exits the room:
> {
> 	"state": 1
> }

When client should select the object:
> {
> 	"state": 3
> }

When client has to wait for other players:
> {
> 	"state": 4
> }

When the game is finished:
> {
> 	"state": 1
>	"result": `-1 for a loss, 0 for a tie and 1 for a win`
> }
