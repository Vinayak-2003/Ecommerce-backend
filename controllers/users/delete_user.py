from sqlalchemy.orm import Session
from schemas.user_schema import User
from fastapi.responses import JSONResponse

def delete_user_by_email(email: str, db_session: Session):
    try:
        stored_user = db_session.query(User).get(email)

        if not stored_user:
            return JSONResponse(
                content=f"User with {email} does not exists !!",
                status_code=404
            )
        
        db_session.delete(stored_user)
        db_session.commit()
        db_session.refresh()

        return JSONResponse(
            content=f"User with email {email} deleted successsfully!!",
        )
    except Exception as e:
        db_session.rollback()
        print("An error raised while deleting the user", e)
        raise e
    