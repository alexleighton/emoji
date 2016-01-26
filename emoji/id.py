import time
import uuid

class Id(object):
    "Class containing a string value meant to represent an identifier."

    def __init__(self, id_value):
        self.value = id_value

    def __eq__(self, other):
        return self.value == other.value

    def __str__(self):
        return self.value

    def __repr__(self):
        return self.value

    def __hash__(self):
        return hash(self.value)

    @staticmethod
    def generate(type):
        "Generate an Id given the type of the id."
        return Id(Id.generate_str(type))

    @staticmethod
    def generate_str(type):
        return '.'.join(
            ('id', type, str(int(time.time())), str(uuid.uuid4()))
        )
