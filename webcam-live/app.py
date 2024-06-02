from flask import Flask, render_template, Response
import cv2

app = Flask(__name__)
camera = cv2.VideoCapture(0)  # Assuming camera index 0 is the desired video source

def cctv_live():
    while True:
        success, frame = camera.read()
        if not success:
            break

        # Encode frame as JPEG with appropriate quality parameter (adjust as needed)
        ret, buffer = cv2.imencode('.jpg', frame )

        # Directly yield the encoded JPEG data as bytes
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video')
def video():
    return Response(cctv_live(), mimetype='multipart/x-mixed-replace;boundary=frame')

if __name__ == "__main__":
    app.run(debug=True)
