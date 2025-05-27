import uvicorn

from open_cec_api.api.start import app
from open_cec_api.settings import settings

if __name__ == "__main__":
    # TODO can also set log level or reload
    uvicorn.run(
        app,
        host=settings.host,
        port=settings.port,
    )
