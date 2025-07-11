# plataforma_roleta/wsgi.py

# --- INÍCIO DO CÓDIGO DE TESTE TEMPORÁRIO ---

def application(environ, start_response):
    """Uma aplicação WSGI mínima para teste."""
    status = '200 OK'
    headers = [('Content-type', 'text/plain; charset=utf-8')]
    start_response(status, headers)
    # Retorna uma mensagem de texto simples
    return [b"O servidor WSGI esta respondendo corretamente!"]

# --- FIM DO CÓDIGO DE TESTE ---


# --- CÓDIGO ORIGINAL DO DJANGO (COMENTADO) ---
# import os
#
# from django.core.wsgi import get_wsgi_application
#
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'plataforma_roleta.settings')
#
# application = get_wsgi_application()
