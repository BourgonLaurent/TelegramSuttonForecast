
from suttonforecast import forecast
from os import environ

if __name__ == "__main__":
    try:
        from auth_keys import BOT_HTTP, CHANNEL_ID, ADMIN_ID, TIME_HOUR, TIME_MIN
    except ImportError:
        BOT_HTTP = environ["SUT_BOT"]
        CHANNEL_ID = environ["SUT_CHANNEL"]
        ADMIN_ID = environ["SUT_ADMIN"]
        TIME_HOUR = environ["SUT_TIME_HOUR"]
        TIME_MIN = environ["SUT_TIME_MIN"]

    forecast.Forecast(BOT_HTTP, CHANNEL_ID, ADMIN_ID, TIME_HOUR, TIME_MIN)