from unittest import TestCase

from unittest.mock import MagicMock

from ..db.type_casting import cast_document, create_instance


class TestTypeCasting(TestCase):
    def test_create_instance(self):
        d = {'username': 'john', 'name': 'John', 'last_name': 'Appleseed'}
        obj = create_instance(MagicMock, d)
        self.assertEqual(d, {'username': obj.username,
                             'name': obj.name,
                             'last_name': obj.last_name})

    def test_cast_single_document(self):
        document = {'hello': 'world', 'dict': {'inner': 'obj'}}
        obj = cast_document(MagicMock, document)
        self.assertEqual(document, {'hello': obj.hello,
                                    'dict': obj.dict})

    def test_cast_many_documents(self):
        documents = [
            {'host_name': 'dolores'},
            {'host_name': 'bernard'},
            {'host_name': 'maeve'},
            {'host_name': 'william'},
        ]

        objects = cast_document(MagicMock, documents, True)

        self.assertEqual(len(objects), len(documents))
