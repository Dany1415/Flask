from flask import Flask, render_template,request
import pandas as pd                 # Para la manipulación y análisis de los datos
import numpy as np                  # Para crear vectores y matrices n dimensionales
import matplotlib.pyplot as plt     # Para la generación de gráficas a partir de los datos
from apyori import apriori # Para el algoritmo apriori
import os # os es para crear un folder estatico
import io

app = Flask(__name__)
def mostrarGrafica(data):
  print("yaaaaaa")
  print("pofavot")
  Transacciones = data.values.reshape(-1).tolist() #-1 significa 'dimensión no conocida'
  Lista = pd.DataFrame(Transacciones)
  Lista['Frecuencia'] = 1
  Lista = Lista.groupby(by=[0], as_index=False).count().sort_values(by=['Frecuencia'], ascending=True) #Conteo
  Lista['Porcentaje'] = (Lista['Frecuencia'] / Lista['Frecuencia'].sum()) #Porcentaje
  Lista = Lista.rename(columns={0 : 'Item'})
  
  plt.figure(figsize=(16,20), dpi=300)
  plt.ylabel('Item')
  plt.xlabel('Frecuencia')
  plt.barh(Lista['Item'], width=Lista['Frecuencia'], color='blue')
  
  # Guardar la figura para mostrarla después:
  img = io.BytesIO()
  plt.savefig(img, format='png')
  img.seek(0)
  return render_template('index.html', img_show = img.getvalue())


def apriori(data, minSup, minConf, minLift):
  dataRecived = data.stack().groupby(level=0).apply(list).tolist()
  ReglasC1 = apriori(dataRecived, 
                   min_support=1,#minSup, 
                   min_confidence=1,#minConf, 
                   min_lift=1) #minLift)
  ResultadosC1 = list(ReglasC1)
  pd.DataFrame(ResultadosC1)
  for item in ResultadosC1:
    #El primer índice de la lista
    Emparejar = item[0]
    items = [x for x in Emparejar]
    print("Regla: " + str(item[0]))

    #El segundo índice de la lista
    print("Soporte: " + str(item[1]))

    #El tercer índice de la lista
    print("Confianza: " + str(item[2][0][2]))
    print("Elevación: " + str(item[2][0][3])) 
    print("=====================================") # Aquí deberíamos asociar el valor correspondiente a la etiqueta




# Para guardar el form
@app.route('/',  methods = ['GET','POST'])
def index(): #aqui ponemos toda la logica del guardado
  #si el metodo seleccionado es post
  if request.method=="POST":
    file=request.files['cvsfile']
    df = pd.read_csv(file)
    showdf = df.head() # DataFrame para poder mostrarlo en pantalla.
    #apriori(df,1,1,1) 

    #se genera una carpeta llamada static si no existe antes y ahi guarda los archivos subidos
    if not os.path.isdir('static'):
      os.mkdir('static')
    filepath=os.path.join('static',file.filename)
    file.save(filepath)

    #si se importa el file, deberia poder obtener el mensaje
    #del nombre del archivo con la linea comentada siguiente
    #return 'the file name of the uploaded file is:{}'.format(file.filename)
  return render_template('index.html', data=showdf.to_html(index=False))

#y esto es para que una vez se corra el programa se vayan actualizando lo scambios solos , solo con guardar
if __name__=='__main__':
  app.run(debug=True)

  
