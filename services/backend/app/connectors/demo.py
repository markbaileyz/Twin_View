import asyncio
import random
from datetime import datetime, timezone
from sqlalchemy.orm import Session

from app.correlator.clustering import process_event

DEMO_TEMPLATES = [
    {"category": "vm_power", "severity": "info", "message": "VM '{entity}' powered on by user admin@vsphere.local", "entity_prefix": "vm-prod-"},
    {"category": "vm_power", "severity": "warning", "message": "VM '{entity}' powered off unexpectedly", "entity_prefix": "vm-prod-"},
    {"category": "storage", "severity": "error", "message": "Datastore '{entity}' usage exceeded 90% threshold", "entity_prefix": "ds-"},
    {"category": "alarm", "severity": "critical", "message": "Host '{entity}' not responding to heartbeat", "entity_prefix": "esxi-"},
]


class DemoGenerator:
    def __init__(self) -> None:
        self.running = False
        self.events_generated = 0
        self._task: asyncio.Task | None = None

    async def _loop(self, db_factory):
        while self.running:
            t = random.choice(DEMO_TEMPLATES)
            entity = f"{t['entity_prefix']}{random.randint(1,8):02d}"
            db: Session = db_factory()
            try:
                await process_event({
                    "source_type": "demo",
                    "source_name": "demo-generator",
                    "severity": t["severity"],
                    "category": t["category"],
                    "message": t["message"].format(entity=entity),
                    "entity": entity,
                    "timestamp_utc": datetime.now(timezone.utc),
                }, db)
                self.events_generated += 1
            finally:
                db.close()
            await asyncio.sleep(random.uniform(2, 5))

    async def start(self, db_factory):
        if self.running:
            return False
        self.running = True
        self._task = asyncio.create_task(self._loop(db_factory))
        return True

    async def stop(self):
        if not self.running:
            return False
        self.running = False
        if self._task:
            self._task.cancel()
        return True


demo_generator = DemoGenerator()
