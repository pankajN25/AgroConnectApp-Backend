import datetime
from datetime import datetime
import json

from sqlobject import *
from sqlobject import sqlhub, connectionForURI
from CommonFunction import log_exception, datetime_decoder


# =====================================================
# TABLE MODEL
# =====================================================

class tblFarmerRegister(SQLObject):
    nvcharFullName = StringCol(length=150, default=None)
    nvcharPhoneNumber = StringCol(length=15, default=None)
    nvcharEmail = StringCol(length=150, default=None)
    nvcharPassword = StringCol(length=150, default=None)
    nvcharProfilePhotoUrl = StringCol(length=300, default=None)

    intCityId = StringCol(length=100, default=None)
    intstateId = StringCol(length=100, default=None)
    intcountryId = StringCol(length=100, default=None)

    nvcharFarmingType = StringCol(length=100, default=None)
    nvcharPreferredLanguage = StringCol(length=100, default=None)

    ynPhoneVerified = BoolCol(default=False)

    nvcharDescription = StringCol(length=500, default=None)

    dtDateOfCreation = DateTimeCol(default=datetime.now)
    dtDateofModification = DateTimeCol(default=None)

    user_metadata = StringCol(length=1000, default=None)
    app_metadata = StringCol(length=1000, default=None)

    ynDeleted = BoolCol(default=False)


# =====================================================
# GET ALL FARMERS
# =====================================================

def GettblFarmerRegister():
    try:
        return list(tblFarmerRegister.select(tblFarmerRegister.q.ynDeleted == False))

    except Exception as e:

        log_exception(
            file_name="tblFarmerRegisterRepository",
            function_name="GettblFarmerRegister",
            payload={},
            exc=e
        )

        return []


# =====================================================
# GET FARMER COUNT
# =====================================================

def GettblFarmerRegisterCount():
    try:

        count = tblFarmerRegister.select(
            tblFarmerRegister.q.ynDeleted == False
        ).count()

        return {
            "totalFarmerCount": count
        }

    except Exception as e:

        log_exception(
            file_name="tblFarmerRegisterRepository",
            function_name="GettblFarmerRegisterCount",
            payload={},
            exc=e
        )

        return {
            "totalFarmerCount": 0
        }


# # =====================================================
# # GET BY ID
# # =====================================================

# def GettblFarmerRegisterById(Jid):

#     try:
#         return tblFarmerRegister.get(Jid)

#     except Exception as e:

#         log_exception(
#             file_name="tblFarmerRegisterRepository",
#             function_name="GettblFarmerRegisterById",
#             payload={"id": Jid},
#             exc=e
#         )


def ChangeFarmerPassword(farmer_id, current_password, new_password):
    try:
        farmer = tblFarmerRegister.get(farmer_id)

        if farmer.ynDeleted:
            return {"ok": False, "message": "Farmer not found"}

        existing_password = str(farmer.nvcharPassword or "")
        if existing_password != str(current_password or ""):
            return {"ok": False, "message": "Current password is incorrect"}

        farmer.nvcharPassword = str(new_password or "")
        farmer.dtDateofModification = datetime.now()
        farmer.syncUpdate()

        return {"ok": True, "farmer": farmer}

    except Exception as e:
        log_exception(
            file_name="tblFarmerRegisterRepository",
            function_name="ChangeFarmerPassword",
            payload={"farmer_id": farmer_id},
            exc=e
        )
        return {"ok": False, "message": str(e)}


# =====================================================
# GET FARMER BY CITY
# =====================================================

def GettblFarmerRegisterByCityId(intCityId):
    try:
        row = tblFarmerRegister.select(
            AND(
                tblFarmerRegister.q.intCityId == intCityId,
                tblFarmerRegister.q.ynDeleted == False
            )
        )
        return row

    except Exception as e:
        log_exception(
            file_name="tblFarmerRegisterRepository",
            function_name="GettblFarmerRegisterByCityId",
            payload={"intCityId": intCityId},
            exc=e
        )


# =====================================================
# GET FARMER BY STATE
# =====================================================

def GettblFarmerRegisterByintstateId(intstateId):
    try:
        row = tblFarmerRegister.select(
            AND(
                tblFarmerRegister.q.intstateId == intstateId,
                tblFarmerRegister.q.ynDeleted == False
            )
        )
        return row

    except Exception as e:
        log_exception(
            file_name="tblFarmerRegisterRepository",
            function_name="GettblFarmerRegisterByintstateId",
            payload={"intstateId": intstateId},
            exc=e
        )


# =====================================================
# GET FARMER BY COUNTRY
# =====================================================

def GettblFarmerRegisterByintcountryId(intcountryId):
    try:
        row = tblFarmerRegister.select(
            AND(
                tblFarmerRegister.q.intcountryId == intcountryId,
                tblFarmerRegister.q.ynDeleted == False
            )
        )
        return row

    except Exception as e:
        log_exception(
            file_name="tblFarmerRegisterRepository",
            function_name="GettblFarmerRegisterByintcountryId",
            payload={"intcountryId": intcountryId},
            exc=e
        )


# =====================================================
# GET BY PHONE NUMBER
# =====================================================

