import requests
import datetime


class GXRest:
    # This class constant are used by J.A.R.V.I.S mic.say() method

    ASK_ORDERS_TYPE = 'Suchen sie nach einer bestimmten Bestellung oder wollen sie die letzten diktiert bekommen?'
    ASK_VALID_ANSWERS = 'Bitte antworte mit den KeyWords: alle oder bestimmte'

    ASK_ORDERS_AMOUNT = 'Wie viele Bestellungen sollen diktiert werden?'
    ASK_ORDERS_SEARCH_KEYWORD = 'Wonach soll in den Bestellungen gesucht werden?'

    ANSWER_INVALID_TYPE = 'Die Antwort konnte nicht richtig verstanden werden'
    ANSWER_REPEAT_FETCH = 'Soll der Suchvorgang wiederholt werden?'
    YES = 'Ja'
    NO = 'Nein'
    END = 'Module wird beendet.'

    def __init__(self):
        """
        Initialization of the gx rest module.
        Initialized properties:
            ::rest_url
            ::admin_mail
            ::admin_pass
            ::all_orders
            ::all_customers
        """

        self.rest_url = 'http://localhost/gxshops/gx_2720/api.php/v2/'
        self.admin_mail = 'admin@shop.de'
        self.admin_pass = '12345'

        # properties to handle the orders curl request
        self.all_orders = 'orders'
        self.orders_search = self.all_orders + '?q='

        # properties to handle the customers curl request
        self.all_customers = 'customers'

    def get_orders(self, amount=10):
        """
        Returns a prepared message for the last xy (specified by amount argument) orders.

        :param int amount: Amount of orders data to fetch.
        :return: Well defined string with information about orders.
        """
        orders_json = self._request_helper(self.all_orders)
        return GXRest._get_orders_message(orders_json, amount)

    def get_orders_by(self, search_keyword, amount=10):
        """
        Returns a prepared message for the last xy (specified by amount argument) orders by the given search keyword.

        :param string search_keyword: Keyword to search by.
        :param int amount: Amount of orders data to fetch.
        :return: Well defined string with information about orders.
        """

        orders_json = self._request_helper(self.orders_search + search_keyword.lower())
        return GXRest._get_orders_message(orders_json, amount)

    def get_customers(self, amount=10):
        """
        Returns a prepared message for the last xy (specified by amount argument) customers.

        :param int amount: Amount of customers data to fetch.
        :return: Well defined string with information about customers.
        """
        customers_json = self._request_helper(self.all_customers)
        return GXRest._get_customers_message(customers_json, amount)

    @staticmethod
    def _get_orders_message(orders_json, amount=10):
        """
        Returns prepared order messages for the last xy orders.
        :param json orders_json: Json which contains information about the order
        :param int amount: Amount of orders to recognize (from the order json)
        :return str: Prepared order messages.
        """

        orders_array = []

        for index, order in enumerate(orders_json):
            order_message = ''
            order_message += 'Bestellung von: ' + order['customerName'] + "\n"
            order_message += 'Summe: ' + str(order['totalSum']) + ' EUR' + "\n"
            order_message += 'Datum: ' + GXRest._format_gx_datetime(order['purchaseDate']) + "\n"
            order_message += 'Zahlungsart: ' + order['paymentType']['title'] + "\n"
            order_message += 'Versandart: ' + order['shippingType']['title'] + "\n"
            order_message += "\n"
            orders_array.append(order_message)

        slice_last_entries = slice(-amount, None)
        message = ''

        for order_message in orders_array[slice_last_entries]:
            message += order_message
        return message

    def _request_helper(self, req):
        """
        Helper function to send curl requests to the gambio shop.
        :param req: Last segment of the requests url path.
        :return: Json decoded object from the curl request.
        """

        r = requests.get(self.rest_url + req, auth=(self.admin_mail, self.admin_pass))
        return r.json()

    @staticmethod
    def _get_customers_message(customers_json, amount=10):
        """
        Create a well defined message string from the passed customers json.

        :param json customers_json: Json which holds information about customers.
        :param int amount: Amount of customers to fetch.
        :return:
        """
        customers_array = []

        for index, customer in enumerate(customers_json):
            if customer['gender'] == 'm':
                customer_gender = 'Mann'
            else:
                customer_gender = 'Frau'

            customer_message = str(index + 1) + '.\n'
            customer_message += customer['firstname'] + '\n'
            customer_message += customer['lastname'] + '\n'
            customer_message += 'Anrede: ' + customer_gender + '\n'
            customer_message += 'E-Mail: ' + customer['email'] + '\n'
            customer_message += 'Telefon Nummer: ' + customer['telephone'] + '\n'
            if customer['dateOfBirth'] != '0000-00-00':
                customer_message += 'Geburtstag: ' + GXRest._format_gx_datetime(customer['dateOfBirth'], 'date') + '\n'
            customer_message += '\n'
            customers_array.append(customer_message)

        slice_last_entries = slice(-amount, None)
        message = ''

        for customer_message in customers_array[slice_last_entries]:
            message += customer_message
        return message

    @staticmethod
    def _format_gx_datetime(date, date_type='datetime'):
        """
        Format the dates which are get by the gx-rest API json.

        :param str date: Unformatted date value.
        :param str date_type: Type of passed date value, default is datetime.
        :return: Formatted date value
        """
        if date_type == 'datetime':
            return datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S').strftime('%d.%m.%y %H:%M')
        elif date_type == 'date':
            return datetime.datetime.strptime(date, '%Y-%m-%d').strftime('%d.%m.%y')
        else:
            return TypeError('unexpected date type for GXRest::format_gx_datetime')
