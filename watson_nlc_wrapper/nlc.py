# -*- coding: utf-8 -*-
"""
Wrapper class for v1 Natural Language Classifier service
"""
import os
import json

from six.moves import UserList
from io import IOBase, open

from watson_developer_cloud import NaturalLanguageClassifierV1 as NaturalLanguageClassifier

from .constants import DEFAULT_CREDENTIAL_PATH
from .utils import DotAccessibleDict, is_valid_recode_num

class NLC(object):
    def __init__(self, credential_file_path=None):
        self.__nlc = None
        self.__initialize(credential_file_path)

    def __initialize(self, credential_file_path):
        if not credential_file_path:
            credential_file_path = os.path.expanduser(DEFAULT_CREDENTIAL_PATH)
 
        with open(credential_file_path, 'r') as credential_file:
            credential = json.load(credential_file)

            self.__nlc = NaturalLanguageClassifier(url=credential['url'], username=credential['username'], password=credential['password'])

    def create(self, traning_data, name=None, language='en'):
        """
        :param traning_data: A csv file or file path representing the traning data
        :param name: The optional descriptive name for the classifier
        :param language: The language og the input data
        :return: A instance object with the classifier_id of the newly created classifier, still in traning
        """
        create_result = None

        if isinstance(traning_data, file) or isinstance(traning_data, IOBase): # traning_data is file discripter
            create_result = self.__nlc.create(traning_data, name=name, language=language)
        elif isinstance(traning_data, str): # traning_data is file path
            with open(traning_data, newline=None, mode='r', encoding='utf-8') as csv_file:
                if is_valid_recode_num(csv_file):
                    create_result = self.__nlc.create(csv_file, name=name, language=language)

        return CreateResult(create_result)

    def classifiers(self):
        classifiers_raw = self.__nlc.list()
        classifiers_ = [Classifier(c) for c in classifiers_raw['classifiers']]
        return Classifiers(classifiers_)

    def status(self, classifier_id):
        return Status(self.__nlc.status(classifier_id))

    def classify(self, classifier_id, text):
        return ClassifyResult(self.__nlc.classify(classifier_id, text))

    def remove(self, classifier_id):
        """
        param: classifier_id: Unique identifier for the classifier
        retrun: empty dict object
        raise: watson_developer_cloud.watson_developer_cloud_service.WatsonException: Not found
        """
        return self.__nlc.remove(classifier_id)

    def remove_all(self):
        classifiers_ = self.classifiers()
        return [self.remove(c.classifier_id) for c in classifiers_]


class Status(DotAccessibleDict):
    def __init__(self, status):
        super(Status, self).__init__(status)


class Classifier(DotAccessibleDict):
    def __init__(self, classifier):
        super(Classifier, self).__init__(classifier)


class Classifiers(UserList):
    def __init__(self, classifiers):
        super(Classifiers, self).__init__(classifiers)

    def get_classifiers_by_name(self, name):
        return filter(lambda c: c.name == name, self)

    def get_classifier_by_id(self, classifier_id):
        item = filter(lambda c: c.classifier_id == classifier_id, self)
        if not item:
            raise KeyError(classifier_id)
        
        return item[0]

    def to_json(self, *args, **kwargs):
        return json.dumps([c for c in self], *args, **kwargs)


class ClassifyResult(DotAccessibleDict):
    def __init__(self, classify):
        super(ClassifyResult, self).__init__(classify)


class CreateResult(DotAccessibleDict):
    def __init__(self, create_result):
        super(CreateResult, self).__init__(create_result)
