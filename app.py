from flask import Flask, request, jsonify, render_template
import requests
import discord

app = Flask(__name__)

def perform_operation(num1, num2, operation):
    try:
        num1 = float(num1)
        num2 = float(num2)
        if operation == 'add':
            return num1 + num2
        elif operation == 'subtract':
            return num1 - num2
        elif operation == 'multiply':
            return num1 * num2
        elif operation == 'divide':
            if num2 == 0:
                return 'Erreur : Division par zéro'
            return num1 / num2
        else:
            return 'Opération invalide'
    except ValueError:
        return 'Erreur : Entrée non valide'

def send_to_discord(result, num1, num2, operation_text):
    """Envoie le résultat du calcul vers Discord via un webhook."""
    content = f"**Nouveau calcul :**\n{num1} {operation_text} {num2} = {result}"
    data = {"content": content}

    # Envoi de la requête POST au webhook Discord
    response = requests.post("https://discord.com/api/webhooks/1299643581706797106/2OM_OxlcQxya7ulqCBLzgxRHfmoZfpy-5PW7frhZhlzmBGnNH0J-DRbBEK2xm-ZRxwZl", json=data)
    if response.status_code == 204:
        print("Message envoyé avec succès sur Discord.")
    else:
        print(f"Erreur lors de l'envoi sur Discord : {response.status_code}, {response.text}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    num1 = request.form.get('num1')
    num2 = request.form.get('num2')
    operation = request.form.get('operation')
    
    result = perform_operation(num1, num2, operation)

    # Texte de l'opération pour l'historique et le message Discord
    operation_text = {
        'add': '+',
        'subtract': '-',
        'multiply': '*',
        'divide': '/'
    }.get(operation, '?')

    # Envoi du résultat sur Discord
    send_to_discord(result, num1, num2, operation_text)

    # Retourne le résultat en JSON
    return jsonify({'result': result})


if __name__ == '__main__':
    app.run(debug=True)
