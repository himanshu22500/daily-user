import uuid

class UUIDMixin:
    @staticmethod
    def is_valid_uuid_v4(uuid_str):
        try:
            uuid_obj = uuid.UUID(uuid_str, version=4)
        except ValueError:
            return False
        return True