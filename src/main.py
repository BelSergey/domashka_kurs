from src.masks import get_mask_account, get_mask_card_number

card = input("Введите номер карты: ")
account = input("Введите номер счёта: ")

masked_card = get_mask_card_number(card)
print(f"Карта: {masked_card}")
masked_account = get_mask_account(account)
print(f"Маска: {masked_account}")
