from pypresence import Presence

CLIENT_ID = "1391086889125154937"  # <-- Replace with your actual Client ID

rpc = Presence(CLIENT_ID)
connected = False

def connect():
    global connected
    try:
        rpc.connect()
        connected = True
        print("✅ Connected to Discord RPC")
    except Exception as e:
        print(f"❌ Failed to connect to Discord RPC: {e}")

def update_status(details=None, state=None, large_image=None, large_text=None, small_image=None, small_text=None):
    if not connected:
        print("⚠️ Not connected to Discord RPC, cannot update status")
        return
    presence_data = {}
    if details:
        presence_data['details'] = details
    if state:
        presence_data['state'] = state
    if large_image:
        presence_data['large_image'] = large_image
    if large_text:
        presence_data['large_text'] = large_text
    if small_image:
        presence_data['small_image'] = small_image
    if small_text:
        presence_data['small_text'] = small_text

    try:
        rpc.update(**presence_data)
        print(f"🔄 Updated status: details='{details}', state='{state}'")
    except Exception as e:
        print(f"❌ Failed to update Discord status: {e}")
