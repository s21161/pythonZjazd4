from starlette.routing import Route
import server.api.users.endpoints


routes = [
    Route("/register", endpoints.register, methods=["POST"]),
    Route("/login", endpoints.login, methods=["POST"]),
    Route("/refresh_token", endpoints.refresh_token, methods=["POST"])
]
