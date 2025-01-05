def format_phone(phone_number: str) -> str:
    numbers = set('0123456789')
    cleaned_phone_number = ''.join(char for char in phone_number if char in numbers)

    if len(cleaned_phone_number) == 10:
        cleaned_phone_number = '8' + cleaned_phone_number
    elif len(cleaned_phone_number) == 11:
        if cleaned_phone_number.startswith('7'):
            cleaned_phone_number = '8' + cleaned_phone_number[1:]
        elif cleaned_phone_number.startswith('8'):
            pass
        else:
            return cleaned_phone_number
    else:
        return cleaned_phone_number

    formatted_phone_number = f"8 ({cleaned_phone_number[1:4]}) {cleaned_phone_number[4:7]}-{cleaned_phone_number[7:9]}-{cleaned_phone_number[9:11]}"

    return formatted_phone_number

