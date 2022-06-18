# Emotion detection
## Built with
- Python
- Flask
- OpenCV
- Javascript
- HTML
- CSS

## Getting Started
This is the instruction of setting up the project and running the project locally
### Prerequisites
 Optional : Create a virtual environment and activate the virtual environment. This github repository doen't contain my virtual env.
```sh
pip install virtualenv
```

Create a veitualnv
```sh
virtualenv my_name
```

Activate virtula env
```sh
my_name\Scripts\activate.bat
```

1. Install the packages mentioned `requirements.txt`
or Run
    ```sh
    pip install requirements.txt
    ```

2. Open the folder `flask_live`
    ```sh
    cd flask_live
    ```

3. Run the `app.py` file
    ```sh
    python app.py
    ```

4. Open the server link provided by python which is usually `http://127.0.0.1:5000/` in the browser.

5. Another devices can also be logged but both the host device and second device should be connected to same network and second link which is provided by python in commandline.


# Emotions which can be detected

- Angry
- Confident
- Confused
- Contempt
- Crying
- Disgust
- Fear
- Happy
- Neutral
- Sad
- Shy
- Sleepy
- Surprised




![Mr bean](https://github.com/Nithin1506200/EmotionDetection/blob/main/mrbean.png)

## Models
Models can be found in the `Models\grayscalemodel_1_new.hdf5` which is built using dcnn.

This project also uses javascript's fetch api to get the prediction result. This javascript requests the result once per 500ms which can be changed by editing `static\js\index.js` and changing `setInterval(500,GetData)` at last line.