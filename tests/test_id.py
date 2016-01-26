import time
import unittest
from unittest.mock import patch
import uuid

from emoji.id import Id

class IdTest(unittest.TestCase):

    @patch("time.time")
    @patch("uuid.uuid4")
    def test_generate(self, uuid_func, time_func):
        uuid_func.return_value = 'uuid'
        time_func.return_value = 123.456

        id = Id.generate('typ')

        self.assertEqual(Id('id.typ.123.uuid'), id)
        self.assertEqual(hash(Id('id.typ.123.uuid')), hash(id))
        self.assertEqual('id.typ.123.uuid', str(id))
        self.assertEqual('id.typ.123.uuid', repr(id))
