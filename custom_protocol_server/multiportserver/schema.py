



SCHEMA = {
    'test_server_1': {
        'host': '127.0.0.1',
        'port': 3000,
        'message': 'Merry Christmas. Welcome to hell :)'
    },
    'test_server_2': {
        'host': '127.0.0.1',
        'port': 6002,
        'message': 'test server 2 message'
    }
}


link = 'https://thomas-christmas.s3.us-east-2.amazonaws.com/DCmsyDq.jpg'

index = 4001

for index, letter in enumerate(link):
    SCHEMA[f'congration{index}'] = {
        'host': '127.0.0.1',
        'port': 4000 + index,
        'message': letter,
    }

SCHEMA['congration_termination'] = {
    'host': '127.0.0.1',
    'port': index,
    'message': 'you got it, stop iterating pls',
}

