from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.conf import settings
from django.templatetags.static import static
from django.contrib.staticfiles.storage import staticfiles_storage
import json
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly, AllowAny
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
import csv
import os
import pandas as pd
import numpy as np
from django.contrib.staticfiles.finders import find
from unicodedata import name
#from sklearn.metrics import cosine_similarity

def index(request):
    template = loader.get_template('home.html')
    return HttpResponse(template.render())

def test(request):
    my_dict = {'name': 'John', 'age': 30, 'city': 'New York'}
    return HttpResponse(json.dumps(my_dict), content_type='application/json')

def SAR(request):
    print("hi")

def KNN(request):
    print("hi")

# Create your views here.
@api_view(['GET'])
def apitest(request):
    return Response()

@csrf_exempt
def get_recommendations(request):

    if request.method == 'POST':

        #test_vector = [2.3,4.6,3.4,1.5,1.6,2.9,1.1,3.9,3.1,3.2,2.8,3.0,2.6,1.6,2.4,1.6,2.4,1.7,2.6,1.1,3.3,1.8,2.3,2.5,1.7,1.4,2.8,1.8,2.5,4.7,4.0,4.1,3.4,4.2,4.2,4.9,4.5,1.4,4.3,2.2,2.0,2.6,3.2,3.5,1.3,4.9,2.6,3.9,3.7,1.9,1.7,3.9,4.5,2.6,1.4,4.7,2.4,2.7,1.7,3.3,4.4,4.2,1.4,4.7,3.0,2.5,2.9,3.1,5.0,4.0,2.5,3.4,2.7,1.4,3.1,2.4,1.1,3.4,4.7,2.1,4.3,3.2,1.1,2.4,3.2,1.1,3.9,1.8,4.0,3.5,2.4,3.5,3.1,4.6,3.1,3.4,2.9,3.8,1.5,3.9,4.5,3.1,3.7,2.7,4.9,2.5,3.5,2.0,3.7,4.5,2.0,1.6,4.3,2.9,2.4,4.7,2.8,3.0,1.2,1.5,3.2,1.2,2.2,2.5,3.4,4.3,1.7,4.1,2.2,4.1,4.7,1.9,5.0,2.2,4.5,3.8,1.2,1.8,4.4,3.6,4.5,3.9,1.4,1.1,1.7,2.1,3.7,3.3,2.5,2.1,1.8,2.3,2.5,1.8,3.4,1.3,3.9,3.9,3.4,3.9,3.9,4.1,3.7,4.2,3.4,4.4,2.8,2.6,2.1,1.4,2.7,3.7,2.0,2.4,3.5,3.7,2.4,3.0,2.6,4.0,1.6,3.9,3.1,2.3,4.7,4.9,3.2,1.4,3.7,4.7,2.1,1.5,4.4,3.8,4.6,4.8,3.1,3.8,2.7,4.5,3.6,1.4,2.2,2.2,2.3,1.5,3.4,2.9,1.4,2.2,3.5,1.3,1.7,3.8,3.4,3.1,3.1,2.0,3.7,1.1,3.7,3.3,3.2,1.6,1.5,3.2,3.3,4.3,2.4,3.4,3.7,1.4,3.9,3.9,4.5,2.7,1.9,3.7,4.9,3.3,2.0,2.4,3.5,3.7,3.6,3.7,3.3,2.8,3.4,2.5,2.0,4.8,3.4,4.3,3.0,3.7,3.0,1.9,2.4,4.1,1.4,4.3,1.4,3.5]

        data = json.loads(request.body)
        user_affinity_vector = data["WorkspaceRatingsVector"]

        # Get workspace to workspace affinity matrix 
        csv_path = 'staticfiles/csv/workspace_affinity.csv'
        workspace_workspace_df = pd.read_csv(csv_path, delimiter=',')
        workspace_workspace_df.drop(['Unnamed: 0'], axis=1, inplace=True)
        print(workspace_workspace_df)

        # Recommendation scores are obtained by multiplying the workspace-to-workspace affinity matrix
        # by the User_1 affinity vector
        rec_scores = workspace_workspace_df.values.dot(user_affinity_vector)

        # Get data_frame for User_1 Workspace recommendation scores (descending order)
        # Index equates to the workspace Id for each workspace
        data = {"User_1_Recommendations": rec_scores}
        user_1_rec = pd.DataFrame(data=data, index=workspace_workspace_df.index)
        user_1_rec.sort_values("User_1_Recommendations", ascending=False, inplace=True)
        top_10_ids = (user_1_rec.head(10).index).tolist()
        response = {"top_10_ids": top_10_ids}
        print(top_10_ids)

        return JsonResponse(response)

        #return HttpResponse(json.dumps(a), content_type='application/json')

    # If the request method is not POST, just return django index template
    else:
        template = loader.get_template('home.html')
        return HttpResponse(template.render())
        