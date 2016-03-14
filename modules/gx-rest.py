import requests
import datetime

WORDS = ['REST', 'SHOP']


class GXRest:
    # variable initialization
    rest_url = 'http://localhost/gxshops/gx_2720/api.php/v2/'  # was ist besser? Constructor init oder direkt?
    all_orders = 'orders'

    admin_mail = 'admin@shop.de'
    admin_pass = '12345'

    def __init__(self):
        """
        Initialization of the gx rest module.
        """

        self.rest_url = 'http://localhost/gxshops/gx_2720/api.php/v2/'
        self.all_orders = 'orders'

        self.admin_mail = 'admin@shop.de'
        self.admin_pass = '12345'

    def request_helper(self, req):
        """
        Helper function to send curl requests to the gambio shop.
        :param req: Last segment of the requests url path.
        :return: Json decoded object from the curl request.
        """

        r = requests.get(self.rest_url + req, auth=(self.admin_mail, self.admin_pass))
        return r.json()

    def get_orders(self, amount=10):
        """
        Returns a prepared message for the last xy (specified by amount argument) orders
        :param int amount:
        :return str: Prepared messages with information about the last xy orders.
        """

        orders_json = self.request_helper('orders')
        return self.get_orders_message(orders_json, amount)

    def get_orders_message(self, order_json, amount=10):
        """
        Returns prepared order messages for the last xy orders.
        :param json order_json: Json which contains information about the order
        :param int amount: Amount of orders to recognize (from the order json)
        :return str: Prepared order messages.
        """

        orders_array = []

        for index, order in enumerate(order_json):
            order_message = ''
            order_message += 'Bestellung von: ' + order['customerName'] + "\n"
            order_message += 'Summe: ' + str(order['totalSum']) + ' EUR' + "\n"
            order_message += 'Datum: ' + self.format_gx_datetime(order['purchaseDate']) + "\n"
            order_message += 'Zahlungsart: ' + order['paymentType']['title'] + "\n"
            order_message += 'Versandart: ' + order['shippingType']['title'] + "\n"
            order_message += "\n"
            orders_array.append(order_message)

        slice_last_entries = slice(-amount, None)
        message = ''

        for order_message in orders_array[slice_last_entries]:
            message += order_message
        return message

    @staticmethod
    def format_gx_datetime(purchase_date):
        return datetime.datetime.strptime(purchase_date, '%Y-%m-%d %H:%M:%S').strftime('%d.%m.%y %H:%M')


# checks if the stt engine recognize the correct words.
def isValid(text):
    rest = bool(re.search(r'\rest\b', text, re.IGNORECASE))
    shop = bool(re.search(r'\rest\b', text, re.IGNORECASE))

    return rest or shop
