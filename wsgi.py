import os
import sys
from core.app import app
from core import views


def run_dev():
    port = int(os.environ.get('PORT', 5000))
    app.run(host='localhost', port=port, debug=True)


if __name__ == "__main__":
    try:
        mode = str(sys.argv[1])
        if mode == "dev":
            run_dev()
        else:
            print("Invalid argument")
    except IndexError:
        app.run()
