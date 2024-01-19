import argparse

import uvicorn
from fastapi import FastAPI
from core.database import Base, engine

app = FastAPI(arbitrary_types_allowed=True, debug=True)
Base.metadata.create_all(bind=engine)


@app.get('/',)
def index():
    return {'data': {'name': 'Its base!'}}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--host', default='127.0.0.1', help='Host IP address for the server'
    )
    parser.add_argument(
        '--port', type=int, default=8000, help='Port for the server'
    )
    args = parser.parse_args()
    uvicorn.run('main:app', host=args.host, port=args.port, reload=True)


if __name__ == '__main__':
    main()
