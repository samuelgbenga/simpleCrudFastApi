
from fastapi import APIRouter, HTTPException
from config.database import SessionLocal
from models.index import users
from schemas.index import User, UserResponseSchema
from fastapi import Depends

user = APIRouter()

# Dependency to get the session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@user.get("/")
async def read_data(db = Depends(get_db)):
    all_users = db.execute(users.select()).fetchall()

    result = []
    for user in all_users:
        user_dict = {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            # Add other fields as necessary
        }
        result.append(user_dict)

    return result

# get a user by id
@user.get("/{id}")
async def read_data_by_id(id: int, db= Depends(get_db)):
    existing_user =  db.execute(users.select().where(users.c.id == id)).fetchone()

    if existing_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    # Create a UserResponseSchema instance from the query result
    user_response = UserResponseSchema(
        id=existing_user.id,
        name=existing_user.name,
        email=existing_user.email
    )

    return user_response

@user.post("/new_user")
async def create_user(user: User, db = Depends(get_db)):

   # Check if the user already exists by email
    existing_user = db.execute(
        users.select().where(users.c.email == user.email)
    ).fetchone()

    if existing_user:
        # If user exists, raise an HTTPException
        raise HTTPException(status_code=400, detail="User already exists")

    db.execute(
        users.insert().values(
            name = user.name,
            email = user.email,
            password = user.password
        )
    )
    db.commit()
    return {"message": "User created successfully"}


@user.put("/update_user/{id}")
async def update_user(id: int, user: User, db = Depends(get_db)):
    
    
    # Check if the user exists
    existing_user = db.execute(
        users.select().where(users.c.id == id)).fetchone()
    
    if not existing_user:
        # If user exists, raise an HTTPException
        raise HTTPException(status_code=400, detail="User deos not exist")

    db.execute(
        users.update()
        .where(users.c.id == id)
        .values(
            name = user.name,
            email = user.email,
            password = user.password
        )
    )
    db.commit()

    return {"message": "User Updated successfully"}

@user.delete("/delete")
async def delete_user(id: int, db = Depends(get_db)):

    # Check if the user exists
    existing_user = db.execute(
        users.select().where(users.c.id == id)).fetchone()
    
    if not existing_user:
        # If user exists, raise an HTTPException
        raise HTTPException(status_code=400, detail="Already deleted")

    db.execute(users.delete().where(users.c.id == id))
    db.commit()
    return {"message": "User deleted successfully"}