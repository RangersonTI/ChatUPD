import socket
import threading

# Endereço IP e porta para o servidor
host = '192.168.1.104'  # Endereço IP do servidor
porta = 12345  # Porta do servidor

# Lista de amigos
participantes = {
    'Rangerson':'192.168.1.104',
    'PC2-ranger':'192.168.1.106',
    # já que eu fiz o código em casa não pude salvar o contatos de amigos
}

# Cria um objeto socket UDP
socket_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Liga o socket ao endereço e porta especificados
socket_server.bind((host, porta))

print(f"Servidor UDP aguardando mensagens em {host}:{porta}")

# Função para receber mensagens


def receber_mensagens():
    while True:
        try:
            # Recebe os dados e o endereço do remetente
            dados, endereco = socket_server.recvfrom(
                1024)  # Tamanho do buffer é 1024 bytes

            mensagem = dados.decode('utf-8')

            if mensagem == '.contatos':
                # Send a response with the list of friends and their IP addresses to the sender
                sender_ip = endereco[0]
                response = "\n".join(
                    [f"{name},{ip}" for name, ip in participantes.items()])
                socket_server.sendto(response.encode('utf-8'), (sender_ip, porta))
            else:
                # Separar a mensagem em nome e conteúdo
                parts = mensagem.split('_', 1)
                if len(parts) == 2:
                    friend_name, message_content = parts
                    if friend_name in participantes:
                        destino_ip = participantes[friend_name]
                        print(
                            f"Mensagem enviada para ** {friend_name}:{message_content}")
                        cliente_socket = socket.socket(
                            socket.AF_INET, socket.SOCK_DGRAM)
                        cliente_socket.sendto(message_content.encode(
                            'utf-8'), (destino_ip, porta))
                    else:
                        print("Nome de amigo inválido. Tente novamente.")

        except UnicodeDecodeError:
            print(
                f"Recebido de {endereco[0]}:{endereco[1]}: Erro de decodificação (não UTF-8)")


# Inicializa uma thread para receber mensagens
thread_recebimento = threading.Thread(target=receber_mensagens)
thread_recebimento.daemon = True
thread_recebimento.start()

# Função para enviar mensagens


def enviar_mensagens():
    while True:
        mensage = input(
            "Digite o nome seguido da mensagem: Ex.: fulano_mensagem: ")
        if mensage == "/sair":
            print("Encerrando o programa...")
            print("Fechando portas de escuta: ")
            thread_recebimento.join()
            break
        elif '.contatos' in mensage:
            # Send a request to your host to retrieve the list of friends and their IP addresses via UDP
            host_address = host  # Replace with your host's IP address
            host_port = 12345  # Replace with the port your host is listening on
            request = '.contatos'
            socket_server.sendto(request.encode('utf-8'),
                                 (host_address, host_port))
        else:
            # Separar a entrada em nome e conteúdo
            partes = mensage.split('_', 1)
            if len(partes) == 2:
                friend_name, message_content = partes
                if friend_name in participantes:
                    destino_ip = participantes[friend_name]
                    print(
                        f"Enviando mensagem para {friend_name}: {message_content}")
                    cliente_socket = socket.socket(
                        socket.AF_INET, socket.SOCK_DGRAM)
                    cliente_socket.sendto(message_content.encode(
                        'utf-8'), (destino_ip, porta))
                else:
                    print("Nome de amigo inválido. Tente novamente.")


# Inicializa uma thread para enviar mensagens
thread_envio = threading.Thread(target=enviar_mensagens)
thread_envio.start()

# Aguarde as threads finalizarem
thread_envio.join()
print("Threads encerradas.")
# Feche o socket (isso nunca será executado no loop acima)
socket_server.close()
print("Socket encerrado. Bye Bye")