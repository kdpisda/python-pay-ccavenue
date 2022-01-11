import os


class Config:
    WORKING_KEY = os.environ.get('CCAVENUE_WORKING_KEY')
    ACCESS_CODE = os.environ.get('CCAVENUE_ACCESS_CODE')
    MERCHANT_CODE = os.environ.get('CCAVENUE_MERCHANT_CODE')
