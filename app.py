from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def init_db():
    conexao = sqlite3.connect('estoque.db')
    cursor = conexao.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS produtos(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            quantidade INTEGER NOT NULL DEFAULT 0,
            preco REAL NOT NULL
        )
    """)
        
    conexao.commit()
    conexao.close()
    
init_db()

@app.route("/")
def home():
    conexao = sqlite3.connect('estoque.db')
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM produtos")
    produtos = cursor.fetchall()
    conexao.close()
    return render_template("index.html", produtos=produtos)
    
@app.route("/cadastrar", methods=["GET","POST"])
def cadastrar():
    nome = request.form.get("nome", "").strip()
    quantidade = request.form.get("quantidade", 0)
    preco = request.form.get("preco", 0)
    
    if not nome:
        return redirect("/")
        
    conexao = sqlite3.connect('estoque.db')
    cursor = conexao.cursor()
    cursor.execute(
        "INSERT INTO produtos VALUES (NULL, ?, ?, ?)",
        (nome, quantidade, preco)
    )
    conexao.commit()
    conexao.close()
    return redirect("/")
    
@app.route("/entrada/<int:id>")
def entrada(id):
    conexao = sqlite3.connect('estoque.db')
    cursor = conexao.cursor()
    cursor.execute("UPDATE produtos SET quantidade = quantidade + 1 WHERE id = ?", (id,))
    conexao.commit()
    conexao.close()
    return redirect("/")
    
@app.route("/saida/<int:id>")
def saida(id):
    conexao = sqlite3.connect('estoque.db')
    cursor = conexao.cursor()
    cursor.execute("UPDATE produtos SET quantidade = quantidade - 1 WHERE id = ?", (id,))
    conexao.commit()
    conexao.close()
    return redirect("/")
    
@app.route("/excluir/int:id>")
def excluir(id):
    conexao = sqlite3.connect('estoque.db')
    cursor = conexao.cursor()
    
    cursor.execute("DELETE FROM produtos WHERE id = ?",(id,))
    conexao.commit()
    conecao.close()
    return redirect("/")
    
if __name__ == '__main__':
    app.run(debug=True)