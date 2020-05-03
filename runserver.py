import sys
import os
from core.app import app


def run_dev():
    port = int(os.environ.get('PORT', 5000))
    app.run(host='localhost', port=port, debug=True)


def run_prod():
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, threaded=False, debug=False)


if __name__ == "__main__":
    try:
        mode = str(sys.argv[1])
        if mode == "dev":
            run_dev()
        if mode == "prod":
            run_prod()
    except IndexError:
        print("Missing server mode argument")
