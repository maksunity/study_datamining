with open('mbox.txt', 'r') as file:
    lines = file.readlines()

auth_dict = {}

for line in lines:
    if line.startswith('From '):
        parts = line.split()
        if len(parts) > 1:
            email = parts[1]
            if email in auth_dict:
                auth_dict[email] += 1
            else:
                auth_dict[email] = 1

if auth_dict:
    max_author = max(auth_dict, key=auth_dict.get)
    max_count = auth_dict[max_author]
    print(f"Автор с наибольшим количеством писем: {max_author}, количество писем: {max_count}")
else:
    print("Авторы не найдены.")