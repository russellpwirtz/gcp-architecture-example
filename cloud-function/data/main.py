from google.cloud import firestore
import uuid
from flask import jsonify, Response

class Adjustment:
    def __init__(self, id: str, account_id: str, timestamp: str, amount: str, asset: str, description: str):
        self.id = id
        self.account_id = account_id
        self.timestamp = timestamp
        self.amount = amount
        self.asset = asset
        self.description = description

    @classmethod
    def from_json(cls, json: dict):
        return cls(**json)

def get_account(request) -> Response:
    try:
        if request.args and 'account_id' in request.args:
            account_id = request.args.get('account_id')
        else:
            return 'Precondition Failed', 412

        client = firestore.Client()
        doc_ref = client.collection(u'account').document(u'{}'.format(account_id))
        doc = doc_ref.get()

        if doc.to_dict():
            response = jsonify(doc.to_dict())
            response.status_code = 200
            return response
        else:
            response = jsonify({
                'httpResponseCode': '404',
                'errorMessage': 'Account does not exist'
            })
            response.status_code = 404
            return response
    except Exception as e:
        return e

def add_update_account(request):
    try:
        json_ = request.get_json()
        if 'id' not in json_:
            return 'Precondition Failed', 412
        client = firestore.Client()
        doc_ref = client.collection(u'account').document(u'{}'.format(json_.get('id')))
        doc_ref.set(json_)
        return {"created": True}, 201
    except Exception as e:
        return e

def post_adjustment(request) -> Response:
    try:
        json_ = request.get_json()['input']
        gcp_project = json_.pop("gcp_project", None)
        gcp_region = json_.pop("gcp_region", None)

        if 'account_id' not in json_:
            return 'Precondition Failed', 412
        # TODO validate account id

        if 'id' not in json_:
            json_['id'] = str(uuid.uuid4())
        # TODO validate unique id

        adjustment: Adjustment = Adjustment.from_json(json=json_)

        client = firestore.Client()
        doc_ref = client.collection(u'adjustments').document(u'{}'.format(adjustment.id))
        doc_ref.set(adjustment.__dict__)
        print(f'Posted adjustment: {str(adjustment)}')
        return {"created": True}, 201
    except Exception as e:
        print(str(e))
        return {"created": False}, 500
