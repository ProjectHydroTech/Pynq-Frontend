# init.py

from flask import Flask

def create_app():
    app = Flask(__name__)
    
    app.config['SECRET_KEY'] = 'secret-key-goes-here'

    # blueprint for non-auth parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .camera import camerastream as camerastream_blueprint
    app.register_blueprint(camerastream_blueprint)
    
    return app

if __name__ == "__main__":
    app.run()
