from pyspark.sql import SparkSession, SQLContext
from pyspark.sql.types import *


#Definicao do diretorio de trabalho
caminhoInterno = "/home/airine/spark-2.2.0-bin-hadoop2.7/Mapa-Streaming/"


class Processador:
    #Definicao do schema do CSV e geracao de um Dataframe com os dados
    def __init__(self, sc, dataset_path): 
        sqlContext = SQLContext(sc)
        schema = StructType([StructField("dataHora", StringType(), True), StructField("ordem", StringType(), True), StructField("linha", StringType(), True), StructField("latitude", StringType(), True), StructField("longitude", StringType(), True), StructField("velocidade", StringType(), True)])
        lines = sc.textFile(dataset_path)        
        
        self.lista_onibus = lines.map(lambda x: x.replace(u'"','')).map(lambda l: l.split(','))
        header = self.lista_onibus.first()
        self.lista_onibus_NoHeader = self.lista_onibus.filter(lambda row : row != header)
        self.loDF = sqlContext.createDataFrame(self.lista_onibus_NoHeader, schema)

        
    #Aplicacao dos filtros do usuario no Dataframe e coleta dos dados como uma String
    def get_lista_onibus(self, linha = "", ordem = ""):
        
        if linha == 'all' and ordem == 'all':
            self.loDF2 = self.loDF
        elif linha != 'all' and ordem != 'all':            
            self.loDF2 = self.loDF.filter("ordem = '"+ordem+"'").filter("linha = "+linha)
        elif linha != 'all':
            self.loDF2 = self.loDF.filter("linha = '"+linha+"'")
        elif ordem != 'all':
            self.loDF2 = self.loDF.filter("ordem = '"+ordem+"'")

        colecao = self.loDF2.collect()
        return colecao

    
    #Contagem do total de onibus presentes no Dataframe 
    def get_total_onibus(self):
        quant = self.loDF2.count()
        return quant
