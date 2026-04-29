from datetime import datetime
import json
from sqlobject import *
from sqlobject import sqlhub, connectionForURI
from CommonFunction import log_exception, datetime_decoder


# =====================================================
# TABLE MODEL (Updated with Strings and Password)
# =====================================================
class tblBuyerRegister(SQLObject):
    nvcharFullName = StringCol(length=150, default=None)
    nvcharPhoneNumber = StringCol(length=15, default=None)
    nvcharEmail = StringCol(length=150, default=None)
    nvcharPassword = StringCol(length=150, default=None)  # Added Password!
    nvcharProfilePhotoUrl = StringCol(length=300, default=None)

    # Changed from IDs to Text (Strings)
    nvcharCity = StringCol(length=150, default=None)
    nvcharState = StringCol(length=150, default=None)
    nvcharCountry = StringCol(length=150, default=None)

    nvcharAddress = StringCol(length=500, default=None)
    ynPhoneVerified = BoolCol(default=False)
    dtCreatedDatetime = DateTimeCol(default=datetime.now)
    dtModifyDatetime = DateTimeCol(default=None)

    ynDeleted = BoolCol(default=False)


# =====================================================
# GET ALL BUYERS
# =====================================================
def GettblBuyerRegister():
    try:
        return list(tblBuyerRegister.select(tblBuyerRegister.q.ynDeleted == False))
    except Exception as e:
        log_exception(file_name="tblBuyerRegister_Repository", function_name="GettblBuyerRegister", payload={}, exc=e)
        return []


# =====================================================
# GET BUYER COUNT
# =====================================================
def GettblBuyerRegisterCount():
    try:
        count = tblBuyerRegister.select(tblBuyerRegister.q.ynDeleted == False).count()
        return {"totalBuyerCount": count}
    except Exception as e:
        log_exception(file_name="tblBuyerRegister_Repository", function_name="GettblBuyerRegisterCount", payload={},
                      exc=e)
        return {"totalBuyerCount": 0}


# =====================================================
# GET BUYER BY ID
# =====================================================
def GettblBuyerRegisterById(buyerId):
    try:
        buyer = tblBuyerRegister.get(buyerId)
        if buyer.ynDeleted:
            return None
        return buyer
    except Exception as e:
        log_exception(file_name="tblBuyerRegister_Repository", function_name="GettblBuyerRegisterById",
                      payload={"buyerId": buyerId}, exc=e)
        return None


def ChangeBuyerPassword(buyer_id, current_password, new_password):
    try:
        buyer = tblBuyerRegister.get(buyer_id)

        if buyer.ynDeleted:
            return {"ok": False, "message": "Buyer not found"}

        existing_password = str(buyer.nvcharPassword or "")
        if existing_password != str(current_password or ""):
            return {"ok": False, "message": "Current password is incorrect"}

        buyer.nvcharPassword = str(new_password or "")
        buyer.dtModifyDatetime = datetime.now()
        buyer.syncUpdate()

        return {"ok": True, "buyer": buyer}

    except Exception as e:
        log_exception(
            file_name="tblBuyerRegister_Repository",
            function_name="ChangeBuyerPassword",
            payload={"buyer_id": buyer_id},
            exc=e
        )
        return {"ok": False, "message": str(e)}


# =====================================================
# SAVE BUYER
# =====================================================
ALLOWED_BUYER_FIELDS = {
    'nvcharFullName', 'nvcharPhoneNumber', 'nvcharEmail',
    'nvcharPassword', 'nvcharProfilePhotoUrl', 'nvcharCity',
    'nvcharState', 'nvcharCountry', 'nvcharAddress', 'ynPhoneVerified'
}

def savetblBuyerRegister(JsonString):
    global obj
    try:
        obj = JsonString
        existing = None

        if obj.get('id'):
            try:
                existing = tblBuyerRegister.get(obj['id'])
            except:
                existing = None

        if existing:
            for key, value in obj.items():
                if hasattr(existing, key):
                    setattr(existing, key, value)
            existing.syncUpdate()
            return existing
        else:
            filtered_obj = {k: v for k, v in obj.items() if k in ALLOWED_BUYER_FIELDS}
            buyer = tblBuyerRegister(**filtered_obj)
            buyer.sync()
            return buyer

    except Exception as e:
        log_exception(file_name="tblBuyerRegister_Repository", function_name="savetblBuyerRegister", payload=obj, exc=e)
        return None


# =====================================================
# EDIT BUYER
# =====================================================
def edittblBuyerRegister(JsonString1):
    try:
        jstr = json.dumps(JsonString1)
        JsonString = json.loads(jstr, object_hook=datetime_decoder)

        buyer = tblBuyerRegister.get(JsonString['id'])

        buyer.nvcharFullName = JsonString.get('nvcharFullName', buyer.nvcharFullName)
        buyer.nvcharPhoneNumber = JsonString.get('nvcharPhoneNumber', buyer.nvcharPhoneNumber)
        buyer.nvcharEmail = JsonString.get('nvcharEmail', buyer.nvcharEmail)
        buyer.nvcharPassword = JsonString.get('nvcharPassword', buyer.nvcharPassword)
        buyer.nvcharProfilePhotoUrl = JsonString.get('nvcharProfilePhotoUrl', buyer.nvcharProfilePhotoUrl)

        # Updated to use the new string fields
        buyer.nvcharCity = JsonString.get('nvcharCity', buyer.nvcharCity)
        buyer.nvcharState = JsonString.get('nvcharState', buyer.nvcharState)
        buyer.nvcharCountry = JsonString.get('nvcharCountry', buyer.nvcharCountry)

        buyer.nvcharAddress = JsonString.get('nvcharAddress', buyer.nvcharAddress)
        buyer.ynPhoneVerified = JsonString.get('ynPhoneVerified', buyer.ynPhoneVerified)

        buyer.dtModifyDatetime = datetime.now()

        return buyer

    except Exception as e:
        log_exception(file_name="tblBuyerRegister_Repository", function_name="edittblBuyerRegister",
                      payload=JsonString1, exc=e)
        return None


# =====================================================
# DELETE BUYER
# =====================================================
def deletetblBuyerRegister(JsonString):
    try:
        buyer = tblBuyerRegister.get(JsonString['id'])
        buyer.ynDeleted = True
        return buyer

    except Exception as e:
        log_exception(file_name="tblBuyerRegister_Repository", function_name="deletetblBuyerRegister",
                      payload=JsonString, exc=e)
        return None


# =====================================================
# BUYER LOGIN (FLEXIBLE: EMAIL OR PHONE)
# =====================================================
def GettblBuyerLoginFlexible(json_data):
    try:
        identifier = json_data.get('identifier')
        password = json_data.get('nvcharPassword')

        # Get all active buyers
        buyers = list(tblBuyerRegister.select(tblBuyerRegister.q.ynDeleted == False))

        # Search for a match
        for buyer in buyers:
            if (
                    buyer.nvcharEmail == identifier or buyer.nvcharPhoneNumber == identifier) and buyer.nvcharPassword == password:
                return buyer  # Match found!

        return None  # No match found

    except Exception as e:
        log_exception(file_name="tblBuyerRegister_Repository", function_name="GettblBuyerLoginFlexible",
                      payload=json_data, exc=e)
        return None

# =====================================================
# CREATE TABLE
# =====================================================
sqlhub.processConnection = connectionForURI('sqlite:./world.sqlite3')
tblBuyerRegister.createTable(ifNotExists=True)
