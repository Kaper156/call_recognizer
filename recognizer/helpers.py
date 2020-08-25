def read_client_credentials(filepath='../configuration.ini'):
    # TODO rewrite using ConfigParser
    with open(filepath, 'rt', encoding='utf-8') as file_handler:
        keys = file_handler.read().split('\n')
        return {'api_key': keys[0], 'secret_key': keys[-1]}


def remove_file(filepath):
    print(f"Removing: {filepath}")
