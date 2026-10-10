from fastapi import BackgroundTasks, APIRouter
import time

router = APIRouter()

def write_log(massage: str):
    print(f"BACKGROUND TASK: {massage}")
    time.sleep(5)
    with open("log.txt", mode="a") as log:
        log.write(f"{massage}\n")
    print('BACKGROUND TASK: Completed writing to log.')

@router.post("/send-notification/{email}")
def send_notification(email: str, background_task: BackgroundTasks):
    background_task.add_task(write_log, f"Sending notificatio to {email} with message: It's too long!")
    return {"massage": "Notification will be sent in the background."}