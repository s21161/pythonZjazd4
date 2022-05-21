import server.api as api_routes
from starlette.routing import Mount

routes = [
    Mount("/api", routes=api_routes.routes, name="api"),
]
