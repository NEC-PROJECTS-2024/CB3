from flask import Flask, render_template, request, session, redirect, url_for
from werkzeug.utils import secure_filename
import urllib.request
import re
import os
import bone_fracture_detector


app = Flask(__name__, static_folder='static', template_folder='templates')
UPLOAD_FOLDER = 'static/uploads/'
RESULT_FOLDER = 'static/results/'
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['RESULT_FOLDER'] = RESULT_FOLDER


@app.route('/')
def home():
    return render_template('Index.html')


@app.route('/image')
def image():
    return render_template('Result.html')




@app.route('/image', methods=['POST'])
def upload_image():
    file = request.files['value1']
    filename = secure_filename(file.filename)
    pattern = r'^\d'
    
    if re.match(pattern, filename):
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        with open('filenames.txt', 'a') as f:
            f.write(filename + '\n')
        return render_template('Result.html', filename=filename)
    else:
        error_message = "Please upload X-ray image"
        return f'''
            <script>
                alert('{error_message}');
                window.history.back();
            </script>
        '''


@app.route('/image/display/<filename>')
def display_image(filename):
    session['filename'] = filename
    print(filename)
    return redirect(url_for('static', filename='uploads/' + filename), code=301)

@app.route('/image/detect/')
def detect():
    filename = session.get('filename', None)
    with open('filenames.txt', 'r') as f:
        filename = f.readlines()[-1].strip()
    path = 'static/uploads/'+str(filename)
    print(path)
    prediction = bone_fracture_detector.bone_image(path)
    print(filename, prediction)
    return render_template('Result.html', filename=filename, prediction=prediction)


if __name__ == '__main__':
    app.run(host="0.0.0.0",port=8080,debug=True)
