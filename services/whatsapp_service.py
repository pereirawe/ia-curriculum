import urllib


def _clean_contact_name(name):
    name = name.strip()
    parts = name.split()

    cleaned_parts = []
    i = 0
    while i < len(parts):
        if (
            i < len(parts) - 1
            and len(parts[i]) == 1
            and len(parts[i + 1]) == 1
            and parts[i].isalpha()
            and parts[i + 1].isalpha()
        ):

            combined = []
            while i < len(parts) and len(parts[i]) == 1 and parts[i].isalpha():
                combined.append(parts[i])
                i += 1
            cleaned_parts.append("".join(combined))
        else:
            cleaned_parts.append(parts[i])
            i += 1

    lowercase_particles = {"de", "do", "da", "dos", "das", "e"}
    cleaned_name_parts = []
    for i, part in enumerate(cleaned_parts):
        if i > 0 and part.lower() in lowercase_particles:
            cleaned_name_parts.append(part.lower())
        else:
            cleaned_name_parts.append(part.capitalize())

    return " ".join(cleaned_name_parts)


def _create_whatsapp_url(phone_number: str, message: str) -> str:
    # URL encode the message
    encoded_message = urllib.parse.quote(message)
    # Construct the WhatsApp URL
    url = f"https://web.whatsapp.com/send?phone={phone_number}&text={encoded_message}"
    return url


def invite_whatsapp_url(vacancy_name: str, contact_name: str, contact_phone: str):

    message = f"""\
Olá {_clean_contact_name(contact_name)}! Tudo bem?

Meu nome é William Pereira, sou Líder de Desenvolvimento e BI na *Setup Tecnologia*.

O seu currículo e experiência chamaram a nossa atenção para a vaga *{vacancy_name}*, e gostaríamos de convidar você para uma entrevista!

A vaga é 100% presencial em Curitiba. Para agendar um horário, basta acessar o link abaixo:
👈 https://calendly.com/william-pereira-setuptecnologia/30min

Ficarei no aguardo! Se tiver alguma dúvida, é só me avisar.
"""

    return _create_whatsapp_url(contact_phone, message)


def approve_whatsapp_url(vacancy_name: str, contact_name: str, contact_phone: str):
    message = f"""\
Olá *{_clean_contact_name(contact_name)}*!

Tudo bem! O seu currículo e experiência chamaram a nossa atenção para a vaga *{vacancy_name}*, e gostaríamos de aprová-la!

Ficarei no aguardo! Se tiver alguma dúvida, é só me avisar.
"""

    return _create_whatsapp_url(contact_phone, message)


def reject_whatsapp_url(vacancy_name: str, contact_name: str, contact_phone: str):
    message = f"""\
Olá *{_clean_contact_name(contact_name)}*!

Desculpe, mas o seu currículo e experiência não chamaram a nossa atenção para a vaga *{vacancy_name}*.
"""

    return _create_whatsapp_url(contact_phone, message)
