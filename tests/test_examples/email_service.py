"""Example classes for testing ObjectFactory functionality."""

from typing import List, Optional
from specrec.interfaces import ConstructorParameterInfo, IConstructorCalledWith, IObjectWithId


class IEmailService:
    """Interface for email services (Python Protocol would be more idiomatic, but this works)."""

    def send(self, to: str, subject: str, body: str = "") -> bool:
        """Send an email."""
        raise NotImplementedError


class EmailService(IEmailService):
    """Real email service implementation."""

    def __init__(self, smtp_server: str, port: int = 587, username: Optional[str] = None):
        self.smtp_server = smtp_server
        self.port = port
        self.username = username
        self.sent_emails: List[dict] = []

    def send(self, to: str, subject: str, body: str = "") -> bool:
        """Send an email (fake implementation for testing)."""
        email = {
            "to": to,
            "subject": subject,
            "body": body,
            "server": self.smtp_server,
            "port": self.port
        }
        self.sent_emails.append(email)
        return True


class SqlRepository:
    """Example repository class requiring connection string."""

    def __init__(self, connection_string: str, timeout: int = 30):
        self.connection_string = connection_string
        self.timeout = timeout
        self.queries_executed: List[str] = []

    def execute(self, query: str) -> List[dict]:
        """Execute a SQL query (fake implementation)."""
        self.queries_executed.append(query)
        return [{"id": 1, "name": "test"}]


class ServiceWithTracking(IConstructorCalledWith):
    """Service that tracks its constructor parameters."""

    def __init__(self, name: str, port: int, enabled: bool = True):
        self.name = name
        self.port = port
        self.enabled = enabled
        self.constructor_params: List[ConstructorParameterInfo] = []

    def constructor_called_with(self, params: List[ConstructorParameterInfo]) -> None:
        """Track constructor parameters."""
        self.constructor_params = params


class ServiceWithId(IObjectWithId):
    """Service that has an ID for logging/tracking."""

    def __init__(self, service_name: str):
        self.service_name = service_name
        self._object_id: str = ""

    @property
    def object_id(self) -> str:
        """Get the object ID."""
        return self._object_id


class MultiConstructorService:
    """Service with multiple constructor patterns."""

    def __init__(self, *args, **kwargs):
        if len(args) == 1 and isinstance(args[0], str):
            # Single string constructor
            self.mode = "name_only"
            self.name = args[0]
            self.port = 80
        elif len(args) == 2 and isinstance(args[0], str) and isinstance(args[1], int):
            # Name and port constructor
            self.mode = "name_and_port"
            self.name = args[0]
            self.port = args[1]
        elif "config" in kwargs:
            # Config-based constructor
            self.mode = "config"
            self.name = kwargs.get("name", "default")
            self.port = kwargs["config"].get("port", 80)
        else:
            # Default constructor
            self.mode = "default"
            self.name = "default"
            self.port = 80


class NoArgsService:
    """Simple service with no constructor arguments."""

    def __init__(self):
        self.created = True
        self.calls: List[str] = []

    def do_something(self) -> str:
        """Do something and track the call."""
        self.calls.append("do_something")
        return "done"