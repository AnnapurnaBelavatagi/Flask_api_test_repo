from werkzeug.security import safe_str_cmp
from models.user import UserModel


def authenticate(username, password):
    user = UserModel.find_by_username(username)
    if user and safe_str_cmp(user.password, password):
        return user

def identity(payload):
    user_id = payload['identity']
    return UserModel.find_by_id(user_id)


'''
users = [
    {
        'id' :1,
        'username':'anu',
        'password' : 'anu123'
    }
]

username_mapping = {
    'anu' : {
        'id' :1,
        'username':'anu',
        'password' : 'anu123'
    }
}

userid_mapping = { 
    1: {
        'id' :1,
        'username':'anu',
        'password' : 'anu123'
    }
}
'''
'''
users = [
    User(1,'anu','anu123')
]

username_mapping = {u.username : u for u in users}
userid_mapping = {u.id :u for u in users}

def authenticate(username, password):
    user = username_mapping.get(username, None)
    #if user and safe_str_cmp(user.password == password):
    if user and safe_str_cmp(user.password, password):
        return user

def identity(payload):
    user_id = payload['identity']
    return userid_mapping.get(user_id, None)
'''


