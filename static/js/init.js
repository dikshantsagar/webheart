
// js
   

(function($){
  $(function(){



    

    $('.sidenav').sidenav();
    $('.dropdown-trigger').dropdown();
    $('.modal').modal();
    $('.tooltipped').tooltip();
    $('select').formSelect();

    $('.predict').click(function(){
      console.log("predict");

      var values = {
        'Syncope':0, 'Diaphoresis':0, 'Cardiogenic Shock at presentation':0,
       'Delay_To_Hospital':0, 'Anterior Wall MI':0, 'Posterior Wall MI':0,
       'Inferior Wall MI':0, 'Lateral Wall MI':0, 'LAD_0_1':0, 'LAD TIMI flow 2&3':0,
       'LAD_angiography':0, 'LCX_Angiography':0, 'LMCA_angiography':0, 'RCA_0_1':0,
       'RCA_2_3':0, 'RCA_angiography':0, 'SCAD_angiography':0, 'Female':0, 'Age':0,
       'Family_Historyof_CAD':0, 'Diabetes Mellitus':0, 'Hypertension':0,
       'Physical_Activity':0, 'Smoking_Pack_year':0, 'pre_ACE_ARB':0,
       'pre_Beta_blocker':0, 'Heart Failure at presentation ':0, 'EF_>50Percent':0,
       'Ejection Fraction 41-49%':0, 'Ejection Fraction <30%':0,
       'MR_Moderate-Severe':0, 'Creatinine':0, 'Hb':0, 'HbA1C':0, 'No PCI':0,
       'PCI_Timing <=12 hours':0
      }


      
      values.Age = Number($('#age').val());
      values.Female = Number($('#gender').prop('checked'));
      values.Syncope = Number($('#syncope').prop('checked'));
      values.Diaphoresis = Number($('#diaphoresis').prop('checked'));

      if($("#mr").val() <= 2){
        values["MR_Moderate-Severe"]= 0;

      }
      else{
        values["MR_Moderate-Severe"]= 1;
      }

      values["Heart Failure at presentation "] = Number($('#hfap').prop('checked'));
      values["Cardiogenic Shock at presentation"] = Number($('#csap').prop('checked'));
      values.Delay_To_Hospital = Number($('#delay').prop('checked'));
      

      if($('#wall').val() == 1){
        values["Anterior Wall MI"] = 1;
      }
      else if($('#wall').val() == 2){
        values["Posterior Wall MI"] = 1;
      }
      else if ($('#wall').val() == 3){
        values["Lateral Wall MI"] = 1;
      }
      else if($('#wall').val() == 4){
        values["Inferior Wall MI"] = 1;
      }

      
      if($('#angiography').val().includes('1')){
        values.LAD_angiography = 1;
      }
      if($('#angiography').val().includes('2')){
        values.LCX_Angiography = 1;
      }
      if ($('#angiography').val().includes('3')){
        values.LMCA_angiography = 1;
      }
      if($('#angiography').val().includes('4')){
        values.RCA_angiography = 1;
      }
      if($('#angiography').val().includes('5')){
        values.SCAD_angiography = 1;
      }


     if($('#timi').val() <=1 ){
       values.LAD_0_1 = 1;
     }
     else{
       values["LAD TIMI flow 2&3"] = 1;
     }

     if($('#rca').val() <=1 ){
        values.RCA_0_1 = 1;
      }
      else{
        values.RCA_2_3 = 1;
      }



     values["Diabetes Mellitus"] = Number($('#diamel').prop('checked'));
     values.Hypertension = Number($('#hyp').prop('checked'));
     values["No PCI"] = Number($('#pci').prop('checked'));
     values["PCI_Timing <=12 hours"] = Number($('#pcitime').prop('checked'));
     values.Hb = Number($('#hemoglobin').val());
     values.Creatinine = Number($('#creatinine').val());
     values.HbA1C = Number($('#hb1ac').val());
     values.Family_Historyof_CAD = Number($('#famcad').prop('checked'));
     values.Physical_Activity = Number($('#physactivity').prop('checked'));
     var cigperday = $('#cigperday').val();
     var years = $('#smokingyears').val();
     values.Smoking_Pack_year = (cigperday/20) * years;
     if($('#ejfrac').val() <= 30){
       values["Ejection Fraction <30%"] = 1;
     }
     else if($('#ejfrac').val() > 41 && $('#ejfrac').val() <= 49)
     {
       values["Ejection Fraction 41-49%"] = 1;
     }
     else if ($('#ejfrac').val() >= 50){
       values["EF_>50Percent"] = 1;
     }

     values.pre_ACE_ARB = Number($('#acearb').prop('checked'));
     values.pre_Beta_blocker = Number($('#beta').prop('checked'));

     var data = Object.values(values);
     console.log(values);
     console.log(data);

     $.ajax({
       type: "POST",
       url : "/inference",
       data: {'datainf': data.toString()},
       error: function(xhr, error){
        console.debug(xhr); console.debug(error);
         },
       success: function(resp){
        output = JSON.parse(resp).output;
        console.log(output);
        console.log("data sent successfully");
        $('#result').removeClass('hidden');
        console.log(output);
        $('#measure').css('width',(output*100).toString()+"%");
        $('#meas').html((Math.round(output*100).toString()+"%"));
        
        
       }
     });
    });

  }); // end of document ready

})(jQuery); // end of jQuery name space





