from flask import Flask, request
import webbrowser

app = Flask(__name__)

@app.route('/zoho/callback')
def zoho_callback():
    code = request.args.get("code")
    return f"Authorization code received: {code***REMOVED***. Copy this and paste it into your Python script."

if __name__ == '__main__':
    webbrowser.open("http://localhost:5000")
    app.run(port=5000)
