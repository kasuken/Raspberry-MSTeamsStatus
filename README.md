# 🚀 Raspberry Pi 5 - MS Teams Status Indicator

A simple and effective way to display your **Microsoft Teams status** outside your door using a **Raspberry Pi 5** and a **Unicorn HAT HD** LED matrix. Never get interrupted again while on a call! 📢🚦

## ✨ Features
- **Real-time MS Teams status sync** 🟢🔴🟡
- **Displays meeting time remaining** ⏳
- **Uses Raspberry Pi 5 & Unicorn HAT HD** 🎨
- **Customizable colors & effects** 🌈
- **Low power consumption** ⚡
- **Works headless (no monitor needed)** 🖥️🚫

---

## 🛠️ Hardware Requirements
- **Raspberry Pi 5** (or compatible)
- **Unicorn HAT HD** (16x16 RGB LED matrix)
- **MicroSD Card** (with Raspberry Pi OS installed)
- **Power supply** (USB-C recommended)
- **Internet connection** (Wi-Fi or Ethernet)

## 📦 Software Requirements
- **Raspberry Pi OS** (Latest version recommended)
- **Python 3**
- **MS Teams API Access**
- **Unicorn HAT HD Python Library**
- **Requests & asyncio libraries**

---

## 🔧 Installation & Setup

### 1️⃣ Install Raspberry Pi OS
Follow the official guide to install **Raspberry Pi OS** on your SD card: [Raspberry Pi Imager](https://www.raspberrypi.com/software/)

### 2️⃣ Set Up the Unicorn HAT HD
```bash
sudo apt update && sudo apt install python3-pip python3-dev
pip3 install unicornhathd
```

### 4️⃣ Get Microsoft Teams Status via API
You need to authenticate with **Microsoft Graph API** to fetch your Teams status.

#### Steps:
1. **Register an Azure App**
   - Go to **Azure Portal** → App registrations → **New registration**
   - Set **Redirect URI**: `http://localhost`
   - Note your **Client ID** & **Tenant ID**
2. **Grant API Permissions**
   - `Presence.Read` (for Teams status)
   - `Calendars.Read` (to fetch meeting details)
   - Click **Grant admin consent**
3. **Generate a Client Secret**
   - Store the **Client Secret** securely

### 5️⃣ Configure the Script
Create a `.env` file:
```ini
AZURE_TENANT_ID=your-tenant-id
AZURE_CLIENT_ID=your-client-id
AZURE_CLIENT_SECRET=your-client-secret
```

### 6️⃣ Run the Script
```bash
python3 teams_status.py
```

---

## 🎨 Customization
This project divides the **Unicorn HAT HD** display into two sections:
- **Upper part:** Displays the Teams status (Available, Busy, Away, Do Not Disturb)
- **Lower part:** Shows the number of minutes until the end of the current meeting

Modify `teams_status.py` to:
- Adjust colors for **Available, Busy, Away, Do Not Disturb**
- Change font size and positioning of the countdown timer ⏳
- Add animations or effects 🎭

Example:
```python
STATUS_COLORS = {
    "Available": (0, 255, 0),  # Green
    "Busy": (255, 0, 0),       # Red
    "Away": (255, 165, 0),     # Orange
    "DoNotDisturb": (128, 0, 128) # Purple
}
```

## 🛠️ Troubleshooting
- **LEDs not lighting up?** Ensure Unicorn HAT HD is installed properly.
- **Status not updating?** Check API permissions in Azure.
- **Meeting time not showing?** Ensure `Calendars.Read` permission is granted.
- **Authentication issues?** Double-check your `.env` credentials.

---

## 📜 License
This project is licensed under the **MIT License**.

## 🤝 Contributing
Feel free to open an **issue** or submit a **pull request**!

## 💡 Future Improvements
- 🖥️ **Web-based status dashboard**

---

💙 **Made with love for Hackathons** 🚀
