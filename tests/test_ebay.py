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
