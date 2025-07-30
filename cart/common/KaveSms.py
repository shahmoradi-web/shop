from kavenegar import *
from urllib.error import HTTPError


def send_sms_with_template(receptor, tokens: dict, template):
    """
        sending sms that needs template
    """
    try:
        api = KavenegarAPI(
            '5530455A5A45644B5179414C6F737044477648354B426A456D414D522F4A58345545665258646A744F6D6B3D'
        )
        params = {
            'receptor': receptor,
            'template': template,
        }
        for key, value in tokens.items():
            params[key] = value

        response = api.verify_lookup(params)
        print(response)
        return True
    except APIException as e:
        print(e)
        return False
    except HTTPError as e:
        print(e)
        return False


def send_sms_normal(receptor, message):
    try:
        api = KavenegarAPI(
            '5530455A5A45644B5179414C6F737044477648354B426A456D414D522F4A58345545665258646A744F6D6B3D')
        params_buyer = {
            'receptor': receptor,
            'message': message,
            'sender': '20006535'
        }
        response = api.sms_send(params_buyer)
        print(response)
    except APIException as e:
        print(e)
    except HTTPError as e:
        print(e)