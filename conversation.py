sessions = {}

SLOTS = [
    ('no_of_dependents', "How many dependents do you have? (enter a number, e.g. 0, 1, 2...)", 'int'),
    ('education', "What is your education level? (Graduate / Not Graduate)", 'education'),
    ('self_employed', "Are you self-employed? (Yes / No)", 'yesno'),
    ('income_annum', "What is your annual income? (numbers only, e.g. 500000 or '5 lakh')", 'float'),
    ('loan_amount', "How much loan amount are you requesting?", 'float'),
    ('loan_term', "What loan term do you want (in years)?", 'int'),
    ('cibil_score', "What is your CIBIL score? (must be between 300-900)", 'cibil'),
    ('residential_assets_value', "What is the value of your residential assets?", 'float'),
    ('commercial_assets_value', "What is the value of your commercial assets?", 'float'),
    ('luxury_assets_value', "What is the value of your luxury assets?", 'float'),
    ('bank_asset_value', "What is the value of your bank assets?", 'float'),
]

def start_application(session_id):
    sessions[session_id] = {'step': 0, 'data': {}, 'in_progress': True}
    question = SLOTS[0][1]
    return f"Great, I'd love to help you check your loan eligibility! Let's go step by step. {question}"

def is_applying(session_id):
    return session_id in sessions and sessions[session_id].get('in_progress', False)

def extract_number_with_multiplier(raw_value):
    """
    Handles words like 'lakh', 'lac', 'crore' as multipliers.
    Returns a float, or raises ValueError if nothing usable is found.
    """
    text = raw_value.lower().strip()

    multiplier = 1
    if 'crore' in text:
        multiplier = 10000000
        text = text.replace('crore', '')
    elif 'lakh' in text or 'lac' in text:
        multiplier = 100000
        text = text.replace('lakh', '').replace('lac', '')

    # Keep digits and one decimal point only
    cleaned = ''
    dot_seen = False
    for ch in text:
        if ch.isdigit():
            cleaned += ch
        elif ch == '.' and not dot_seen:
            cleaned += ch
            dot_seen = True

    if cleaned == '' or cleaned == '.':
        raise ValueError("No valid number found")

    number = float(cleaned)
    return number * multiplier

def parse_value(raw_value, value_type):
    raw_value = raw_value.strip()

    if value_type == 'int':
        number = extract_number_with_multiplier(raw_value)
        return int(round(number))  # rounds decimals instead of mangling digits

    elif value_type == 'float':
        return extract_number_with_multiplier(raw_value)

    elif value_type == 'cibil':
        number = int(round(extract_number_with_multiplier(raw_value)))
        if number < 300 or number > 900:
            raise ValueError("CIBIL score out of valid range")
        return number

    elif value_type == 'education':
        return 0 if 'not' not in raw_value.lower() else 1

    elif value_type == 'yesno':
        text = raw_value.lower().strip()
        if text in ('yes', 'y', 'yeah', 'yep'):
            return 1
        elif text in ('no', 'n', 'nope'):
            return 0
        else:
            raise ValueError("Unclear yes/no answer")  # now forces a re-ask instead of silently guessing

    return raw_value

def handle_slot_input(session_id, message):
    session = sessions[session_id]
    step = session['step']
    key, question, value_type = SLOTS[step]

    try:
        parsed_value = parse_value(message, value_type)
        session['data'][key] = parsed_value
    except ValueError:
        if value_type == 'cibil':
            return f"That doesn't look like a valid CIBIL score. {question}", False
        elif value_type == 'yesno':
            return f"Please answer clearly with Yes or No. {question}", False
        else:
            return f"Sorry, I didn't quite catch that. {question}", False

    session['step'] += 1

    if session['step'] < len(SLOTS):
        next_question = SLOTS[session['step']][1]
        return next_question, False
    else:
        session['in_progress'] = False
        return None, True

def get_collected_data(session_id):
    return sessions[session_id]['data']