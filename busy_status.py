import requests
from msal import ConfidentialClientApplication
from datetime import datetime, timezone
import unicornhathd

def get_access_token(client_id, client_secret, tenant_id):
    app = ConfidentialClientApplication(
        client_id,
        authority=f"https://login.microsoftonline.com/{tenant_id}",
        client_credential=client_secret,
    )
    result = app.acquire_token_for_client(scopes=["https://graph.microsoft.com/.default"])
    if "access_token" in result:
        return result["access_token"]
    else:
        raise Exception("Could not acquire access token")

def get_user_status(access_token, user_id):
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    response = requests.get(
        f"https://graph.microsoft.com/v1.0/users/{user_id}/presence",
        headers=headers
    )
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error fetching user status: {response.status_code} - {response.text}")

def get_user_calendar(access_token, user_id):
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    response = requests.get(
        f"https://graph.microsoft.com/v1.0/users/{user_id}/calendar/events",
        headers=headers
    )
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error fetching user calendar: {response.status_code} - {response.text}")

def get_remaining_minutes(current_event):
    end_time = datetime.fromisoformat(current_event['end']['dateTime']).replace(tzinfo=timezone.utc)
    now = datetime.now(timezone.utc)
    remaining_time = end_time - now
    return remaining_time.total_seconds() // 60

def display_status_on_unicornhat(is_busy, remaining_minutes):
    unicornhathd.rotation(0)
    unicornhathd.brightness(0.5)
    width, height = unicornhathd.get_shape()

    # Clear the display
    unicornhathd.clear()

    # Display busy status
    color = (255, 0, 0) if is_busy else (0, 255, 0)
    for y in range(height // 2):
        for x in range(width):
            unicornhathd.set_pixel(x, y, *color)

    # Display remaining minutes
    for x in range(min(remaining_minutes, width)):
        unicornhathd.set_pixel(x, height - 1, 0, 0, 255)

    unicornhathd.show()

if __name__ == "__main__":
    client_id = "YOUR_CLIENT_ID"
    client_secret = "YOUR_CLIENT_SECRET"
    tenant_id = "YOUR_TENANT_ID"
    user_id = "USER_ID"

    access_token = get_access_token(client_id, client_secret, tenant_id)
    user_status = get_user_status(access_token, user_id)
    print(user_status)

    user_calendar = get_user_calendar(access_token, user_id)
    if user_calendar['value']:
        current_event = user_calendar['value'][0]
        remaining_minutes = get_remaining_minutes(current_event)
        print(f"Remaining minutes until the current appointment ends: {remaining_minutes}")
    else:
        remaining_minutes = 0
        print("No current appointments found.")

    is_busy = user_status.get("availability") == "Busy"
    display_status_on_unicornhat(is_busy, remaining_minutes)
