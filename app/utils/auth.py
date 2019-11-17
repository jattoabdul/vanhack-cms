import jwt

from app.repositories.admin_repo import AdminRepo
from app.repositories.student_repo import StudentRepo
from config import get_env
from functools import wraps
from flask import request, jsonify, make_response


class Auth:
    """ This class will house Authentication and Authorization Methods """

    """ Routes The Location Header Should Not Be Applied To """
    location_header_ignore = [
        '/locations'
    ]

    """ Routes The Authentication Header Should Not Be Applied To """
    authentication_header_ignore = [
        '/auth/login',
        '/auth/logout',
        '/accounts/signup/',
        '/password/reset/',
        '/docs',
        'loaderio-038d65e72fe3012184259133474caec4.txt'
    ]

    @staticmethod
    def check_token():
        if request.method != 'OPTIONS':

            for endpoint in Auth.authentication_header_ignore:
                if request.path.find(endpoint) > -1:  # If endpoint in request.path, ignore this check
                    return None

            try:
                token = Auth.get_token()
            except Exception as e:
                print(e)
                return make_response(jsonify({'msg': str(e)}), 401)

            try:
                decoded = Auth.decode_token(token)
                admin = AdminRepo().find_first(id=decoded['identity']['id'], auth_key=decoded['identity']['authKey'])
                student = StudentRepo().find_first(id=decoded['identity']['id'], auth_key=decoded['identity']['authKey'])
                user_exist = False
                if admin or student:
                    user_exist = True
                if not user_exist:
                    return make_response(jsonify({'msg': 'Token Invalid. Please Login Again'}), 401)
            except Exception as e:
                return make_response(jsonify({'msg': str(e)}), 401)

    @staticmethod
    def _get_user():
        token = None
        try:
            token = Auth.get_token()
        except Exception as e:
            raise e

        try:
            if token:
                return Auth.decode_token(token)['identity']
        except Exception as e:
            raise e

    @staticmethod
    def user(*keys):
        user = Auth._get_user()
        if keys:
            if len(keys) > 1:
                values = list()
                for key in keys:
                    values.append(user[key]) if key in user else values.append(None)
                return values
            if len(keys) == 1 and keys[0] in user:
                return user[keys[0]]

        return user

    @staticmethod
    def get_token(request_obj=None):
        if request_obj:
            header = request_obj.headers.get('Authorization', None)
        else:
            header = request.headers.get('Authorization', None)
        if not header:
            raise Exception('Authorization Header is Expected')

        header_parts = header.split()

        if header_parts[0].lower() != 'bearer':
            raise Exception('Authorization Header Must Start With Bearer')
        elif len(header_parts) > 1:
            return header_parts[1]

        raise Exception('Internal Application Error')

    @staticmethod
    def decode_token(token):
        jwt_secret = get_env('SECRET_KEY')
        try:
            decoded = jwt.decode(token, jwt_secret, verify=True)
            return decoded
        except jwt.ExpiredSignature:
            raise Exception('Token is Expired')
        except jwt.DecodeError:
            raise Exception('Invalid Token - Could Not Verify Signature')

    @staticmethod
    def check_location_header():
        if request.method != 'OPTIONS':
            for endpoint in Auth.location_header_ignore:
                if request.path.find(endpoint) > -1:  # If endpoint in request.path, ignore this check
                    return None
            try:
                Auth.get_location()
            except Exception as e:
                return make_response(jsonify({'msg': str(e)}), 400)

    @staticmethod
    def get_location():
        location = request.headers.get('X-Location', None)
        if not location:
            raise Exception('Location Header is Expected')
        if not location.isdigit():
            raise Exception('Location Header Value is Invalid')
        return int(location)
