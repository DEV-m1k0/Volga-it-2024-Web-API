from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from .models import *


@registry.register_document
class HistoryDocument(Document):

    pacientId = fields.ObjectField(properties={
        'id': fields.IntegerField(),
        'username': fields.TextField(),
        'firstName': fields.TextField(),
        'lastName': fields.TextField()
    })
    hospitalId = fields.ObjectField(properties={
        'id': fields.IntegerField(),
        'name': fields.TextField(),
        'address': fields.TextField(),
        'contactPhone': fields.TextField()
    })
    doctorId = fields.ObjectField(properties={
        'id': fields.IntegerField(),
        'username': fields.TextField(),
        'firstName': fields.TextField(),
        'lastName': fields.TextField()
    })
    room = fields.ObjectField(properties={
        'id': fields.IntegerField(),
        'room': fields.TextField()
    })

    class Index:
        name = 'history'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0
        }

    class Django:
        model = History
        fields = [
            'date',
            'data'
        ]