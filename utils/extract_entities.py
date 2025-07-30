import re
import phonenumbers
from email_validator import validate_email, EmailNotValidError
from stdnum.pt import nif
from stdnum import iban  

def extract_entities(text: str) -> dict:
    emails = list(set(re.findall(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", text)))
    phones = [
        match.number
        for match in phonenumbers.PhoneNumberMatcher(text, "PT")
    ]
    ibans = list(set(re.findall(r"\bPT\d{2}\d{21}\b", text)))  # regex para IBAN PT
    # valida IBANs encontrados
    ibans = [iban for iban in ibans if iban.is_valid(iban)]

    nifs = [n for n in re.findall(r"\b\d{9}\b", text) if nif.is_valid(n)]

    return {
        "emails": emails,
        "phones": phones,
        "ibans": ibans,
        "nifs": nifs
    }
