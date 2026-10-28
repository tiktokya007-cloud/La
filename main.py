import os
import time
import requests
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# טעינת הגדרות מתוך משתני סביבה (מאובטח)
USER_KEY = os.getenv("PUSHOVER_USER_KEY")
APP_TOKEN = os.getenv("PUSHOVER_APP_TOKEN")
DIRECTORY_TO_WATCH = os.getenv("DIRECTORY_TO_WATCH", "/path/to/ftp/folder")

def send_pushover_notification(title, message):
    # הכתובת הנכונה והמלאה של ה-API של Pushover
    url = "https://pushover.net"
    payload = {
        "token": APP_TOKEN,
        "user": USER_KEY,
        "title": title,
        "message": message,
        "sound": "magic"
    }
    try:
        response = requests.post(url, data=payload)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"שגיאה בשליחת ההתראה: {e}")

class Handler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            # שימוש ב-os.path.basename כדי לתמוך בכל מערכות ההפעלה
            filename = os.path.basename(event.src_path)
            title = "🔔 קובץ חדש ב-FTP"
            message = f"הקובץ {filename} הועלה בהצלחה לתיקייה."
            send_pushover_notification(title, message)

if __name__ == "__main__":
    if not USER_KEY or not APP_TOKEN:
        print("שגיאה: חסרים מפתחות Pushover במשתני הסביבה!")
        exit(1)
        
    print(f"מתחיל לעקוב אחר התיקייה: {DIRECTORY_TO_WATCH}")
    event_handler = Handler()
    observer = Observer()
    observer.schedule(event_handler, path=DIRECTORY_TO_WATCH, recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
