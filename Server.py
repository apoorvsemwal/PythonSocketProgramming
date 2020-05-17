# Basic starter code taken from: https://docs.python.org/3/library/socketserver.html
import socketserver

PYTHON_DB = dict()


class MyTCPHandler(socketserver.BaseRequestHandler):
    """
    The RequestHandler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def handle(self):
        # self.request is the TCP socket connected to the client
        print('New client communication started....')
        while True:
            data = eval(self.request.recv(4096).decode('utf-8'))
            if data[0] == '1':
                res = find_customer(data[1])
            if data[0] == '2':
                res = add_customer(data[1])
            if data[0] == '3':
                res = delete_customer(data[1])
            if data[0] == '7':
                res = get_data_for_print_report()
            if data[0] == '8':
                print(data[1])
                self.request.sendall(str(data).encode())
                break;
            if isinstance(res, list):
                self.request.sendall(str(res).encode())
            else:
                self.request.sendall(res.encode())


    # def update_customer_age():
    #     pass
    #
    #
    # def update_customer_address():
    #     pass
    #
    #
    # def update_customer_phone():
    #     pass
    #
    #


def find_customer(cust_name):
    if cust_name in PYTHON_DB:
        return PYTHON_DB[cust_name]
    else:
        return 'Customer not found...'


def add_customer(cust_data):
    if cust_data[0] in PYTHON_DB:
        return 'Customer already exists...'
    else:
        PYTHON_DB[cust_data[0]] = cust_data[1]
    return cust_data


def delete_customer(cust_name):
    if cust_name in PYTHON_DB:
        del PYTHON_DB[cust_name]
    else:
        return 'Customer does not exist...'
    return [cust_name]


def get_data_for_print_report():
    sorted_data = []
    for customer in sorted(PYTHON_DB.keys()):
        record = [customer]
        record.extend(PYTHON_DB[customer])
        sorted_data.append(record)
    return sorted_data


# def check_age():
#     pass
#
#
# def check_address():
#     pass
#
#
# def check_phone():
#     pass


def is_valid_record(split_record):
    if split_record[0].strip().isnumeric():
        return False
    return True


def add_record_to_db(split_record):
    customer_details = []
    for i in range(1, len(split_record)):
        customer_details.append(split_record[i].strip())
    PYTHON_DB[split_record[0].strip()] = customer_details


def load_data_in_memory():
    data_file = open("data.txt", "r")
    records = data_file.readlines()
    for record in records:
        split_record = record.split("|", 3)
        valid_record = is_valid_record(split_record)
        if valid_record:
            add_record_to_db(split_record)
    return 0


def create_server():
    HOST, PORT = "localhost", 9999
    # Create the server, binding to localhost on port 9999
    with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:
        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        print('Server Started...')
        server.serve_forever()


if __name__ == "__main__":
    load_data_in_memory()
    create_server()
