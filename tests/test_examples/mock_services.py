"""Mock services for testing test double injection."""

from typing import List
from specrec.interfaces import ConstructorParameterInfo, IConstructorCalledWith


class MockEmailService:
    """Mock email service that records calls (demonstrates duck typing)."""

    def __init__(self):
        self.sent_emails: List[dict] = []
        self.calls: List[str] = []

    def send(self, to: str, subject: str, body: str = "") -> bool:
        """Mock send method that records the call."""
        self.calls.append("send")
        email = {
            "to": to,
            "subject": subject,
            "body": body
        }
        self.sent_emails.append(email)
        return True


class StubRepository:
    """Stub repository that returns predefined data."""

    def __init__(self):
        self.queries_executed: List[str] = []
        self.predefined_results = [{"id": 42, "name": "stub_result"}]

    def execute(self, query: str) -> List[dict]:
        """Stub execute method."""
        self.queries_executed.append(query)
        return self.predefined_results


class FakeServiceWithTracking(IConstructorCalledWith):
    """Fake service that also tracks constructor calls."""

    def __init__(self):
        self.constructor_params: List[ConstructorParameterInfo] = []
        self.operations: List[str] = []

    def constructor_called_with(self, params: List[ConstructorParameterInfo]) -> None:
        """Track constructor parameters."""
        self.constructor_params = params

    def do_operation(self, operation: str) -> None:
        """Record an operation."""
        self.operations.append(operation)


class SpyService:
    """Spy service that records all method calls."""

    def __init__(self, target_name: str = "spy"):
        self.target_name = target_name
        self.method_calls: List[dict] = []

    def __getattr__(self, name: str):
        """Intercept all method calls."""
        def spy_method(*args, **kwargs):
            call_info = {
                "method": name,
                "args": args,
                "kwargs": kwargs
            }
            self.method_calls.append(call_info)
            return f"spy_{name}_result"

        return spy_method