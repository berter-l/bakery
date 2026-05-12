from ninja import NinjaAPI
from catalog.api import router as catalog_router
from cart.api import router as cart_router
from orders.api import router as order_router
from ninja.errors import ValidationError
from promotions.api import router as promotions_router
from ninja_jwt.routers.blacklist import blacklist_router
from ninja_jwt.routers.obtain import obtain_pair_router, sliding_router
from ninja_jwt.routers.verify import verify_router
from authentication.api import router as authentication_router
from reports.api import router as report_router

api = NinjaAPI()
api.add_router('catalog/', catalog_router)
api.add_router('carts/', cart_router)
api.add_router('orders/', order_router)
api.add_router('promotions/', promotions_router)
api.add_router('login/', authentication_router)
api.add_router('reports/', report_router)
