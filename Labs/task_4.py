def read_input_from_file(filename):
    with open(filename, 'r') as file:
        participants = file.readline().strip().split()

        n = int(file.readline())
        expenses = {name: 0 for name in participants}
        for _ in range(n):
            name, amount = file.readline().strip().split()
            expenses[name] += int(amount)

    return participants, expenses


def calculate_transfers(participants, expenses):
    total = sum(expenses.values())
    average = total / len(participants)

    balances = {}
    for name in participants:
        balance = expenses[name] - average
        if abs(balance) > 0.001:
            balances[name] = balance

    debtors = [(name, -balance) for name, balance in balances.items() if balance < -0.001]
    creditors = [(name, balance) for name, balance in balances.items() if balance > 0.001]

    transfers = []

    while debtors and creditors:
        debtors.sort(key=lambda x: x[1], reverse=True)
        creditors.sort(key=lambda x: x[1], reverse=True)
        
        debtor_name, debt_amount = debtors[0]
        creditor_name, credit_amount = creditors[0]
        
        transfer_amount = min(debt_amount, credit_amount)
        
        if transfer_amount > 0.001:
            transfers.append((debtor_name, creditor_name, round(transfer_amount, 2)))
        
        new_debt = debt_amount - transfer_amount
        new_credit = credit_amount - transfer_amount
        
        debtors[0] = (debtor_name, new_debt)
        creditors[0] = (creditor_name, new_credit)
        
        if new_debt < 0.001:
            debtors.pop(0)
        if new_credit < 0.001:
            creditors.pop(0)

    return transfers


def main():
    try:
        participants, expenses = read_input_from_file('friends.txt')
    except FileNotFoundError:
        print("Файл friends.txt не найден!")
        return
    except Exception as e:
        print(f"Ошибка при чтении файла: {e}")
        return

    transfers = calculate_transfers(participants, expenses)

    print(len(transfers))
    for transfer in transfers:
        print(f"{transfer[0]} {transfer[1]} {transfer[2]:.2f}")


if __name__ == "__main__":
    main()