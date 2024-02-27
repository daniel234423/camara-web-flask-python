from flask import Flask, render_template, Response, jsonify
import uuid
import cv2 as cv
from app import crate_app
import imutils as imt


app = crate_app()

camra = cv.VideoCapture(0)
def  gen():
    while True:
        ret, frame = frames_de_camara()
        if not ret: break
        else:
            yield b"--frame\r\nContent-Type: image/jpeg\r\n\r\n" + frame + b"\r\n"

def frames_de_camara(): 
    ret, frame = camra.read()
    if not ret:
            return False, None
    _, bufer = cv.imencode(".jpg", frame)
    imagen = bufer.tobytes()
    return True, imagen

@app.route('/camara_web')
def camara_web():
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')




@app.route('/descargar_foto')
def  descargar_foto():
    ret, frame = frames_de_camara()
    if not ret:
        abort(503)
        return
    answer = Response(frame)
    answer.headers["Content-Disposition"]= "attachment; filename=\"foto.jpg\""
    answer.headers["Content-Type"] = "image/jpeg"
    answer.headers["Content-Transfer-Encoding"] = "Binary"
    return answer

@app.route("/foto_guardada")
def foto_guardada():
    nombreImagen = str(uuid.uuid4())+".jpg"
    ret, frame = camra.read()
    if ret:
        cv.imwrite(nombreImagen, frame)
    return jsonify({
        "ret":ret,
        "nomreImagen":nombreImagen
    })
@app.route('/')
def index():
    return render_template("index.html")


app.run(debug=True ,host="0.0.0.0")