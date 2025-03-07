import requests
from msal import ConfidentialClientApplication
from datetime import datetime, timezone
import unicornhathd
from PIL import Image, ImageDraw, ImageFont
from enum import Enum
import time
from dotenv import load_dotenv
import os

class Status(Enum):
    AVAILABLE = 0
    BUSY = 1
    AWAY = 2
    DO_NOT_DISTURB = 3
    BE_RIGHT_BACK = 4
    OFFLINE = 5


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
    start = datetime.now(timezone.utc)
    end = start.replace(hour=23, minute=59, second=59)
    start_str = f"{start.year}-{start.month:02d}-{start.day:02d}T{start.hour:02d}:{start.minute:02d}:{start.second:02d}Z"
    end_str = f"{end.year}-{end.month:02d}-{end.day:02d}T{end.hour:02d}:{end.minute:02d}:{end.second:02d}Z"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    response = requests.get(
        f"https://graph.microsoft.com/v1.0/users/{user_id}/calendarView?startDateTime={start_str}&endDateTime={end_str}&$top=1&$select=subject,start,end",
        headers=headers
    )
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error fetching user calendar: {response.status_code} - {response.text}")

def get_remaining_minutes(current_event):
    now = datetime.now(timezone.utc)
    end_time = datetime.fromisoformat(current_event['end']['dateTime']).replace(tzinfo=timezone.utc)
    
    remaining_time = end_time - now
    return int(remaining_time.total_seconds() // 60)

def display_status_on_unicornhat(status: Status, remaining_minutes: int):
    unicornhathd.rotation(0)
    unicornhathd.brightness(0.5)
    width, height = unicornhathd.get_shape()

    # Clear the display
    unicornhathd.clear()

    background_color = (0, 0, 0)
    if status == Status.AVAILABLE:
        background_color = (0, 164, 0)
    elif status == Status.BUSY:
        background_color = (164, 0, 0)
    elif status == Status.AWAY:
        background_color = (255, 165, 0)
    elif status == Status.DO_NOT_DISTURB:
        background_color = (128, 0, 128)

    # Create an image with the remaining minutes as text
    font_color = (255, 255, 255)
    image = Image.new('RGB', (width, height), background_color)
    draw = ImageDraw.Draw(image)


    if remaining_minutes > 0:
        font_path="Micro5-Regular.ttf"
        font_size = 18
        font = ImageFont.truetype(font_path, font_size)

        if remaining_minutes > 60:
            text = f">1h"
        else:
            text = f"{remaining_minutes}"

        text_bbox = draw.textbbox((0, 0), text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        text_x = (width - text_width) // 2 + 1
        text_y = 0
        draw.text((text_x, text_y), text, font=font, fill=font_color)
        image = image.transpose(Image.FLIP_LEFT_RIGHT)
    

    # Display the image on the Unicorn HAT HD
    for y in range(height):
        for x in range(width):
            r, g, b = image.getpixel((x, y))
            unicornhathd.set_pixel(x, y, r, g, b)

    unicornhathd.show()

def run(access_token, user_id):
    status_mapping = {
        "Available": Status.AVAILABLE,
        "Busy": Status.BUSY,
        "Away": Status.AWAY,
        "DoNotDisturb": Status.DO_NOT_DISTURB,
        "BeRightBack": Status.BE_RIGHT_BACK,
        "Offline": Status.OFFLINE,
    }

    current_status = ""
    currnet_remaining_minutes = 0
    while True:
        user_status = get_user_status(access_token, user_id)
        status_str = user_status.get("availability")

        if status_str != current_status:
            print(f"Status changed to: {status_str}")
            current_status = status_str
        status = status_mapping.get(status_str, Status.AVAILABLE)

        remaining_minutes = 0
        if status == Status.BUSY or status == Status.DO_NOT_DISTURB:
            user_calendar = get_user_calendar(access_token, user_id)
            if user_calendar['value']:
                current_event = user_calendar['value'][0]
                event_start = datetime.fromisoformat(current_event['start']['dateTime']).replace(tzinfo=timezone.utc)
                if event_start <= datetime.now(timezone.utc):
                    remaining_minutes = get_remaining_minutes(current_event)
        

        if currnet_remaining_minutes != remaining_minutes:
            print(f"Remaining minutes changed to: {remaining_minutes}")
            currnet_remaining_minutes = remaining_minutes

        display_status_on_unicornhat(status, remaining_minutes)
        time.sleep(60)



if __name__ == "__main__":
    load_dotenv()

    client_id = os.getenv("client_id")
    client_secret = os.getenv("client_secret")
    tenant_id = os.getenv("tenant_id")
    user_id = os.getenv("user_id")

    access_token = get_access_token(client_id, client_secret, tenant_id)
    
    run(access_token, user_id)
