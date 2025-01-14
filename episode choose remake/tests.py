import socket

def is_connected():
    try:
        # Попытка подключения к Google (или любому другому серверу)
        socket.create_connection(("www.google.com", 80), timeout=5)
        return True
    except (socket.timeout, socket.gaierror):
        return False

if is_connected():
    # Код, который требует интернет-соединения
    print("Интернет доступен, выполняем код с интернетом.")
else:
    # Код, который выполняется, если интернета нет
    print("Нет интернета, пропускаем код с интернетом.")