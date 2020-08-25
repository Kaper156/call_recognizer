def read_client_credentials(filepath='../credentials.ini'):
    # TODO rewrite using ConfigParser
    with open(filepath, 'rt', encoding='utf-8') as file_handler:
        return file_handler.read().split('\n')


def remove_file(filepath):
    print(f"Removing: {filepath}")
