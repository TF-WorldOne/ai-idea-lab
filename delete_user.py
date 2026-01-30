import firebase_admin
from firebase_admin import credentials, auth
import os

# Initialize app with service account
try:
    cred = credentials.Certificate("service-account-key.json")
    firebase_admin.initialize_app(cred)

    email = "tf@xworld.one"

    try:
        user = auth.get_user_by_email(email)
        auth.delete_user(user.uid)
        print(f"Successfully deleted user: {email}")
    except auth.UserNotFoundError:
        print(f"User not found: {email}")
    except Exception as e:
        print(f"Error deleting user: {e}")
except Exception as e:
    print(f"Failed to initialize Firebase Admin: {e}")
