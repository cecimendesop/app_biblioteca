from http.client import responses

import flet as ft
import requests
from flet import AppBar, Text, View, ElevatedButton
from flet.core.colors import Colors
from flet.core.types import CrossAxisAlignment

def main(page: ft.Page):
    # Configurações
    page.title = "Exemplo de listas"
    page.theme_mode = ft.ThemeMode.DARK  # ou ft.ThemeMode.DARK
    page.window.width = 375
    page.window.height = 667

    def salvar_livro(e):
        if (input_titulo.value == "" or input_isbn.value == ""
                or input_resumo.value == "" or input_autor.value == ""):
            page.overlay.append(msg_error)
            msg_error.open = True
            page.update()
        else:
            novo_livro = {
                "titulo": input_titulo.value,
                "autor": input_autor.value,
                "isbn": input_isbn.value,
                "resumo": input_resumo.value
            }
            cadastro_livro(novo_livro)


    def salvar_usuario(e):
        if (input_nome.value == "" or input_cpf.value == ""
                or input_endereco.value == "" or input_papel.value == ""):
            page.overlay.append(msg_error)
            msg_error.open = True
            page.update()
        else:
            novo_usuario = {
                'nome': input_nome.value,
                'cpf': input_cpf.value,
                "endereco": input_endereco.value,
                "papel": input_papel.value,
            }

            cadastro_usuario(novo_usuario)

    def salvar_emprestimo(e):
        if (input_livro_id.value == "" or input_usuario_id.value == ""
                or input_data_emprestimo.value == "" or input_devolucao_prevista.value == ""):
            page.overlay.append(msg_error)
            msg_error.open = True
            page.update()
        else:
            novo_emprestimo = {
                'livro_id': input_livro_id.value,
                'usuario_id': input_usuario_id.value,
                "data_emprestimo": input_data_emprestimo.value,
                "data_devolucao_prevista": input_devolucao_prevista.value,
            }

            cadastro_emprestimo(novo_emprestimo)



    def cadastro_livro(novo_livro):
        url = 'http://10.135.232.20:5000/novo_livro'

        response = requests.post(url, json=novo_livro)

        if response.status_code == 201:
            dados_livros = response.json()
            txt_titulo.value = dados_livros['titulo']

            input_titulo.value = ""
            input_isbn.value = ""
            input_resumo.value = ""
            input_autor.value = ""
            page.overlay.append(msg_sucesso)
            msg_sucesso.open = True
            page.update()

        else:
            print(response.status_code)
        cadastro_livro(salvar_livro)

    def cadastro_usuario(novo_usuario):
        url = 'http://10.135.232.20:5000/novo_usuario'
        response = requests.post(url, json=novo_usuario)

        if response.status_code == 201:
            dados_usuario = response.json()
            txt_nome.value = dados_usuario['nome']
            input_nome.value = ''
            input_cpf.value = ""
            input_endereco.value = ""
            input_papel.value = ""
            page.overlay.append(msg_sucesso)
            msg_sucesso.open = True
            page.update()
        else:
            print(response.json())

    def cadastro_emprestimo(novo_emprestimo):
        url = 'http://10.135.232.20:5000/realizar_emprestimo'
        response = requests.post(url, json=novo_emprestimo)

        if response.status_code == 201:
            dados_emprestimo = response.json()

            txt_livroID.value = dados_emprestimo['livro_id']

            input_livro_id.value = ""
            input_usuario_id.value = ""
            input_data_emprestimo.value = ""
            input_devolucao_prevista.value = ""
            page.overlay.append(msg_sucesso)
            msg_sucesso.open = True
            page.update()
        else:
            print(response.status_code)
            print(response.json())

    def lista_livros():
        url = 'http://10.135.232.20:5000/livros'
        response_livros = requests.get(url)

        if response_livros.status_code == 200:
            dados_livro = response_livros.json()
            return dados_livro
        else:
            msg_error.open = True

    def lista_emprestimos():
        url = 'http://10.135.232.20:5000/emprestimos'
        response_emprestimos = requests.get(url)

        if response_emprestimos.status_code == 200:
            dados_emprestimos = response_emprestimos.json()
            return dados_emprestimos
        else:
            msg_error.open = True

    def lista_usuarios():
        url = 'http://10.135.232.20:5000/usuarios'
        response_usuarios = requests.get(url)

        if response_usuarios.status_code == 200:
            dados_usuario = response_usuarios.json()
            return dados_usuario
        else:
            msg_error.open = True

    def lista_status():
        url = 'http://10.135.232.20:5000/livro_status'
        response_status = requests.get(url)

        if response_status.status_code == 200:
            dados_emprestimo = response_status.json()
            return dados_emprestimo
        else:
            msg_error.open = True

    def atualizar_livros(id):
        url = 'http://10.135.232.20:5000/atualizar_livro/<int:id>'

        atualizar_livro = {
            'id': id,
            'titulo': input_titulo.value,
            'isbn': input_isbn.value,
            'resumo': input_resumo.value,
            'autor': input_autor.value,
        }

        antes = requests.get(url, json=atualizar_livro)
        response = requests.put(url, json=atualizar_livro)

        if response.status_code == 200:
            if antes.status_code == 200:
                dados_antes = antes.json()
                print(f' Titulo antigo: {dados_antes["title"]}')
            else:
                print(f' Erro: {response.status_code}')
            dados_put = response.json()
            print(f' Titulo: {dados_put["title"]}')
            print(f' Conteudo: {dados_put["body"]}\n')
            page.go('/editar_livro')
        else:
            print(f' Erro: {response.status_code}')

    def atualizar_usuarios(id):
        url = 'http://10.135.232.20:5000/atualizar_usuario/<id>'

        atualizar_livros = {
            'id': id,
            'titulo': input_titulo.value,
            'isbn': input_isbn.value,
            'resumo': input_resumo.value,
            'autor': input_autor.value,
        }

        antes = requests.get(url, json=atualizar_livros)
        response = requests.put(url, json=atualizar_livros)

        if response.status_code == 200:
            if antes.status_code == 200:
                dados_antes = antes.json()
                print(f' Titulo antigo: {dados_antes["title"]}')
            else:
                print(f' Erro: {response.status_code}')
            dados_put = response.json()
            print(f' Titulo: {dados_put["title"]}')
            print(f' Conteudo: {dados_put["body"]}\n')
        else:
            print(f' Erro: {response.status_code}')

    def atualizar_emprestimo(id):
        url = 'http://10.135.232.20:5000/editar_emprestimo/<id>'

        atualizar_emprestimo = {
            'id': id,
            'livro_id': input_livro_id.value,
            'usuario_id': input_usuario_id.value,
            'data_emprestimo': input_data_emprestimo.value,
            'data_devolucao': input_devolucao_prevista.value
        }

        antes = requests.get(url, json=atualizar_emprestimo)
        response = requests.put(url, json=atualizar_emprestimo)

        if response.status_code == 200:
            if antes.status_code == 200:
                dados_antes = antes.json()
                print(f' Data de devolução antiga: {dados_antes["title"]}')
            else:
                print(f' Erro: {response.status_code}')
            dados_put = response.json()
            print(f' Titulo: {dados_put["title"]}')
            print(f' Conteudo: {dados_put["body"]}\n')
        else:
            print(f' Erro: {response.status_code}')


    def livros(e):
        lv.controls.clear()
        resultado_lista = lista_livros()
        print(f' Livros: {resultado_lista["livros"]}')
        for livro in resultado_lista['livros']:
            lv.controls.append(
                ft.ListTile(
                    leading=ft.Icon(ft.Icons.BOOK),
                    title=ft.Text(f'Título: {livro["titulo"]}'),
                    trailing=ft.PopupMenuButton(
                        icon=ft.Icons.MORE_VERT,
                        items=[
                            ft.PopupMenuItem(text="DETALHES"),
                            ft.PopupMenuItem(text="EDITAR", on_click=lambda _, l=livro: atualizar_livros(l)),
                        ]
                    )
                )
            )

    def status(e):
        lv.controls.clear()
        resultado_status = lista_status()
        print(f' Status: {resultado_status["livros_emprestados"]}')
        for status in resultado_status['livros_emprestados']:
            lv.controls.append(
                ft.ListTile(
                    leading=ft.Icon(ft.Icons.BOOK_OUTLINED),
                    title=ft.Text(f'Título: {status["titulo"]}'),
                    trailing=ft.PopupMenuButton(
                        icon=ft.Icons.MORE_VERT,
                        items=[
                            ft.PopupMenuItem(text="DETALHES", on_click=lambda _, l=status: lista_status()),
                        ]
                    )
                )
            )

        for status_disponiveis in resultado_status['livros_disponiveis']:
            lv.controls.append(
                ft.ListTile(
                    leading=ft.Icon(ft.Icons.BOOK),
                    title=ft.Text(f'Título: {status_disponiveis["titulo"]}'),
                    trailing=ft.PopupMenuButton(
                        icon=ft.Icons.MORE_VERT,
                        items=[
                            ft.PopupMenuItem(text="DETALHES", on_click=lambda _, l=status: lista_status()),
                        ]
                    )
                )
            )


    def emprestimos(e):
        lv.controls.clear()
        resultado_emprestimo = lista_emprestimos()
        print(f' Livros: {resultado_emprestimo["emprestimos"]}')
        for emprestimo in resultado_emprestimo['emprestimos']:
            lv.controls.append(
                ft.ListTile(
                    leading=ft.Icon(ft.Icons.BOOK),
                    title=ft.Text(f'Livro id: {emprestimo["livro_id"]}'),
                    trailing=ft.PopupMenuButton(
                        icon=ft.Icons.MORE_VERT,
                        items=[
                            ft.PopupMenuItem(text="DETALHES"),
                            ft.PopupMenuItem(text="EDITAR", on_click=lambda _: atualizar_emprestimo(id)),
                        ]
                    )
                )
            )

    def usuarios(e):
        lv.controls.clear()
        resultado_usuario = lista_usuarios()
        print(f' Usuarios: {resultado_usuario["usuarios"]}')
        for usuario in resultado_usuario['usuarios']:
            lv.controls.append(
                ft.ListTile(
                    leading=ft.Icon(ft.Icons.PERSON),
                    title=ft.Text(f'Usuario: {usuario["nome"]}'),
                    trailing=ft.PopupMenuButton(
                        icon=ft.Icons.MORE_VERT,
                        items=[
                            ft.PopupMenuItem(text="DETALHES",),
                            ft.PopupMenuItem(text="EDITAR", on_click=lambda _: atualizar_usuarios(id)),
                        ]
                    )
                )
            )



    def gerenciar_rotas(e):
        page.views.clear()
        page.views.append(
            View(
                "/",
                (
                    ft.Container(
                        ft.Image(src="livro.png"),
                        margin=30,
                    ),

                    ElevatedButton(text="Cadastrar",
                                       color=ft.Colors.WHITE,
                                       on_click=lambda _: page.go("/cadastros"),
                                       bgcolor=Colors.BLACK),

                    ElevatedButton(
                        text="Listar",
                        color=ft.Colors.BLACK,
                        on_click=lambda _: page.go("/listas"),
                        bgcolor=Colors.WHITE,
                    ),

                    ElevatedButton(
                        text="Status",
                        color=ft.Colors.BLACK,
                        on_click=lambda _: page.go("/livro_status"),
                        bgcolor=Colors.WHITE,
                    ),
                ),
                bgcolor="#213D85",
                horizontal_alignment=CrossAxisAlignment.CENTER,
            )
        )

        if page.route == "/cadastros":
            page.views.append(
                View(
                    "/cadastros",
                    [
                        AppBar(title=Text("Cadastros"), bgcolor="#2CC3FF"),
                        ElevatedButton(text="Livro",
                                       color=ft.Colors.WHITE,
                                       on_click=lambda _: page.go("/novo_livro"),
                                       bgcolor="#2C30FF",
                                       width=page.window.width),

                        ElevatedButton(text="Usuário",
                                       color=ft.Colors.BLACK,
                                       on_click=lambda _: page.go("/novo_usuario"),
                                       bgcolor="#2CC3FF",
                                       width=page.window.width),

                        ElevatedButton(text="Empréstimo",
                                       color=ft.Colors.WHITE,
                                       on_click=lambda _: page.go("/realizar_emprestimo"),
                                       bgcolor="#2C30FF",
                                       width=page.window.width)

                    ],
                    bgcolor="#213D85",
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                )
            )

        if page.route == "/novo_livro":
            page.views.append(
                View(
                    "/novo_livro",
                    [
                        AppBar(title=Text("Cadastrar Livro"), bgcolor="#2CC3FF"),
                        input_titulo,
                        input_autor,
                        input_resumo,
                        input_isbn,
                        ElevatedButton(text="Enviar",
                                       color=ft.Colors.WHITE,
                                       on_click=lambda _: salvar_livro(e),
                                       bgcolor=Colors.BLACK,
                                       width=page.window.width)

                    ],
                    bgcolor = "#213D85",
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                )
            )

        if page.route == "/realizar_emprestimo":
            page.views.append(
                View(
                    "/realizar_emprestimo",
                    [
                        AppBar(title=Text("Cadastrar Emprestimo"), bgcolor="#2CC3FF"),
                        input_livro_id,
                        input_usuario_id,
                        input_data_emprestimo,
                        input_devolucao_prevista,
                        ElevatedButton(text="Enviar",
                                       color=ft.Colors.WHITE,
                                       on_click=lambda _: salvar_emprestimo(e),
                                       bgcolor=Colors.BLACK,
                                       width=page.window.width)

                    ],
                    bgcolor = "#213D85",
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                )
            )

        if page.route == "/novo_usuario":
            page.views.append(
                View(
                    "/novo_usuario",
                    [
                        AppBar(title=Text("Cadastrar Usuário"), bgcolor="#6EC2F6"),
                        input_nome,
                        input_cpf,
                        input_endereco,
                        input_papel,
                        ElevatedButton(text="Enviar",
                                       color=ft.Colors.WHITE,
                                       on_click=lambda _: salvar_usuario(e),
                                       bgcolor=Colors.BLACK,
                                       width=page.window.width)

                    ],
                    bgcolor = "#213D85",
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                )
            )

        if page.route == "/listas":
            page.views.append(
                View(
                    "/listas",
                    [
                        AppBar(title=Text("Listas"), bgcolor="#2CC3FF"),
                        ElevatedButton(text="Livro",
                                       color=ft.Colors.WHITE,
                                       on_click=lambda _: page.go("/li"),
                                       bgcolor="#2C30FF",
                                       width=page.window.width),

                        ElevatedButton(text="Usuário",
                                       color=ft.Colors.BLACK,
                                       on_click=lambda _: page.go("/lista_usuario"),
                                       bgcolor="#2CC3FF",
                                       width=page.window.width),

                        ElevatedButton(text="Empréstimo",
                                       color=ft.Colors.WHITE,
                                       on_click=lambda _: page.go("/lista_emprestimo"),
                                       bgcolor="#2C30FF",
                                       width=page.window.width)

                    ],
                    bgcolor="#213D85",
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                )
            )

        if page.route == "/lista_livro":
            livros(e)
            page.views.append(
                View(
                    "/lista_livro",
                    [
                        AppBar(title=Text("Livros"), bgcolor="#2CC3FF"),
                        lv
                    ],
                    bgcolor = "#213D85",
                    horizontal_alignment = CrossAxisAlignment.CENTER,
                )
            )

        if page.route == "/lista_usuario":
            usuarios(e)
            page.views.append(
                View(
                    "/lista_usuario",
                    [
                        AppBar(title=Text("Usuários"), bgcolor="#2CC3FF"),
                        lv
                    ],
                    bgcolor="#213D85",
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                )
            )

        if page.route == "/lista_emprestimo":
            emprestimos(e)
            page.views.append(
                View(
                    "/lista_emprestimo",
                    [
                        AppBar(title=Text("Emprestimos"), bgcolor="#2CC3FF"),
                        lv
                    ],
                    bgcolor="#213D85",
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                )
            )

        if page.route == "/status":
            status(e)
            page.views.append(
                View(
                    "/status",
                    [
                        AppBar(title=Text("Status"), bgcolor="#2CC3FF"),
                        lv
                    ],
                    bgcolor = "#213D85",
                    horizontal_alignment = CrossAxisAlignment.CENTER,
                )
            )

        page.update()

    # Criação de componentes
    input_titulo = ft.TextField(label="Titulo", hint_text="Digite o título do livro")
    input_isbn = ft.TextField(label="ISBN", hint_text="Digite o ISBN")
    input_resumo = ft.TextField(label="Resumo", hint_text="Digite um breve resumo")
    input_autor = ft.TextField(label="Autor", hint_text="Digite o autor")

    input_nome = ft.TextField(label="Nome", hint_text="Digite seu nome")
    input_cpf = ft.TextField(label="CPF", hint_text="Digite o seu CPF")
    input_endereco = ft.TextField(label="Endereço", hint_text="Digite o seu endereço")
    input_papel = ft.TextField(label="Papel", hint_text="Digite o seu papel")
    #
    # input_livro_id = ft.Dropdown(label="Id do livro", width=page.window.width,
    #                      options=[Option(key="id", text="Masculino"),
    #                               Option(key="fem", text="Feminino")], fill_color=Colors.WHITE, filled=True)

    input_livro_id = ft.TextField(label="ID do Livro", hint_text="Digite o ID do livro")
    input_usuario_id = ft.TextField(label="ID do Usuário", hint_text="Digite o ID do usuário")
    input_devolucao_prevista = ft.TextField(label="Data prevista para devolução", hint_text="Digite a data prevista de devolução")
    input_data_emprestimo = ft.TextField(label="Data do empréstimo", hint_text="Digite a data do empréstimo")

    lv = ft.ListView(
        height=500
    )

    msg_sucesso = ft.SnackBar(
        bgcolor=Colors.GREEN,
        content=ft.Text("Informações salvas com sucesso")
    )

    msg_error = ft.SnackBar(
        bgcolor=Colors.RED,
        content=ft.Text("Dados não inseridos não podem ser salvos")
    )

    txt_titulo = ft.Text()
    txt_isbn = ft.Text()
    txt_autor = ft.Text()
    txt_resumo = ft.Text()

    txt_nome = ft.Text()
    txt_cpf = ft.Text()
    txt_endereco = ft.Text()
    txt_papel = ft.Text()


    txt_livroID = ft.Text()
    txt_usuarioID = ft.Text()
    txt_previsao_devolucao = ft.Text()
    txt_data_emprestimo = ft.Text()

    page.on_route_change = gerenciar_rotas
    page.go(page.route)

#popular os inputs
#encaminhar do botão editar para a página cadastrar

ft.app(main)