import argparse
import os

import uvicorn

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-H",
        "--host",
        type=str,
        default="0.0.0.0",
        help="The host where the app is running, default is 0.0.0.0",
    )
    parser.add_argument(
        "-p",
        "--port",
        type=int,
        default=5000,
        help="The port where the app is running, default is 5000",
    )
    parser.add_argument(
        "-r",
        "--reload",
        type=bool,
        help="The server reloads on code changes, default is False",
        default=False,
    )

    args = parser.parse_args()

    HOST = args.host
    PORT = args.port
    RELOAD = args.reload

    uvicorn.run("app.main:app", port=int(PORT), host=HOST, reload=RELOAD)
