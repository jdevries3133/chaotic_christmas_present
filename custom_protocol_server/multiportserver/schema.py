from random import randint

SCHEMA = {
    'hello world / please kill me now': {
        'host': '0.0.0.0',
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
        'host': '0.0.0.0',
        'message': message,
    }

SCHEMA['JAIL'] = {
    'port': 5245,  # JAIL on a number pad
    'host': '0.0.0.0',
    'message': (
        'Nice job buddy ol boy. Go to this link: https://thomasdevri.es'
        '/staff/docs/you.might/'
    ),
}

class GenSchema:
    """
    Generate part of schema for round 1 challenge.
    """

    def __init__(self,secret, root_node_port, ports_used):
        self.secret = secret
        self.root_node = root_node_port
        self.ports_used = ports_used
        self.last_port = None
        self.schema = {}

    def gen_schema(self):
        """
        Distribute a self.secret amongst a linked list of tcp ports. Output data
        in a schema which can be used to spin up actual servers.
        """
        if self.schema:
            return self.schema
        port = None
        for letter in self.secret[:0:-1]:
            port = None
            while not port:
                tmp_port = randint(1025, 65534)
                if tmp_port in self.ports_used:
                    continue
                port = tmp_port
            if not self.last_port:
                message = f'CHAR: {letter}; GOTO: NULL'
            else:
                message = f'CHAR: {letter}; GOTO: {self.last_port}'
            self.schema[f'__round_1_letter_{letter}_on_port{port}'] = {
                'host': '0.0.0.0',
                'port': port,
                'message': message,
            }
            self.last_port = port
            self.ports_used.add(port)

        self.schema['__round_1_root_node'] = {
            'host': '0.0.0.0',
            'port': self.root_node,
            'message': f'CHAR: self.secret[0]; GOTO: {port}'
        }
        return self.schema

secret = (
    'dkBiqWBYnpLwYtcRalgjAEQTtPrcCkobBzZDAcuJOPMRDIzIlcQdigzWRnNbdrWLNLxfpwSjOw'
    'RWQcKIcBPyHenwrVXaInIUgCwfaLoAZwCoNpODeHDwmKrUIiPMFPpxBXGOxkEhRppFOwOUjWgf'
    'SnwlFdQQQarKzicxtTWIXrqurdOQUVGDPlDLEfxBcYFRcOlqzuhNfvYFERVuRgkxGXHWYnhzOH'
    'JJAKDtzhPiiFYcLJAtgsmPsXDlfgfyFhiKoBfSotnNPmdqLRYYurOEWpZoprSWXnHpKwtWzYbk'
    'gnBr'
)
root_node_port = 45320
ports_used = {i['port'] for i in SCHEMA.values()}

SCHEMA = {
    **GenSchema(secret, root_node_port, ports_used).gen_schema(),
    **SCHEMA,
}
