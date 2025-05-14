from string import punctuation
import email_validator

def validate_password(value: str):

    if not value:
        return value

    if len(value) < 8:
        raise ValueError('Invalid Password! Password must contains at least 8 characters.')
    
    if len(value) > 64:
        raise ValueError('Invalid Password! Password must contains at max 64 characters.')
    
    has_lowercase = False
    has_uppercase = False
    has_digit = False
    has_special_char = False

    for c in value:
        if c.isalpha():
            if c.islower():
                has_lowercase = True
            if c.isupper():
                has_uppercase = True

        if c.isdigit():
            has_digit = True

        if c in punctuation:
            has_special_char = True

    if not (has_lowercase and has_uppercase and has_digit and has_special_char):
        raise ValueError('Invalid Password! Password must contain at least 1 lowercase, 1 uppercase, 1 digit and 1 special character.')
    
    return value


def validate_email(value: str):
    if not value:
        return value
    return email_validator.validate_email(value).email

def validate_fname(value: str):
    if not value:
        return value

    if not value.isalpha():
        raise ValueError('Invalid input! Fname must only contains alphabets.')
    
    return value

def validate_lname(value: str):

    if not value:
        return value

    if not value.isalpha():
        raise ValueError('Invalid input! Lname must only contains alphabets.')
    
    return value

def validate_mobile_number(value: str):

    if not value:
        return value

    if not value.isdigit():
        raise ValueError('Invalid input! Mobile number must only contain digits.')
    
    if len(value) != 10:
        raise ValueError('Invalid input. Mobile number must be of 10 digits.')
    
    return value