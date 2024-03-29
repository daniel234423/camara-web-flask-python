from flask import render_template, Response,  redirect, url_for
import uuid
import cv2 as cv
from app import crate_app
import imutils as imt
import os


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
    frame = imt.resize(frame,width=800)
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
        rutaImagen = os.path.join('app/imagenes', nombreImagen)
        cv.imwrite(rutaImagen, frame)
    return redirect(url_for('index'))

@app.route("/fotos_guardadas")
def fotos_guardadas():
    return render_template("imagenes.html")

@app.route('/')
def index():
    return render_template("index.html")


app.run(debug=True ,host="0.0.0.0")