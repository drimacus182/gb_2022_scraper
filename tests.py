import unittest
import parsers
from api import Api
import typing


class MyTest(unittest.TestCase):
    def test_datetime_convertion(self):
        self.assertEqual(parsers.parse_datetime("23.08.2021 о 13:07"), "2021-08-23 13:07:00 +0300")
        self.assertEqual(parsers.parse_datetime("23.12.2021 о 13:07"), "2021-12-23 13:07:00 +0200")

    def test_can_get_project_list(self):
        api = Api()

        projects = api.get_project_list()
        self.assertIsNotNone(projects)
        self.assertIsInstance(projects, typing.List)
        self.assertTrue(len(projects) > 500)

    def test_can_get_project(self):
        api = Api()

        project = api.get_project(421)
        self.assertIsNotNone(project)
        self.assertIsNotNone(project['votes_table'])
        self.assertIsNotNone(project['votes_count'])
