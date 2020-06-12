#coding=utf-8
import cv2
import base64
from flask import *
import requests
import face_recognition
from examples.face_mysql import FaceSQL
import numpy as np
from PIL import ImageDraw, Image, ImageFont

REQUEST_URL = 'http://127.0.0.1:5001/'

def predict(byte_file, frame):
    # img = open(img_path, 'rb').read()
    img = byte_file
    param = {'file': img}

    result = requests.post(REQUEST_URL, files=param)
    # print(result.json())
    result = result.json()
    cords = []
    if result['success']:
        cords = result['prediction']
    return cords

if __name__ == '__main__':
    # predict('./fang.jpg')
    video_capture = cv2.VideoCapture(0)
    face_sql = FaceSQL()
    all_faces = face_sql.find_all_face()
    # print(len(all_faces))
    all_faces_encodings = [face.encoding for face in all_faces]
    print(all_faces_encodings)
    all_faces_encodings = [[float(ed) for ed in encoding.split(',')] for encoding in all_faces_encodings]
    # print(all_faces_encodings)
    # fang[-1]
    while True:
        _, frame = video_capture.read()
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        _, jpeg = cv2.imencode('.jpg', small_frame)
        # print(type(jpeg))
        rgb_small_frame = small_frame[:, :, ::-1]
        cords = predict(jpeg.tobytes(), frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, cords)
        names = []
        for face_encoding in face_encodings:
            name = 'unknown'
            matches = face_recognition.compare_faces(all_faces_encodings, face_encoding)
            face_distances = face_recognition.face_distance(all_faces_encodings, face_encoding)
            print(face_distances)
            best_match_index = np.argmin(face_distances)
            print(matches)
            if matches[best_match_index]:
                name = all_faces[best_match_index].name
                names.append(name)
            print(names)
        for cord in cords:
            top, right, bottom, left = cord
            bottom *= 4
            left *= 4
            top *= 4
            right *= 4
            cv2.rectangle(frame, (left, top), (right, bottom), (255, 255, 0), 1)
        image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        draw = ImageDraw.Draw(image)
        for cord, name in zip(cords, names):
            top, right, bottom, left = cord
            bottom *= 4
            left *= 4
            top *= 4
            right *= 4
            # image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            fontStyle = ImageFont.truetype(
                "font/simsun.ttc", 20, encoding="utf-8")
            draw.text((left, top-20), name, (255, 0, 0), font=fontStyle)
        image = cv2.cvtColor(np.asarray(image), cv2.COLOR_RGB2BGR)
        cv2.imshow('img', image)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    video_capture.release()
    cv2.destroyAllWindows()





