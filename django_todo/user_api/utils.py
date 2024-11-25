import smtplib

from django.conf import settings
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.urls import reverse
import jwt

from .errors import InvalidTokenScope, UserBanned
from .models import Ban


# Utility Functions
# =================
def send_email(sender, recipient, subject, text, html):
    # Compose email message
    msg = f"""From: {settings.WEBSITE_NAME} <{settings.EMAIL_HOST_USER}>
To: {recipient}
Reply-To: {settings.WEBSITE_EMAIL}
Subject: {subject}
Content-Type: multipart/alternative; boundary="SECTION"

--SECTION
Content-Type: text/plain; charset="utf-8"
Content-Transfer-Encoding: quoted-printable
Content-Disposition: inline

{text}

--SECTION
Content-Type: text/html; charset="utf-8"
Content-Transfer-Encoding: quoted-printable
Content-Disposition: inline

{html}

--SECTION--"""

    # Send email
    s = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
    s.starttls()
    s.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
    s.sendmail(settings.EMAIL_HOST_USER, recipient, msg)
    s.quit()


def send_verification_email(user):
    # Generate verification token and compose URL
    token = jwt.encode(
        {
            "user_id": user.id,
            "scope": "VERIFY_EMAIL"
        },
        settings.SECRET_KEY
    )
    url = settings.WEBSITE_HOST + reverse("user-verify") + f"?token={token}"

    # Compose email message
    text = render_to_string(
        "user_api/verification_email.txt",
        {
            "WEBSITE_NAME": settings.WEBSITE_NAME,
            "url": url
        }
    )
    html = render_to_string(
        "user_api/verification_email.html",
        {
            "WEBSITE_NAME": settings.WEBSITE_NAME,
            "url": url
        }
    )

    # Send email message
    try:
        send_email(
            settings.EMAIL_HOST_USER,
            user.email,
            "Email Verification",
            text,
            html
        )

    except Exception:
        pass  # Ignore email errors. We can always do manual verification. :)


def verify_user(token):
    # Decode token
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])

    # Check token scope
    if payload["scope"] != "VERIFY_EMAIL":
        raise InvalidTokenScope(
            "The scope of the given token doesn't permit email verification.")

    # Make sure the user isn't banned
    user = User.objects.get(pk=payload["user_id"])

    if Ban.objects.filter(user=user).count():
        raise UserBanned("The user is banned.")

    # Verify user
    user.is_active = True
    user.save()


def send_password_reset_email(user):
    # Generate password reset token and URL
    token = jwt.encode(
        {
            "user_id": user.id,
            "scope": "RESET_PASSWORD"
        },
        settings.SECRET_KEY
    )
    url = settings.WEBSITE_HOST + f"/accounts/reset_password/?token={token}"

    # Compose email message
    text = render_to_string(
        "user_api/password_reset.txt",
        {
            "WEBSITE_NAME": settings.WEBSITE_NAME,
            "url": url,
            "username": user.username
        }
    )
    html = render_to_string(
        "user_api/password_reset.html",
        {
            "WEBSITE_NAME": settings.WEBSITE_NAME,
            "url": url,
            "username": user.username
        }
    )

    # Send email message
    try:
        send_email(
            settings.EMAIL_HOST_USER,
            user.email,
            "Password Reset",
            text,
            html
        )

    except Exception:
        # Ignore email errors. The process can be repeated or the user can
        # contact us for assistance.
        pass


def reset_password(token, password):
    # Decode token
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])

    # Check token scope
    if payload["scope"] != "RESET_PASSWORD":
        raise InvalidTokenScope(
            "The scope of the given token doesn't permit password resets.")

    # Reset password
    user = User.objects.get(pk=payload["user_id"])
    user.set_password(password)
    user.save()


def ban_user(user, reason=""):
    # Mark the user as inactive
    user.is_active = False
    user.save()

    # Add a ban entry
    Ban.objects.create(user=user, reason=reason)


def unban_user(user):
    # Remove ban entry
    try:
        Ban.objects.get(user=user).delete()

    except Ban.DoesNotExist:
        # Ignore this. Users that aren't banned don't need to be unbanned.
        pass

    # Mark user as active
    user.is_active = True
    user.save()
