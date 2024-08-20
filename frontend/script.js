document.getElementById('send-button').addEventListener('click', function() {
    const userInput = document.getElementById('user-input').value;
    if (userInput.trim() === '') {
        return; // No enviar mensajes vacíos
    }

    // Añadir el input del usuario al chat log
    addMessageToChatLog('Usuario', userInput);
    document.getElementById('user-input').value = ''; // Limpiar el input

    // Enviar la solicitud a la API
    fetch('http://127.0.0.1:5000/diagnostico', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ sintomas: userInput })
    })
    .then(response => response.json())
    .then(data => {
        // Añadir la respuesta del bot al chat log
        if (data.diagnosticos.length > 0) {
            data.diagnosticos.forEach(d => {
                addMessageToChatLog('Chatbot', `Diagnóstico: ${d.diagnostico}. Recomendación: ${d.recomendacion}.`);
            });
        } else {
            addMessageToChatLog('Chatbot', 'No se encontraron diagnósticos para los síntomas proporcionados.');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        addMessageToChatLog('Chatbot', 'Ocurrió un error al procesar tu solicitud.');
    });
});

function addMessageToChatLog(sender, message) {
    const chatLog = document.getElementById('chat-log');
    const messageElement = document.createElement('div');
    messageElement.textContent = `${sender}: ${message}`;
    chatLog.appendChild(messageElement);
    chatLog.scrollTop = chatLog.scrollHeight; // Desplazar hacia abajo
}
