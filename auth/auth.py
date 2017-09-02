import string, random

class Auth:
    @staticmethod
    def ValidateUser(user, request):
        return 'Session-Token' in request.headers and user['session_token'] == request.headers['Session-Token']

    @staticmethod
    def GenerateSessionToken():
        return ''.join(random.choice(string.ascii_lowercase) for _ in range(32))
