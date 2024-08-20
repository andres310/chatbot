from flask import Flask, request, jsonify
from flask_cors import CORS
import spacy
import pandas as pd
from nltk.corpus import wordnet
from spacy.matcher import PhraseMatcher

# Inicializar la aplicación Flask
app = Flask(__name__)
CORS(app)  # Esto habilita CORS para todas las rutas

# Cargar el modelo de SpaCy para español
nlp = spacy.load('es_core_news_sm')
matcher = PhraseMatcher(nlp.vocab, attr='LOWER')

# Cargar la base de datos de síntomas y diagnósticos
data = pd.read_csv("base_conocimientos.csv")

# Crear un listado de síntomas en la base de datos
sintomas_base = set()
for _, row in data.iterrows():
    for sintoma in row['sintomas'].split(','):
        sintomas_base.add(sintoma.strip())
# Añadir todas las frases de síntomas a PhraseMatcher
patterns = [nlp(sintoma) for sintoma in sintomas_base]
matcher.add("SINTOMAS", patterns)

def obtener_sinonimos(palabra):
    sinonimos = set()
    for syn in wordnet.synsets(palabra, lang='spa'):
        for lemma in syn.lemmas('spa'):
            sinonimos.add(lemma.name())
    return sinonimos

# Función para procesar el texto y extraer síntomas
def procesar_texto(texto):
    doc = nlp(texto)
    sintomas = []
    sintomas_detectados = []
    matches = matcher(doc)

    """for token in doc:
        if token.pos_ == 'NOUN':  # Identificar sustantivos como síntomas
            sintomas.append(token.text)
    return sintomas"""
    for match_id, start, end in matches:
        sintomas_detectados.append(doc[start:end].text)
    
    return sintomas_detectados

# Función para hacer el diagnóstico basado en los síntomas
def diagnosticar(sintomas_usuario):
    diagnosticos_posibles = []
    diagnosticos_vistos = set()
    
    for _, row in data.iterrows():
        sintomas_base = row['sintomas'].split(',')
        coincidencias = [sintoma for sintoma in sintomas_usuario if sintoma in sintomas_base]
        
        if len(coincidencias) > 0:
            clave_diagnostico = (row['diagnostico'], row['recomendacion'])
            if clave_diagnostico not in diagnosticos_vistos:
                diagnosticos_vistos.add(clave_diagnostico)
                diagnosticos_posibles.append({
                    "diagnostico": row['diagnostico'],
                    "recomendacion": row['recomendacion'],
                    "sintomas_detectados": coincidencias
                })
    
    return diagnosticos_posibles
"""def diagnosticar(sintomas_usuario):
    diagnosticos_posibles = []
    diagnosticos_vistos = set()  # Usamos un set para evitar duplicados
    
    for _, row in data.iterrows():
        sintomas_base = row['sintomas'].split(',')
        coincidencias = [sintoma for sintoma in sintomas_usuario if sintoma in sintomas_base]
        
        if len(coincidencias) > 0:
            # Crear una clave única para evitar duplicados
            clave_diagnostico = (row['diagnostico'], row['recomendacion'])
            
            # Si el diagnóstico no ha sido agregado aún, añadirlo
            if clave_diagnostico not in diagnosticos_vistos:
                diagnosticos_vistos.add(clave_diagnostico)
                diagnosticos_posibles.append({
                    "diagnostico": row['diagnostico'],
                    "recomendacion": row['recomendacion'],
                    "sintomas_detectados": coincidencias
                })
                
    return diagnosticos_posibles"""

# Ruta para manejar solicitudes POST para diagnóstico
@app.route('/diagnostico', methods=['POST'])
def obtener_diagnostico():
    datos = request.get_json()  # Obtener los datos en formato JSON
    sintomas = procesar_texto(datos['sintomas'])  # Procesar los síntomas enviados
    diagnosticos = diagnosticar(sintomas)  # Obtener posibles diagnósticos
    
    if diagnosticos:
        return jsonify({
            "diagnosticos": diagnosticos
        }), 200
    else:
        return jsonify({
            "mensaje": "No se pudo identificar ningún diagnóstico basado en los síntomas."
        }), 400

# Ruta de prueba para verificar que la API está funcionando
@app.route('/test', methods=['GET'])
def test():
    return "La API está funcionando correctamente", 200

# Iniciar la aplicación Flask
if __name__ == '__main__':

    app.run(debug=True)
