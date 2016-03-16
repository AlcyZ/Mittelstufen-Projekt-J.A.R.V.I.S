import re
import pprint
from classes.gxrest import GXRest

rest = GXRest()

orders = rest.get_orders_by('post')
customers = rest.get_customers()

pattern = 'jap'

prog = re.compile(pattern, re.IGNORECASE)

test = bool(prog.match('jap'))

print test

