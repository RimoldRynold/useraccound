from django.shortcuts import render,HttpResponse
from .models import *


mappings = {
    ' eq ': ' = ',
    ' ne ': ' != ',
    ' gt ': ' > ',
    ' lt ': ' < ',
    ' gte ': ' >= ',
    ' lte ': ' <= ',
}

def home(request):
    # q_string = "(date eq '2021-12-05') AND ((distance gt 20) OR (distance lt 10))"
    q_string = "(name ne 'amit') AND (roll gt 20 OR roll lt 10)"

    
    for expression, operation in mappings.items():
        q_string = q_string.replace(expression, operation)
    print(q_string) 
    #expected output -> q_string = (date = '2021-12-05') AND ((distance > 20) OR (distance < 10))
    model_datas = Mymodel.objects.raw('SELECT * FROM app1_mymodel WHERE ' + q_string)
    for data in model_datas:
        print(data)
        #also we can use object.field_name to get a specific field value
        #eg.  data.time or data.distance
        
 
    return HttpResponse('some response')