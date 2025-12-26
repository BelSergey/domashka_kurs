from masks import get_mask_account, get_mask_card_number

def mask_account_card(incoming_string: str) -> str:
    """" Функция обрабатывает информацию о картах и счетах"""
    output_string = ""
    incoming_string=incoming_string.split(" ")
    if incoming_string[0] == "Visa" or incoming_string == "Maestro" or incoming_string == "MasterCard":
        card_name = " ".join(incoming_string[:-1])
        output_string = f"{card_name} {get_mask_card_number(incoming_string[-1])}"
    elif incoming_string[0] == "Счет":
        output_string = f"{incoming_string[0]} {get_mask_account(incoming_string[-1])}"
    return output_string


