from gunicorn.app.base import BaseApplication
from flask.app import Flask


class StandaloneApplication(BaseApplication):
    def __init__(self, app, options=None):
        self.options = options or {}
        self.application = app
        super().__init__()

    def load_config(self):
        config = {
            key: value
            for key, value in self.options.items()
            if key in self.cfg.settings and value is not None
        }
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application


def start(app: Flask, host: str, port: int, server: str, workers: int, debug: bool):
    if server == "gunicorn":
        StandaloneApplication(
            app=app,
            options={"bind": f"{host}:{port}", "workers": workers, "debug": debug},
        ).run()
    else:
        app.run(host=host, port=port, debug=debug)
