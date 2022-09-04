from flask import Flask, render_template, Response
from object_camera import VideoCamera
from tensorflow.python.framework.ops import disable_eager_execution
disable_eager_execution()
app = Flask(__name__)
video_stream = VideoCamera()

@app.route('/')
def index():
    return render_template('object_index.html')


def gen(camera):
    flag = 1
    while True:
        frame = camera.get_frame(flag)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        flag = 0


@app.route('/object_start_video')
def object_start_video():
    return Response(gen(video_stream),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(threaded=False)