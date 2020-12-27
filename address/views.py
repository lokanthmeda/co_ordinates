from django.shortcuts import render
import pandas as pd
import os
from geopy.geocoders import Nominatim
from django.http import HttpResponse, Http404


def home(request):
    return render(request,'data.html')

def co_ordinates(request):
    try:
        if request.method == 'POST':
            data = request.FILES['file']
            csv = pd.read_excel(data,engine='openpyxl')
            csv.to_excel("media/loku.xlsx",index=None)
            d = pd.read_excel('media/loku.xlsx', engine='openpyxl')
            d =d.fillna('')
            cols = ['address1','city','pincode']
            d['combined']=d[cols].apply(lambda row:' '.join(row.values.astype(str)),axis=1)
            try:
                for i in range(len(list(d['combined']))):
                    geolocator = Nominatim(user_agent="lokanath")
                    location = geolocator.geocode(list(d['combined'])[i])
                    d['latitude'] = location.latitude
                    d['longitude'] = location.longitude

            except:
                d['error'] = 'location not identified'
            finally:
                data = pd.DataFrame(d)
                del data['combined']
                data.to_excel('media/loku.xlsx', index=None)
    except FileNotFoundError as e:
        print(e)



    return render(request,'download.html')





def download(request):
    file_path = 'media/loku.xlsx'
    if os.path.exists(file_path):
        with open(file_path,'rb') as f:
            response = HttpResponse(f.read(),content_type='application/loku.xlsx')
            response['Content-Disposition'] = 'inline;filename='+os.path.basename(file_path)
            return response
    raise Http404



