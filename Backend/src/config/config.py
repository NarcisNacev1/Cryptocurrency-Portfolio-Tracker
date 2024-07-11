class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:narcis1@localhost:5432/portfolio'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

class TestingConfig(Config):
    DEBUG = True
    TESTING = True
