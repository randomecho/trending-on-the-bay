import requests
import yaml


config = yaml.safe_load(open("config.yml"))


def searchSold(keyword):
    r = requests.get(config['base_url'] + '/services/search/' \
        'FindingService/v1?OPERATION-NAME=findCompletedItems&' \
        'SERVICE-NAME=FindingService&' \
        'SERVICE-VERSION=1.0.0&GLOBAL-ID=EBAY-US&' \
        'SECURITY-APPNAME=' + config['client_id'] + \
        '&RESPONSE-DATA-FORMAT=JSON&REST-PAYLOAD&' \
        'keywords=' + keyword + \
        '&itemFilter(0).name=SoldItemsOnly&itemFilter(0).value=true')

    return processSoldResults(r.json())

def processSoldResults(json):
    if json['findCompletedItemsResponse'][0]['ack'][0] == 'Success':
        resultCount = json['findCompletedItemsResponse'][0]['searchResult'][0]['@count']
        results = {'matches': resultCount}

        if (int(resultCount) > 0):
            results['products'] = json['findCompletedItemsResponse'][0]['searchResult'][0]['item']
    else:
        results = {'error': json['findCompletedItemsResponse'][0]['errorMessage'][0]['error'][0]['message'][0]}

    return results
