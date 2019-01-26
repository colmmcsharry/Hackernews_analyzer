from flask import Flask, jsonify
from flask import render_template
app = Flask(__name__)

@app.route('/')
def mypage():
    return jsonify({})

if __name__ == '__main__':
  app.run()
