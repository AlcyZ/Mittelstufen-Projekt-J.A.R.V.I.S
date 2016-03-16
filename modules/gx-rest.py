WORDS = ['REST', 'SHOP']





# checks if the stt engine recognize the correct words.
def isValid(text):
    rest = bool(re.search(r'\rest\b', text, re.IGNORECASE))
    shop = bool(re.search(r'\rest\b', text, re.IGNORECASE))

    return rest or shop
