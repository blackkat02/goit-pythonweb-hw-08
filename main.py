from fastapi import FastAPI
import logging

app = FastAPI()


@app.get("/")
def read_root():
    response = {"message": "Welcome to FastAPI"}
    return response


# from fastapi import FastAPI
# import logging

# from fastapi import FastAPI, Depends, HTTPException, status
# from sqlalchemy import text
# from sqlalchemy.orm import Session

# from src.database.db import session_manager

# app = FastAPI()


# @app.get("/")
# def read_root(db: Session = Depends(session_manager)):
#     try:
#         # Make request
#         result = db.execute(text("SELECT 1")).fetchone()
#         if result is None:
#             raise HTTPException(
#                 status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#                 detail="Database is not configured correctly",
#             )
#         return {"message": "Welcome to FastAPI!"}
#     except Exception as e:
#         print(e)
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail="Error connecting to the database",
#         )


# if __name__ == "__main__":
#     import uvicorn

#     uvicorn.run(app, host="127.0.0.1", port=8000)
