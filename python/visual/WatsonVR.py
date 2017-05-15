import json
import os
from os.path import join, dirname
from watson_developer_cloud import VisualRecognitionV3
from dotenv import load_dotenv, find_dotenv
import argparse

test_url = 'https://www.ibm.com/ibm/ginni/images' \
           '/ginni_bio_780x981_v4_03162016.jpg'

try:
    load_dotenv(find_dotenv())
except IOError:
    print ('warning: no .env file loaded')

visual_recognition = VisualRecognitionV3('2016-05-20', api_key=os.getenv('VR_API_KEY'))


def createClassifier(positive_imageFile, negative_imagefile, classname):
    with open(positive_imageFile, 'rb') as positive_class, \
            open(negative_imagefile, 'rb') as negatives:
        print("Creating a new classifier")
        example_type = classname + '_positive_examples'
        print(json.dumps(visual_recognition.create_classifier('SpidersVsRest', spider_positive_examples=positive_class, negative_examples=negatives), indent = 2))

def classifyImage(image, classifierId):
    with open(image, 'rb') as images_file:
        results = visual_recognition.classify(images_file=images_file,
                                                threshold=0.1,
                                                classifier_ids=[
                                                classifierId,
                                                'default'])
        print(json.dumps(results, indent=2))

def getClassifier(classifierId):
    print(json.dumps(visual_recognition.get_classifier(classifier_id), indent=2))

def updateClassifier(image, classifier_id, positive_class):
    with open(image, 'rb') as image_file:
        example_type = positive_class + '_positive_examples'
        print(json.dumps(visual_recognition.update_classifier(classifier_id, example_type=image_file), indent = 2))


def detectFaces(image, classify):
    faces_result = visual_recognition.detect_faces(images_url=image)
    print(json.dumps(faces_result, indent=2))

def deleteClassifier(classifierId):
    print(json.dumps(visual_recognition.delete_classifier(classifier_id=classifierId), indent=2))

def listClassifiers():
    print(json.dumps(visual_recognition.list_classifiers(), indent=2))

def recognizeText(imageFile):
    with open(imageFile, 'rb') as image_file:
        text_results = visual_recognition.recognize_text(images_file=image_file)
        print(json.dumps(text_results, indent=2))

def parse_args():
        """ Parse args """
        parser = argparse.ArgumentParser(description='Run a VR Image classification service')
        parser.add_argument('--action', type=str, help='Options are create, classify, status, detect, list,recognize,delete')
        parser.add_argument('--positive', type=str, help='positive examples')
        parser.add_argument('--negative', type=str, help='negative examples')
        parser.add_argument('--positive_class', type=str, help='positive class name')
        parser.add_argument('--classifier_id',type=str, help='classifier id')
        parser.add_argument('--image', type=str,help="image file")
        ns = parser.parse_args()

        return ns.action, ns.positive, ns.negative, ns.positive_class,ns.classifier_id,ns.image

if __name__ == "__main__":
    action, positives, negatives, positive_class,classifier_id,image = parse_args()

    if action == "create" and positives != None and negatives != None:
        print positive_class
        createClassifier(positives,negatives,positive_class)
    elif action == "status" and classifier_id is not None:
        print action
        getClassifier(classifier_id)
    elif action == "classify" and classifier_id is not None and image is not None:
        print action
        classifyImage(image, classifier_id)
    elif action == "list":
        print action
        listClassifiers()
    elif action == "delete" and classifier_id is not None:
        print action
        deleteClassifier(classifier_id)
    else:
        print("Invalid arguments for %s. Please check the arguments by using -h parameter." % action)

