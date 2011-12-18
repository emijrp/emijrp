#!/bin/bash

#rm acum.html
#rm temp.html
for year in {1996..2012} 
do
    for i in {0..9} #1000 es el límite
    do
        let offset=i*100
        echo "year = $year, page = $i, offset = $offset"
        wget -U mozilla -O temp.html "http://scholar.google.es/scholar?hl=es&start=$offset&num=100&q=allintitle%3A+wikipedia+OR+wiki+OR+wikis+OR+wikifarm&btnG=Buscar&lr=&as_ylo=$year&as_yhi=$year&as_vis=0" 2> /dev/null
        if grep -iE "<div class=gs_r>" temp.html > /dev/null; then
            cat temp.html >> acum.html
        else
            break
        fi
        rm temp.html
        sleep 2
    done
done

