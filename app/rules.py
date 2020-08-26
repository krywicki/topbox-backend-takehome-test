'''
Author: Joe Krywicki
Date  : 2020-08-25

Rules to validate incoming http requests
'''
import bson
from flask_request_validator import AbstractRule

class UnixTimestampRule(AbstractRule):
    ''' Validate a unix timestamp to ensure it's in range '''
    def validate(self, value:int):        
        errors = []
        if value < 0:
            errors.append(f'out-of-range value:"{value}"')        
        return errors

class ObjectIdRule(AbstractRule):
    ''' Validate a BSON ObjectId to ensure it's valid '''
    def validate(self, value:str):
        errors = []
        if bson.ObjectId.is_valid(value) == False:
            errors.append(f'id is not valid:"{value}')
        return errors
        