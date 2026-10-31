from app.users.passwords import hash_password, verify_password



def test_right_password():
    password_hash = hash_password("abc")
    assert verify_password("abc", password_hash) == True


def test_incorrent_password():
    password_hash = hash_password("abc")
    assert verify_password("123", password_hash) == False


def test_strip_password():
    password_hash = hash_password(" abc ")
    assert verify_password(" abc ", password_hash) == True
    assert verify_password("abc", password_hash) == False
