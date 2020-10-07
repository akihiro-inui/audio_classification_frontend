import json


def read_json_file(json_file_path: str) -> dict:
    """
    Read json file, return as dictionary
    :param json_file_path: Input json file path
    :return: json object as dictionary
    """
    try:
        with open(json_file_path, 'r') as fh:
            data = fh.read()
        return json.loads(data)
    except ValueError:
        assert 'Invalid json format'
    except FileNotFoundError:
        assert 'Invalid json file path was given'
    except Exception as err:
        assert f'Error while reading json file {err}'
