import pkg_resources

from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from starlette.responses import RedirectResponse, JSONResponse
from routers import (
    auth, media, video, photo, user,
    igtv, clip, album, story,
    insights
)
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    servers=[
        {"url": "https://mymacserver.ddns.net:9443", "description": "Home environment"},
    ],
    root_path="/instaloaderweb-rest",
)

app.include_router(auth.router)
app.include_router(media.router)
app.include_router(video.router)
app.include_router(photo.router)
app.include_router(user.router)
app.include_router(igtv.router)
app.include_router(clip.router)
app.include_router(album.router)
app.include_router(story.router)
app.include_router(insights.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags=["system"], summary="Redirect to /docs")
async def root():
    """Redirect to /docs
    """
    return RedirectResponse(url="/instaloaderweb-rest/docs")


@app.get("/version", tags=["system"], summary="Get dependency versions")
async def version():
    """Get dependency versions
    """
    versions = {}
    for name in ('instagrapi', ):
        item = pkg_resources.require(name)
        if item:
            versions[name] = item[0].version
    return versions


@app.exception_handler(Exception)
async def handle_exception(request, exc: Exception):
    return JSONResponse({
        "detail": str(exc),
        "exc_type": str(type(exc).__name__)
    }, status_code=500)


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title="instaloaderweb-rest",
        version="1.0.0",
        description="RESTful API Service for instagrapi",
        routes=app.routes,
        servers=[
            {"url": "https://mymacserver.ddns.net:9443/instaloaderweb-rest", "description": "Home environment"},
        ]
    )

    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
