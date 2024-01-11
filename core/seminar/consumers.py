import cv2, numpy
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from core import models
from . import utils
from django.utils import timezone

class SeminarConsumer(WebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.created_at = None

    def connect(self):
        if self.scope['user'].is_authenticated:
            self.slug = self.scope['url_route']['kwargs']['slug']
            try:
                self.seminar = models.Seminar.objects.get(slug=self.slug, user=self.scope['user'])
                async_to_sync(self.channel_layer.group_add)(self.slug, self.channel_name)
                models.Statistic.objects.filter(seminar=self.seminar).delete()
                self.accept()
            except models.Seminar.DoesNotExist:
                self.close()
        else:
            self.close()
    
    def receive(self, bytes_data=None, text_data=None):
        if bytes_data is not None:
            frame = self.decode_blob(bytes_data)

            results = utils.predictor.process(frame)

            if results is not None:
                if self.created_at is None:
                    self.created_at = timezone.now()
                if (timezone.now() - self.created_at).total_seconds() >= 5:
                    self.created_at = timezone.now()
                    models.Statistic(data=str(results.tolist()), seminar=self.seminar, created_at=self.created_at).save()

            frame = self.encode_blob(frame)

            async_to_sync(self.channel_layer.group_send)(
                self.slug,
                {
                    'type': 'send_bytes_data',
                    'bytes_data': frame,
                }
            )

    def decode_blob(self, bytes_data):
        nparr = numpy.frombuffer(bytes_data, numpy.uint8)
        return cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    def encode_blob(self, image):
        success, encoded_img = cv2.imencode('.jpeg', image)
        return encoded_img.tobytes() if success else None
    
    def send_bytes_data(self, event):
        bytes_data = event['bytes_data']
        self.send(bytes_data=bytes_data)