import flet as ft
from flet import AppBar, Text, View, ElevatedButton
from flet.core.colors import Colors
import requests


def cadastro_livro(e, livro):
    url = f"http://10.135.232.7:5000/novo_livro"
    novo_livro = {
        "Título": input_titulo.value,
        "Autor": input_autor.value,
        "ISBN": input_isbn.value,
        "Resumo": input_resumo.value,
    }

    resposta_post = requests.post(url, json=novo_livro)
    if resposta_post.status_code == 201:
        dados_livro = resposta_post.json()
        print(f"Título: {dados_livro['titulo']}")
        print(f"Autor: {dados_livro['autor']}")
        print(f"ISBN: {dados_livro['isbn']}")
        print(f"Resumo: {dados_livro['resumo']}")

    else:
        print(f"Erro: {resposta_post.status_code}")





























































































































def cadastro_usuario(e, usuario):
    url = f"http://127.0.0.1:5000/novo_usuario"


# componentes
input_titulo = ft.TextField(label="Título")
input_autor = ft.TextField(label="Autor")
input_resumo = ft.TextField(label="Resumo")
input_isbn = ft.TextField(label="ISBN")
