import pytest
import ebay


def test_calculate_average_on_empty_list():
    result = ebay.calculateAverage([])
    assert result == 0.0


def test_calculate_average_on_short_list():
    sales = [3, 8]
    result = ebay.calculateAverage(sales)

    assert result == 5.5


def test_calculate_average_without_outliers():
    sales = [1, 22.75, 8.50, 8000]
    result = ebay.calculateAverage(sales)

    assert result == 15.62


def test_shipping_is_zero_on_free():
    shipping = {'shippingType': ['Free']}
    result = ebay.calculateShipping(shipping)

    assert result == 0.0


def test_shipping_where_known_is_given_as_value():
    shipping = {
        'shippingType': ['Flat'],
        'shippingServiceCost': [{'__value__' : 2.66}]}
    result = ebay.calculateShipping(shipping)

    assert result == 2.66


def test_shipping_defaults_to_calculated():
    shipping = {'shippingType': ['FlatDomesticCalculatedInternational']}
    result = ebay.calculateShipping(shipping)

    assert result == 'Calculated'


def test_total_price_calculation():
    result = ebay.calculateTotalPrice(10, 7.5)

    assert result == 17.5


def test_shrug_total_price_with_iffy_shipping():
    result = ebay.calculateTotalPrice(10, 'Calculated')

    assert result == '10+'
