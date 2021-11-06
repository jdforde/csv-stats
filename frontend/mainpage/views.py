from django.shortcuts import render
import requests
import re


HOSTNAME = 'http://localhost:105/'
URL_REGEX = 'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'


def home(request):
    context = {}
    simple_request = True
    if not request.GET:
        return render(request, 'mainpage/home.html', context)
    parsed_request = {}

    for item in request.GET.dict():
        if request.GET[item]:
            parsed_request[item] = request.GET[item]

    if 'stats-option' in parsed_request:
        simple_request = False
        context['stats_option'] = parsed_request['stats-option']
        context['csv_site'] = parsed_request['csv-site']
        endpoint = HOSTNAME + "compute_stats/?url=" + parsed_request['csv-site'] + "&numerical_category=" + parsed_request['stats-option']
        try:
            endpoint_response = requests.get(endpoint).json()
            
            if endpoint_response['status_code'] == 0:
                context.update(endpoint_response)
                context['numerical_categories'] = context['numerical_categories'].replace('"', '').replace('[', '').replace(']', '').split(",")
                context['all_categories']= context['all_categories'].replace('"', '').replace('[', '').replace(']', '').split(",")
            else:
                context['status_code'] = 3
        except:
            context['status_code'] = 6
    
    if 'avg-option-1' in parsed_request and 'avg-option-2' in parsed_request and 'avg-option-3' in parsed_request and 'avg-option-4' in parsed_request:
        simple_request = False
        context['csv_site'] = parsed_request['csv-site']
        context['avg_option_1'] = parsed_request['avg-option-1']
        context['avg_option_2'] = parsed_request['avg-option-2']
        context['avg_option_3'] = parsed_request['avg-option-3']
        context['avg_option_4'] = parsed_request['avg-option-4']
        if (not context['avg_option_3'] == '==' and not context['avg_option_4'].isdigit()):
            context['status_code'] = 5
        else:
            try:
                endpoint = HOSTNAME + "compute_avg_cond?url=" + context['csv_site'] + "&numerical_category=" + parsed_request['avg-option-1'] + "&any_category=" + parsed_request['avg-option-2'] + "&comparison=" + parsed_request['avg-option-3'] + "&value=" + parsed_request['avg-option-4']
                endpoint_response = requests.get(endpoint).json()
                if (endpoint_response['status_code'] == 0):
                    context.update(endpoint_response)
                    context['numerical_categories'] = context['numerical_categories'].replace('"', '').replace('[', '').replace(']', '').split(",")
                    context['all_categories']= context['all_categories'].replace('"', '').replace('[', '').replace(']', '').split(",")
                    
                else: 
                    context['status_code'] = 4
            except:
                context['status_code'] = 6

    if 'csv-site' in parsed_request and simple_request:
        context['csv_site'] = parsed_request['csv-site']
        if re.match(URL_REGEX, context['csv_site']) and context['csv_site'].endswith('.csv'):
                endpoint = HOSTNAME + "parse_csv/?url=" + context['csv_site']
                try:
                    endpoint_response= requests.get(endpoint).json()
                    if (endpoint_response['status_code'] == 0):
                        context.update(endpoint_response)
                        context['numerical_categories'] = context['numerical_categories'].replace('"', '').replace('[', '').replace(']', '').split(",")
                        context['all_categories']= context['all_categories'].replace('"', '').replace('[', '').replace(']', '').split(",")
                    else:
                        context['status_code'] = endpoint_response['status_code']
                except:
                    context['status_code'] = 6
        else:
            context['status_code'] = 2

    return render(request, 'mainpage/home.html', context)
