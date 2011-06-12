#!/bin/bash

#download youtube-dl script from http://rg3.github.com/youtube-dl/download.html

#rm youtubepages youtubelinks

for tag in "acampadasol" "spanishrevolution" "democraciarealya" "15menpleno" "nolesvotes" "acampadaacoruna" "acampadacoruna" "acampadaalcala" "acampadaalicante" "acampadaalmeria" "acampadabarcelona" "acampadabcn" "acampadabenicarlo" "acampadabilbao" "acampadacadiz" "acampadacaceres" "acampadacastellon" "acampadachiclana" "acampadacordoba" "acampadadonostia" "acampadaelche" "acampadaferrol" "acampadagasteiz" "acampadagranada" "acampadaibiza" "acampadajerez" "acampadalaspalmas" "acampadapalmas" "acampadaleon" "acampadalleida" "acampadalogrono" "acampadamadrid" "acampadamalaga" "acampadamurcia" "acampadapalencia" "acampadapalma" "acampadamallorca" "acampadapamplona" "acampadaoviedo" "acampadaronda" "acampadasalamanca" "acampadasantiago" "acampadasevilla" "acampadasoria" "acampadatarragona" "acampadaterrasa" "acampadatoledo" "acampadavalencia" "acampadavigo" "acampadavlc" "acampadazamora" "acampadazaragoza" "acampadazgz"
do
    for i in {1..50}
    do
        curl -d "" "http://www.youtube.com/results?search_type=videos&search_query=$tag&page=$i" >> youtubepages
    done
done

egrep -E -o "/watch\?v=[0-9a-zA-Z\-\_]+\"" youtubepages | cut -d '"' -f 1 | sort | uniq | sed "s/^/http:\/\/www.youtube.com/g" >> youtubelinks

#python youtube-dl -a youtubelinks -t -c
