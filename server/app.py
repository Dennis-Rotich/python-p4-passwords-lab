#!/usr/bin/env python3

from flask import request, session, make_response
from flask_restful import Resource, reqparse

from config import app, db, api
from models import User

class ClearSession(Resource):

    def delete(self):
    
        session['page_views'] = None
        session['user_id'] = None

        return {}, 204

class Signup(Resource):
    
    def post(self):
        json = request.get_json()
        user = User(
            username=json['username']
        )
        user.password_hash = json['password']
        db.session.add(user)
        db.session.commit()
        new_user = User.query.filter_by(username=user.username).first()
        session['user_id'] = new_user.id
        return make_response(user.to_dict(), 201)

class CheckSession(Resource):
    def get(self):
        if session['user_id'] != None:
            user = User.query.filter_by(id=session.get('user_id')).first()
            response_body = user.to_dict()
            return make_response(response_body, 200)
        else:
            return make_response({}, 204)        
    pass

class Login(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("username", type=str)
        parser.add_argument("password", type=str)
        data = parser.parse_args()
        new_user = User(username=data.get("username"), _password_hash=data.get("password"))
        db.session.add(new_user)
        db.session.commit()
        user = User.query.filter_by(username=new_user.username).first()
        session['user_id'] = user.id
        return make_response(user.to_dict(), 200)
    pass

class Logout(Resource):
    def delete(self):
        session['user_id'] = None
        return make_response({'message':'Logged out successfully'}, 204)
    pass

api.add_resource(ClearSession, '/clear', endpoint='clear')
api.add_resource(Signup, '/signup', endpoint='signup')
api.add_resource(CheckSession, '/check_session', endpoint='check_session')
api.add_resource(Login, "/login", endpoint="login")
api.add_resource(Logout, '/logout', endpoint='logout')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
