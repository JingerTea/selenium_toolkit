def proxy_options(method, host, port, user=None, password=None):
    if user and password:
        authentication = f"{user}:{password}@"
    elif not user and not password:
        authentication = ""
    else:
        raise ValueError("Proxy credentials are missing")

    if method == "http" or method == "https":
        method = ["http", "https"]
    elif method == "socks5":
        method = ["socks5", "socks5"]

    options = {
        "proxy": {
            "http": f"{method[0]}://{authentication}{host}:{port}",
            "https": f"{method[1]}://{authentication}{host}:{port}",
            'no_proxy': 'localhost,127.0.0.1'
        }
    }
    return options
