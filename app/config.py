class BaseConfig:  # Basic Configurations
    pass


class DevelopmentConfig(BaseConfig):
    ENV = 'development'
    DEBUG = True


config = {'development': DevelopmentConfig, 'default': DevelopmentConfig}
webcam_op = {
    'photo': '/photoaf.jpg',
    'video': '/video',
    'enabletorch': '/enabletorch',
    'disabletorch': '/disabletorch',
    'ptz': '/ptz?zoom={zoom}',
    'photo_size': '/settings/photo_size?set={size}',
    'status': '/status.json?show_avail=1'
}
