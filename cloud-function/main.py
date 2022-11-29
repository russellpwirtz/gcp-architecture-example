from flask import jsonify
from google.cloud import firestore


def get_account(request):
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
        else:
            response = jsonify({
                'httpResponseCode': '404',
                'errorMessage': 'Account does not exist'
            })
            response.status_code = 404
        return response
    except Exception as e:
        return e
