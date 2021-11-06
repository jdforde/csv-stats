from flask import Flask, request
import requests, pandas as pd, json, numpy as np 
import io

app = Flask(__name__) #Create an instance of the class

#Helper functions, not routes
def get_categories(csv):
    categories = [item for item in csv.columns.values.tolist() if 'Unnamed' not in item]

    numerical_categories = categories.copy()

    for item in numerical_categories[:]:
        numeric_row = pd.to_numeric(csv[item], errors='coerce').dropna()
        if numeric_row.size > 0:
            continue

        if not csv[item].dtype.kind in 'iuf':
            numerical_categories.remove(item)
    
    return categories, numerical_categories

def get_csv(url):
    req = requests.get(url)

    #We are able to parse csv files separated by comma and by semicolon
    try:
        csv = pd.read_csv(io.StringIO(req.text))
    except pd.errors.ParserError:
        csv = pd.read_csv(io.StringIO(req.text), sep=';')
    
    return csv


# http://localhost:105/parse_csv/?url=<csv_site>
@app.route('/parse_csv/') 
def parse_csv():

    returnable = {
        'status_code' : 1,
        'url' : '',
        'numerical_categories' : '',
        'all_categories' : ''
    }

    if 'url' in request.args:
        csv = get_csv(request.args['url'])

        categories, numerical_categories = get_categories(csv)

        if numerical_categories and categories:
            returnable['status_code'] = 0
        else:
            returnable['status_code'] = 1

        returnable['numerical_categories'] = json.dumps(numerical_categories)
        returnable['all_categories'] = json.dumps(categories)
        returnable['url'] = request.args['url']

    return returnable
    
# http://localhost:105/compute_stats/?url=<csv_site>&numerical_category=<category>
@app.route('/compute_stats/')
def compute_stats():

    returnable = {
        'status_code' : 3,
        'Max' : None,
        'Min' : None,
        'Range': None,
        'Mean': None,
        'all_categories': '',
        'numerical_categories': ''
    }

    if 'url' in request.args and 'numerical_category' in request.args:
        numerical_category = request.args['numerical_category']
        csv = get_csv(request.args['url'])

        csv[numerical_category] = pd.to_numeric(csv[numerical_category], errors='coerce').dropna()
        returnable['Max'] = float(np.amax(csv[numerical_category]))
        returnable['Min'] = float(np.amin(csv[numerical_category]))
        returnable['Range'] = returnable['Max'] - returnable['Min']
        returnable['Mean'] = float(np.mean(csv[numerical_category]))

        if not np.isnan(returnable['Max']) or not np.isnan(returnable['Min']) or not np.isnan(returnable['Range']) or not np.isnan(returnable['Mean']):
            returnable['status_code'] = 0
        
        categories, numerical_categories = get_categories(csv)
        
        returnable['numerical_categories'] = json.dumps(numerical_categories)
        returnable['all_categories'] = json.dumps(categories)

    return returnable

#http://localhost:105/compute_avg_cond/?url=<csv_site>&numerical_category=<category1>&any_category=<category2>&comparison=<comparison>&value=<value>
@app.route('/compute_avg_cond/')
def compute_avg_cond():
    returnable = {
        'status_code' : 4,
        'Avg' : None,
        'all_categories' : '',
        'numerical_categories' : ''
    }
    if 'url' in request.args and 'numerical_category' in request.args and 'any_category' in request.args and 'comparison' in request.args and 'value' in request.args:
        value = request.args['value']
        numerical_category = request.args['numerical_category']
        any_category = request.args['any_category']
        comparison = request.args['comparison']
        
        csv = get_csv(request.args['url'])

        #Three options for condition

        if comparison == '==':
            condition = (csv[any_category] == value)
        elif comparison == '<': 
            condition =  pd.to_numeric(csv[any_category], errors='coerce') < float(value)
        elif comparison == '>': 
            condition = pd.to_numeric(csv[any_category], errors='coerce') > float(value)
        

        result = csv[condition]
        returnable['Avg'] = np.mean(pd.to_numeric(result[numerical_category], errors='coerce').dropna())


        if returnable['Avg']:
            if not np.isnan(returnable['Avg']):
                returnable['status_code'] = 0
            else:
                returnable['status_code'] = 6
        
        categories, numerical_categories = get_categories(csv)
        
        returnable['numerical_categories'] = json.dumps(numerical_categories)
        returnable['all_categories'] = json.dumps(categories)



    return returnable


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=105)