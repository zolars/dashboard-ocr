class BaseConfig:  # Basic Configurations
    pass


class DevelopmentConfig(BaseConfig):
    ENV = 'development'
    DEBUG = True


config = {'development': DevelopmentConfig, 'default': DevelopmentConfig}
