from app import create_app
from app.scheduler import start_scheduler
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('price_alert.log'),
        logging.StreamHandler()
    ]
)

app = create_app()

if __name__ == '__main__':
    start_scheduler(app)
    app.run(debug=True, use_reloader=False)
