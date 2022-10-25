from flask import Flask, render_template, request
import boto3
import json
app = Flask(__name__)
from werkzeug.utils import secure_filename

ak="ASIA4RW7ZWQXKO6T4NNS"
ask="g+y12Sa6r/sVNTHmAYDWTtPTZQc4ggyG23vvcRJn"
at="FwoGZXIvYXdzEBEaDJ36Ja6m8Ec42pOnWyLFAXFErezIJ0epbjSLLhEDHBcdgPQEzb08N/1r+t42OFyzao0/LqGUUl2dCRbrGxnjVrZmnYwebr4Zrup5Z8fARGa//p98pfM87TIqOofpQqIWYMxaPjaJfeXY20985agmEgoaXgGuof5QApdYIhlHqO3R9HsSkY5EU55W60yifWi86n/fPWN9bWsHV9U/cQ+XDP+NozSmaEfZFBsTkVFlv/AE8QHO1m0NR2/SuS7ArgAVeUSON2th3ZEoSPVdHz9uVklZEk1dKKeN4JoGMi1/CRullN/9ZuX+ZC9hZOdhinnOnqAROGn+XV5/2cxaUXLLnEPoeiMBWcR9xT0="

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
