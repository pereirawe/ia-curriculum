def format_phone_number(phone_number: str):
    """
    Formata o número de telefone para o padrão do WhatsApp.
    O número deve ser passado no formato 'XX999999999'.
    """

    phone_number = (
        phone_number.replace(" ", "")
        .replace("-", "")
        .replace(")", "")
        .replace("(", "")
        .replace(".", "")
        .replace("_", "")
        .replace("+", "")
    )

    if len(phone_number) == 8:
        phone_number = "9" + phone_number
    elif len(phone_number) == 11:
        phone_number = "55" + phone_number

    return phone_number
