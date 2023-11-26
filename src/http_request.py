def parse_http_request(data_binary: bytes) -> dict:
    # TODO: do it
    """Парсинг бинарного HTTP запроса."""
    return {
        'method': method,
        'path': path,
        # 'parameters': parameters
        'query_parameters': query_parameters,
        'json_data': json_data,
    }


def create_http_response(data_json: dict, status_code: int) -> bytes:
    # TODO: do it
    """Сериализация HTTP запроса в бинарные данные."""
    return b"..."
