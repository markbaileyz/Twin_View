import json
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.db.engine import get_db
from app.db.models import RvtoolsImport

router = APIRouter(prefix="/rvtools", tags=["rvtools"])


@router.post('/import')
async def import_xlsx(file: UploadFile = File(...), source_label: str = "rvtools", db: Session = Depends(get_db)):
    rec = RvtoolsImport(filename=file.filename, source_label=source_label, tab_counts=json.dumps({}), total_rows=0, findings_generated=0)
    db.add(rec)
    db.commit()
    db.refresh(rec)
    return {
        "id": rec.id,
        "filename": rec.filename,
        "source_label": rec.source_label,
        "imported_at": rec.imported_at,
        "tab_counts": {},
        "total_rows": 0,
        "findings_generated": 0,
        "findings": [],
    }


@router.get('/imports')
def list_imports(limit: int = 50, offset: int = 0, db: Session = Depends(get_db)):
    rows = db.execute(select(RvtoolsImport).order_by(RvtoolsImport.imported_at.desc()).offset(offset).limit(limit)).scalars().all()
    total = db.scalar(select(func.count()).select_from(RvtoolsImport)) or 0
    return {
        "imports": [
            {
                "id": r.id,
                "filename": r.filename,
                "source_label": r.source_label,
                "imported_at": r.imported_at,
                "tab_counts": json.loads(r.tab_counts or "{}"),
                "total_rows": r.total_rows,
                "findings_generated": r.findings_generated,
            }
            for r in rows
        ],
        "total": total,
    }


@router.get('/imports/{import_id}')
def get_import(import_id: str, db: Session = Depends(get_db)):
    row = db.get(RvtoolsImport, import_id)
    if not row:
        raise HTTPException(status_code=404, detail="import not found")
    return {
        "id": row.id,
        "filename": row.filename,
        "source_label": row.source_label,
        "imported_at": row.imported_at,
        "tab_counts": json.loads(row.tab_counts or "{}"),
        "total_rows": row.total_rows,
        "findings_generated": row.findings_generated,
    }


@router.delete('/imports/{import_id}')
def delete_import(import_id: str, db: Session = Depends(get_db)):
    row = db.get(RvtoolsImport, import_id)
    if row:
        db.delete(row)
        db.commit()
    return {"status": "deleted", "id": import_id}


@router.get('/imports/{import_id}/tabs')
def list_tabs(import_id: str):
    return {"import_id": import_id, "tabs": []}


@router.get('/imports/{import_id}/tabs/{tab_name}')
def tab_rows(import_id: str, tab_name: str):
    return {"import_id": import_id, "tab_name": tab_name, "rows": [], "total": 0}


@router.get('/export/standard/{import_id}')
def export_standard(import_id: str):
    return {"status": "not_implemented", "import_id": import_id, "kind": "standard"}


@router.get('/export/enriched/{import_id}')
def export_enriched(import_id: str):
    return {"status": "not_implemented", "import_id": import_id, "kind": "enriched"}
