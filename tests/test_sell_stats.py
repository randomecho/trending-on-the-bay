import pytest
import sell_stats


def test_get_nothing_on_empty_results():
    result = sell_stats.generate_stats([])

    assert result is None


def test_calculate_average_on_empty_list():
    result = sell_stats.calculate_average([])

    assert result == 0.0


def test_calculate_average_on_short_list():
    sales = [3, 8]
    result = sell_stats.calculate_average(sales)

    assert result == 5.5


def test_calculate_average_without_outliers():
    sales = [1, 22.75, 8.50, 8000]
    result = sell_stats.calculate_average(sales)

    assert result == 15.62
