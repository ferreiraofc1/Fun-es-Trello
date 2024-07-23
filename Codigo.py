import requests
import json
import random
import os

def limpar_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def obter_input(prompt):
    return input(prompt)

def obter_autenticacao_trello():
    key = obter_input("Digite sua API Key do Trello: ")
    token = obter_input("Digite seu Token do Trello: ")
    return key, token

def verificar_autenticacao_trello(key, token):
    url = "https://api.trello.com/1/members/me/boards"
    query = {'key': key, 'token': token}
    response = requests.request("GET", url, params=query)
    return response.status_code == 200

def listar_quadros(key, token):
    url = "https://api.trello.com/1/members/me/boards"
    query = {'key': key, 'token': token}
    response = requests.request("GET", url, params=query)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Erro ao obter quadros: {response.status_code}")
        print(response.text)
        return []

def remover_colaboradores_do_quadro(key, token, board_id):
    url = f"https://api.trello.com/1/boards/{board_id}/members"
    query = {'key': key, 'token': token}
    response = requests.request("GET", url, params=query)
    if response.status_code == 200:
        members = response.json()
        for member in members:
            member_id = member['id']
            delete_url = f"https://api.trello.com/1/boards/{board_id}/members/{member_id}"
            delete_response = requests.request("DELETE", delete_url, params=query)
            if delete_response.status_code == 200:
                print(f"Colaborador {member['fullName']} removido com sucesso.")
            else:
                print(f"Erro ao remover colaborador {member['fullName']}: {delete_response.status_code}")
                print(delete_response.text)
    else:
        print(f"Erro ao obter colaboradores do quadro: {response.status_code}")
        print(response.text)

def deletar_quadro(key, token, board_id):
    url = f"https://api.trello.com/1/boards/{board_id}"
    query = {'key': key, 'token': token}
    response = requests.request("DELETE", url, params=query)
    if response.status_code == 200:
        print("Quadro deletado com sucesso.")
    else:
        print(f"Erro ao deletar quadro: {response.status_code}")
        print(response.text)

def deletar_todas_listas_e_cartoes(key, token, board_id):
    url = f"https://api.trello.com/1/boards/{board_id}/lists"
    query = {'key': key, 'token': token}
    response = requests.request("GET", url, params=query)
    if response.status_code == 200:
        lists = response.json()
        for lista in lists:
            lista_id = lista['id']
            # Arquivar todos os cartões
            archive_url = f"https://api.trello.com/1/lists/{lista_id}/archiveAllCards"
            archive_response = requests.request("POST", archive_url, params=query)
            if archive_response.status_code == 200:
                print(f"Todos os cartões da lista {lista['name']} arquivados com sucesso.")
            else:
                print(f"Erro ao arquivar cartões da lista {lista['name']}: {archive_response.status_code}")
                print(archive_response.text)
            # Deletar a lista
            delete_url = f"https://api.trello.com/1/lists/{lista_id}/closed"
            delete_response = requests.request("PUT", delete_url, params={**query, 'value': 'true'})
            if delete_response.status_code == 200:
                print(f"Lista {lista['name']} deletada com sucesso.")
            else:
                print(f"Erro ao deletar lista {lista['name']}: {delete_response.status_code}")
                print(delete_response.text)
    else:
        print(f"Erro ao obter listas do quadro: {response.status_code}")
        print(response.text)

def criar_listas_aleatorias(key, token, board_id):
    for _ in range(50):
        lista_nome = f"Lista {random.randint(1000, 9999)}"
        url = f"https://api.trello.com/1/lists"
        query = {'key': key, 'token': token, 'name': lista_nome, 'idBoard': board_id}
        response = requests.request("POST", url, params=query)
        if response.status_code == 200:
            print(f"Lista {lista_nome} criada com sucesso.")
        else:
            print(f"Erro ao criar lista {lista_nome}: {response.status_code}")
            print(response.text)

