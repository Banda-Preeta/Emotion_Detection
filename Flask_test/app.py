from cProfile import label
from flask import Flask, render_template, request
from emotion import DetectEmotion
import cv2
from numpy import ndarray
app=Flask(__name__)



@app.route('/')
def index():
    return render_template('index.html')


@app.route('/after', methods=['GET','POST'])
def after():
    img= request.files['file1']
    img.save('static/file.jpg')
    img = cv2.imread('static/file.jpg')
    [result,capture,label,preds]=DetectEmotion(img)
    if  type(result) is ndarray :
        cv2.imwrite('static/result.jpg',result)
        resultpath='result.jpg'
    else:
        resultpath='none.jpg'
    cv2.imwrite('static/capture.jpg',capture)
    return render_template('after.html',data={'label':label,"resultpath":resultpath,'preds':preds})
if __name__== "__main__":
    app.run(debug=True)