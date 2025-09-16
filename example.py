#!/usr/bin/env python3
"""
Example demonstrating Python ObjectFactory usage.

This shows how to migrate legacy code to use the ObjectFactory pattern
and how to write testable code with minimal changes.
"""

from specrec import create, set_one, context
from tests.test_examples.email_service import EmailService, SqlRepository
from tests.test_examples.mock_services import MockEmailService, StubRepository


class UserService:
    """Example service using ObjectFactory for dependency injection."""

    def __init__(self, db_connection: str, smtp_server: str):
        # Using factory instead of direct instantiation
        self.db = create(SqlRepository)(db_connection, timeout=30)
        self.email_service = create(EmailService)(smtp_server, 587)

    def create_user(self, email: str, name: str) -> dict:
        """Create a new user and send welcome email."""
        # Save to database
        user = {"email": email, "name": name, "id": 123}
        query = f"INSERT INTO users (email, name) VALUES ('{email}', '{name}')"
        self.db.execute(query)

        # Send welcome email
        subject = f"Welcome {name}!"
        body = f"Welcome to our platform, {name}!"
        self.email_service.send(email, subject, body)

        return user


def demonstrate_legacy_migration():
    """Show how legacy code can be made testable."""
    print("🍀 Python ObjectFactory Demo")
    print("=" * 40)

    # 1. Production usage (no changes to business logic)
    print("\n1. Production Usage:")
    user_service = UserService("server=prod;db=users", "smtp.company.com")
    user = user_service.create_user("john@example.com", "John Doe")
    print(f"   Created user: {user['name']} ({user['email']})")
    print(f"   Database queries: {len(user_service.db.queries_executed)}")
    print(f"   Emails sent: {len(user_service.email_service.sent_emails)}")

    # 2. Testing with mocks (clean isolation)
    print("\n2. Testing with Mocks:")
    mock_email = MockEmailService()
    mock_db = StubRepository()

    with context():
        set_one(EmailService, mock_email)
        set_one(SqlRepository, mock_db)

        test_user_service = UserService("test_connection", "test_smtp")
        test_user = test_user_service.create_user("test@example.com", "Test User")

        print(f"   Test user: {test_user['name']} ({test_user['email']})")
        print(f"   Mock DB queries: {len(mock_db.queries_executed)}")
        print(f"   Mock emails sent: {len(mock_email.sent_emails)}")
        print(f"   Email subject: '{mock_email.sent_emails[0]['subject']}'")

    # 3. Show that context isolation works
    print("\n3. Context Isolation:")
    post_test_service = UserService("post_test_connection", "post_test_smtp")
    post_test_user = post_test_service.create_user("after@example.com", "After Test")

    print(f"   After context - real instances used:")
    print(f"   Database type: {type(post_test_service.db).__name__}")
    print(f"   Email service type: {type(post_test_service.email_service).__name__}")

    # 4. Demonstrate curried syntax benefits
    print("\n4. Curried Syntax Benefits:")
    create_email_service = create(EmailService)

    # Reuse factory function
    gmail_service = create_email_service("smtp.gmail.com", 587)
    outlook_service = create_email_service("smtp.outlook.com", 587)

    print(f"   Gmail service: {gmail_service.smtp_server}:{gmail_service.port}")
    print(f"   Outlook service: {outlook_service.smtp_server}:{outlook_service.port}")

    print("\n🍀 Demo completed successfully!")
    print("\nKey Python advantages:")
    print("• Duck typing eliminates interface mapping complexity")
    print("• Context managers provide elegant test isolation")
    print("• *args, **kwargs handle any constructor signature")
    print("• Type hints provide IDE support without runtime cost")
    print("• Curried syntax enables functional composition patterns")


if __name__ == "__main__":
    demonstrate_legacy_migration()