import iso8601
import logging
import os
import requests
import yaml


logger = logging.getLogger(__name__)


def calculate_shipping(shipping):
    if shipping['shippingType'][0] == 'Free':
        return 0.0
    elif 'shippingServiceCost' in shipping:
        return float(shipping['shippingServiceCost'][0]['__value__'])
    else:
        return 'Calculated'


def calculate_total_price(sold_price, shipping_cost):
    if type(shipping_cost) is float:
        return round(float(sold_price) + float(shipping_cost), 2)
    else:
        return str(sold_price) + '+'


def clean_up_results(results):
    items = []

    for item in results:
        shipping_cost = calculate_shipping(item['shippingInfo'][0])
        sold_price = item['sellingStatus'][0]['currentPrice'][0]['__value__']

        items.append({
            'title': item['title'][0],
            'url': item['viewItemURL'][0] + '?nordt=true&orig_cvip=true',
            'image': extract_image(item),
            'soldPrice': sold_price,
            'soldCurrency': item['sellingStatus'][0]['currentPrice'][0]['@currencyId'],
            'shipping': shipping_cost,
            'totalPrice': calculate_total_price(sold_price, shipping_cost),
            'endDate': convert_end_time(item['listingInfo'][0]['endTime'][0]),
            'condition': convert_condition(item)
            })

    return items


def convert_condition(item):
    if 'condition' in item and 'conditionDisplayName' in item['condition'][0]:
        return item['condition'][0]['conditionDisplayName'][0]
    else:
        return '--'


def convert_end_time(timestamp):
    end_time = iso8601.parse_date(timestamp)
    return end_time.date()


def create_results_lookup(search_response):
    result_count = search_response['@count']
    results = {'matches': result_count}

    if (int(result_count) > 0):
        items = clean_up_results(search_response['item'])
        results['products'] = items

    return results


def extract_error_message(search_response):
    if 'errorMessage' in search_response:
        return search_response['errorMessage'][0]['error'][0]['message'][0]
    else:
        None


def extract_image(search_response):
    if 'galleryURL' in search_response:
        return search_response['galleryURL'][0]
    else:
        None


def load_config():
    try:
        current_file_directory = os.path.dirname(os.path.abspath(__file__))
        config_file = open(current_file_directory + "/config.yml")
    except FileNotFoundError:
        logger.error("! config.yml is missing. Copy from config.yml.example")

        return None

    with config_file:
        return yaml.safe_load(config_file)


def search_sold(keyword):
    config = load_config()

    if config is None:
        return {'error': 'Configuration file is missing'}

    r = requests.get(config['base_url'] + '/services/search/'
                     'FindingService/v1?OPERATION-NAME=findCompletedItems&'
                     'SERVICE-NAME=FindingService&'
                     'SERVICE-VERSION=1.0.0&GLOBAL-ID=EBAY-US&'
                     'SECURITY-APPNAME=' + config['client_id'] + '&'
                     'RESPONSE-DATA-FORMAT=JSON&REST-PAYLOAD&'
                     'sortOrder=EndTimeSoonest&'
                     'keywords=' + keyword + '&'
                     'itemFilter(0).name=SoldItemsOnly&'
                     'itemFilter(0).value=true')

    response = r.json()

    if 'errorMessage' in response:
        return {
            'error': extract_error_message(response),
            'matches': '0'
        }
    else:
        return process_sold_results(response)


def process_sold_results(json):
    search_response = json['findCompletedItemsResponse'][0]

    if search_response['ack'][0] == 'Success':
        results = create_results_lookup(search_response['searchResult'][0])
    else:
        results = {'error': extract_error_message(search_response)}

    return results
