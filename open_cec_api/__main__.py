import uvicorn

from open_cec_api.settings import settings

if __name__ == "__main__":
    # TODO can also set log level
    uvicorn.run(
        "open_cec_api.api.start:app",
        host=settings.host,
        port=settings.port,
        reload=True,
        reload_dirs=["/app"],
    )
