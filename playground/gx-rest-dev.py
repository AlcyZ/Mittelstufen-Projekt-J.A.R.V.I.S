from classes.gxrest import GXRest

rest = GXRest()

orders = rest.get_orders(1)

print orders
