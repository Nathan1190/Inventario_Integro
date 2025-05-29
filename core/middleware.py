# core/middleware.py
import threading

_thread_locals = threading.local()

class CurrentUserMiddleware:
    """
    Middleware que guarda request.user en una variable thread-local
    para poder recuperarlo luego desde cualquier parte.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # guarda el user en _thread_locals
        _thread_locals.user = getattr(request, 'user', None)
        return self.get_response(request)

def get_current_user():
    """
    Devuelve el user guardado en thread-local o None si no hay.
    """
    return getattr(_thread_locals, 'user', None)
