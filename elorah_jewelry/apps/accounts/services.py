from django.core.exceptions import ValidationError, PermissionDenied
from django.utils import timezone
from django.core.signing import TimestampSigner, BadSignature, SignatureExpired
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from .models import CustomUser, UserProfile, Address

signer = TimestampSigner()
token_generator = PasswordResetTokenGenerator()

class AccountService:
    @staticmethod
    def register_user(email: str, password: str, first_name: str, last_name: str, phone: str = None) -> CustomUser:
        if CustomUser.objects.filter(email__iexact=email).exists():
            raise ValidationError("A user with that email already exists.")
        
        user = CustomUser.objects.create_user(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            phone=phone
        )
        UserProfile.objects.create(user=user)
        AccountService.send_verification_email(user)
        return user

    @staticmethod
    def send_verification_email(user: CustomUser) -> None:
        token = signer.sign(user.pk)
        # In a real setup, we would queue a Celery task here to send the email
        # e.g., send_verification_email_task.delay(user.email, token)
        pass

    @staticmethod
    def verify_email(token: str) -> CustomUser:
        try:
            # Token valid for 24 hours (86400 seconds)
            user_id = signer.unsign(token, max_age=86400)
            user = CustomUser.objects.get(pk=user_id)
            if not user.is_email_verified:
                user.is_email_verified = True
                user.email_verified_at = timezone.now()
                user.save(update_fields=["is_email_verified", "email_verified_at"])
            return user
        except (BadSignature, SignatureExpired, CustomUser.DoesNotExist):
            raise ValidationError("Invalid or expired token.")

    @staticmethod
    def initiate_password_reset(email: str) -> None:
        user = CustomUser.objects.filter(email__iexact=email).first()
        if user:
            token = token_generator.make_token(user)
            # In a real setup, queue a Celery task to send the reset email
            pass

    @staticmethod
    def reset_password(user: CustomUser, token: str, new_password: str) -> None:
        if not token_generator.check_token(user, token):
            raise ValidationError("Invalid or expired token.")
        user.set_password(new_password)
        user.save()

    @staticmethod
    def set_default_address(user: CustomUser, address_id: int, address_type: str) -> Address:
        try:
            address = Address.objects.get(pk=address_id, user=user)
        except Address.DoesNotExist:
            raise PermissionDenied("Address does not exist or does not belong to you.")
        
        if address_type == "shipping":
            Address.objects.filter(user=user, is_default_shipping=True).update(is_default_shipping=False)
            address.is_default_shipping = True
        elif address_type == "billing":
            Address.objects.filter(user=user, is_default_billing=True).update(is_default_billing=False)
            address.is_default_billing = True
        else:
            raise ValidationError("Invalid address type")
            
        address.save()
        return address
