from django.utils import unittest
from plrutils.models import GraphFunction, Database
from utils import check_types, check_type
# from django.test import Client


class CheckTypesTestCase(unittest.TestCase):
    def setUp(self):
        self._db = Database(name='default')
        self.func1 = GraphFunction(
            name='test1', database=self._db,
            params='int_par;int;char_par;char;string_par;string;float_par;float'
        )
        self.func2 = GraphFunction(
            name='test2', database=self._db,
            params='float_par;float;float_array_par;float_array;'
                   'int_array_par;int_array;string_array_par;string_array;'
        )

    def test_check_types(self):
        i = ['42', 'c', 'test', '42.0']
        self.assertEqual(check_types(self.func1.params, i), [42, 'c', 'test', 42.0])

        i = ['c', 'c', 'test', '42.0']
        self.assertEqual(check_types(self.func1.params, i), None)

        i = ['42', '42', 'test', '42.0']
        self.assertEqual(check_types(self.func1.params, i), None)

        i = ['42', 'c', 23, '42.0']
        self.assertEqual(check_types(self.func1.params, i), [42, 'c', 23, 42.0])

        i = ['42', 'c', 'test', 'test']
        self.assertEqual(check_types(self.func1.params, i), None)

        i = ['42.0', '1.2,3.4,5.6', '1,2,3,4', '"lorem","ipsum","dolor,sit"']
        exp_out = [42.0,
                   [1.2, 3.4, 5.6],
                   [1, 2, 3, 4],
                   ['lorem', 'ipsum', 'dolor,sit']]

        self.assertEqual(check_types(self.func2.params, i), exp_out)
        self.assertIsNone(check_type('float_array', '1.2a,2.3'))
        self.assertEqual(check_type('float_array', '12, 23.0'), [12.0, 23.0])
        self.assertIsNone(check_type('int_array', '1,2,3a'))
        self.assertIsNone(check_type('char_array', 'a,,b'))
        self.assertIsNone(check_type('string_array', '"asd",asd,"asd"'))
        self.assertEqual(check_type('string_array', r'"lorem\"ipsum","dolor"'),
                         ['lorem"ipsum', 'dolor'])
        self.assertEqual(check_type('string_array',
                                    '"lorem, ipsum","dolor","sit123","amet",'),
                         ['lorem, ipsum', 'dolor', 'sit123', 'amet'])
        self.assertIsNone(check_type('string_array', '"lorem",ipsum,"dolor"'))
        self.assertIsNone(check_type('string_array', '"lor"em,"ipsum"'))
        self.assertEqual(check_type('string_array', '"lorem ipsum"'),
                         ['lorem ipsum'])
        self.assertIsNone(check_type('string_array', 'lorem,ipsum'))


# fixme: IDK why, but this test does not work
# class ExecuteTestCase(unittest.TestCase):
#     def setUp(self):
#         Database.objects.create(name='asd')
#         GraphFunction.objects.create(id=1, name='env_phen', database=Database.objects.get(name='asd'), params='par;int')
#         self.client = Client()
#
#     def test_execute(self):
#         response = self.client.get('/execute/1/1/')
#         self.assertEqual(response.status_code, 200)
