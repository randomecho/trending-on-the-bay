import requests
import yaml


config = yaml.safe_load(open("config.yml"))


def calculateShipping(shipping):
    if shipping['shippingType'][0] == 'Free':
        return 0
    elif 'shippingServiceCost' in shipping:
        return shipping['shippingServiceCost'][0]['__value__']
    else:
        return shipping['shippingType'][0]


def calculateTotalPrice(sold_price, shipping_cost):
    if shipping_cost == 'Calculated':
        return sold_price + '+'
    else:
        return round(float(sold_price) + float(shipping_cost), 2)


def cleanUpResults(results):
    items = []

    for item in results:
        shipping_cost = calculateShipping(item['shippingInfo'][0])
        sold_price = item['sellingStatus'][0]['currentPrice'][0]['__value__']

        items.append({
            'title': item['title'][0],
            'soldPrice': sold_price,
            'soldCurrency': item['sellingStatus'][0]['currentPrice'][0]['@currencyId'],
            'shipping': shipping_cost,
            'totalPrice': calculateTotalPrice(sold_price, shipping_cost),
            'condition': convertCondition(item)
            })

    return items


def convertCondition(item):
    if 'condition' in item and 'conditionDisplayName' in item['condition'][0]:
        return item['condition'][0]['conditionDisplayName'][0]
    else:
        return 'Unknown'


def searchSold(keyword):
    r = requests.get(config['base_url'] + '/services/search/' \
        'FindingService/v1?OPERATION-NAME=findCompletedItems&' \
        'SERVICE-NAME=FindingService&' \
        'SERVICE-VERSION=1.0.0&GLOBAL-ID=EBAY-US&' \
        'SECURITY-APPNAME=' + config['client_id'] + \
        '&RESPONSE-DATA-FORMAT=JSON&REST-PAYLOAD&' \
        'sortOrder=EndTimeSoonest&' \
        'keywords=' + keyword + \
        '&itemFilter(0).name=SoldItemsOnly&itemFilter(0).value=true')

    return processSoldResults(r.json())

def processSoldResults(json):
    searchResponse = json['findCompletedItemsResponse'][0]

    if searchResponse['ack'][0] == 'Success':
        resultCount = searchResponse['searchResult'][0]['@count']
        results = {'matches': resultCount}

        if (int(resultCount) > 0):
            results['products'] = cleanUpResults(searchResponse['searchResult'][0]['item'])
    else:
        results = {'error': searchResponse['errorMessage'][0]['error'][0]['message'][0]}

    return results
