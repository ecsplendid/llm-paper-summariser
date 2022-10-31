from flask import request
from engine import process_pdf
from flask import Flask
app = Flask(__name__)

# return a basic form which will call POST to /pdf2txt with a url
# we need a text input box and a submit button
@app.route('/')
def index():
    return '''
        <form action="/pdf2txt" method="POST">
            <input type="text" name="url" placeholder="Enter a url to a PDF" />
            <input type="checkbox" name="html" value="html" checked />
            <input type="submit" value="Submit" />
        </form>
    '''

# create a flask http POST method which will take in a url of a pdf in the post message and return the text
# this method will call the pdf2txt.py script and return the text
@app.route('/pdf2txt', methods=['POST'])
def pdf2txt():
    # get the url field from the post message
    url = request.form['url']
    return process_pdf(url, html=True if "html" in request.form else False)

if __name__ == "__main__":
    app.run(port=5000, debug=True, host='0.0.0.0')
