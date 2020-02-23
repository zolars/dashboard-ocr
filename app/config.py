class BaseConfig:  # Basic Configurations
    pass


class DevelopmentConfig(BaseConfig):
    ENV = 'development'
    DEBUG = True


config = {'development': DevelopmentConfig, 'default': DevelopmentConfig}
camera_op = {
    'photo': '/photo.jpg',
    'enabletorch': '/enabletorch',
    'disabletorch': '/disabletorch',
    'ptz': '/ptz?zoom={zoom}',
}
