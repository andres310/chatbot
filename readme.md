# Chatbot de Atención Médica

Este proyecto es un Chatbot de Atención Médica desarrollado con **Python** y **Flask** en el backend, y **HTML**, **CSS**, y **JavaScript** en el frontend. El chatbot permite a los usuarios ingresar síntomas y recibir un diagnóstico junto con una recomendación basada en una base de conocimientos predefinida.

## Tabla de Contenidos

- [Requisitos Previos](#requisitos-previos)
- [Instalación](#instalación)
- [Uso](#uso)
- [Descripción del Backend](#descripción-del-backend)
- [Descripción del Frontend](#descripción-del-frontend)
- [Flujograma](#flujograma)
- [Consideraciones Adicionales](#consideraciones-adicionales)

## Requisitos Previos

- **Python 3.10** (o superior)
- **Flask**
- **Flask_cors**
- **Pandas**
- **SpaCy**
- **Modelo de idioma `es_core_news_sm` de SpaCy**

## Instalación

1. **Clona este repositorio:**

   ```bash
   git clone https://github.com/andres310/chatbot-atencion-medica.git
   cd chatbot-atencion-medica

2. **Instala las dependencias del backend**

    ```bash
    pip install -r requirements.txt
    pip install flask_cors
    python -m spacy download es_core_news_sm

## Uso

1. **Inicia el servidor Flask**

    ```bash
    python app.py

El servidor estará disponible en http://127.0.0.1:5000.

## Descripción del Backend

El backend del proyecto está desarrollado con Flask y utiliza SpaCy para el procesamiento de lenguaje natural. Se basa en una base de conocimientos (base_conocimientos.csv) que mapea síntomas a posibles diagnósticos y recomendaciones.

### Estructura del Backend
- **app.py:** Contiene la lógica principal del backend, incluyendo la API para procesar los síntomas y devolver los diagnósticos.
- **base_conocimientos.csv:** Un archivo CSV que contiene la base de conocimientos, mapeando síntomas a diagnósticos y recomendaciones.
- **requirements.txt:** Lista de dependencias necesarias para ejecutar el backend.

### Ejemplo de Endpoint
- POST /diagnostico: Recibe un JSON con los síntomas del usuario y devuelve un diagnóstico basado en la base de conocimientos.

Ejemplo de solicitud:

    ```bash
    curl -X POST http://127.0.0.1:5000/diagnostico -H "Content-Type: application/json" -d '{"sintomas": "Tengo dolor abdominal"}'


Ejemplo de respuesta:

    ```json
    {
        "diagnosticos": [
            {
                "diagnostico": "apendicitis",
                "recomendacion": "ir a emergencias para cirugía",
                "sintomas_detectados": ["dolor abdominal"]
            }
        ]
    }


## Descripción del Frontend

El frontend es una aplicación web sencilla construida con HTML, CSS, y JavaScript. Permite a los usuarios ingresar sus síntomas y muestra las respuestas del chatbot en una interfaz simple.

### Estructura del Frontend

- **index.html:** Estructura HTML de la interfaz de usuario.
- **styles.css:** Estilos CSS para una presentación atractiva.
- **script.js:** Lógica en JavaScript para manejar la interacción con la API y actualizar la interfaz de usuario.

### Funcionamiento del Frontend
1. **Interfaz de Usuario:** Permite a los usuarios ingresar texto describiendo sus síntomas.
2. **Interacción con la API:** Envía los síntomas del usuario al backend y muestra la respuesta en el chat log.
3. **Manejo de Errores:** Notifica al usuario en caso de que ocurra un error al procesar la solicitud.

## Flujograma

```mermaid
flowchart TD
    A[Usuario] --> B[Frontend (HTML, CSS, JS)]
    B --> C[Envío de síntomas al Backend]
    C --> D[API Flask]
    D --> E[Procesamiento de texto con SpaCy]
    E --> F[Consulta a la base de conocimientos]
    F --> G[Generar diagnóstico y recomendación]
    G --> H[Enviar respuesta al Frontend]
    H --> I[Mostrar diagnóstico al usuario]
