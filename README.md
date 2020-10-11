# socket_server

Module that implements socket server.

Works in 2 modes: Server and Client pair (socket_server) and autonomous Server which runs client in thread (threading_server).
Mode is declared in config.json.
Database - My SQL.

# How it all works

Server send request to client every 2 seconds and client returns string(16) with letters in lowercase.
Server save received string to DB, count of every received letter and count of letter on the first position.
Where count of letter on the first position is > 0 for every letter then server disconnect client and create file result.json.
Result json containts: working time, count of received strings, count of every letter and  count of letter on the first position.
