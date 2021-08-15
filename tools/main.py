
from examples import custom_style_2
from PyInquirer import prompt
import socket
import os
import sys
from collection.db import Server
from collection.producer import (
    Producer
)


choice = {
    'Yes': True,
    'No': False
}


def get_ip_machine():
    """
    This function to get local ip for current machine
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP


hostname = socket.gethostname()
ip = get_ip_machine()


questions = [
    {
        'type': 'list',
        'name': 'choice',
        'message': 'What do you want connect to Hook Processing server ?',
        'choices': [
            'Yes',
            'No',
        ]
    },
]


def save_db():
    try:
        Server().save(hostname=hostname, ip_address=ip)
        return True
    except Exception as ex:
        pass


if __name__ == '__main__':
    try:
        answers = prompt(questions, style=custom_style_2)
        value = choice.get(answers['choice'])
        if value:
            is_save_ok = save_db()
            if is_save_ok:
                Producer(server_info={
                    'hostname': hostname,
                    'ip': ip
                }).produce()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
