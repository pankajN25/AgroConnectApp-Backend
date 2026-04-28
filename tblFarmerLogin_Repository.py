from datetime import datetime
import re
import json
from sqlobject import *
from sqlobject import sqlhub, connectionForURI
from CommonFunction import log_exception, datetime_decoder
from tblFarmerRegister_Repository import tblFarmerRegister


# ===============================
# TABLE MODEL
# ===============================
class tblFarmerLogin(SQLObject):
    nvcharFullName = StringCol(length=100, default=None)
    nvcharPhoneNumber = StringCol(length=50, default=None)
    nvcharEmail = StringCol(length=100, default=None)
    nvcharPassword = StringCol(length=100, default=None)

    intCityId = StringCol(default=None)
    intstateId = StringCol(default=None)
    intcountryId = StringCol(default=None)

    intPhoneVerified = BoolCol(default=False)
    intEmailVerified = BoolCol(default=False)

    VerificationStatus = BigIntCol(default=None)

    dtDateOfCreation = DateTimeCol(default=datetime.now)
    dtDateofModification = DateTimeCol(default=None)

    user_metadata = StringCol(length=1000, default=None)
    app_metadata = StringCol(length=1000, default=None)

    ynDeleted = BoolCol(default=False)


# ===============================
# GET ALL
# ===============================
def GettblFarmerLogin():
    try:
        return list(tblFarmerLogin.select(tblFarmerLogin.q.ynDeleted == False))
    except Exception as e:
        log_exception(
            file_name="tblFarmerLogin_Repository",
            function_name="GettblFarmerLogin",
            payload={},
            exc=e
        )
        return []


# ===============================
# GET BY ID
# ===============================
def GettblFarmerLoginById(Jid):
    try:
        return tblFarmerLogin.get(Jid)
    except Exception as e:
        log_exception(
            file_name="tblFarmerLogin_Repository",
            function_name="GettblFarmerLoginById",
            payload={"id": Jid},
            exc=e
        )
        return None


def UpdateFarmerPassword(nvcharPhoneNumber, newPassword):
    try:

        rows = tblFarmerLogin.select(
            AND(
                tblFarmerLogin.q.nvcharPhoneNumber == nvcharPhoneNumber,
                tblFarmerLogin.q.ynDeleted == False
            )
        )

        for user in rows:
            user.nvcharPassword = newPassword
            user.dtDateofModification = datetime.now()

        return True

    except Exception as e:

        log_exception(
            file_name="tblFarmerLogin_Repository",
            function_name="UpdateFarmerPassword",
            payload={"nvcharPhoneNumber": nvcharPhoneNumber},
            exc=e
        )


# ===============================
# LOGIN FLEXIBLE (FIXED)
# ===============================
def GettblFarmerLoginFlexible(identifier, nvcharPassword):
    try:
        # Normalize identifier (email lowercased, phone digits only).
        raw_identifier = str(identifier or "").strip()
        normalized_email = raw_identifier.lower() if "@" in raw_identifier else ""
        normalized_phone = re.sub(r"\D", "", raw_identifier)

        # First narrow by password + not deleted, then match identifier safely.
        candidates = list(
            tblFarmerRegister.select(
                AND(
                    tblFarmerRegister.q.ynDeleted == False,
                    tblFarmerRegister.q.nvcharPassword == nvcharPassword
                )
            )
        )

        if not candidates:
            return []

        matched = []
        for row in candidates:
            row_email = str(row.nvcharEmail or "").strip().lower()
            row_phone = re.sub(r"\D", "", str(row.nvcharPhoneNumber or "").strip())

            if normalized_email and row_email == normalized_email:
                matched.append(row)
                continue

            if normalized_phone and row_phone == normalized_phone:
                matched.append(row)

        return matched
    except Exception as e:
        log_exception(
            file_name="tblFarmerLogin_Repository",
            function_name="GettblFarmerLoginFlexible",
            payload={"identifier": identifier},
            exc=e
        )
        return []


# ===============================
# GET BY EMAIL
# ===============================
def GettblFarmerLoginBynvcharEmail(nvcharEmail):
    try:
        return list(tblFarmerLogin.select(
            AND(tblFarmerLogin.q.nvcharEmail == nvcharEmail, tblFarmerLogin.q.ynDeleted == False)
        ))
    except Exception as e:
        log_exception(
            file_name="tblFarmerLogin_Repository",
            function_name="GettblFarmerLoginBynvcharEmail",
            payload={"nvcharEmail": nvcharEmail},
            exc=e
        )
        return []


