#!/bin/bash
rm fr24.tar.gz
tar -xcvf fr24.tar.gz . --exclude 'fr24.tar.gz'
scp fr24.tar.gz kmcartelle@sxbcbz.duckdns.org:testing/fr24/.