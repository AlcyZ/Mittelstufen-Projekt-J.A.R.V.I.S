import re
from classes.gxrest import GXRest

# expected words to start the module
WORDS = ['BESTELLUNGEN', 'BESTELLUNG', 'ABRUFEN']

PRIORITY = 2


def handle(text, mic, profile):
    gx_rest = GXRest()

    # ask the user to specify the fetch type
    mic.say(GXRest.ASK_ORDERS_TYPE)
    mic.say(GXRest.ASK_VALID_ANSWERS)

    # wait until the user select the type
    search_type = mic.activeListen().upper()

    gx_orders_main(search_type, mic, gx_rest)


# checks if the speech input is valid to start the module
def isValid(text):
    orders = bool(re.search(r'\bestellungen abrufen\b', text, re.IGNORECASE))
    order = bool(re.search(r'\bestellung abrufen\b', text, re.IGNORECASE))

    return orders or order


def gx_orders_main(search_type, mic, gx_rest):
    if bool(re.search(r'\all\b', search_type, re.IGNORECASE)):
        mic.say(GXRest.ASK_ORDERS_AMOUNT)
        amount = int(mic.activeListen())

        if amount == 0:
            amount = 1

        message = gx_rest.get_orders(amount)

    elif bool(re.search(r'\bestimmt\b', search_type, re.IGNORECASE)):
        mic.say(GXRest.ASK_ORDERS_SEARCH_KEYWORD)
        search_keyword = mic.activeListen()

        mic.say(GXRest.ASK_ORDERS_AMOUNT)
        amount = int(mic.activeListen())

        if amount == 0:
            amount = 1

        message = gx_rest.get_orders_by(search_keyword, amount)
    else:
        mic.say(GXRest.ANSWER_INVALID_TYPE)
        mic.say(GXRest.ANSWER_REPEAT_FETCH)

        repeat_answer = mic.activeListen()
        regex_yes = re.compile(GXRest.YES, re.IGNORECASE)

        if bool(regex_yes.match(repeat_answer)):
            return gx_orders_main(search_type, mic, gx_rest)
        else:
            message = GXRest.END

    mic.say(message)
