from flask import Flask, jsonify, request
import threading

app = Flask(__name__)

lock = threading.Lock()

PROXY_FILE = "proxy.txt"

def ler_proxies():
    """Lê todos os proxies do arquivo, mesmo que estejam em uma única linha."""
    with lock:
        with open(PROXY_FILE, "r") as file:
            data = file.read()
            proxies = data.replace("\n", " ").split()
            return proxies

def salvar_proxies(proxies):
    """Salva os proxies de volta ao arquivo em formato de uma única linha."""
    with lock:
        with open(PROXY_FILE, "w") as file:
            file.write(" ".join(proxies) + "\n")

@app.route("/get_proxy", methods=["GET"])
def get_proxy():
    proxies = ler_proxies()
    if not proxies:
        return jsonify({"error": "No proxies available"}), 404

    proxy = proxies.pop(0) 
    salvar_proxies(proxies)
    return jsonify({"proxy": proxy})

@app.route("/add_proxy", methods=["POST"])
def add_proxy():
    new_proxies = request.json.get("proxies", [])
    if not new_proxies:
        return jsonify({"error": "No proxies provided"}), 400

    proxies = ler_proxies()
    proxies.extend(new_proxies)
    salvar_proxies(proxies)
    return jsonify({"message": "Proxies added successfully"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)