# ===============================
# GET BY PHONE NUMBER
# ===============================
def GettblFarmerLoginBynvcharPhoneNumber(nvcharPhoneNumber):
    try:
        return list(tblFarmerLogin.select(
            AND(tblFarmerLogin.q.nvcharPhoneNumber == nvcharPhoneNumber, tblFarmerLogin.q.ynDeleted == False)
        ))
    except Exception as e:
        log_exception(
            file_name="tblFarmerLogin_Repository",
            function_name="GettblFarmerLoginByPhoneNumber",
            payload={"nvcharPhoneNumber": nvcharPhoneNumber},
            exc=e
        )
        return []


# ===============================
# CHECK USER EXISTS
# ===============================
def ChecktblFarmerLoginExists(nvcharPhoneNumber):
    try:
        rows = tblFarmerLogin.select(
            AND(tblFarmerLogin.q.nvcharPhoneNumber == nvcharPhoneNumber, tblFarmerLogin.q.ynDeleted == False)
        )

        for row in rows:
            return row

        return None

    except Exception as e:
        log_exception(
            file_name="tblFarmerLogin_Repository",
            function_name="ChecktblFarmerLoginExists",
            payload={"nvcharPhoneNumber": nvcharPhoneNumber},
            exc=e
        )
        return None


# ===============================
# SAVE
# ===============================
def savetblFarmerLogin(JsonString):
    try:
        if JsonString.get("id"):

            obj = tblFarmerLogin.get(JsonString["id"])

            for k, v in JsonString.items():
                if hasattr(obj, k):
                    setattr(obj, k, v)

            obj.dtDateofModification = datetime.now()

            return obj

        return tblFarmerLogin(**JsonString)

    except Exception as e:
        log_exception(
            file_name="tblFarmerLogin_Repository",
            function_name="savetblFarmerLogin",
            payload=JsonString,
            exc=e
        )
        return None


# ===============================
# EDIT
# ===============================
def edittblFarmerLogin(JsonString1):
    try:

        jstr = json.dumps(JsonString1)
        JsonString = json.loads(jstr, object_hook=datetime_decoder)

        tblFarmerLogin_Repository = tblFarmerLogin.get(JsonString['id'])

        tblFarmerLogin_Repository.nvcharFullName = JsonString['nvcharFullName']
        tblFarmerLogin_Repository.nvcharPhoneNumber = JsonString['nvcharPhoneNumber']
        tblFarmerLogin_Repository.nvcharEmail = JsonString['nvcharEmail']
        tblFarmerLogin_Repository.nvcharPassword = JsonString['nvcharPassword']

        tblFarmerLogin_Repository.intCityId = JsonString['intCityId']
        tblFarmerLogin_Repository.intstateId = JsonString['intstateId']
        tblFarmerLogin_Repository.intcountryId = JsonString['intcountryId']

        tblFarmerLogin_Repository.intPhoneVerified = JsonString['intPhoneVerified']
        tblFarmerLogin_Repository.intEmailVerified = JsonString['intEmailVerified']

        tblFarmerLogin_Repository.VerificationStatus = JsonString['VerificationStatus']

        tblFarmerLogin_Repository.dtDateofModification = datetime.now()

        return tblFarmerLogin_Repository

    except Exception as e:
        log_exception(
            file_name="tblFarmerLogin_Repository",
            function_name="edittblFarmerLogin",
            payload=JsonString1,
            exc=e
        )


# ===============================
# DELETE
# ===============================
def deletetblFarmerLogin(JsonString):
    try:
        obj = tblFarmerLogin.get(JsonString["id"])
        obj.ynDeleted = True
        obj.dtDateofModification = datetime.now()
        return obj
    except Exception as e:
        log_exception(
            file_name="tblFarmerLogin_Repository",
            function_name="deletetblFarmerLogin",
            payload=JsonString,
            exc=e
        )
        return None


# ===============================
# UPDATE PHONE VERIFICATION
# ===============================
def updatephoneverifactionstatus(nvcharPhoneNumber):
    try:
        return list(tblFarmerLogin.select(
            AND(tblFarmerLogin.q.nvcharPhoneNumber == nvcharPhoneNumber, tblFarmerLogin.q.ynDeleted == False)
        ))
    except Exception as e:
        log_exception(
            file_name="tblFarmerLogin_Repository",
            function_name="updatephoneverifactionstatus",
            payload={"nvcharPhoneNumber": nvcharPhoneNumber},
            exc=e
        )
        return []


# ===============================
# DB CONNECTION
# ===============================
sqlhub.processConnection = connectionForURI("sqlite:./world.sqlite3")

tblFarmerLogin.createTable(ifNotExists=True)
