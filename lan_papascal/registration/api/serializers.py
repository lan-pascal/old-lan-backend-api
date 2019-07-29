class UserSignUpSerializer(serializers.ModelSerializer):
    email_confirm = serializers.EmailField(label="Confirm Email",  required=True)
    password_confirm = serializers.CharField(label="Confirm Password", required=True)
    class Meta:
        model = User
        fields = ('username', "first_name", "last_name", 'email',"email_confirm", "password","password_confirm")
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate_email_confirm(self, value):
        data = self.get_initial()
        email = data.get("email")
        email_confirm = value
        if email != email_confirm:
            raise ValidationError("The emails don't match!", code="email_confirmation_error")
        return value

    def validate_password_confirm(self, value):
        data = self.get_initial()
        password = data.get("password")
        password_confirm = value
        if password != password_confirm:
            raise ValidationError("The passwords don't match!", code="password_confirmation_error")
        return value
    
    def create(self, validated_data):
        username = validated_data["username"]
        email = validated_data["email"]
        password = validated_data["password"]

        user = User(
            username = username,
            email = email,
            )
        user.set_password(password)
        user.save()

        return validated_data

class UserSignInSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username","email","password")
        extra_kwargs = {
            'username': 
            {
                'required': settings.AUTH_BACKEND_METHOD == AuthMethod.USERNAME or settings.AUTH_BACKEND_METHOD == AuthMethod.USERNAME_EMAIL
            },
            'email' : 
            {
                'required' : settings.AUTH_BACKEND_METHOD == AuthMethod.EMAIL or settings.AUTH_BACKEND_METHOD == AuthMethod.USERNAME_EMAIL
            },
            'password': {'write_only': True}
        }

    def validate(self, data):
        username = data["username"]
        email = data["email"]
        password = data["passsword"]

        user = authenticate(self.data["request"],username=username,email=email,password=password)
        
        if user:
            if not user.is_active:
                raise ValidationError("This user account is inactive") 
        else
            raise ValidationError("You were unable to sign in with the provided credentials")

        data['user'] = user
        return value

    
class UserPasswordChangeSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(label="Old Password", required=True)
    new_password = serializers.CharField(label="New Password", required=True)
    new_password_confirmW = serializers.CharField(label="Confirm New Password", required=True)

    class Meta:
        model = User
        fields = ("old_password","new_password","new_password_confirm")}

    def validate_old_password(self, value):
        invalid_password_conditions = (
            self.user,
            not self.user.check_password(value)
        )

        if all(invalid_password_conditions):
            err_msg = ("Your old password is invalid.")
            raise ValidationError(err_msg)
        return value

    def validate_new_password(self, value):
        new_password = value
        validate_password(new_password,self.user)
        return value

    def validate_new_password_confirm(self, value):
        data = self.get_initial()
        password = data.get("password")
        password_confirm = value
        if password != password_confirm:
            raise ValidationError("The passwords don't match!", code="password_confirmation_error")
        return value