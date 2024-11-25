import smtplib

from django.conf import settings
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.urls import reverse
import jwt


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
    token = jwt.encode({"user_id": user.id}, settings.SECRET_KEY)
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

    # Verify user
    user = User.objects.get(pk=payload["user_id"])
    user.is_active = True
    user.save()


def send_password_reset_email(user):
    # Generate password reset token and URL
    token = jwt.encode({"user_id": user.id}, settings.SECRET_KEY)
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
        pass  # Ignore email errors. The process can be repeated or the user can contact us for assistance.


def reset_password(token, password):
    # Decode token
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])

    # Reset password
    user = User.objects.get(pk=payload["user_id"])
    user.set_password(password)
    user.save()
