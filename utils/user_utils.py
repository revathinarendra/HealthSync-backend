from accounts.models import Account

def fetch_user_profile_by_id(profile_id):
    try:
        profile_id = int(profile_id)
    except ValueError:
        return {"error": 'Invalid "profile_id" format. Must be an integer.'}

    try:
        user_profile = Account.objects.get(id=profile_id)
        return {
            "name": user_profile.username,
            "DOB":user_profile.DOB,
            "gender": user_profile.gender,
            "last_visit": user_profile.last_login
        }
    except Account.DoesNotExist:
        return {"error": "User profile not found."}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}
