from django.apps import AppConfig
from mtcnn_cv2 import MTCNN #Loading MTCNN face detector
import tensorflow as tf
import os

class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'API'

    model = MTCNN()  # Load-model

    MODEL_PATH = os.path.dirname(__file__)+"/model/mobilenetV2"
    mask_model = tf.keras.models.load_model(MODEL_PATH)


