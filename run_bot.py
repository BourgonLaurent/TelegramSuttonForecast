from auth_keys import BOT_HTTP, CHANNEL_ID, ADMIN_ID
from suttonforecast import forecast

if __name__ == "__main__":
    forecast.Forecast(BOT_HTTP, CHANNEL_ID, ADMIN_ID)