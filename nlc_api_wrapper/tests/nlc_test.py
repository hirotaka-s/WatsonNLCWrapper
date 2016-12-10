from unittest import TestCase

from getpass import getpass
import json

from nlc_api_wrapper.core.nlc import NLC 

class WrapperTest(TestCase):
    @classmethod
    def setUpClass(cls):
        conf = dict()
        conf["url"] = input('url: ')
        conf["username"] = input('username: ')
        conf["password"] = getpass('password:' )
    

        with open('./tmp_conf_file.json', 'w') as f:
            json.dump(conf, f)

    def setUp(self):
      self.nlc = NLC(config_file_path='./tmp_conf_file.json')

    def test_classifiers(self):
        expect = {"classifiers": []}
        actual = self.nlc.classifiers()
        self.asserEqual(expected, actual)

    def test_dump_classifiers(self):
        expext = '{"classifiers": []}'
        actual = self.nlc.classifiers()
        self.asserEqual(expected, actual)
