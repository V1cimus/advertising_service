import argparse

import uvicorn
from announcements.categorys.router import router as router_category
from core.db_utils import create_superuser
from fastapi import FastAPI
from users.router import router_auth, router_user

from config import settings

app = FastAPI(arbitrary_types_allowed=True, debug=True)
app.include_router(
    router_auth, prefix=f'{settings.API_URL}/auth', tags=['Authentication'],
)
app.include_router(
    router_user, prefix=f'{settings.API_URL}/users', tags=['Users'],
)
app.include_router(
    router_category, prefix=f'{settings.API_URL}/categorys',
    tags=['Categorys'],
)


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
