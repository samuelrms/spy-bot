from datetime import datetime, timedelta


class SleepService:
    _sleep_until = None
    _manual_sleep = False

    @classmethod
    def sleep(cls, duration_seconds=None):
        if duration_seconds:
            cls._sleep_until = datetime.now() + timedelta(seconds=duration_seconds)
            cls._manual_sleep = False
        else:
            cls._sleep_until = None
            cls._manual_sleep = True

    @classmethod
    def wake(cls):
        cls._sleep_until = None
        cls._manual_sleep = False

    @classmethod
    def is_sleeping(cls):
        if cls._manual_sleep:
            return True
        if cls._sleep_until:
            if datetime.now() < cls._sleep_until:
                return True
            else:
                cls._sleep_until = None
        return False

    @classmethod
    def get_status(cls):
        if cls._manual_sleep:
            return "dormindo até ser acordado manualmente"
        if cls._sleep_until:
            if datetime.now() < cls._sleep_until:
                return f"dormindo até {cls._sleep_until.strftime('%d/%m %H:%M:%S')}"
        return "acordado"
