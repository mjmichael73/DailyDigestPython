import threading
import time
import schedule


class DailyDigestScheduler(threading.Thread):

    def __init__(self):
        super().__init__()
        self.__stop_running = threading.Event()

    def schedule_daily(self, hour, minute, job):
        schedule.clear()
        schedule.every().day.at(f"{hour:02d}:{minute:02d}").do(job)

    def run(self):
        self.__stop_running.clear()
        while not self.__stop_running.is_set():
            schedule.run_pending()
            time.sleep(1)

    def stop(self):
        self.__stop_running.set()


if __name__ == "__main__":
    import dd_email
    email = dd_email.DailyDigestEmail()
    scheduler = DailyDigestScheduler()
    scheduler.start()

    hour = time.localtime().tm_hour
    minute = time.localtime().tm_min + 1
    print(f"Scheduling test email for {hour:02d}:{minute:02d}")
    scheduler.schedule_daily(hour, minute, email.send_email)
    time.sleep(60)
    scheduler.stop()
