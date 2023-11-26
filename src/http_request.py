import json
from http import HTTPStatus
from urllib.parse import parse_qs

status_codes = {s.value: s.phrase for s in HTTPStatus}


def parse_http_request(data_binary: bytes) -> dict:
    # TODO: do it
    """Парсинг бинарного HTTP запроса."""
    print(f"{data_binary=}")
    print(f"{repr(data_binary)}")
    # Разделяем заголовок и тело запроса
    headers, body = data_binary.split('\r\n\r\n', 1)

    # Разбираем заголовки
    header_lines = headers.split('\r\n')
    first_line = header_lines[0].split()
    method = first_line[0]
    path = first_line[1]

    # Разбираем тело запроса
    if method == 'GET':
        # Если это GET-запрос, параметры передаются в URL
        if '?' in path:
            path, query_string = path.split('?', 1)
            parameters = parse_qs(query_string)
        else:
            parameters = {}
    elif method == 'POST':
        # Если это POST-запрос, параметры могут быть в различных форматах
        content_type = None
        for header_line in header_lines[1:]:
            if header_line.startswith('Content-Type:'):
                content_type = header_line.split(': ')[1]
                break

        if content_type == 'application/json':
            # Если Content-Type указывает на JSON, парсим JSON данные
            parameters = json.loads(body)
        else:
            # В противном случае, парсим параметры как строки запроса
            parameters = parse_qs(body)
    else:
        raise NotImplementedError()

    return {
        'method': method,
        'path': path,
        'data': parameters,
    }


def create_http_response(data_json: dict, status_code: int) -> bytes:
    response_json = json.dumps(data_json)
    response = f"HTTP/1.1 {status_code} {status_codes[status_code]}\r\n"
    response += "Content-Type: application/json\r\n"
    response += f"Content-Length: {len(response_json)}\r\n"
    response += "\r\n"
    response += response_json + "\r\n\r\n"
    return response.encode('utf-8')
