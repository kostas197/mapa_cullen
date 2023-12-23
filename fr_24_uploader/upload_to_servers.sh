#!/bin/bash

version=1.0

#docker build -t fr24trucho:$version .

scp vuelos.sh 192.168.9.5:.

#scp ../fr24trucho_1.0.tar.gz kmcartelle@sxbcbz.duckdns.org:testing/fr24/.
#ssh kmcartelle@sxbcbz.duckdns.org "docker load < testing/fr24/fr24trucho_$version.tar.gz;docker stop --name fr24trucho ;docker stop --name fr24trucho "