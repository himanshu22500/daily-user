from rest_framework import serializers

class CreateUserSerializer(serializers.Serializer):
    full_name = serializers.CharField(max_length=255)
    manager_id = serializers.IntegerField(required=False)
    mob_num = serializers.CharField(max_length=15)
    pan_num = serializers.CharField(max_length=10)

class DeleteUserSerializer(serializers.Serializer):
    user_id = serializers.IntegerField(required=False)
    mob_num = serializers.CharField(max_length=15,required=False)

class GetUsersSerializer(serializers.Serializer):
    user_id = serializers.CharField(max_length=255,required=False)
    manager_id = serializers.CharField(max_length=255,required=False)
    mob_num = serializers.CharField(max_length=15, required=False)


class UpdateUserSerializer(serializers.Serializer):
    user_ids = serializers.ListField(child=serializers.CharField(max_length=255), required=True)
    update_data = serializers.DictField(required=True)