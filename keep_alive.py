from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    # Serve the index.html file
    return app.send_static_file('index.html')

@app.route('/run')
def run_script():
    # Run your Python script and return the output
    # Modify this part to execute your specific script
    output = "Hello, world!"

    return output

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
