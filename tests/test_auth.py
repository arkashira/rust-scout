from auth import AuthManager, User

def test_create_account():
    auth = AuthManager()
    assert auth.create_account("test@example.com", "password123")
    assert not auth.create_account("test@example.com", "password123")

def test_log_in():
    auth = AuthManager()
    auth.create_account("test@example.com", "password123")
    assert auth.log_in("test@example.com", "password123")
    assert not auth.log_in("test@example.com", "wrongpassword")

def test_get_premium_features():
    auth = AuthManager()
    auth.create_account("test@example.com", "password123")
    assert auth.get_premium_features("test@example.com") == "Premium features"
    assert auth.get_premium_features("nonexistent@example.com") == "Access denied"

def test_save_and_load():
    auth = AuthManager()
    auth.create_account("test@example.com", "password123")
    auth.save_to_file("users.json")
    new_auth = AuthManager()
    new_auth.load_from_file("users.json")
    assert new_auth.log_in("test@example.com", "password123")
