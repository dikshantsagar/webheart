from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
import pickle
import numpy as np
import pandas as pd
import json
import glob
from sklearn.ensemble import ExtraTreesClassifier
import lime
from lime import lime_tabular

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
        V_data = pd.read_excel("static/data/test.xlsx")
        validation_data = V_data.copy()

        
        validation_data.rename(columns={'30_days_Mortality':'mortality','Sex_1e0ale':"Female",'initial_creatinine_val':"Creatinine",
                                        'PCI_1t_done':'No PCI','Age_group':"Age < 40",'EF_<30Percent':'Ejection Fraction <30%',
                                    'LAD_2_3':'LAD TIMI flow 2&3','CardiacStatus_Presentation_HF':'Heart Failure at presentation ',
                                        'Presentation_Cardiogenic shock ':'Cardiogenic Shock at presentation','initial_hb_value':'Hb',
                                    'pre_Diabetes_Mellitus':'Diabetes Mellitus','pre_Hypertension':'Hypertension',
                                        'initial_hg_baic':'HbA1C',
                                    'EF_41-49Percent':'Ejection Fraction 41-49%'}, inplace=True)



        #'EF_31-40Percent', 'PCI_Timing>72hours','Pre_PCI_TIMI_Grade','Inferior Wall MI', 'Lateral Wall MI' 'LAD_angiography', 
        #'LCX_Angiography', 'LMCA_angiography', 'RCA_angiography',
        validation_data = validation_data.drop(['patient_UID', 'pre_CVA', 'Chest pain',
            'pre_Hyperlipidemia', 'pre_ASPIRIN', 'pre_STATIN','MR_mild','Anticoagulant_UFH',
            'pre_Anticoagulant', 'Patient/Relative unwillingness','PCI_Timing>72hours','EF_31-40Percent','Shortness of breath',
            'Transient resolution of Sx', 'Misinterpretation of Sx', 'DAPT_therapy',  'AtH_Anticoagulant_LMWH','pre_P2Y12_Inhibitors','total occusion','Age < 40','AtH_Tirofiban',
                                                'pre_Atrial_fib_flutter','pre_HeartFailure','Time_to_1st_ECG >6hours',
                                            'pre_INSULIN'
        ], axis=1)
        
        X_unseen = validation_data.drop(labels=['mortality'], axis=1)
        y_unseen = validation_data['mortality']

        explainer = lime_tabular.LimeTabularExplainer(
                        training_data=np.array(X_unseen),
                        feature_names=X_unseen.columns,
                        class_names=['Alive', 'Mortality'],
                        mode='classification')
        
        #print(data.shape)
        exp = explainer.explain_instance(
                    data_row=data.reshape((36,)), 
                    predict_fn=model.predict_proba)
        
        exp.save_to_file('static/data/explain.html')

        

    return HttpResponse(json.dumps(dict({'output':output.tolist()[0][1]})))




def insight(request):

    return redirect('static/data/explain.html')
