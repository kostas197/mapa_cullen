#!/bin/bash

vuelos=$(curl -s 192.168.0.3/flights.js)
vuelos=$(echo $vuelos | cut -c 15-)
vuelos=${vuelos::-2}
echo $vuelos
if [[ ${#vuelos} -gt 4 ]] ; then
	#curl -X POST -d $vuelos -H "Content-Type: application/json" https://script.google.com/macros/s/AKfycbyPggtaLhuf5aFghr1sMPBP7Fl37Wawc5RZTSHp0_U0aBaok0T9nJKgKoJfcAsVAgMW/dev
	#curl -X POST -d $vuelos -H "Content-Type: application/json" http://192.168.9.3:3145/vuelos
	curl -X POST -d $vuelos -H "Content-Type: application/json" http://sxbcbz.duckdns.org:3145/vuelos
else
	vuelos='{"FFFF":["FFFF",-52.894,-68.356,0,0,0,"0",0,"","",1702418628,"","","",false,0,"DUMMY"]}'
	#curl -X POST -d $vuelos -H "Content-Type: application/json" https://script.google.com/macros/s/AKfycbyPggtaLhuf5aFghr1sMPBP7Fl37Wawc5RZTSHp0_U0aBaok0T9nJKgKoJfcAsVAgMW/dev
	#curl -X POST -d $vuelos -H "Content-Type: application/json" http://192.168.9.3:3145/vuelos
	curl -X POST -d $vuelos -H "Content-Type: application/json" http://sxbcbz.duckdns.org:3145/vuelos
fi