
from suttonforecast import forecast
from os import environ

if __name__ == "__main__":
    try:
        from auth_keys import BOT_HTTP, CHANNEL_ID, ADMIN_ID
    except ImportError:
        BOT_HTTP = environ["SUT_BOT"]
        CHANNEL_ID = environ["SUT_CHANNEL"]
        ADMIN_ID = environ["SUT_ADMIN"]

    forecast.Forecast(BOT_HTTP, CHANNEL_ID, ADMIN_ID)