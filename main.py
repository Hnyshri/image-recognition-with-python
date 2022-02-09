from flask import Flask, jsonify, request
import sys
import base64
from google.cloud import automl_v1beta1
import os


app = Flask(__name__)

@app.route("/")
def home():
    return "ALL Good"

@app.route("/upload",methods=['POST'])
def upload():
    if(request.method == "POST"):
    # return jsonify("Hello world")
        imagefile = request.files['image']
        filename = imagefile.filename
        print(filename)
        imagefile.save("uploadimages/" + filename)
        #print(get_prediction(filename, "onyx-oxygen-3396545", "IOD671560371720001945454"))

        data = get_prediction("/var/www/html/uploadimages/"+filename, "onyx-oxygen-3396545", "IOD671560371720001945454")
        return jsonify({
            "message" : str(data)
        })
    



# 'content' is base-64-encoded image data.
def get_prediction(content, project_id, model_id):
  os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="onyx-oxygen-339613-0b1c948a896c.json"
  
  with open(content, "rb") as image_file:
    data = base64.b64encode(image_file.read())
  # print(base64.b64decode(data))
    base_64 = base64.b64decode(data)

  prediction_client = automl_v1beta1.PredictionServiceClient()

  name = 'projects/{}/locations/us-central1/models/{}'.format(project_id, model_id)
  payload = {'image': {'image_bytes': base_64 }}
  params = {}
  request = prediction_client.predict(name= name, payload=payload, params=params)
  return request  # waits till request is returned

    

if __name__ == "__main__":
    app.run(host="0.0.0.0")
