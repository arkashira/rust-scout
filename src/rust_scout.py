import json
from dataclasses import dataclass
from email.message import EmailMessage
import smtplib
from typing import List

@dataclass
class Library:
    name: str
    version: str
    changelog: str

@dataclass
class User:
    email: str
    rust_toolchain: str

def send_email_notification(library: Library, user: User):
    msg = EmailMessage()
    msg.set_content(f"New version of {library.name} available: {library.version}\nChangelog: {library.changelog}")
    msg['Subject'] = f"New version of {library.name} available"
    msg['From'] = "rust-scout@example.com"
    msg['To'] = user.email
    with smtplib.SMTP_SSL("smtp.example.com", 465) as smtp:
        smtp.login("rust-scout@example.com", "password")
        smtp.send_message(msg)

def check_version_compatibility(library: Library, user: User):
    if library.version != user.rust_toolchain:
        return f"Version {library.version} is not compatible with your current Rust toolchain {user.rust_toolchain}"
    return None

def get_one_click_upgrade_instructions(library: Library):
    return f"Run `cargo update {library.name}` to upgrade to version {library.version}"

def main():
    libraries = [
        Library("library1", "1.2.3", "Fixed bug"),
        Library("library2", "4.5.6", "Added feature")
    ]
    users = [
        User("user1@example.com", "1.2.3"),
        User("user2@example.com", "4.5.6")
    ]
    for library in libraries:
        for user in users:
            send_email_notification(library, user)
            compatibility_warning = check_version_compatibility(library, user)
            if compatibility_warning:
                print(compatibility_warning)
            print(get_one_click_upgrade_instructions(library))

if __name__ == "__main__":
    main()
