from app import USER_TABLE

def get_user_from_db(user_id):
    response = USER_TABLE.get_item(Key={"user_id": user_id})
    return response.get("Item")
