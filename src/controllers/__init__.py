from controllers.blogs_controllers import blogs
from controllers.reviews_controllers import reviews
from controllers.auth_controller import user


registerable_controllers = [
    blogs,
    reviews,
    user
]
