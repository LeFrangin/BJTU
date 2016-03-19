# Game tool - Week 2

## Team
- Alan CHAUCHET 15129189
- Florian GUERIN 15129095

## Problem / Goal

To understand how online game works, we have made a little game using socket to send and receive different kind of data that allow multiple clients to play the famous `rock, paper, scisors`.
How can the server update the available items and notify clients of this change so that players can play with other items than rock, paper and scisors?

## Architecture

For the project, we used python as programming language. You have to install **python 3.4**. By default, the port is 5000.
The project only use two distinct architecture, one is the client and one the server.

The graphical part is made on the client side using 'pygame'

Data are saved in an xml file called init.xml

We implemented a basic protocol between the client and server using JSON format system, every data has a 'state' corresponding to an action and a set of data depending of this action

The editor is on the client side and allows user to edit, remove and add item. The server is then notified, changes his items, update the init.xml file and notify clients

## How to use the program

First, you have to launch the server :

> python main.py

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

When editor edited an object:
> {
> 	"state": 5,
>	"object": `object in JSON format`
> }

When editor created an object:
> {
> 	"state": 6,
>	"object": `object in JSON format`
> }

When editor removed an object:
> {
> 	"state": 7,
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
>	"result": `-1 for a loss and 1 for a win`
> }

When object has been updated / clients connected:
> {
> 	"state": 5,
>	"objects": `array of object in JSON format`
> }