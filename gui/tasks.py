# coding: UTF-8
'''
Created on 2013-04-06

@author: tianwei

Desc: Celery Tasks
'''
import os
import sys
import uuid
import time

from celery.decorators import task

from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.http import HttpResponseForbidden, Http404
from django.template import RequestContext
from django.utils import simplejson
from django.views.decorators import csrf
from django.contrib.auth.decorators import login_required
from django.core.files.uploadedfile import UploadedFile
from calcore.controllers.prediciton_model import PredictionModel
from backend.logging import logger, loginfo
from calcore.models import SingleTask, ProcessedFile, SuiteTask
from const.models import StatusCategory
from const import STATUS_WORKING, STATUS_SUCCESS, STATUS_FAILED, STATUS_UNDEFINED
from settings import MEDIA_ROOT,SETTINGS_ROOT


def get_ModelName(name):
    temp={
            "koa":"logKOA",
            "pl":"logRP",
            "kof":"logKOF"
            }
    # return temp.get(name)
    if temp.has_key(name):
        return temp.get(name)
    else: 
        raise KeyError,"We don't have this model"


@task()
def add(x, y):
    print "sleep!"
    return x+y+x+y


@task()
def add_a(x, y):
    print "sleep! a"
    return x+y+x+y


@task()
def calculateTask(task, model_name):
    para = dict.fromkeys(['smilestring', 'filename', 'cas'], "")

    fullpath = os.path.join(SETTINGS_ROOT, task.file_obj.file_obj.path)
    para['filename'] = os.path.basename(fullpath)
    filepath = os.path.dirname(fullpath)

    print fullpath
    print para["filename"]
    print filepath

    try:
        pm = PredictionModel([get_ModelName(model_name)], para, filepath)
        result = pm.predict_results[para['filename'].split(".")[0]][get_ModelName(model_name)]
        loginfo(p=result, label="calculate task result")
    except KeyError:
        task.result_state="We don't have this model"
        print "We don't have this model"
        result=0
        suite=task.sid
        suite.status_id=StatusCategory.objects.get(category=STATUS_WORKING)
        suite.has_finished_tasks+=1
        suite.save()
        #add singletask state
    else:
        suite=task.sid
        suite.status_id=StatusCategory.objects.get(category=STATUS_SUCCESS)
        suite.has_finished_tasks+=1
        suite.save()
    task.results=result
    task.save()

    return result
