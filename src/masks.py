def get_mask_card_number(card_number: str) -> str:
    """Маскирует номер банковской карты. Формат: XXXX XX** **** XXXX. Видны первые 6 цифр и последние 4 цифры, остальные заменены на *."""

    cleaned_number = "".join(filter(str.isdigit, card_number))

    if len(cleaned_number) != 16:
        raise ValueError(f"Номер карты должен содержать 16 цифр, получено {len(cleaned_number)}")

    first_part = cleaned_number[:4]
    second_part = cleaned_number[4:6]
    last_part = cleaned_number[-4:]
    masked_card = f"{first_part} {second_part}** **** {last_part}"

    return masked_card


def get_mask_account(account_number: str) -> str:
    """Маскирует номер банковского счета. Формат: **XXXX. Видны только последние 4 цифры, перед ними две звездочки."""

    cleaned_number = "".join(filter(str.isdigit, account_number))
    if len(cleaned_number) < 4:
        raise ValueError(f"Номер счета должен содержать минимум 4 цифры, получено {len(cleaned_number)}")
    last_four_digits = cleaned_number[-4:]
    masked_account = f"**{last_four_digits}"
    return masked_account
