from rest_framework import serializers

class CreateUserSerializer(serializers.Serializer):
    full_name = serializers.CharField(max_length=255)
    manager_id = serializers.IntegerField(required=False)
    mob_num = serializers.CharField(max_length=15)
    pan_num = serializers.CharField(max_length=10)

class DeleteUserSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    mob_num = serializers.CharField(max_length=15)