from flask import Flask
from flask import render_template,request
from fer import FER
import base64
from PIL import Image
import cv2
from io import BytesIO
import numpy as np
data1=""
app = Flask(__name__)
def readb64(base64_string):
    sbuf = BytesIO()
    sbuf.write(base64.b64decode(base64_string))
    pimg = Image.open(sbuf)
    return cv2.cvtColor(np.array(pimg), cv2.COLOR_RGB2BGR)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/webcam')
def webcam():
    return render_template('webcam.html')

@app.route('/player', methods = ['POST'])
def get_data():
    jsdata = request.form.get('javascript_data')
    # print(jsdata)
    data1=jsdata[23:]
    # return render_template('player1.html',jsdata=jsdata)
    img=readb64(data1)
    detector=FER()
    x=detector.detect_emotions(img)
    key_list = list(x[0]['emotions'].keys())
    val_list = list(x[0]['emotions'].values())
    print(x[0]['emotions'])
    top_emotion=sorted(x[0]['emotions'].values())[-1]
    position = val_list.index(top_emotion)
    if(key_list[position]=='neutral'):
        em2=sorted(x[0]['emotions'].values())[-2]
        position = val_list.index(em2)
        print(key_list[position])
        print("Output1:", em2)
        final_emotion=key_list[position]
    else:
        final_emotion=key_list[position]
    if(final_emotion=='happy'):
        playlist="https://open.spotify.com/embed/playlist/37i9dQZF1DXdPec7aLTmlC"
    elif(final_emotion=='sad'):
        playlist="https://open.spotify.com/embed/playlist/37i9dQZF1DX7qK8ma5wgG1"
    else:
        playlist="https://open.spotify.com/embed/playlist/477J7LQ97g60MvkjUGWbQN"
    return render_template("player.html",playlist=playlist)

# @app.route('/player')
# def player():
#     img=readb64(data1)
#     detector=FER()
#     x=detector.detect_emotions(img)
#     key_list = list(x[0]['emotions'].keys())
#     val_list = list(x[0]['emotions'].values())
#     print(x[0]['emotions'])
#     top_emotion=sorted(x[0]['emotions'].values())[-1]
#     position = val_list.index(top_emotion)
#     if(key_list[position]=='neutral'):
#         em2=sorted(x[0]['emotions'].values())[-2]
#         position = val_list.index(em2)
#         print(key_list[position])
#         print("Output1:", em2)
#         final_emotion=key_list[position]
#     else:
#         final_emotion=key_list[position]
#     if(final_emotion=='happy'):
#         playlist="https://open.spotify.com/embed/playlist/37i9dQZF1DXdPec7aLTmlC"
#     elif(final_emotion=='sad'):
#         playlist="https://open.spotify.com/embed/playlist/37i9dQZF1DX7qK8ma5wgG1"
#     else:
#         playlist="https://open.spotify.com/embed/playlist/477J7LQ97g60MvkjUGWbQN"
    # return render_template("player.html",playlist=playlist)
# app.run()