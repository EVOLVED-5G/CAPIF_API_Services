def sign_csr_body(username, public_key):
    data = {
        "csr":  public_key.decode("utf-8"),
        "mode":  "client",
        "filename": username
    }
    return data
