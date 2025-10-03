from datetime import datetime


def parse_date(date_str):
    for fmt in ['%d.%m.%Y', '%d/%m/%Y']:
        try:
            return datetime.strptime(date_str, fmt).date()
        except ValueError:
            continue
    return None


def parse_price(price_str):
    try:
        return float(price_str.replace(',', '.'))
    except ValueError:
        return None


def parse_order_line(line):
    line = line.strip()
    if not line:
        return None
    
    separators = [' ', ',', ';']
    parts = []
    
    for sep in separators:
        if sep in line:
            parts = [p.strip() for p in line.split(sep) if p.strip()]
            break
    
    if not parts or len(parts) < 3:
        return None

    date = None
    name_parts = []
    price = None

    for i, part in enumerate(parts):
        d = parse_date(part)
        if d:
            date = d
            parts.pop(i)
            break

    if not date:
        return None

    for i in range(len(parts) - 1, -1, -1):
        p = parse_price(parts[i])
        if p is not None:
            price = p
            parts.pop(i)
            break

    if price is None:
        return None

    name = ' '.join(parts).strip('"\'')
    
    if date and name and price is not None:
        return date, name, price
    return None

def process_orders(filename):
    pizza_counts = {}
    date_totals = {}
    max_order = None
    total_orders = 0
    total_price = 0.0

    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            order = parse_order_line(line)
            if not order:
                continue

            date, name, price = order

            pizza_counts[name] = pizza_counts.get(name, 0) + 1

            date_totals[date] = date_totals.get(date, 0.0) + price

            if max_order is None or price > max_order[2]:
                max_order = (date, name, price)

            total_orders += 1
            total_price += price

    return {
        'pizza_counts': pizza_counts,
        'date_totals': date_totals,
        'max_order': max_order,
        'total_orders': total_orders,
        'total_price': total_price
    }


def print_statistics(stats):
    #Список пицц по популярности
    print("а) Список пицц по популярности:")
    for name, count in sorted(stats['pizza_counts'].items(), key=lambda x: (-x[1], x[0])):
        print(f"{name} - {count}")

    #Суммарная стоимость по дням
    print("\nб) Суммарная стоимость по дням:")
    for date, total in sorted(stats['date_totals'].items()):
        print(f"{date.strftime('%d.%m.%Y')} {total:.2f}")

    #Самый дорогой заказ
    if stats['max_order']:
        date, name, price = stats['max_order']
        print(f"\nв) {date.strftime('%d.%m.%Y')} {name} {price:.2f}")

    #Средняя стоимость заказа
    if stats['total_orders'] > 0:
        avg = stats['total_price'] / stats['total_orders']
        print(f"\nг) {avg:.2f}")


def main():
    filename = "pizza.txt"
    # filename = "Lab01_task3_input.txt"
    try:
        stats = process_orders(filename)
        print_statistics(stats)
    except FileNotFoundError:
        print("Файл не найден!")
    except Exception as e:
        print(f"Ошибка: {e}")


if __name__ == "__main__":
    main()