import datetime

LOG_FILE = "logs/system.log"

def write_log(message):

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(LOG_FILE, "a") as file:

        file.write(f"[{timestamp}] {message}\n")
