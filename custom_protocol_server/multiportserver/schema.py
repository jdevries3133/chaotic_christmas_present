SCHEMA = {
    'hello world / please kill me now': {
        'host': '127.0.0.1',
        'port': 1050,
        'message': (
            'Dear god please help me world! These assholes have me replying to '
            'every request by hand. This is insanity. No person should have to '
            'suffer such a fate!!!'
        ),
    },
}

fibbonaci_ports = [
    1597,
    2584,
    4181,
    6765,
    10946,
    17711,
    28657,
    46368,
]
fibbonaci_message = 'GOTOJAIL'

assert len(fibbonaci_ports) == len(fibbonaci_message)

for port, message in zip(fibbonaci_ports, fibbonaci_message):
    SCHEMA[f'Fibbonaci, port {port}'] = {
        'port': port,
        'host': '127.0.0.1',
        'message': message,
    }

SCHEMA['JAIL'] = {
    'port': 5245,  # JAIL on a number pad
    'host': '127.0.0.1',
    'message': (
        'Nice job buddy ol boy. Go to this link: https://thomasdevri.es'
        '/staff/docs/you.might/'
    ),
}
