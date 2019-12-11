clients = 'pablo,ricardo,'



def create_client(client_name):
    global clients

    if client_name not in clients:
        clients += client_name
        add_comma()
    else:
        print('The client {} is alredy in the list:'.format(client_name))
    list_clients()

def get_name ():
    client_name = None
    while client_name:
        client_name = input('What is the client name? \n')
    
    return client_name
    


def add_comma():
    global clients

    clients += ','

def update_client(client_name, update_client_name):
    global clients
    if client_name in clients:
        clients = clients.replace(client_name + ',', update_client_name)
    else:
        print('client not found')
    list_clients()

def delete_client(client_name):
    global clients
    if client_name in clients:
        clients = clients.replace(client_name + ',', '')
    else:
        print('client not found')
    list_clients()
def  search_client(client_name):
    global clients
    if client_name in clients:
        return True
    else:
        return False

def list_clients():
    global clients
    print(clients)


def print_welcome():

    print('WELCOME TO PLATZI VENTAS')
    print('*'*50)
    print('what do you like to do today?')
    print('[C]reate client')
    print('[D]elete client')
    print('[U]pdate client')
    print('[S]earch client')


if __name__ == "__main__":

    print_welcome()
    command = input().upper()
    if command == 'C':
        client_name = get_name()
        create_client(client_name)
    elif command == 'D':
        client_name = get_name()
        delete_client(client_name)
    elif command == 'U':
        client_name = get_name()
        update_client_name = input('What is the new clien name\n')
        update_client(client_name, update_client_name)
    elif command == 'S':
        client_name = get_name()
        found = search_client(client_name)

        if found:
            print('The client is in the client\'s list')
        else: 
            print('Client {} not found in the list'.format(client_name))

    else:
        print('Invalid command¡')
