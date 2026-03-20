from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)

MEMORY_FILE = os.path.join(os.path.dirname(__file__), "memory.json")

def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {
        "مرحبا": "أهلاً وسهلاً بك! كيف يمكنني مساعدتك؟",
        "من أنت": "أنا Zenith AI، مساعدك الذكي الذي يتعلم منك!",
        "كيف حالك": "بخير جداً شكراً! وأنت؟",
        "شكرا": "العفو! سعيد بمساعدتك دائماً 🙏",
        "وداعا": "مع السلامة! أراك قريباً.",
    }

def save_memory(memory):
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(memory, f, ensure_ascii=False, indent=4)

@app.route("/")
def index():
    return send_from_directory(".", "zenith-ai.html")

@app.route("/memory", methods=["GET"])
def get_memory():
    return jsonify(load_memory())

@app.route("/memory", methods=["POST"])
def add_memory():
    data = request.json
    q = data.get("question", "").strip()
    a = data.get("answer", "").strip()
    if not q or not a:
        return jsonify({"error": "السؤال والجواب مطلوبان"}), 400
    memory = load_memory()
    memory[q] = a
    save_memory(memory)
    return jsonify({"success": True, "total": len(memory)})

@app.route("/memory/<path:question>", methods=["DELETE"])
def delete_memory(question):
    memory = load_memory()
    if question in memory:
        del memory[question]
        save_memory(memory)
        return jsonify({"success": True})
    return jsonify({"error": "غير موجود"}), 404

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print("=" * 40)
    print(f"  Zenith AI يعمل على المنفذ {port}")
    print("=" * 40)
    app.run(host="0.0.0.0", port=port, debug=False)