def adicionar_colaborador(key, token, board_id, email):
    url = f"https://api.trello.com/1/boards/{board_id}/members"
    query = {'key': key, 'token': token, 'email': email, 'type': 'normal'}
    response = requests.request("PUT", url, params=query)
    if response.status_code == 200:
        print(f"Colaborador {email} adicionado com sucesso.")
    else:
        print(f"Erro ao adicionar colaborador {email}: {response.status_code}")
        print(response.text)

def ver_informacoes(key, token):
    print("\nInformações da conta Trello:")
    print(f"API Key: {key}")
    print(f"Token: {token}")

    boards = listar_quadros(key, token)
    if boards:
        for board in boards:
            print(f"\nNome do Quadro: {board['name']}")
            print(f"ID do Quadro: {board['id']}")
            url = f"https://api.trello.com/1/boards/{board['id']}/lists"
            query = {'key': key, 'token': token}
            response = requests.request("GET", url, params=query)
            if response.status_code == 200:
                lists = response.json()
                for lista in lists:
                    print(f"  Nome da Lista: {lista['name']}")
                    print(f"  ID da Lista: {lista['id']}")
                    card_url = f"https://api.trello.com/1/lists/{lista['id']}/cards"
                    card_response = requests.request("GET", card_url, params=query)
                    if card_response.status_code == 200:
                        cards = card_response.json()
                        for card in cards:
                            print(f"    Nome do Cartão: {card['name']}")
                            print(f"    ID do Cartão: {card['id']}")
                    else:
                        print(f"    Erro ao obter cartões: {card_response.status_code}")
                        print(card_response.text)
            else:
                print(f"Erro ao obter listas: {response.status_code}")
                print(response.text)

def menu():
    key, token = obter_autenticacao_trello()
    if not verificar_autenticacao_trello(key, token):
        print("Autenticação falhou. Verifique sua API Key e Token.")
        return

    while True:
        limpar_terminal()
        print("\nEscolha uma opção:")
        print("1. Remover todos os colaboradores de um quadro")
        print("2. Deletar um quadro")
        print("3. Deletar todas as listas e cartões de um quadro")
        print("4. Criar listas aleatórias em um quadro")
        print("5. Adicionar colaborador a um quadro")
        print("6. Ver informações detalhadas")
        print("7. Sair")
        opcao = obter_input("Digite o número da opção desejada: ")

        if opcao == '1':
            boards = listar_quadros(key, token)
            for board in boards:
                print(f"Nome do Quadro: {board['name']}, ID do Quadro: {board['id']}")
            board_id = obter_input("Digite o ID do quadro: ")
            remover_colaboradores_do_quadro(key, token, board_id)
        elif opcao == '2':
            boards = listar_quadros(key, token)
            for board in boards:
                print(f"Nome do Quadro: {board['name']}, ID do Quadro: {board['id']}")
            board_id = obter_input("Digite o ID do quadro: ")
            deletar_quadro(key, token, board_id)
        elif opcao == '3':
            boards = listar_quadros(key, token)
            for board in boards:
                print(f"Nome do Quadro: {board['name']}, ID do Quadro: {board['id']}")
            board_id = obter_input("Digite o ID do quadro: ")
            deletar_todas_listas_e_cartoes(key, token, board_id)
        elif opcao == '4':
            boards = listar_quadros(key, token)
            for board in boards:
                print(f"Nome do Quadro: {board['name']}, ID do Quadro: {board['id']}")
            board_id = obter_input("Digite o ID do quadro: ")
            criar_listas_aleatorias(key, token, board_id)
        elif opcao == '5':
            boards = listar_quadros(key, token)
            for board in boards:
                print(f"Nome do Quadro: {board['name']}, ID do Quadro: {board['id']}")
            board_id = obter_input("Digite o ID do quadro: ")
            email = obter_input("Digite o email do colaborador: ")
            adicionar_colaborador(key, token, board_id, email)
        elif opcao == '6':
            ver_informacoes(key, token)
            input("\nPressione Enter para voltar ao menu...")
        elif opcao == '7':
            print("Saindo...")
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    menu()
