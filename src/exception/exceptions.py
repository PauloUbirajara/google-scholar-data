class DefaultException(Exception):
    """Exceção base para outras customizadas"""
    pass


class InvalidInputException(DefaultException):
    """Exceção para campo inválido"""

    def __init__(self, field_name: str, reason: str):
        message = f'Campo "{field_name}" é inválido - {reason}!'

        super().__init__(message)


class InvalidResearcherURLException(DefaultException):
    """Exceção para uma linha mal formatada"""

    def __init__(self, researcher_name: str):
        message = f'Link do pesquisador "{researcher_name}" é inválido!'

        super().__init__(message)


class FetchException(DefaultException):
    """Exceção gerada ao tentar buscar dados da API"""

    def __init__(self, reason: str):
        message = f'Erro ao buscar link de API - "{reason}"!'

        super().__init__(message)
