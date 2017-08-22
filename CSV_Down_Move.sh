wget -O /home/airine/spark-2.2.0-bin-hadoop2.7/Mapa-Streaming/CSV_temp/temp.csv http://dadosabertos.rio.rj.gov.br/apiTransporte/apresentacao/csv/onibus.cfm
if [ $(find /home/airine/spark-2.2.0-bin-hadoop2.7/Mapa-Streaming/CSV_temp/temp.csv -type f -size +0c 2>/dev/null) ]; then
    mv /home/airine/spark-2.2.0-bin-hadoop2.7/Mapa-Streaming/CSV_temp/temp.csv /home/airine/spark-2.2.0-bin-hadoop2.7/Mapa-Streaming/dados/onibus.csv
else
    rm /home/airine/spark-2.2.0-bin-hadoop2.7/Mapa-Streaming/CSV_temp/temp.csv
fi

