from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
import pickle
import numpy as np
import json
import glob
from sklearn.ensemble import ExtraTreesClassifier

def home(request):
    return render(request,'index.html')



def runmodel(request):

    return request



@csrf_exempt
def inference(request):

    if request.method == 'POST':
        
        data = request.POST['datainf']
        data = data.split(',')
        data = list(map(float, data))
        data = np.asarray(data)
        data = data.reshape((1,36))
       #print(data)
        extra_tree_forest = ExtraTreesClassifier(n_estimators=100,
                                            criterion="entropy",
                                            max_depth=None,
                                            min_samples_split=4,
                                            min_samples_leaf=2,
                                            min_weight_fraction_leaf=0.01,
                                            max_features='auto',
                                            max_leaf_nodes=None,
                                            min_impurity_decrease=0.0,
                                            min_impurity_split=None,
                                            bootstrap=False,
                                            oob_score=False,
                                            random_state=7,
                                            verbose=0,
                                            class_weight={0: 1, 1: 1},
                                            warm_start=False,
                                            ccp_alpha=0.01,
                                            max_samples=None,)
        
        filename = 'static/models/ET_for_web_app.sav'
        model = pickle.load(open(filename,'rb'))
        print('model loaded succesfully')
        
        output = model.predict_proba(data)
        print("mortality",)

        

    return HttpResponse(json.dumps(dict({'output':output.tolist()[0][0]})))

