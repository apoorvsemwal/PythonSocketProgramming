# Basic starter code taken from: https://docs.python.org/3/library/socketserver.html
import socket
import sys


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


def establish_client_connection_to_server():
    HOST, PORT = "localhost", 9999
    data = " ".join(sys.argv[1:])

    # Create a socket (SOCK_STREAM means a TCP socket)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        # Connect to server and send data
        sock.connect((HOST, PORT))
        sock.sendall(bytes(data + "\n", "utf-8"))

        # Receive data from the server and shut down
        received = str(sock.recv(1024), "utf-8")

    print("Sent:     {}".format(data))
    print("Received: {}".format(received))


def find_customer():
    pass


def add_customer():
    pass


def delete_customer():
    pass


def update_customer_age():
    pass


def update_customer_address():
    pass


def update_customer_phone():
    pass


def print_report():
    pass


def exit_code():
    print("Good bye")
    return 8


def invalid_choice():
    print("Invalid Choice!!!")


def process_user_input(inp):
    user_input = {'1': find_customer,
                  '2': add_customer,
                  '3': delete_customer,
                  '4': update_customer_age,
                  '5': update_customer_address,
                  '6': update_customer_phone,
                  '7': print_report,
                  '8': exit_code
                  }
    return user_input.get(inp, invalid_choice)()


if __name__ == "__main__":
    # establish_client_connection_to_server()
    while True:
        inp = display_menu_and_get_user_input()
        res = process_user_input(inp)
        if res == 8:
            break