def GettblFarmerRegisterBynvcharPhoneNumber(nvcharPhoneNumber):
    try:

        row = tblFarmerRegister.select(

            AND(
                tblFarmerRegister.q.nvcharPhoneNumber == nvcharPhoneNumber,
                tblFarmerRegister.q.ynDeleted == False
            )
        )

        return row

    except Exception as e:

        log_exception(
            file_name="tblFarmerRegisterRepository",
            function_name="GettblFarmerRegisterBynvcharPhoneNumber",
            payload={"nvcharPhoneNumber": nvcharPhoneNumber},
            exc=e
        )


# =====================================================
# GET BY EMAIL
# =====================================================

def GettblFarmerRegisterBynvcharEmail(nvcharEmail):
    try:

        row = tblFarmerRegister.select(

            AND(
                tblFarmerRegister.q.nvcharEmail == nvcharEmail,
                tblFarmerRegister.q.ynDeleted == False
            )
        )

        return row

    except Exception as e:

        log_exception(
            file_name="tblFarmerRegisterRepository",
            function_name="GettblFarmerRegisterBynvcharEmail",
            payload={"nvcharEmail": nvcharEmail},
            exc=e
        )


# =====================================================
# SAVE
# =====================================================

def savetblFarmerRegister(JsonString):
    global obj

    try:

        obj = JsonString

        existing = None

        if obj.get('id'):

            try:
                existing = tblFarmerRegister.get(obj['id'])
            except:
                existing = None

        if existing:

            for key, value in obj.items():

                if hasattr(existing, key):
                    setattr(existing, key, value)

            existing.syncUpdate()

            return existing

        else:

            farmer = tblFarmerRegister(**obj)
            farmer.sync()
            return farmer

    except Exception as e:

        log_exception(
            file_name="tblFarmerRegisterRepository",
            function_name="savetblFarmerRegister",
            payload=obj,
            exc=e
        )

        return None


# =====================================================
# EDIT FARMER
# =====================================================

def edittblFarmerRegister(JsonString1):
    try:

        jstr = json.dumps(JsonString1)

        JsonString = json.loads(jstr, object_hook=datetime_decoder)

        tblFarmerRegister_Repository = tblFarmerRegister.get(JsonString['id'])

        tblFarmerRegister_Repository.nvcharFullName = JsonString['nvcharFullName']
        tblFarmerRegister_Repository.nvcharPhoneNumber = JsonString['nvcharPhoneNumber']
        tblFarmerRegister_Repository.nvcharEmail = JsonString['nvcharEmail']
        tblFarmerRegister_Repository.nvcharPassword = JsonString['nvcharPassword']
        tblFarmerRegister_Repository.nvcharProfilePhotoUrl = JsonString['nvcharProfilePhotoUrl']

        tblFarmerRegister_Repository.intCityId = JsonString['intCityId']
        tblFarmerRegister_Repository.intstateId = JsonString['intstateId']
        tblFarmerRegister_Repository.intcountryId = JsonString['intcountryId']

        tblFarmerRegister_Repository.nvcharFarmingType = JsonString['nvcharFarmingType']
        tblFarmerRegister_Repository.nvcharPreferredLanguage = JsonString['nvcharPreferredLanguage']

        tblFarmerRegister_Repository.ynPhoneVerified = JsonString['ynPhoneVerified']

        tblFarmerRegister_Repository.nvcharDescription = JsonString['nvcharDescription']

        tblFarmerRegister_Repository.dtDateofModification = datetime.now()

        return tblFarmerRegister_Repository

    except Exception as e:

        log_exception(
            file_name="tblFarmerRegisterRepository",
            function_name="edittblFarmerRegister",
            payload=JsonString1,
            exc=e
        )


# =====================================================
# DELETE
# =====================================================

def deletetblFarmerRegister(JsonString):
    try:

        oRepository = tblFarmerRegister.get(JsonString['id'])

        oRepository.ynDeleted = True

        return oRepository

    except Exception as e:

        log_exception(
            file_name="tblFarmerRegisterRepository",
            function_name="deletetblFarmerRegister",
            payload=JsonString,
            exc=e
        )


# =====================================================
# UPDATE PHONE VERIFICATION
# =====================================================

def updatephoneverifactionstatus(nvcharPhoneNumber):
    try:

        farmers = tblFarmerRegister.select(

            AND(
                tblFarmerRegister.q.nvcharPhoneNumber == nvcharPhoneNumber,
                tblFarmerRegister.q.ynDeleted == False
            )
        )

        updated = []

        for farmer in farmers:
            farmer.ynPhoneVerified = True
            farmer.syncUpdate()

            updated.append(farmer)

        return updated

    except Exception as e:

        log_exception(
            file_name="tblFarmerRegisterRepository",
            function_name="updatephoneverifactionstatus",
            payload={"nvcharPhoneNumber": nvcharPhoneNumber},
            exc=e
        )

        return []


# =====================================================
# CREATE TABLE
# =====================================================

sqlhub.processConnection = connectionForURI('sqlite:./world.sqlite3')
tblFarmerRegister.createTable(ifNotExists=True)
