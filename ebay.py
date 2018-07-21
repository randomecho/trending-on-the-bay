import iso8601
import requests
import yaml


config = yaml.safe_load(open("config.yml"))


def calculateShipping(shipping):
    if shipping['shippingType'][0] == 'Free':
        return 0.0
    elif 'shippingServiceCost' in shipping:
        return float(shipping['shippingServiceCost'][0]['__value__'])
    else:
        return 'Calculated'


def calculateTotalPrice(sold_price, shipping_cost):
    if type(shipping_cost) is float:
        return round(float(sold_price) + float(shipping_cost), 2)
    else:
        return sold_price + '+'


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
            'endDate': convertEndTime(item['listingInfo'][0]['endTime'][0]),
            'condition': convertCondition(item)
            })

    return items


def convertCondition(item):
    if 'condition' in item and 'conditionDisplayName' in item['condition'][0]:
        return item['condition'][0]['conditionDisplayName'][0]
    else:
        return '--'


def convertEndTime(timestamp):
    end_time = iso8601.parse_date(timestamp)
    return end_time.date()


def generateStatistics(items):
    total_price = []
    total_price_new = []
    total_price_other = []
    average_sale_price = 0
    average_new_price = 0
    average_other_price = 0

    for item in items:
        if type(item['shipping']) is float and item['soldCurrency'] == 'USD':
            total_price.append(item['totalPrice'])

            if "new" in item['condition'].lower():
                total_price_new.append(item['totalPrice'])
            else:
                total_price_other.append(item['totalPrice'])

    if len(total_price) > 0:
        if len(total_price) > 2:
            average_sale_price = round(float((sum(total_price) - min(total_price) - max(total_price))/ (len(total_price) - 2)), 2)
        else:
            average_sale_price = round(float(sum(total_price) / len(total_price)), 2)

    if len(total_price_new) > 0:
        if len(total_price_new) > 2:
            average_new_price = round(float((sum(total_price_new) - min(total_price_new) - max(total_price_new))/ (len(total_price_new) - 2)), 2)
        else:
            average_new_price = round(float(sum(total_price_new) / len(total_price_new)), 2)

    if len(total_price_other) > 0:
        if len(total_price_new) > 2:
            average_other_price = round(float((sum(total_price_other) - min(total_price_other) - max(total_price_other))/ (len(total_price_other) - 2)), 2)
        else:
            average_other_price = round(float(sum(total_price_other) / len(total_price_other)), 2)

    stats = {
        'average': average_sale_price,
        'average_new': average_new_price,
        'average_other': average_other_price,
        'highest': max(total_price),
        'lowest': min(total_price)
        }

    return stats


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
            items = cleanUpResults(searchResponse['searchResult'][0]['item'])
            results['products'] = items
            results['stats'] = generateStatistics(items)
    else:
        results = {'error': searchResponse['errorMessage'][0]['error'][0]['message'][0]}

    return results
