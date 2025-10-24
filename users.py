from database import db
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import text
import os
from dotenv import load_dotenv
import bcrypt
import uvicorn

load_dotenv()

app = FastAPI(title="simple App", version="1.0.0")

class Simple(BaseModel):
    name: str = Field(..., example="Sam Larry")
    email: str = Field(..., example="sam@email.com")
    password: str = Field(..., example="sam123")
    userType: str = Field(..., example="student")
    
@app.post("/signup")
def signUp(input: Simple):
    try:
        duplicate_query =text("""
            SELECT * FROM users
            WHERE email = :email                     
        """)
        existing = db.execute(duplicate_query, {"email": input.email})
        if existing:
            print("email already exist")
            # raise HTTPException(status_code=400, detail="Email alreaady exist")
        
        query = text("""
            INSERT INTO users (name, email, password, userType)
            VALUES (:name, :email, :password, :userType)           
        """)
        
        salt = bcrypt.gensalt()
        hashedPassword = bcrypt.hashpw(input.password.encode('utf-8'), salt)
        print(hashedPassword)
        
        db.execute(query,{"name": input.name, "email": input.email, "password": hashedPassword, "userType": input.userType})
        db.commit()
        
        return{"message": "User created successfully",
               "data": {"name": input.name, "email": input.email, "userType": input.userType}}
    except Exception as e:
        raise HTTPException(status_code=500, detail=e)
    
class LoginRequest(BaseModel):
    email: str = Field(..., example= "sam@gmail.com")
    password: str = Field(..., example="sam123")
        
@app.post("/login")
def login(input: LoginRequest):
    try:
        query = text("""
              SELECT * FROM users WHERE email = :email
""")
        
        result = db.execute(query,{"email": input.email}).fetchone()
         
        if not result:
            raise HTTPException(status_code=401, detail = "invalid email or password")  
    
    verified_password = bcrypt.checkpw(input.password.encode('utf-8'), result.password.encode('utf-8'))
    if not verified_password:
        raise HTTPException(status_code=404, detail= "invalid email or password")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
if __name__=="__main__":
     uvicorn.run(app,host=os.getenv("host"), port=int(os.getenv("port")))

# from database import db
# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel, Field
# from sqlalchemy import text
# import os
# from dotenv import load_dotenv
# import bcrypt
# import uvicorn
# load_dotenv()
# app = FastAPI(title="Simple App", version="1.0.0")
# class Simple(BaseModel):
#     name: str = Field(..., example="Sam Larry")
#     email: str = Field(..., example="sam@email.com")
#     password: str = Field(..., example="sam123")
# @app.post("/signup")
# def signUp(input: Simple):
#     try:
#         duplicate_query =text("""
#             SELECT * FROM users
#             WHERE email = :email
#         """)
#         existing = db.execute(duplicate_query, {"email": input.email})
#         if existing:
#             print("Email already esists!")
#             # raise HTTPException(status_code=400, detail="Email already exists")
#         query = text("""
#             INSERT INTO users (name, email, password)
#             VALUES (:name, :email, :password)
#         """)
#         salt = bcrypt.gensalt()
#         hashedPassword = bcrypt.hashpw(input.password.encode('utf-8'), salt)
#         print(hashedPassword)
#         db.execute(query, {"name": input.name, "email": input.email, "password": hashedPassword})
#         db.commit()
#         return {"message": "User created successfully",
#                 "data": {"name": input.name, "email": input.email}}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail= e)
# if __name__=="__main__":
#      uvicorn.run(app,host=os.getenv("host"), port=int(os.getenv("port")))