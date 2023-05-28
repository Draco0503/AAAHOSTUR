from security import security
import jwt

sec = security.Security("secret", "HS256")


def prueba_jwt_firma():
    payload = {
        "user": "fulanito",
        "role": 100
    }

    token = sec.generate_jwt(payload)
    print(token)

    new_payload = sec.decode_jwt(token)
    print(new_payload)
    assert payload == new_payload

    # esto deberia petar si está bien
    test_payload = jwt.decode(token, "newSecret", ["HS256"])
    print(test_payload)
    assert payload == test_payload

    print("FIN DE EJECUCION")


def datos_usuario_prueba():
    pwd = "penelmao123"
    hashed_pwd = "$2b$12$YEmfU4TvAaRNupl8VlFqCurzUx/trQbOJv8nQxRHWvqq2DX2.SiwG"
    assert sec.verify_password(pwd, hashed_pwd)


datos_usuario_prueba()
