from http.client import responses

import flet as ft
import requests
from flet import AppBar, Text, View, ElevatedButton
from flet.core.colors import Colors
from flet.core.types import MainAxisAlignment, CrossAxisAlignment


def main(page: ft.Page):
    page.title = "Gerenciamento Biblioteca"
    page.theme_mode = ft.ThemeMode.DARK
    page.window.width = 375
    page.window.height = 667

    # --- Funções de cadastro ---
    def cadastrar_livro(novo_livro):
        url = "http://10.135.232.20:5000/cadastrar_livro"
        response = requests.post(url, json=novo_livro)
        if response.status_code == 201:
            dados = response.json()
            txt_titulo.value = dados['titulo']
            input_titulo.value = ""
            input_autor.value = ""
            input_resumo.value = ""
            input_isbn.value = ""
            page.overlay.append(msg_sucesso)
            msg_sucesso.open = True
            page.update()
        else:
            msg_error.open = True
            page.update()

    def cadastrar_usuario(novo_usuario):
        url = "http://10.135.232.20:5000/cadastrar_usuario"
        response = requests.post(url, json=novo_usuario)
        if response.status_code == 201:
            dados = response.json()
            txt_nome.value = dados['nome']
            input_nome.value = ""
            input_cpf.value = ""
            input_endereco.value = ""
            input_papel.value = ""
            page.overlay.append(msg_sucesso)
            msg_sucesso.open = True
            page.update()
        else:
            msg_error.open = True
            page.update()

    def cadastrar_emprestimo(novo_emprestimo):
        url = "http://10.135.232.20:5000/cadastrar_emprestimo"
        response = requests.post(url, json=novo_emprestimo)
        if response.status_code == 201:
            dados = response.json()
            txt_livroID.value = dados['livro_id']
            input_livro_id.value = ""
            input_usuario_id.value = ""
            input_data_emprestimo.value = ""
            input_devolucao_prevista.value = ""
            page.overlay.append(msg_sucesso)
            msg_sucesso.open = True
            page.update()
        else:
            msg_error.open = True
            page.update()

    # --- Funções de listagem ---
    def lista_livros():
        url = "http://10.135.232.7:5000/livros"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            msg_error.open = True
            page.update()
            return response.json()

    def lista_usuarios():
        url = "http://10.135.232.20:5000/usuarios"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            msg_error.open = True
            page.update()
            return None

    def lista_emprestimos():
        url = "http://10.135.232.20:5000/emprestimos"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            msg_error.open = True
            page.update()
            return None

    # --- Funções de atualização ---
    def atualizar_livro(id):
        url = f"http://10.135.232.20:5000/editar_livro/{id}"
        dados_atualizados = {
            "titulo": input_titulo.value,
            "autor": input_autor.value,
            "resumo": input_resumo.value,
            "isbn": input_isbn.value
        }
        response = requests.put(url, json=dados_atualizados)
        if response.status_code == 200:
            page.overlay.append(msg_sucesso)
            msg_sucesso.open = True
            page.update()
        else:
            msg_error.open = True
            page.update()

    def atualizar_usuario(id):
        url = f"http://10.135.232.20:5000/editar_usuario/{id}"
        dados_atualizados = {
            "nome": input_nome.value,
            "cpf": input_cpf.value,
            "endereco": input_endereco.value,
            "papel": input_papel.value
        }
        response = requests.put(url, json=dados_atualizados)
        if response.status_code == 200:
            page.overlay.append(msg_sucesso)
            msg_sucesso.open = True
            page.update()
        else:
            msg_error.open = True
            page.update()

    def atualizar_emprestimo(id):
        url = f"http://10.135.232.20:5000/editar_emprestimo/{id}"
        dados_atualizados = {
            "livro_id": input_livro_id.value,
            "usuario_id": input_usuario_id.value,
            "data_emprestimo": input_data_emprestimo.value,
            "data_devolucao": input_devolucao_prevista.value
        }
        response = requests.put(url, json=dados_atualizados)
        if response.status_code == 200:
            page.overlay.append(msg_sucesso)
            msg_sucesso.open = True
            page.update()
        else:
            msg_error.open = True
            page.update()

    # --- Funções para mostrar detalhes e listas ---
    def detalhes_livro(titulo, autor, resumo, isbn):
        txt_titulo.value = titulo
        txt_autor.value = autor
        txt_resumo.value = resumo
        txt_isbn.value = isbn
        page.update()
        page.go("/detalhes_livro")

    def detalhes_usuario(nome, cpf, endereco, papel):
        txt_nome.value = nome
        txt_cpf.value = cpf
        txt_endereco.value = endereco
        txt_papel.value = papel
        page.update()
        page.go("/detalhes_usuario")

    def detalhes_emprestimo(livro_id, usuario_id, data_emprestimo, data_devolucao):
        txt_livroID.value = livro_id
        txt_usuarioID.value = usuario_id
        txt_data_emprestimo.value = data_emprestimo
        txt_previsao_devolucao.value = data_devolucao
        page.update()
        page.go("/detalhes_emprestimo")

    def mostrar_livros(e):
        print("Entrou")
        lv.controls.clear()
        print("Esperando")
        dados = lista_livros()
        print(dados)
        if dados:
            print(dados['lista_livros'])
            for livro in dados['lista_livros']:
                lv.controls.append(
                    ft.ListTile(
                        leading=ft.Icon(ft.Icons.BOOK),
                        title=ft.Text(f"Título: {livro['titulo']}"),
                        trailing=ft.PopupMenuButton(
                            icon=ft.Icons.MORE_VERT,
                            items=[
                                ft.PopupMenuItem(
                                    text="Detalhes",
                                    on_click=lambda _, l=livro: detalhes_livro(l['titulo'], l['autor'], l['resumo'], l['isbn'])
                                )
                            ]
                        )
                    )
                )
        page.update()

    def mostrar_usuarios(e):
        lv.controls.clear()
        dados = lista_usuarios()
        if dados:
            for usuario in dados['usuarios']:
                lv.controls.append(
                    ft.ListTile(
                        leading=ft.Icon(ft.Icons.PERSON),
                        title=ft.Text(f"Nome: {usuario['nome']}"),
                        trailing=ft.PopupMenuButton(
                            icon=ft.Icons.MORE_VERT,
                            items=[
                                ft.PopupMenuItem(
                                    text="Detalhes",
                                    on_click=lambda _, u=usuario: detalhes_usuario(u['nome'], u['cpf'], u['endereco'], u['papel'])
                                )
                            ]
                        )
                    )
                )
        page.update()

    def mostrar_emprestimos(e):
        lv.controls.clear()
        dados = lista_emprestimos()
        if dados:
            for emprestimo in dados['emprestimos']:
                lv.controls.append(
                    ft.ListTile(
                        leading=ft.Icon(ft.Icons.SCHEDULE),
                        title=ft.Text(f"Livro ID: {emprestimo['livro_id']} - Usuário ID: {emprestimo['usuario_id']}"),
                        trailing=ft.PopupMenuButton(
                            icon=ft.Icons.MORE_VERT,
                            items=[
                                ft.PopupMenuItem(
                                    text="Detalhes",
                                    on_click=lambda _, em=emprestimo: detalhes_emprestimo(
                                        em['livro_id'],
                                        em['usuario_id'],
                                        em['data_emprestimo'],
                                        em['data_devolucao']
                                    )
                                )
                            ]
                        )
                    )
                )
        page.update()

    # --- Funções salvar a partir dos inputs ---
    def salvar_livro(e):
        if (input_titulo.value == "" or input_autor.value == "" or
                input_resumo.value == "" or input_isbn.value == ""):
            page.overlay.append(msg_error)
            msg_error.open = True
            page.update()
        else:
            novo_livro = {
                "titulo": input_titulo.value,
                "autor": input_autor.value,
                "resumo": input_resumo.value,
                "isbn": input_isbn.value
            }
            cadastrar_livro(novo_livro)

    def salvar_usuario(e):
        if (input_nome.value == "" or input_cpf.value == "" or
                input_endereco.value == "" or input_papel.value == ""):
            page.overlay.append(msg_error)
            msg_error.open = True
            page.update()
        else:
            novo_usuario = {
                "nome": input_nome.value,
                "cpf": input_cpf.value,
                "endereco": input_endereco.value,
                "papel": input_papel.value
            }
            cadastrar_usuario(novo_usuario)

    def salvar_emprestimo(e):
        if (input_livro_id.value == "" or input_usuario_id.value == "" or
                input_data_emprestimo.value == "" or input_devolucao_prevista.value == ""):
            page.overlay.append(msg_error)
            msg_error.open = True
            page.update()
        else:
            novo_emprestimo = {
                "livro_id": input_livro_id.value,
                "usuario_id": input_usuario_id.value,
                "data_emprestimo": input_data_emprestimo.value,
                "data_devolucao": input_devolucao_prevista.value
            }
            cadastrar_emprestimo(novo_emprestimo)

    # --- Mensagens popups ---
    msg_sucesso = ft.AlertDialog(
        title=Text("Sucesso!"),
        content=Text("Operação realizada com sucesso."),
        actions=[ft.TextButton("OK", on_click=lambda e: fechar_popup(msg_sucesso))],
        modal=True,
    )
    msg_error = ft.AlertDialog(
        title=Text("Erro!"),
        content=Text("Ocorreu um erro, tente novamente."),
        actions=[ft.TextButton("OK", on_click=lambda e: fechar_popup(msg_error))],
        modal=True,
    )

    def fechar_popup(popup):
        popup.open = False
        page.update()

    # --- Inputs comuns ---
    input_titulo = ft.TextField(label="Título")
    input_autor = ft.TextField(label="Autor")
    input_resumo = ft.TextField(label="Resumo")
    input_isbn = ft.TextField(label="ISBN")

    input_nome = ft.TextField(label="Nome")
    input_cpf = ft.TextField(label="CPF")
    input_endereco = ft.TextField(label="Endereço")
    input_papel = ft.TextField(label="Papel")

    input_livro_id = ft.TextField(label="Livro ID")
    input_usuario_id = ft.TextField(label="Usuário ID")
    input_data_emprestimo = ft.TextField(label="Data Empréstimo (AAAA-MM-DD)")
    input_devolucao_prevista = ft.TextField(label="Data Devolução Prevista (AAAA-MM-DD)")

    # --- Textos para exibição de detalhes ---
    txt_titulo = ft.Text("")
    txt_autor = ft.Text("")
    txt_resumo = ft.Text("")
    txt_isbn = ft.Text("")

    txt_nome = ft.Text("")
    txt_cpf = ft.Text("")
    txt_endereco = ft.Text("")
    txt_papel = ft.Text("")

    txt_livroID = ft.Text("")
    txt_usuarioID = ft.Text("")
    txt_data_emprestimo = ft.Text("")
    txt_previsao_devolucao = ft.Text("")

    # --- ListView ---
    lv = ft.ListView(expand=True, spacing=10)

    # --- Páginas (Views) ---
    def home_view():
        return View(
            "/",
            [
                AppBar(title=Text("Biblioteca - Home")),
                ElevatedButton("Listar Livros", on_click= mostrar_livros),
                ElevatedButton("Listar Usuários", on_click=mostrar_usuarios),
                ElevatedButton("Listar Empréstimos", on_click=mostrar_emprestimos),
                ElevatedButton("Cadastrar Empréstimos"),
                lv,
            ],
        )

    def detalhes_livro_view():
        return View(
            "/detalhes_livro",
            [
                AppBar(title=Text("Detalhes Livro")),
                txt_titulo,
                txt_autor,
                txt_resumo,
                txt_isbn,
                ElevatedButton("Voltar", on_click=lambda e: page.go("/")),
            ],
        )

    def detalhes_usuario_view():
        return View(
            "/detalhes_usuario",
            [
                AppBar(title=Text("Detalhes Usuário")),
                txt_nome,
                txt_cpf,
                txt_endereco,
                txt_papel,
                ElevatedButton("Voltar", on_click=lambda e: page.go("/")),
            ],
        )

    def detalhes_emprestimo_view():
        return View(
            "/detalhes_emprestimo",
            [
                AppBar(title=Text("Detalhes Empréstimo")),
                txt_livroID,
                txt_usuarioID,
                txt_data_emprestimo,
                txt_previsao_devolucao,
                ElevatedButton("Voltar", on_click=lambda e: page.go("/")),
            ],
        )

    # --- Adicionar Views ---
    page.views.append(home_view())
    page.views.append(detalhes_livro_view())
    page.views.append(detalhes_usuario_view())
    page.views.append(detalhes_emprestimo_view())

    def route_change(route):
        page.views.clear()
        page.views.append(home_view())
        if page.route == "/detalhes_livro":
            page.views.append(detalhes_livro_view())
        elif page.route == "/detalhes_usuario":
            page.views.append(detalhes_usuario_view())
        elif page.route == "/detalhes_emprestimo":
            page.views.append(detalhes_emprestimo_view())
        page.update()

    page.on_route_change = route_change
    page.go("/")

if __name__ == "__main__":
    ft.app(target=main)
