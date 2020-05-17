# Basic starter code taken from: https://docs.python.org/3/library/socketserver.html
import socket

HOST, PORT = "localhost", 9999


def display_menu_and_get_user_input():
    print("Python DB Menu \n")
    print("1. Find customer")
    print("2. Add customer")
    print("3. Delete customer")
    print("4. Update customer age")
    print("5. Update customer address")
    print("6. Update customer phone")
    print("7. Print report")
    print("8. Exit \n")
    inp = input("Select: ")
    return inp


def get_socket_to_server():
    # Create a socket (SOCK_STREAM means a TCP socket)
    return socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def do_client_send_receive(sock, data):
    try:
        sock.sendall(str(data).encode())
        res = eval(sock.recv(4096).decode('utf-8'))
        return res
    except:
        print('Issues connecting to server...')


def find_customer(sock):
    cust_name = input("Enter the customer name to find: ")
    data = ['1', cust_name]
    do_client_send_receive(sock, data)
    if isinstance(res, list):
        print('Customer record for: ' + cust_name)
        for idx, val in enumerate(res):
            if idx == 0:
                print('Age - ' + val)
            elif idx == 1:
                print('Address - ' + val)
            elif idx == 2:
                print('Phone - ' + val)
    else:
        print(res)
    print("\n")


def add_customer():
    cust_name = input("Enter the customer name to add: ")
    cust_age = input("Enter customer's age: ")
    cust_address = input("Enter customer's address: ")
    cust_phone = input("Enter customer's phone number: ")
    cust_data = [2, [cust_name, cust_age, cust_address, cust_phone]]
    res = do_client_send_receive(sock, cust_data)
    if isinstance(res, list):
        print('New customer ' + cust_name + ' successfully added to DB.')
    else:
        print(res)
    print("\n")


def delete_customer(sock):
    cust_name = input("Enter the customer name to delete: ")
    cust_data = [3, cust_name]
    res = do_client_send_receive(sock, cust_data)
    if isinstance(res, list):
        print('Customer ' + cust_name + ' successfully deleted from DB.')
    else:
        print(res)
    print("\n")


def update_customer_age():
    return 4


def update_customer_address():
    return 5


def update_customer_phone():
    return 6


def print_report(sock):
    res = do_client_send_receive(sock, [7])
    if isinstance(res, list) and len(res) > 0:
        dash = '-' * 90
        print(dash)
        print('{:<25s}{:<10s}{:<40s}{:<12s}'.format("Name", "Age", "Street Address", "Phone #"))
        print(dash)
        for i in range(len(res)):
            print('{:<25s}{:<10s}{:<40s}{:<12s}'.format(res[i][0], res[i][1], res[i][2],
                                                        res[i][3]))
    else:
        print('No records in DB to show...')
    print("\n")


def exit_code(sock):
    print("Good bye!!!!")
    data = ['8', 'Client said Good bye!!!!']
    sock.sendall(str(data).encode())
    res = eval(sock.recv(4096).decode('utf-8'))
    return res


def invalid_choice():
    print("Invalid Choice!!!")


def process_user_input(inp, sock):
    user_input = {'1': find_customer,
                  '2': add_customer,
                  '3': delete_customer,
                  '4': update_customer_age,
                  '5': update_customer_address,
                  '6': update_customer_phone,
                  '7': print_report,
                  '8': exit_code
                  }
    return user_input.get(inp, invalid_choice)(sock)


def start_client():
    sock = get_socket_to_server()
    sock.connect((HOST, PORT))
    while True:
        inp = display_menu_and_get_user_input()
        res = process_user_input(inp, sock)
        if res and res[0] == '8':
            sock.close()
            break


if __name__ == "__main__":
    start_client()