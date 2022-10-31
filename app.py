import threading
import atexit
from flask import Flask
import random

COLORS = ['RED', 'BLUE', 'GREEN']

# variables that are accessible from anywhere
color = random.choice(COLORS)

# lock to control access to variable
dataLock = threading.Lock()
# thread handler
colorThread = None

def create_app():
    app = Flask(__name__)

    def interrupt():
        global colorThread
        colorThread.cancel()

    def setColor():
        global color
        global colorThread
        with dataLock:
            color = random.choice(COLORS)

        # Set the next thread to happen
        colorThread = threading.Timer(random.uniform(0.5, 2.5), setColor, ())
        colorThread.start()

    def startThread():
        # Do initialisation stuff here
        global colorThread
        # Create your thread
        colorThread = threading.Timer(random.uniform(0.5, 2.5), setColor, ())
        colorThread.start()

    @app.route('/color')
    def success():
        return color

    # Initiate
    startThread()
    # When you kill Flask (SIGTERM), clear the trigger for the next thread
    atexit.register(interrupt)
    return app

app = create_app()

if __name__ == '__main__':
    app.run()