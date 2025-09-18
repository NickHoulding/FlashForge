import logging

logger = logging.getLogger(__name__)

class CustomException(Exception):
    def __init__(self, message, status_code) -> None:
        super().__init__(message)
        self.status_code = status_code
        logger.error(f"Exception raised: {self.__class__.__name__}: {message}")

# Custom Exceptions
class AuthenticationException(CustomException):
    """Raised when authentication fails"""
    pass

class UserAlreadyExistsException(CustomException):
    """Raised when attempting to register a new account with an existing user's credentials"""
    pass

class UserNotFoundException(CustomException):
    """Raised when a user's credentials is not found in the database"""
    pass

class InvalidCredentialsException(CustomException):
    """Raised when login credentials are invalid"""
    pass

class TokenException(CustomException):
    """Raise when there are any issues with JWT tokens (invalid, expired, etc.)"""
    pass

class MissingRequiredFieldException(CustomException):
    """Raised when required fields are missing"""
    pass

class InvalidPasswordException(CustomException):
    """Raised when password doesn't meet requirements"""
    pass

class DatabaseConnectionException(CustomException):
    """Raised when database connection fails"""
    pass

class DatabaseTransactionException(CustomException):
    """Raised when a database transaction fails"""
    pass

class ConfigurationException(CustomException):
    """Raised when there are configuration errors"""
    pass

class ServiceUnavailableException(CustomException):
    """Raised when external services are unavailable"""
    pass

#Validation Exceptions
class ValidationException(CustomException):
    """Base class for validation errors"""
    pass

class InvalidUsernameException(ValidationException):
    """raised when username validation fails"""
    pass

class InvalidChatNameException(ValidationException):
    """Raised when chat name validation fails"""
    pass

class InvalidFlashcardException(ValidationException):
    """Raised when flashcard data validation fails"""
    pass

class InvalidContentException(ValidationException):
    """Raised when file validation fails"""
    pass

class InvalidFileException(ValidationException):
    """Raised when file validation fails"""
    pass

def handle_exception(e: Exception):
    """Error hanlder to handle custom exceptions"""

    if isinstance(e, CustomException):
        return {
            "error": str(e)
        }, e.status_code
    elif isinstance(e, ValueError):
        return {
            "error": "Invalid input provided"
        }, 400
    else:
        logger.error(f"Unexpected error: {str(e)}")
        return {
            "error": "An unexpected error occurred"
        }, 500
