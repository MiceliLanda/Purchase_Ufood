
from fastapi import APIRouter
from config.db import conn
from models.user import tableUser
from fastapi import status
from fastapi.responses import JSONResponse
from sqlalchemy import select
from config.db import conn
from models.user import tableUser

userRoute = APIRouter()

@userRoute.post("/user/recharge")
def rechargeCredits(email: str,creditos: int):
    try:
        credito = conn.execute(select([tableUser.c.credits]).where(tableUser.c.email == email)).first()
        if credito is None:
            return {"message": "User not found"}, status.HTTP_404_NOT_FOUND
        else:
            newCredits = credito[0]+creditos
            conn.execute(tableUser.update().where(tableUser.c.email == email).values(credits=newCredits))
            newcredito = conn.execute(select([tableUser.c.credits]).where(tableUser.c.email == email)).first()
            return {"Credits": newcredito[0]}
    except Exception as e:
        return {"Error":str(e)}

@userRoute.post("/user/purchase")
def purchase(id:int,total: int):
    try:
        credito = conn.execute(select([tableUser.c.credits]).where(tableUser.c.id == id)).first()
        if credito is None:
            return {"message": "User not found"}, status.HTTP_404_NOT_FOUND
        else:
            if credito[0] < total:
                return JSONResponse({"message": "No tiene créditos suficientes, haga una recarga"}, status_code=status.HTTP_402_PAYMENT_REQUIRED)
            else:
                newCredits = credito[0]-total
                conn.execute(tableUser.update().where(tableUser.c.id == id).values(credits=newCredits))
                newcredito = conn.execute(select([tableUser.c.credits]).where(tableUser.c.id == id)).first()
            return {"Credits": newcredito[0]}
        
    except Exception as e:
        return {"Error":str(e)}
        