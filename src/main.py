import argparse

import uvicorn
from fastapi import FastAPI
from fastapi_pagination import add_pagination

from announcements.announcements.router import router as router_announcements
from announcements.categorys.router import router as router_category
from announcements.comments.router import router as router_comments
from announcements.complaints.router import router as router_complaints
from announcements.review.router import router as router_review
from config import settings
from core.db_utils import create_superuser
from users.router import router_auth, router_user

app = FastAPI(
    title='Advertising API',
    description='API for advertising service for test SurfIt',
    version='1.0.0',
    arbitrary_types_allowed=True,
    debug=True
)
app.include_router(
    router_auth, prefix=f'{settings.API_URL}/auth', tags=['Authentication'],
)
app.include_router(
    router_user, prefix=f'{settings.API_URL}/users', tags=['Users'],
)
app.include_router(
    router_announcements, prefix=f'{settings.API_URL}/announcements',
    tags=['Announcements'],
)
app.include_router(
    router_category, prefix=f'{settings.API_URL}/categorys',
    tags=['Categorys'],
)
app.include_router(
    router_comments, prefix=f'{settings.API_URL}/announcements',
    tags=['Comments'],
)
app.include_router(
    router_complaints, prefix=f'{settings.API_URL}/announcements',
    tags=['Complaints'],
)
app.include_router(
    router_review, prefix=f'{settings.API_URL}/announcements',
    tags=['Reviews'],
)
add_pagination(app)


@app.get('/',)
def index():
    return {'data': {'name': 'Its base!'}}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'create_superuser', type=str, nargs='?',
        help='Create user with superuser role'
    )
    parser.add_argument(
        '--host', default='127.0.0.1', help='Host IP address for the server'
    )
    parser.add_argument(
        '--port', type=int, default=8000, help='Port for the server'
    )
    args = parser.parse_args()
    if args.create_superuser == 'create_superuser':
        print(create_superuser())
    else:
        uvicorn.run('main:app', host=args.host, port=args.port, reload=True)


if __name__ == '__main__':
    main()
