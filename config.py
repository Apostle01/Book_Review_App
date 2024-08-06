import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///site.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False



# class Config:
#     SECRET_KEY = os.environ.get('SECRET_KEY') or \
#         'f5bc222cb7bcd4d4bc933528608bc608d3f25680723aaf60'
#     SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
#         'postgresql://postgres:Admin@localhost/postgres'
#     SQLALCHEMY_TRACK_MODIFICATIONS = False
