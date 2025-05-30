from http.client import responses

import flet as ft
import requests
from flet import AppBar, Text, View, ElevatedButton
from flet.core.colors import Colors
from flet.core.types import CrossAxisAlignment


def main(page: ft.Page):
    # configurar
    page.title = "Biblioteca"
    page.theme_mode = ft.ThemeMode.LIGHT
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
                "resumo": input_resumo.value,
            }

            cadastrar_livro(novo_livro)
            page.update()

    def cadastrar_livro(novo_livro):
        url = 'http://10.135.232.15:5001/novo_livro'

        response = requests.post(url, json=novo_livro)
        print(response)


        if response.status_code == 201:
            dados_livro = response.json()
            txt_titulo.value = dados_livro['titulo']
            txt_autor.value = dados_livro['autor']
            txt_isbn.value = dados_livro['isbn']
            txt_resumo.value = dados_livro['resumo']

            input_titulo.value = ""
            input_autor.value = ""
            input_isbn.value = ""
            input_resumo.value = ""
            page.overlay.append(msg_sucesso)
            msg_sucesso.open = True
            page.update()

        else:
            print(response.status_code)

    def livros(e):
        lv.controls.clear()
        resultado_lista = lista_livros()

        print(f' Livros: {resultado_lista}')
        for livro in resultado_lista:
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


    def salvar_usuario(e):
        if (input_nome.value == "" or input_cpf.value == ""
                or input_endereco == ""):
            page.overlay.append(msg_error)
            msg_error.open = True
            page.update()
        else:
            novo_usuario = {
                "nome": input_nome.value,
                "cpf": input_cpf.value,
                "endereco": input_endereco.value,
            }

            cadastrar_usuario(novo_usuario)
            page.update()

    def status(e):
        lv.controls.clear()
        resultado_status = listar_status()
        print(f' Status: {resultado_status["livros_emprestados"]}')
        for status in resultado_status['livros_emprestados']:
            lv.controls.append(
                ft.ListTile(
                    leading=ft.Icon(ft.Icons.BOOK_OUTLINED),
                    title=ft.Text(f'Título: {status["titulo"]}'),
                    trailing=ft.PopupMenuButton(
                        icon=ft.Icons.MORE_VERT,
                        items=[
                            ft.PopupMenuItem(text="DETALHES", on_click=lambda _, l=status: listar_status()),
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
                            ft.PopupMenuItem(text="DETALHES", on_click=lambda _, l=status: listar_status()),
                        ]
                    )
                )
            )

    def emprestimos(e):
        lv.controls.clear()
        resultado_emprestimo = lista_emprestimos()
        print(f'Empréstimos: {resultado_emprestimo}')
        for emprestimo in resultado_emprestimo:
            lv.controls.append(
                ft.ListTile(
                    leading=ft.Icon(ft.Icons.BOOK),
                    title=ft.Text(f'Empréstimos: {emprestimo}'),
                    trailing=ft.PopupMenuButton(
                        icon=ft.Icons.MORE_VERT,
                        items=[
                            ft.PopupMenuItem(text="DETALHES"),
                            ft.PopupMenuItem(text="EDITAR", on_click=lambda _: atualizar_emprestimo(id)),
                        ]
                    )
                )
            )

    def atualizar_emprestimo(id):
        url = 'http://10.135.232.20:5000/editar_emprestimo/<id>'

        atualizar_emprestimo = {
            'id': id,
            'livro_id': input_id_livro.value,
            'usuario_id': input_id_usuario.value,
            'data_emprestimo': input_data_emprestimo.value,
            'data_devolucao': input_data_devolucao.value
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



    def cadastrar_usuario(novo_usuario):
        url = 'http://10.135.232.15:5001/novo_usuario'
        response = requests.post(url, json=novo_usuario)

        if response.status_code == 201:
            dados_usuario = response.json()
            txt_nome.value = dados_usuario['nome']
            txt_cpf.value = dados_usuario['cpf']
            txt_endereco.value = dados_usuario['endereco']

            input_nome.value = ""
            input_cpf.value = ""
            input_endereco.value = ""
            page.overlay.append(msg_sucesso)
            msg_sucesso.open = True
            page.update()
        else:
            print(response.status_code)

    def usuarios(e):
        lv.controls.clear()
        resultado_usuario = lista_usuarios()
        print(f' Usuarios: {resultado_usuario}')
        for usuario in resultado_usuario:
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


    def atualizar_usuarios(id):
        url = 'http://10.135.232.15:5000/atualizar_usuario/<id>'

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



    def salvar_emprestimo(e):
        if (input_id_livro.value == "" or input_id_usuario == ""
                or input_data_emprestimo.value == "" or input_data_devolucao.value == ""):
            page.overlay.append(msg_error)
            msg_error.open = True
            page.update()
        else:
            novo_emprestimo = {
                "id_livro": input_id_livro.value,
                "id_usuario": input_id_usuario.value,
                "data_emprestimo": input_data_emprestimo.value,
                "data_devolucao": input_data_devolucao.value,
            }
            cadastrar_emprestimo(novo_emprestimo)

    def cadastrar_emprestimo(novo_emprestimo):
        url = 'http://10.135.232.15:5001/realizar_emprestimo'
        response = requests.post(url, json=novo_emprestimo)
        print(response)

        if response.status_code == 201:
            dados_emprestimo = response.json()
            txt_id_livro.value = dados_emprestimo['id_livro']
            txt_id_usuario.value = dados_emprestimo['id_usuario']
            txt_data_emprestimo.value = dados_emprestimo['data_emprestimo']
            txt_data_devolucao.value = dados_emprestimo['data_devolucao']

            input_id_livro.value = ""
            input_id_usuario.value = ""
            input_data_emprestimo.value = ""
            input_data_devolucao.value = ""
            page.overlay.append(msg_sucesso)
            msg_sucesso.open = True
            page.update()
        else:
            print(response)



    def lista_livros():
        url = 'http://10.135.232.15:5001/livros'
        response_livros = requests.get(url)
        if response_livros.status_code == 200:
            dados_livros = response_livros.json()
            print(f"{dados_livros}")
            return dados_livros['livros']
        else:
            msg_error.open = True


    def lista_emprestimos():
        url = 'http://10.135.232.15:5001/emprestimos'
        response_emprestimos = requests.get(url)
        if response_emprestimos.status_code == 200:
            dados_emprestimos = response_emprestimos.json()
            return dados_emprestimos['emprestimos']
        else:
            msg_error.open = True

    def lista_usuarios():
        url = 'http://10.135.232.15:5001/usuarios'
        response_usuarios = requests.get(url)
        if response_usuarios.status_code == 200:
            dados_usuarios = response_usuarios.json()
            print(f"kkkkkkkkk {dados_usuarios}")
            return dados_usuarios["usuarios"]

        else:
            msg_error.open = True


    def listar_status():
        url = 'http://10.135.232.15:5000/livro_status'
        response_status = requests.get(url)
        if response_status.status_code == 200:
            dados_status = response_status.json()
            return dados_status
        else:
            msg_error.open = True
        page.update()

    def gerencia_rota(e):
        page.views.clear()
        page.views.append(
            View(
                "/",
                (
                    ft.Container(
                        ft.Image(src="static/livro.png"),
                        margin=30,
                    ),
                    ElevatedButton(text="Cadastros",
                                   color=ft.Colors.WHITE,
                                   on_click=lambda _: page.go("/cadastros"),
                                   bgcolor=ft.Colors.BLACK),
                    ElevatedButton(text="Listas",
                                   color=ft.Colors.WHITE,
                                   on_click=lambda _: page.go("/listas"),
                                   bgcolor=ft.Colors.BLACK),
                    ElevatedButton(text="Status",
                                   color=ft.Colors.WHITE,
                                   on_click=lambda _: page.go("/status"),
                                   bgcolor=ft.Colors.BLACK),
                    ElevatedButton(text="Atualizações",
                                   color=ft.Colors.WHITE,
                                   on_click=lambda _: page.go("/atualizacao"),
                                   bgcolor=ft.Colors.BLACK
                                   ),
                ),
                bgcolor="",
                horizontal_alignment=CrossAxisAlignment.CENTER,
            )
        )
        if page.route == "/cadastros":
            page.views.append(
                View(
                    "/cadastros",
                    [
                        AppBar(title=Text("Cadastros")),
                        ElevatedButton(text="Cadastrar Livro",
                                       color=ft.Colors.WHITE,
                                       on_click=lambda _: page.go("/novo_livro"),
                                       bgcolor=ft.Colors.BLACK),
                        ElevatedButton(text="Cadastrar Usuário",
                                       color=ft.Colors.WHITE,
                                       on_click=lambda _: page.go("/novo_usuario"),
                                       bgcolor=ft.Colors.BLACK),
                        ElevatedButton(text="Cadastrar Emprestimo",
                                       color=ft.Colors.WHITE,
                                       on_click=lambda _: page.go("/realizar_emprestimo"),
                                       bgcolor=ft.Colors.BLACK),
                    ],
                    bgcolor="",
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                )
            )
        if page.route == "/novo_livro":
            page.views.append(
                View(
                    "/novo_livro",
                    [
                        AppBar(title=Text("Cadastrar Livro")),
                        input_titulo,
                        input_autor,
                        input_isbn,
                        input_resumo,
                        ElevatedButton(text="Enviar",
                                       color=ft.Colors.WHITE,
                                       on_click=lambda _: salvar_livro(e),
                                       bgcolor=ft.Colors.BLACK)
                    ],
                    bgcolor="",
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                )
            )
        if page.route == "/realizar_emprestimo":
            page.views.append(
                View(
                    "/realizar_emprestimo",
                    [
                        AppBar(title=Text("Cadastrar Emprestimo")),
                        input_id_livro,
                        input_id_usuario,
                        input_data_emprestimo,
                        input_data_devolucao,
                        ElevatedButton(text="Enviar",
                                       color=ft.Colors.WHITE,
                                       on_click=lambda _: salvar_emprestimo(e),
                                       bgcolor=ft.Colors.BLACK)
                    ],
                    bgcolor="",
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                )
            )
        if page.route == "/novo_usuario":
            page.views.append(
                View(
                    "/novo_usuario",
                    [
                        AppBar(title=Text("Cadastrar Usuario")),
                        input_nome,
                        input_cpf,
                        input_endereco,
                        ElevatedButton(text="Enviar",
                                       color=ft.Colors.WHITE,
                                       on_click=lambda _: salvar_usuario(e),
                                       bgcolor=ft.Colors.BLACK)
                    ],
                    bgcolor="",
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                )
            )
        if page.route == "/listas":
            page.views.append(
                View(
                    "/listas",
                    [
                        AppBar(title=Text("Listas")),
                        ElevatedButton(text="Lista de Livros",
                                       color=ft.Colors.WHITE,
                                       on_click=lambda _: page.go("/livros")),
                        ElevatedButton(text="Lista de Usuários",
                                       color=ft.Colors.WHITE,
                                       on_click=lambda _: page.go("/usuarios")),
                        ElevatedButton(text="Lista de Emprestimos",
                                       color=ft.Colors.WHITE,
                                       on_click=lambda _: page.go("/emprestimos")),
                    ],
                    bgcolor="",
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                )
            )
        if page.route == "/livros":
            livros(e)
            page.views.append(
                View(
                    "/livros",
                    [
                        AppBar(title=Text("Livros")),
                        lv
                    ],
                    bgcolor="",
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                )
            )
        if page.route == "/usuarios":
            usuarios(e)
            page.views.append(
                View(
                    "/usuarios",
                    [
                        AppBar(title=Text("Usuários")),
                        lv
                    ],
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                )
            )

        if page.route == "/emprestimos":
            emprestimos(e)
            page.views.append(
                View(
                    "/emprestimos",
                    [
                        AppBar(title=Text("Emprestimos"), bgcolor=""),
                        lv
                    ],
                    bgcolor="",
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






    # componente
    # livro inserir
    input_titulo = ft.TextField(label="titulo")
    input_autor = ft.TextField(label="autor")
    input_isbn = ft.TextField(label="isbn")
    input_resumo = ft.TextField(label="resumo")

    # livro mostrar
    txt_titulo = ft.Text()
    txt_autor = ft.Text()
    txt_isbn = ft.Text()
    txt_resumo = ft.Text()

    # usuario inserir
    input_nome = ft.TextField(label="nome")
    input_cpf = ft.TextField(label="cpf")
    input_endereco = ft.TextField(label="endereco")

    # usuario mostrar
    txt_nome = ft.Text()
    txt_cpf = ft.Text()
    txt_endereco = ft.Text()

    # emprestimo inserir
    input_id_usuario = ft.TextField(label="id_usuario")
    input_id_livro = ft.TextField(label="id_livro")
    input_data_emprestimo = ft.TextField(label="data_emprestimo")
    input_data_devolucao = ft.TextField(label="data_devolucao")

    # emprestimo mostrar
    txt_id_usuario = ft.Text()
    txt_id_livro = ft.Text()
    txt_data_emprestimo = ft.Text()
    txt_data_devolucao = ft.Text()

    # mensagens
    msg_sucesso = ft.SnackBar(
        bgcolor=Colors.GREEN,
        content=ft.Text("Informações salvas com sucesso!")
    )
    msg_error = ft.SnackBar(
        bgcolor=Colors.RED,
        content=ft.Text("Informações não correspondentes")
    )

    lv = ft.ListView(
        height=500
    )

    page.on_route_change = gerencia_rota
    page.go(page.route)


ft.app(main)
