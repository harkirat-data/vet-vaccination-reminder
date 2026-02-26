import re

def clean_phone(phone):
    phone = re.sub(r'\D', '', str(phone))  # Remove non-digits
    if not phone.startswith("91"):  # India country code
        phone = "91" + phone
    return phone

def create_message(owner, pet, vaccine):
    return (
        f"Hi {owner}, this is a reminder that {pet} is due for a "
        f"{vaccine} vaccination. Please contact us to schedule an appointment."
    )