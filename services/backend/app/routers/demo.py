from fastapi import APIRouter, HTTPException
from app.connectors.demo import demo_generator
from app.db.engine import SessionLocal

router = APIRouter(prefix="/demo", tags=["demo"])


@router.post('/start')
async def start_demo():
    ok = await demo_generator.start(SessionLocal)
    if not ok:
        raise HTTPException(status_code=409, detail='already running')
    return {"status": "running"}


@router.post('/stop')
async def stop_demo():
    ok = await demo_generator.stop()
    if not ok:
        raise HTTPException(status_code=409, detail='not running')
    return {"status": "stopped"}


@router.get('/status')
def status_demo():
    return {"running": demo_generator.running, "events_generated": demo_generator.events_generated}
