import pytest
import ebay


def test_calculate_average_on_empty_list():
    result = ebay.calculate_average([])
    assert result == 0.0


def test_calculate_average_on_short_list():
    sales = [3, 8]
    result = ebay.calculate_average(sales)

    assert result == 5.5


def test_calculate_average_without_outliers():
    sales = [1, 22.75, 8.50, 8000]
    result = ebay.calculate_average(sales)

    assert result == 15.62


def test_shipping_is_zero_on_free():
    shipping = {'shippingType': ['Free']}
    result = ebay.calculate_shipping(shipping)

    assert result == 0.0


def test_shipping_where_known_is_given_as_value():
    shipping = {
        'shippingType': ['Flat'],
        'shippingServiceCost': [{'__value__' : 2.66}]}
    result = ebay.calculate_shipping(shipping)

    assert result == 2.66


def test_shipping_defaults_to_calculated():
    shipping = {'shippingType': ['FlatDomesticCalculatedInternational']}
    result = ebay.calculate_shipping(shipping)

    assert result == 'Calculated'


def test_total_price_calculation():
    result = ebay.calculate_total_price(10, 7.5)

    assert result == 17.5


def test_shrug_total_price_with_iffy_shipping():
    result = ebay.calculate_total_price(10, 'Calculated')

    assert result == '10+'


def test_render_condition_name_from_json():
    item = {'condition': [{'conditionDisplayName': ['New with tags']}]}
    result = ebay.convert_condition(item)

    assert result == 'New with tags'


def test_get_dashes_on_missing_condition():
    result = ebay.convert_condition({})

    assert result == '--'


def test_converting_timedate_to_date():
    result = ebay.convert_end_time('2000-09-15T18:00:36.000Z')

    assert format(result, '%Y-%m-%d') == '2000-09-15'


def test_extracting_error_message_from_api_json():
    response = {'errorMessage': [{'error': [{'message': ['No persimmons left']}]}]}
    result = ebay.extract_error_message(response)

    assert result == 'No persimmons left'


def test_extracting_error_message_from_api_json():
    response = {'mehMessage': 'The lychees are on sale again'}
    result = ebay.extract_error_message(response)

    assert result is None


def test_create_results_with_zero_matches():
    result = ebay.create_results_lookup({'@count': 0})

    assert result['matches'] == 0
