from gamerverse import create_app
from waitress import serve
app = create_app()

if __name__ == '__main__':
    
    host = '127.0.0.1'
    port = 80

    serve(app, host=host, port=port)
    print(f'App running on: https://{host}:{port}\nPress CTRL + C to quit.')