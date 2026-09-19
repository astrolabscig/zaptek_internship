from typing import Optional
from datetime import datetime, timezone
from fastapi import APIRouter, HTTPException

from app.data import applications
from app.schemas import Application, ApplicationCreate, ApplicationUpdate, Status

router = APIRouter(prefix="/applications", tags=["Applications"])


# Helper functions
def find_application(application_id: int):
    for application in applications:
        if application["id"] == application_id:
            return application
    raise HTTPException(status_code=404, detail=f"Application with id {application_id} not found")

def email_taken(email: str, exclude_id: Optional[int] = None):
    for application in applications:
        if application["email"].lower() == email.lower() and application["id"] != exclude_id:
            return True
    return False

# READ
@router.get("/", response_model=list[Application])
def get_all_applications(status: Optional[Status] = None):
    if status is None:
        return applications
    return [app for app in applications if app["status"] == status.value]

@router.get("/{application_id}", response_model=Application)
def get_application(application_id: int):
    return find_application(application_id)

# CREATE
@router.post("/", response_model=Application, status_code=201)
def create_application(payload: ApplicationCreate):
    if email_taken(payload.email):
        raise HTTPException(status_code=409, detail="An application with this email already exists")

    new_id = max((app["id"] for app in applications), default=0) + 1

    new_application = payload.model_dump(mode="json")
    new_application["id"] = new_id
    new_application["status"] = "pending"
    new_application["submittedAt"] = datetime.now(timezone.utc).isoformat()

    applications.append(new_application)
    return new_application

# UPDATE(full)
@router.put("/{application_id}", response_model=Application)
def replace_application(application_id: int, payload: ApplicationCreate):
    application = find_application(application_id)

    if email_taken(payload.email, exclude_id=application_id):
        raise HTTPException(status_code=409, detail="Another application already uses this email")

    application.update(payload.model_dump(mode="json"))
    return application

# UPDATE(partial)
@router.patch("/{application_id}", response_model=Application)
def update_application(application_id: int, payload: ApplicationUpdate):
    application = find_application(application_id)
    changes = payload.model_dump(mode="json", exclude_unset=True)

    if not changes:
        raise HTTPException(status_code=400, detail="No fields provided to update")

    if "email" in changes and email_taken(changes["email"], exclude_id=application_id):
        raise HTTPException(status_code=409, detail="Another application already uses this email")

    application.update(changes)
    return application

# DELETE
@router.delete("/{application_id}", status_code=204)
def delete_application(application_id: int):
    application = find_application(application_id)
    applications.remove(application)

