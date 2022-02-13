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
import matplotlib.pyplot as plt



@csrf_exempt
def home(request):
    with open('static/models/counter.dat','rb') as f:
        count = pickle.load(f)[0]

    with open('static/models/counter.dat','wb') as f:
        pickle.dump([count+1],f)
        
    return render(request,'index.html', {'visits': count})
    #clearreturn render(request,'down.html')



def runmodel(request):

    return request



@csrf_exempt
def inference(request):

    if request.method == 'POST':
        
        data = request.POST['datainf']
        data = data.split(',')
        data = list(map(float, data))
        data = np.asarray(data)
        data = data.reshape((1,32))
       #print(data)
        extra_tree_forest = ExtraTreesClassifier(n_estimators=100,
                                            criterion="entropy",
                                            max_depth=None,
                                            min_samples_split=4,
                                            min_samples_leaf=2,
                                            min_weight_fraction_leaf=0.01,
                                            max_features='auto',
                                            min_impurity_decrease=0.0,
                                            bootstrap=False,
                                            oob_score=False,
                                            random_state=7,
                                            verbose=0,
                                            class_weight={0: 1, 1: 1},
                                            warm_start=False,
                                            ccp_alpha=0.01,
                                            max_samples=None,)
        
        filename = 'static/models/ET_Jan2022.sav'
        model = pickle.load(open(filename,'rb'))
        print('model loaded succesfully')
        
        output = model.predict_proba(data)
        print("mortality",output)
        V_data = pd.read_excel("static/data/test.xlsx")
        validation_data = V_data.copy()

        
        validation_data.rename(columns={'30_days_Mortality':"mortality",'pre_Beta_blocker':"Pre-treatment (beta-blockers)",
                                'MR_mild':'mild MR','LAD_0_1':'TIMI flow grade 0-1 in LAD','RCA_0_1':'TIMI flow grade 0-1 in RCA'
                                ,'RCA_2_3':'TIMI flow grade 2-3 in RCA','EF_>50Percent': 'LVEF >50%',
                                'Physical_Activity':'Physical Activity',
                                'Sex_1e0ale':"Gender",'initial_creatinine_val':"Serum Creatinine", 
                                'PCI_1t_done':'Medical Therapy without PCI','Age_group':"Age < 40 years",'EF_<30Percent':'LVEF<30%',
                               'LAD_2_3':'TIMI flow grade 2-3 in LAD', 'CardiacStatus_Presentation_HF':'Heart Failure at presentation ',
                               'Presentation_Cardiogenic shock ':'Cardiogenic Shock at presentation',
                                'Delay_To_Hospital':"Delayed Presentation",
                                'pre_ACE_ARB':"Pre-treatment (ACEi/ARBs)",'Smoking_Pack_year':"Smokimg (pack-year)",
                                'MR_Moderate-Severe':"Moderate-severe MR",
                                'PCI_Timing <=12 hours':"PCI performed within 12 hours",
                                  'initial_hb_value':'Hemoglobin','pre_Diabetes_Mellitus':'Diabetes Mellitus',
                                'initial_hg_baic':'HbA1C',
                                'EF_41-49Percent':'LVEF 41-49%','pre_Hypertension':'Hypertension'}, inplace=True)



        #'EF_31-40Percent', 'PCI_Timing>72hours','Pre_PCI_TIMI_Grade','Inferior Wall MI', 'Lateral Wall MI' 'LAD_angiography', 
        #'LCX_Angiography', 'LMCA_angiography', 'RCA_angiography',
        validation_data = validation_data.drop(['patient_UID', 'pre_CVA', 'Chest pain',
       'pre_Hyperlipidemia', 'pre_ASPIRIN', 'pre_STATIN','mild MR','Anticoagulant_UFH',
       'pre_Anticoagulant', 'Patient/Relative unwillingness','PCI_Timing>72hours','EF_31-40Percent','Shortness of breath',
       'Transient resolution of Sx', 'Misinterpretation of Sx', 'DAPT_therapy',  'AtH_Anticoagulant_LMWH',
                                        'pre_P2Y12_Inhibitors','total occusion','AtH_Tirofiban',
                                        'pre_Atrial_fib_flutter','pre_HeartFailure','Time_to_1st_ECG >6hours',
                                       'pre_INSULIN','LAD_angiography', 'LCX_Angiography',
                                        'LMCA_angiography','RCA_angiography', 'SCAD_angiography'], axis=1)
        
        
        X_unseen = validation_data.drop(labels=['mortality'], axis=1)
        # y_unseen = validation_data['mortality']

        explainer = lime_tabular.LimeTabularExplainer(
                        training_data=np.array(X_unseen),
                        feature_names=X_unseen.columns,
                        class_names=['Alive', 'Mortality'],
                        mode='classification')
        
        
        exp = explainer.explain_instance(
                    data_row=data.reshape((32,)), 
                    predict_fn=model.predict_proba)
        
        exp.save_to_file('static/data/explain.html')
        import shap
        from shap import Explanation
        #print(shap.__version__)
        explainer = shap.TreeExplainer(model)
        shap_values = explainer.shap_values(data)
        shap.force_plot(explainer.expected_value[1], shap_values[1], features=data, feature_names=list(X_unseen.columns),matplotlib=True)
        plt.savefig('static/data/shap.png', format = "png",dpi = 600,max_display=50, bbox_inches = 'tight')
        # shap.waterfall_plot(Explanation(shap_values[1], explainer.expected_value[1],feature_names=X_unseen.columns), show=False)
        # plt.savefig('static/data/shap_w.png', format = "png",dpi = 300,max_display=50, bbox_inches = 'tight')


        

    return HttpResponse(json.dumps(dict({'output':output.tolist()[0][1]})))




def insight(request):

    return redirect('static/data/explain.html')

def shap(request):
    return redirect('static/data/shap.html')