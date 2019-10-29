# app/main/views.py
from app import mongo, limiter, flask_uuid
from flask import jsonify, request, abort
from flask import current_app as app
from app.main import bp
from app.assertions import assert_valid_schema
from app.decorators import require_access_level
from jsonschema.exceptions import ValidationError as JsonValidationError
from pymongo import ASCENDING, DESCENDING
import uuid
import datetime

#-----------------------------------------------------------------------------#

# reject any non-json requests
@bp.before_request
def only_json():
    if not request.is_json:
        abort(400)

#-----------------------------------------------------------------------------#

@bp.route('/list/favourites', methods=['GET', 'POST', 'DELETE'])
@require_access_level(10, request)
def favourites(public_id, request):

    return _perform_action(request, public_id, 'favourites')

#-----------------------------------------------------------------------------#

@bp.route('/list/watchlist', methods=['GET', 'POST', 'DELETE'])
@require_access_level(10, request)
def watchlist(public_id, request):

    return _perform_action(request, public_id, 'watchlist')

#-----------------------------------------------------------------------------#

@bp.route('/list/viewed', methods=['GET', 'POST'])
@require_access_level(10, request)
def recently_viewed(public_id, request):

    return _perform_action(request, public_id, 'viewed')

#-----------------------------------------------------------------------------#

@bp.route('/list/purchased', methods=['GET', 'POST'])
@require_access_level(10, request)
def purchase_history(public_id, request):

    return _perform_action(request, public_id, 'purchased')

#-----------------------------------------------------------------------------#

#@bp.route('/list/bid_on', methods=['GET', 'POST'])
#@require_access_level(10, request)
#def recently_bid_on(public_id, request):
#
#    return _perform_action(request, public_id, 'purchased')

#-----------------------------------------------------------------------------#
# system routes
#-----------------------------------------------------------------------------#

@bp.route('/list/status', methods=['GET'])
def system_running():

    return jsonify({ 'message': 'System running...' }), 200

#-----------------------------------------------------------------------------#
# debug and helper functions
#-----------------------------------------------------------------------------#

def _return_document(public_id, list_name):

    record = None
    try:
        record = mongo.db[list_name].find_one({ '_id': public_id })
    except Exception as e:
        app.logger.warning("Error fetching doc [%s]", str(e))
        return False 

    if record is None:
        return False 

    return(record)

#-----------------------------------------------------------------------------#

def _perform_action(request, public_id, list_type):

    if request.method == 'DELETE' or request.method == 'POST':
        # check input is valid json
        try:
            data = request.get_json()
        except:
            return jsonify({ 'message': 'Check ya inputs mate. Yer not valid, Jason'}), 400

        # validate input against json schemas
        try:
            assert_valid_schema(data, 'uuid')
        except JsonValidationError as err:
            return jsonify({ 'message': 'Check ya inputs mate.', 'error': err.message }), 400

    # get document if it exists or create if not
    document = _return_document(public_id, list_type)

    if request.method == 'GET':
        if isinstance(document,dict):
            del document['_id']
            return jsonify(document), 200

        return jsonify({ 'message': 'Could not find any favourites' }), 404

    if request.method == 'POST':
        if document:
            list_of_uuids = document[list_type]
            if data['uuid'] not in list_of_uuids:
                list_of_uuids.insert(0, data['uuid'])
                mongo.db[list_type].update({ '_id': public_id },
                                           { '$set': { list_type: list_of_uuids } },
                                             upsert=False)
        else:
            # create a record
            mongo.db[list_type].insert_one({"_id" : public_id, list_type: [data['uuid']]})

        return jsonify({}), 201

    if request.method == 'DELETE':
        if document:
            list_of_uuids = document[list_type]
            if data['uuid'] in list_of_uuids:
                list_of_uuids.remove(data['uuid'])
                mongo.db[list_type].update({ '_id': public_id },
                                           { '$set': { list_type: list_of_uuids } },
                                             upsert=False)
        else:
            return jsonify({}), 404

        return jsonify({}), 204

    return jsonify({ 'message': 'more tea vicar?' }), 418

