#!/bin/bash

rm acum.html
rm temp.html

for tag in "wikipedia" "wikipedias" "wiki" "wikis" "wikifarm" "wikifarms" "mediawiki" "wikimedia" "wikixray" "WikiNavMap" "wikitracer" "wikihadoop" "wikipride" "wikiprep" "wikiwikiweb" "graphingwiki" "wiktionary" "wikibooks" "wikiquote" "wikisource" "wikinews" "wikiversity" "wikispecies"
do
    for year in {1996..2012} 
    do
        for i in {0..9} #1000 es el límite
        do
            let offset=i*100
            echo "tag = $tag, year = $year, page = $i, offset = $offset"
            #as_vis=1 solo muestra aquellos que tienen al menos un resumen, excluyendo las citas (ganamos resultados así, para años con más de 1000)
            wget -U mozilla -O temp.html "http://scholar.google.es/scholar?hl=es&start=$offset&num=100&q=allintitle%3A+$tag&btnG=Buscar&lr=&as_ylo=$year&as_yhi=$year&as_vis=1" 2> /dev/null
            if grep -iE "<div class=gs_r>" temp.html > /dev/null; then
                cat temp.html >> acum.html
            else
                break
            fi
            rm temp.html
            sleep 2
        done
    done
done
