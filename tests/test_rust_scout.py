import pytest
from rust_scout import send_email_notification, check_version_compatibility, get_one_click_upgrade_instructions, main
from unittest.mock import patch, MagicMock
from email.message import EmailMessage

@pytest.fixture
def library():
    return type("Library", (), {"name": "library1", "version": "1.2.3", "changelog": "Fixed bug"})

@pytest.fixture
def user():
    return type("User", (), {"email": "user1@example.com", "rust_toolchain": "1.2.3"})

def test_send_email_notification(library, user):
    with patch("smtplib.SMTP_SSL") as mock_smtp:
        mock_smtp.return_value.__enter__.return_value.login = MagicMock()
        mock_smtp.return_value.__enter__.return_value.send_message = MagicMock()
        send_email_notification(library, user)
        mock_smtp.return_value.__enter__.return_value.send_message.assert_called_once()

def test_check_version_compatibility(library, user):
    assert check_version_compatibility(library, user) is None
    library.version = "4.5.6"
    assert check_version_compatibility(library, user) == "Version 4.5.6 is not compatible with your current Rust toolchain 1.2.3"

def test_get_one_click_upgrade_instructions(library):
    assert get_one_click_upgrade_instructions(library) == "Run `cargo update library1` to upgrade to version 1.2.3"

def test_main():
    with patch("rust_scout.send_email_notification") as mock_send_email_notification:
        with patch("rust_scout.check_version_compatibility") as mock_check_version_compatibility:
            with patch("rust_scout.get_one_click_upgrade_instructions") as mock_get_one_click_upgrade_instructions:
                mock_send_email_notification.return_value = None
                mock_check_version_compatibility.return_value = None
                mock_get_one_click_upgrade_instructions.return_value = "instructions"
                main()
                mock_send_email_notification.assert_called()
                mock_check_version_compatibility.assert_called()
                mock_get_one_click_upgrade_instructions.assert_called()
