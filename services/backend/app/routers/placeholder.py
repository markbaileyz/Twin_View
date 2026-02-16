from fastapi import APIRouter

def make_router(prefix: str, tag: str):
    r = APIRouter(prefix=prefix, tags=[tag])
    @r.get('')
    def root():
        return {'status': 'not_implemented', 'endpoint': prefix}
    return r
