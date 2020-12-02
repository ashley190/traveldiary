from controllers.blogs_controllers import blogs
from controllers.reviews_controllers import reviews
from controllers.auth_controller import user
from controllers.images_controller import images


registerable_controllers = [
    blogs,
    reviews,
    user,
    images
]
