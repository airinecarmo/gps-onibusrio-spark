from processador import Processador
import json
from flask import Flask, request, render_template
import time, sys, os
from pyspark.sql import SparkSession, SQLContext, Row
from pyspark.sql.types import *
from pyspark import SparkContext
import numpy as np

#Definicoes da aplicacao Flask        
app = Flask(__name__) 

#Definicao dos diretorios de trabalho
caminho = "/home/airine/spark-2.2.0-bin-hadoop2.7/Mapa-Streaming/"
caminhoInterno = "/home/airine/spark-2.2.0-bin-hadoop2.7/Mapa-Streaming/"
    
@app.route('/')
def index():
    return render_template("login.html")

@app.route('/cadastroindex')
def cadastro_index():      
    return render_template("cadastro.html")

def run_server(app):
  app.run(port=5000)

  
@app.route("/onibus-json/<linha>/<ordem>", methods=["GET"])
def onibus_json(linha, ordem): 
  
  #Execucao da funcao que processa os filtros do usuario
  lista = processador.get_lista_onibus(linha, ordem)    

  #Conversao dos dados coletados do Dataframe para o formato JSON
  lista_onibus = []
  for row in lista:
    onibus = {'dataHora' : row[0],
              'ordem' :      row[1],
              'linha' :      row[2],
              'latitude' :   row[3],
              'longitude' :  row[4],
              'velocidade' : row[5]}
    lista_onibus.append(onibus)          
  retorno = json.dumps(lista_onibus)
  return retorno

@app.route("/cadastro", methods=["POST"])
def cadastro(): 
  nome = request.form['nome']
  senha = request.form['senha']
  linhaOnibus = request.form['linhasOnibus']

  sqlContext_usuario = SQLContext(sc)
  schema_usuario = StructType([StructField("nome", StringType(), True), StructField("senha", StringType(), True), StructField("linha", StringType(), True)])
  
  lines = sc.textFile(caminho+"/dados/usuario.csv")        
  usuarios = lines.map(lambda x: x.replace(u'"','')).map(lambda l: l.split(','))
  loDF_usuario = sqlContext_usuario.createDataFrame(usuarios, schema_usuario)  
  
  newRow = spark.createDataFrame([Row(nome=nome, senha=senha, linha=linhaOnibus)],schema_usuario)
  print(newRow)
  
  loDF_usuario = loDF_usuario.union(newRow)

  uc = loDF_usuario.collect()
  print(uc)

  loDF_usuario.toPandas().to_csv(caminhoInterno+'dados/usuario.csv', header=False, index=False)

  return render_template("home.html")

@app.route("/login", methods=["POST"])
def login(): 
  nome = request.form['nome']
  senha = request.form['senha']

  sqlContext_usuario = SQLContext(sc)
  schema_usuario = StructType([StructField("nome", StringType(), True), StructField("senha", StringType(), True), StructField("linha", StringType(), True)])
  
  lines = sc.textFile(caminho+"/dados/usuario.csv")        
  usuarios = lines.map(lambda x: x.replace(u'"','')).map(lambda l: l.split(','))
  loDF_usuario = sqlContext_usuario.createDataFrame(usuarios, schema_usuario)
  loDF_usuario_filtrado = loDF_usuario.filter("nome = '"+nome+"' AND senha ='"+senha+"'")

  colecao = loDF_usuario_filtrado.collect()  
  print(colecao)

  print(loDF_usuario_filtrado.select("linha"))

  if colecao != []:
    return render_template("home.html")
  
  return render_template("login.html")

#Inicializacao do Spark
if __name__ == "__main__":
  sc = SparkContext("local", "App Name", pyFiles=[caminhoInterno+'mapagps.py', caminhoInterno+'processador.py'])
  spark = SparkSession.builder.appName("GPS Onibus RJ").getOrCreate()  
  sc.setLogLevel('ERROR')  
  
  global processador
  processador = Processador(sc, caminho+"/dados/onibus.csv")  
  

  #Inicializacao da aplicacao Flask
  run_server(app)
