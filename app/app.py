import sys
from bson import json_util, ObjectId, Timestamp
from flask import Flask
from datetime import datetime, timezone

from app.helpers import mongo_client


from . import rules
from flask_request_validator import (
    exceptions,
    Param,
    validate_params,
    Pattern,
    GET
)

API_VERSION = '1.0'

app = Flask(__name__)
db = mongo_client()

################################
# Routes
################################

@app.route('/')
def root():
    response = {'apiVersion': API_VERSION, 'appName': 'Topbox Backend Take Home Test'}
    return json_util.dumps(response)


@app.route('/clients')
def clients():
    return json_util.dumps(db.clients.find({}))


@app.route('/clients/<client_id>')
def clients_by_id(client_id):
    client_object_id = ObjectId(client_id)
    return json_util.dumps(db.clients.find_one({'_id': client_object_id}))


@app.route('/engagements')
def engagements():
    return json_util.dumps(db.engagements.find({}))


@app.route('/engagements/<engagement_id>')
def engagements_by_id(engagement_id):
    engagement_object_id = ObjectId(engagement_id)
    return json_util.dumps(db.engagements.find_one({'_id': engagement_object_id}))

@app.route('/interactions')
@validate_params(
    Param(name='engagementId', param_type=GET, value_type=str, required=True, rules=[rules.ObjectIdRule()]),
    Param(name='startDate', param_type=GET, value_type=int, required=False, rules=[rules.UnixTimestampRule()]),
    Param(name='endDate', param_type=GET, value_type=int, required=False, rules=[rules.UnixTimestampRule()])
)
def interactions(engagement_id:str, start_date:int, end_date:int):    
    date_filter = {}
    db_query = {
        'engagementId': ObjectId(engagement_id),                        
    }

    if start_date is not None:
        date_filter['$gte'] = datetime.fromtimestamp(start_date/1000.0, timezone.utc)

    if end_date is not None:
        date_filter['$lt'] = datetime.fromtimestamp(end_date/1000.0, timezone.utc)
    
    if any(date_filter):
        db_query['interactionDate'] = date_filter            
    
    return json_util.dumps(db.interactions.find(db_query))

@app.route('/interactions/<interaction_id>')
def interactions_by_id(interaction_id):
    interaction_object_id = ObjectId(interaction_id)
    return json_util.dumps(db.interactions.find_one({'_id': interaction_object_id}))


################################
# Client Error Handlers
################################

@app.errorhandler(exceptions.InvalidRequest)
def handle_invalid_request(e: exceptions.InvalidRequest):
    return json_util.dumps({ 'error': e.message }), 400

@app.errorhandler(exceptions.NotAllowedType)
def handle_not_allowed_type(e: exceptions.NotAllowedType):
    return json_util.dumps({'error': e.message }), 400

@app.errorhandler(exceptions.UndefinedParamType)
def handle_undefined_param_type(e: exceptions.UndefinedParamType):
    return json_util.dumps({'errror': e.message }), 400


