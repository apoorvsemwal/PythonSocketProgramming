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
        print('$ERROR$: Issues connecting to server...')


def get_valid_customer_name_input(prompt_msg):
    cust_name = input(prompt_msg)
    if not cust_name.strip():
        print('$ERROR$: Customer name cannot be empty. Please try again.')
        return
    return cust_name.strip().upper()


def display_results(res, action, cust_name):
    msg = ""
    if isinstance(res[0], str) and res[0][0:7] == '$ERROR$':
        print(res[0])
    elif action == 'Find':
        msg = 'Customer record for: ' + cust_name + '\n'
        for idx, val in enumerate(res):
            if idx == 0:
                msg = msg + 'Age - ' + val + '\n'
            elif idx == 1:
                msg = msg + 'Address - ' + val + '\n'
            elif idx == 2:
                msg = msg + 'Phone - ' + val + '\n'
    elif action == 'Add':
        msg = 'New customer ' + cust_name + ' successfully added to DB.'
    elif action == 'Del':
        msg = 'Customer ' + cust_name + ' successfully deleted from DB.'
    elif action == 'Upd_Age':
        msg = 'Age updated successfully for Customer ' + cust_name
    elif action == 'Upd_Address':
        msg = 'Address updated successfully for Customer ' + cust_name
    elif action == 'Upd_Phone':
        msg = 'Phone number updated successfully for Customer ' + cust_name
    print(msg)
    print("\n")


def find_customer(sock, data):
    return do_client_send_receive(sock, data)


def find_customer_display_record(sock):
    cust_name = get_valid_customer_name_input("Enter the customer's name whose record to find: ")
    if not cust_name:
        return
    data = [1, cust_name]
    res = find_customer(sock, data)
    display_results(res, 'Find', cust_name)


def add_customer(sock):
    cust_name = get_valid_customer_name_input("Enter the customer's name whose record to add: ")
    if not cust_name:
        return
    data = [1, cust_name]
    res = find_customer(sock, data)
    if isinstance(res[0], str) and res[0][0:7] != '$ERROR$':
        print('$ERROR$: Customer already exists.')
        return
    cust_age = input("Enter customer's age: ")
    valid_age = get_valid_age(cust_age)
    if valid_age is None:
        print('$ERROR$: Age has to be numeric and greater than 0.')
        return
    cust_address = input("Enter customer's address: ")
    cust_phone = input("Enter customer's phone number: ")
    cust_data = [2, [cust_name, valid_age, cust_address.strip(), cust_phone.strip()]]
    res = do_client_send_receive(sock, cust_data)
    display_results(res, 'Add', cust_name)


def get_valid_age(cust_age):
    if len(cust_age) > 0 and (not cust_age.strip().isnumeric() or int(cust_age.strip()) <= 0):
        return None
    return cust_age.strip()


def delete_customer(sock):
    cust_name = get_valid_customer_name_input("Enter the customer's name whose record to delete: ")
    if not cust_name:
        return
    cust_data = [3, cust_name]
    res = do_client_send_receive(sock, cust_data)
    display_results(res, 'Del', cust_name)


def update_customer_age(sock):
    prompt_name = "Enter the customer's name whose age to update: "
    prompt_field = "Enter customer's new age: "
    opr_idx = 4
    opr_cd = 'Upd_Age'
    update_customer_data(sock, prompt_name, prompt_field, opr_idx, opr_cd)


def update_customer_address(sock):
    prompt_name = "Enter the customer's name whose address to update: "
    prompt_field = "Enter customer's new address: "
    opr_idx = 5
    opr_cd = 'Upd_Address'
    update_customer_data(sock, prompt_name, prompt_field, opr_idx, opr_cd)


def update_customer_phone(sock):
    prompt_name = "Enter the customer's name whose phone number to update: "
    prompt_field = "Enter customer's new phone number: "
    opr_idx = 6
    opr_cd = 'Upd_Phone'
    update_customer_data(sock, prompt_name, prompt_field, opr_idx, opr_cd)


def update_customer_data(sock, prompt_name, prompt_field, operation_idx, operation_cd):
    cust_name = get_valid_customer_name_input(prompt_name)
    if not cust_name:
        return
    data = [1, cust_name]
    res = find_customer(sock, data)
    if isinstance(res[0], str) and res[0][0:7] == '$ERROR$':
        print(res[0])
        return
    cust_field = input(prompt_field)
    cust_field = cust_field.strip()
    if operation_idx == 4:
        valid_age = get_valid_age(cust_field)
        if valid_age is None:
            print('$ERROR$: Age has to be numeric and greater than 0.')
            return
        cust_data = [operation_idx, [cust_name, valid_age]]
    else:
        cust_data = [operation_idx, [cust_name, cust_field]]
    res = do_client_send_receive(sock, cust_data)
    display_results(res, operation_cd, cust_name)


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
        print('$ERROR$: No records in DB to show.')
    print("\n")


def exit_code(sock):
    print("Good bye!!!!")
    data = [8, 'Client said Good bye!!!!']
    sock.sendall(str(data).encode())
    eval(sock.recv(4096).decode('utf-8'))
    return 'Exit'


def invalid_choice(sock):
    print('$ERROR$: Invalid Choice number. Please try again.')


def process_user_input(inp, sock):
    user_input = {'1': find_customer_display_record,
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
        if res == 'Exit':
            sock.close()
            break


if __name__ == "__main__":
    start_client()
