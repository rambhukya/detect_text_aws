from flask import Flask, render_template, request
import boto3
import json
app = Flask(__name__)
from werkzeug.utils import secure_filename

ak=""
ask=""
at=""

s3 = boto3.client(
    's3',
    aws_access_key_id=ak,
    aws_secret_access_key=ask,
    aws_session_token=at
)
rek = boto3.client('rekognition',
    aws_access_key_id=ak,
    aws_secret_access_key=ask,
    aws_session_token=at
)
BUCKET_NAME='test251022'

@app.route('/')  
def home():
    return render_template("index.html")

@app.route('/upload',methods=['post'])
def upload():
    if request.method == 'POST':
        img = request.files['file']
        if img:
                filename = secure_filename(img.filename)
                img.save(filename)
                s3.upload_file(
                    Bucket = BUCKET_NAME,
                    Filename=filename,
                    Key = filename
                )
                response = rek.detect_text(
                 Image={
                    'S3Object': {
                    'Bucket': BUCKET_NAME,
                    'Name': filename,
                }
                })
                msg = "Upload Done ! "
                test = response['TextDetections']
                var = []
                for text in test:
                    var.append(text['DetectedText'])
                data = var
                #tag = test
                #s1=json.dumps(test)
                #object=json.loads(s1)
                #s2=(object['DetectedText'])
                #s4=s2[0]
                #s5=s4['Name']
                
    return render_template("index.html",msg =data )




if __name__ == "__main__":
    
    app.run(debug=True)
