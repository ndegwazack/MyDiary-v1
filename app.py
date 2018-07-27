from flask import Flask, request
from flask_restplus import Api, Resource, fields
from functools import wraps

#Instantiate flask app
app = Flask(__name__)
auth = {
    'apikey' : {
        'type' : 'apiKey',
        'in' : 'header',
        'name' : 'Api-Key'
    }
}
api = Api(app, authorizations=auth, version='v1', title='My Diary API', description='An API for a Diary')

diary_entry = api.model("My Diary", {
    'Id' : fields.Integer(description="The unique key of diary entry"),
    'Title' : fields.String(description="Title of story"),
    'Story' : fields.String(description="The whole story")})

#array that will hold all the entries
diary_entries = []

#dictionary that takes entries of the diary
entry = {'Id' : 1, 'Title' : 'The cat', 'Story' : 'The cat ate the mouse'}
diary_entries.append(entry)

parser = api.parser()
parser.add_argument('Title', type=str, required=True, location='form')
parser.add_argument('Story', type=str, required=True, location='form')

def require_token(f):
    '''
    to access endpoints one must have an authentication key
    '''
    @wraps(f)
    def authenticate(*args, **kwargs):
        '''
        define authentication here
        '''
        
        token = None

        if 'Api-Key' in request.headers:
            token = request.headers['Api-Key']

        if not token:
            return{'message' : 'no token entered'}, 401

        if token != 'pass':
            return{'message' : 'Invalid token'}, 401

        print('Token: {}'.format(token))
        return f(*args, **kwargs)

    return authenticate 

@api.route('/MyDiary/api/v1/entries')
class Diary(Resource):
    @api.doc(security = 'apikey')
    @require_token
    @api.marshal_with(diary_entry, envelope='Entries')
    def get(self):
        '''
        returns a list of all entries in the diary
        '''
        return diary_entries, 200

    @api.expect(diary_entry)
    def post(self):

        """
        adds a new entry to the diary
        """
        new_entry = api.payload
        new_entry['Id'] = len(diary_entries) + 1 #Id auto-increments by 1
        diary_entries.append(new_entry)
        return {'result': 'Entry successfully added to diary'}, 201

@api.route('/MyDiary/api/v1/entries/<int:Id>')
class Entry(Resource):
    @api.doc(security = 'apikey')
    @require_token
    @api.marshal_with(diary_entry, envelope='Entries')
    def get(self, Id):

        """
        return a specific diary entry
        """
        result = [entry for entry in diary_entries if entry['Id'] == Id]
        return result

    @api.doc(parser=parser)
    def put(self, Id):
        '''
        update an existing entry
        '''
        args = parser.parse_args()
        for index, entry in enumerate(diary_entries):
            if entry['Id'] == Id:
                diary_entries[index]['Title'] = args['Title']
                diary_entries[index]['Story'] = args['Story']
            return entry, 201
        return None, 201

    def delete(self, Id):
        '''
        remove an existing entry from the diary
        '''
        for index, entry in enumerate(diary_entries):
            if entry['Id'] == Id:
                del diary_entries[index]
            return{'response' : 'Entry deleted successfully'}, 204
        return None, 204

if __name__ == '__main__':
    app.run(debug=True)