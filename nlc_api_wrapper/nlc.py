# -*- coding: utf-8 -*-
"""
Wrapper class for v1 Natural Language Classifier service
"""
import os
import json

from six.moves import UserList

from watson_developer_cloud import NaturalLanguageClassifierV1 as NaturalLanguageClassifier

from .constants import DEFAULT_CREDENTIAL_PATH
from .utils import DotAccessibleDict

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
        _create_result = None

        if isinstance(traning_data, file): # traning_data is file discripter
            _create_result = self.__nlc.create(traning_data, name=name, language=language)
        elif isinstance(traning_data, str): # traning_data is file path
            with open(traning_data, "r") as traning_data_csv:
                _create_result = self.__nlc.create(traning_data_csv, name=name, language=language)

        return CreateResult(_create_result)

    def classifiers(self):
        _classifiers_raw = self.__nlc.list()
        _classifiers = [Classifier(c) for c in _classifiers_raw['classifiers']]
        #return Classifiers(_classifiers, _classifiers_raw)
        return Classifiers(_classifiers)

    def status(self, classifier_id):
        return State(self.__nlc.status(classifier_id))

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
        _classifiers = self.classifiers()
        return [self.remove(c.classifier_id) for c in _classifiers]


class State(DotAccessibleDict):
    def __init__(self, _status):
        super(State, self).__init__(_status)


class Classifier(DotAccessibleDict):
    def __init__(self, classifier):
        super(Classifier, self).__init__(classifier)


class Classifiers(UserList):
    def __init__(self, classifiers):
        super(Classifiers, self).__init__(classifiers)

    def get_classifiers_by_name(self, name):
        return filter(lambda c: c.name == name, self.data)

    def get_classifier_by_id(self, classifier_id):
        item = filter(lambda c: c.classifier_id == classifier_id, self.data)
        if not item:
            raise KeyError(classifier_id)
        
        return item[0]


class ClassifyResult(DotAccessibleDict):
    def __init__(self, classify):
        super(ClassifyResult, self).__init__(classify)


class CreateResult(DotAccessibleDict):
    def __init__(self, create_result):
        super(CreateResult, self).__init__(create_result)
