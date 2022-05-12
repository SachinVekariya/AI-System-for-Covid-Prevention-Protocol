from django.shortcuts import render

from .apps import ApiConfig
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from rest_framework.decorators import parser_classes

import cv2
import numpy as np
import base64

import io
import PIL.Image

from .flyr_unpack import unpack
from .utils import sensor_vals_to_temp

# Create your views here.

def home(request):
    return render(request,'Home_Page/index.html')

def about(request):
    return render(request,'About/index.html')

def help(request):
    return render(request,'Help/index.html')

def mask_photo(request):
    return render(request,'Mask_Photo/index.html')

def mask_video(request):
    return render(request,'Mask_Video/index.html')

def mask_temp(request):
    return render(request,'Mask_Temp/index.html')

# Create your views here.
@parser_classes((MultiPartParser, ))

class Detection_Photo(APIView):
    def post(self,request,format=None):
        data = request.POST['img']
        data = data.split(',')[1]
        nparr = np.fromstring(base64.b64decode(data),np.uint8)
        img1 = cv2.imdecode(nparr,cv2.IMREAD_COLOR)
        img = cv2.resize(img1, (224, 224))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        _faces = ApiConfig.model.detect_faces(img)
        
        mask = []
        confidence = []
        entry = []
        for key, value in enumerate(_faces):
            (x,y,w,h) = int(value['box'][0]*2.23),int(value['box'][1]*2.23),int(value['box'][2]*2.23),int(value['box'][3]*2.23)
            cv2.rectangle(img1,(x,y),(x+w,y+h),(255,255,255),2)
            cv2.putText(img1, str(key), (x, y),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, 2)
            
            roi = img1[y:y+h, x:x+w]
            roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
            roi = roi/255.0
            roi = cv2.resize(roi, (32, 32))
            roi = roi.reshape(-1, 32, 32, 1)

            prediction = ApiConfig.mask_model(roi)
            cla = np.argmax(prediction)
            category = ["WithMask", "WithoutMask"]
            score = int(prediction[0][cla]*100)
            
            confidence.append(score)
            mask.append(category[cla])

            if category[cla] == "WithMask":
                entry.append("Yes")
            else:
                entry.append("No")

        _,re_img = cv2.imencode('.jpg',img1)
        re_img = base64.b64encode(re_img).decode('utf-8')
        response_data = {'img': re_img,'mask': mask, 'confidence': confidence,'entry':entry}
        return Response(data=response_data,status=200)


class Detection_Video(APIView):
    def post(self,request,format=None):
        data = request.POST['img']
        data = data.split(',')[1]
        nparr = np.fromstring(base64.b64decode(data),np.uint8)
        img1 = cv2.imdecode(nparr,cv2.IMREAD_COLOR)
        img = cv2.resize(img1, (224, 224))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        _faces = ApiConfig.model.detect_faces(img)
        
        mask = []
        confidence = []
        entry = []
        for key, value in enumerate(_faces):
            (x,y,w,h) = int(value['box'][0]*2.28),int(value['box'][1]*1.71),int(value['box'][2]*2.28),int(value['box'][3]*1.71)
            cv2.rectangle(img1,(x,y),(x+w,y+h),(255,255,255),2)
            cv2.putText(img1, str(key), (x, y),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, 2)
            
            roi = img1[y:y+h, x:x+w]
            roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
            roi = roi/255.0
            roi = cv2.resize(roi, (32, 32))
            roi = roi.reshape(-1, 32, 32, 1)

            prediction = ApiConfig.mask_model(roi)
            cla = np.argmax(prediction)
            category = ["WithMask", "WithoutMask"]
            score = int(prediction[0][cla]*100)
            
            confidence.append(score)
            mask.append(category[cla])

            if category[cla] == "WithMask":
                entry.append("Yes")
            else:
                entry.append("No")

        _,re_img = cv2.imencode('.jpg',img1)
        re_img = base64.b64encode(re_img).decode('utf-8')
        response_data = {'img': re_img,'mask': mask, 'confidence': confidence,'entry':entry}
        return Response(data=response_data,status=200)

class Detection_Thermal(APIView):
    def post(self, request, format=None):

        thermal_img = request.FILES['thermal']      # Dimension (320x240)
        raw_sensor_np = unpack(thermal_img)
        thermal_np = sensor_vals_to_temp(raw_sensor_np)

        optical_img = request.FILES['optical']      # Dimension (640x480)
        img = optical_img.read()
        img = PIL.Image.open(io.BytesIO(img))
        img = np.array(img)
        img = img[70:430, 100:580]
        # Original Image with dimension of (480x360)
        img1 = img
        img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, (224, 224))           # Dimension (224x224)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        _faces = ApiConfig.model.detect_faces(img)

        temp = []
        mask = []
        confidence = []
        entry = []
        reason = []

        for key, value in enumerate(_faces):
            (x, y, w, h) = int(value['box'][0]*2.1429), int(value['box'][1] *
                                                            1.6071), int(value['box'][2]*2.1429), int(value['box'][3]*1.6071)
            cv2.rectangle(img1, (x, y), (x+w, y+h), (255, 255, 255), 2)
            cv2.putText(img1, str(key), (x, y),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, 2)

            roi = img1[y:y+h, x:x+w]
            roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
            roi = roi/255.0
            roi = cv2.resize(roi, (32, 32))
            roi = roi.reshape(-1, 32, 32, 1)

            prediction = ApiConfig.mask_model(roi)
            cla = np.argmax(prediction)
            category = ["WithMask", "WithoutMask"]
            score = int(prediction[0][cla]*100)

            (x_t, y_t, w_t, h_t) = int(value['box'][0]*1.4286), int(value['box'][1]*1.0714), int(
                value['box'][2]*1.4286), int(value['box'][3]*1.0714)  # For Thermal Image
            thermal_face = thermal_np[y_t:y_t+int(h_t/4), x_t:x_t+w_t]
            temperature = np.average(thermal_face)

            temp.append(temperature)
            confidence.append(score)
            mask.append(category[cla])

            if temperature <= 39 and category[cla] == "WithMask":
                entry.append("Yes")
                reason.append("Allowed")
            elif temperature <= 39 and category[cla] == "WithoutMask":
                entry.append("No")
                reason.append("No Mask")
            elif temperature > 39 and category[cla] == "WithMask":
                entry.append("No")
                reason.append("High Temperature")
            else:
                entry.append("No")
                reason.append("No Mask + High Temperature")

        _, re_img = cv2.imencode('.jpg', img1)
        re_img = base64.b64encode(re_img).decode('utf-8')
        response_data = {'img': re_img, 'temp': temp,
                         'mask': mask, 'confidence': confidence,'entry':entry,'reason':reason}
        return Response(data=response_data, status=200)
