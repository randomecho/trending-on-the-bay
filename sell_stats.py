def calculate_average(sale_prices):
    if len(sale_prices) == 0:
        return 0.0

    if len(sale_prices) > 2:
        average_sales = float((sum(sale_prices) - min(sale_prices) - max(sale_prices)) / (len(sale_prices) - 2))
    else:
        average_sales = float(sum(sale_prices) / len(sale_prices))

    return round(average_sales, 2)


def generate_stats(items):
    if 'products' not in items or len(items['products']) == 0:
        return

    total_price = []
    total_price_new = []
    total_price_other = []

    for item in items['products']:
        if type(item['shipping']) is float and item['soldCurrency'] == 'USD':
            total_price.append(item['totalPrice'])

            if "new" in item['condition'].lower():
                total_price_new.append(item['totalPrice'])
            else:
                total_price_other.append(item['totalPrice'])

    stats = {
        'average': calculate_average(total_price),
        'average_new': calculate_average(total_price_new),
        'average_other': calculate_average(total_price_other),
        'highest': max(total_price, default=0),
        'highest_new': max(total_price_new, default=0),
        'highest_other': max(total_price_other, default=0),
        'lowest': min(total_price, default=0),
        'lowest_new': min(total_price_new, default=0),
        'lowest_other': min(total_price_other, default=0)
        }

    return stats


