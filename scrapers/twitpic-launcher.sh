#!/bin/bash

for i in "acampadasol" "spanishrevolution" "democraciarealya" "15menpleno" "nolesvotes" "acampadaacoruna" "acampadacoruna" "acampadaalcala" "acampadaalicante" "acampadaalmeria" "acampadabarcelona" "acampadabcn" "acampadabenicarlo" "acampadabilbao" "acampadacadiz" "acampadacaceres" "acampadacastellon" "acampadachiclana" "acampadacordoba" "acampadadonostia" "acampadaelche" "acampadaferrol" "acampadagasteiz" "acampadagranada" "acampadaibiza" "acampadajerez" "acampadalaspalmas" "acampadapalmas" "acampadaleon" "acampadalleida" "acampadalogrono" "acampadamadrid" "acampadamalaga" "acampadamurcia" "acampadapalencia" "acampadapalma" "acampadamallorca" "acampadapamplona" "acampadaoviedo" "acampadaronda" "acampadasalamanca" "acampadasantiago" "acampadasevilla" "acampadasoria" "acampadatarragona" "acampadaterrasa" "acampadatoledo" "acampadavalencia" "acampadavigo" "acampadavlc" "acampadazamora" "acampadazaragoza" "acampadazgz"
do
    python twitpicimages.py $i &
done
