# -*- coding: utf-8 -*-
# @Time    : 2020/5/11 19:17
# @Author  : Fangpf
# @FileName: upload_face_data.py

import os
import logging as log
from PIL import Image
import face_recognition
from examples.face_mysql import FaceSQL
from examples.face import Face

data_path = './face_data/'
file_list = os.listdir(data_path)

if __name__ == '__main__':
    for file in file_list:
        if '.' not in file:
            log.error("文件缺失后缀名")
        filename = file[:file.index('.')]
        image = face_recognition.load_image_file(data_path+file)
        face_encoding = face_recognition.face_encodings(image)[0]
        face_encoding = ','.join(str(s) for s in face_encoding)
        face_mysql = FaceSQL()
        result = face_mysql.select_by_name(filename)
        print(result)
        if result:
            # 更新特征点
            face = Face(result[0], result[1], result[2], result[3], result[4], result[5])
            face.encoding = face_encoding
            result = face_mysql.update(face)
        else:
            # 新增人脸数据库
            face = Face()
            face.name = filename
            face.encoding = face_encoding
            result = face_mysql.save(face)

