from accounts.models import Account
from health.models import BodyParameters

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
            # "last_visit": user_profile.last_login
        }
    except Account.DoesNotExist:
        return {"error": "User profile not found."}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}


def dietician_clients_health_summary(dietician_id):
    try:
        # Fetch users from PostgreSQL by dietician_id
        # users = Account.objects.filter(dietician_id=dietician_id)
        users = Account.objects.filter()
        total_clients = users.count()

        healthy_clients = 0
        need_attention = 0
        client_list = []

        for user in users:
            # Fetch latest body parameter from MongoDB
            latest_param = BodyParameters.objects.filter(user_id=user.id).order_by('-created_at').first()

            # Classify health based on score
            if latest_param:
                if latest_param.score > 60:
                    healthy_clients += 1
                else:
                    need_attention += 1

            # client_list.append({
            #     "id": user.id,
            #     "name": user.username,
            #     "email": user.email,
            #     "phone_number": user.phone_number,
            #     "gender": user.gender,
            #     "DOB": user.DOB,
            #     "profession": user.profession,
            #     "location": user.location
            # })

        return {
            "totalClients": total_clients,
            "healthyClients": healthy_clients,
            "needAttention": need_attention,
            # "clients": client_list
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }