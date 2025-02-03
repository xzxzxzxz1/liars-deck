from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

from routes.lobby import lobby_blueprint
from routes.game import game_blueprint

app = Flask(__name__) 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///liarsbar.db'
db  = SQLAlchemy(app)

app.register_blueprint(lobby_blueprint, url_prefix="/api")
app.register_blueprint(game_blueprint, url_prefix="/api")

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
    