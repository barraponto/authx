from itsdangerous import BadTimeSignature, SignatureExpired, URLSafeTimedSerializer

CASUAL_UT = False


class SignatureSerializer:
    def __init__(self, secret_key, expired_in=0):
        """
        Initialize the serializer with a secret key and an optional expiration time.
        """
        self.ser = URLSafeTimedSerializer(secret_key)
        self.expired_in = expired_in

    def encode(self, dict_obj):
        return self.ser.dumps(dict_obj)

    def decode(self, token):
        if token is None:
            return None, "NoTokenSpecified"
        try:
            if self.expired_in == 0:
                decoded_obj = self.ser.loads(token)
            else:
                decoded_obj = self.ser.loads(token, max_age=self.expired_in)
        except SignatureExpired:
            return None, "SignatureExpired"
        except BadTimeSignature:
            return None, "InvalidSignature"

        return decoded_obj, None


if CASUAL_UT:
    serializer = SignatureSerializer('MY_SECRET_KEY', expired_in=1)
    session_id = 1
    dict_obj = {'session_id': session_id}
    token = serializer.encode(dict_obj)
    data, err = serializer.decode(token)
    assert (
        data is not None and err is None and data['session_id'] == 1
    ), "Failed to decode or session_id does not match."
