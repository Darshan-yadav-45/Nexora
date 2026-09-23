from app.database.database import SessionLocal
from app.models.user import User
from app.schemas.user import UserResponse

db = SessionLocal()
user = db.query(User).first()
if user:
    response = UserResponse.model_validate(user)
    print(response.model_dump_json(indent=2))
else:
    print("No user found")
db.close()
