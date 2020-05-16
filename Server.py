# Basic starter code taken from: https://docs.python.org/3/library/socketserver.html
import socketserver

PYTHON_DB = dict()


def is_valid_record(split_record):
    if split_record[0].strip().isnumeric():
        return False
    return True
    # if len(split_record) == 2:
    #     check_age()
    # elif len(split_record) == 3:
    #     check_age()
    #     check_address()
    # elif len(split_record) == 4:
    #     check_age()
    #     check_address()
    #     check_phone()


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
        server.serve_forever()


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
    sorted_data = []
    for customer in sorted(PYTHON_DB.keys()):
        record = [customer]
        record.extend(PYTHON_DB[customer])
        sorted_data.append(record)

    dash = '-' * 90
    print(dash)
    print('{:<25s}{:<10s}{:<40s}{:<12s}'.format("Name", "Age", "Street Address", "Phone #"))
    print(dash)
    for i in range(len(sorted_data)):
        print('{:<25s}{:<10s}{:<40s}{:<12s}'.format(sorted_data[i][0], sorted_data[i][1], sorted_data[i][2],
                                                    sorted_data[i][3]))


if __name__ == "__main__":
    load_data_in_memory()
    print_report()
    # create_server()


class MyTCPHandler(socketserver.BaseRequestHandler):
    """
    The RequestHandler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()
        print("{} wrote:".format(self.client_address[0]))
        print(self.data)
        # just send back the same data, but upper-cased
        self.request.sendall(self.data.upper())
