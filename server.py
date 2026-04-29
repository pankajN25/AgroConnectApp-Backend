import os  # 🚨 ADD THIS IMPORT

# ====================================================
# SIMPLE ENV LOADER (reads AgroFarmerBackend/.env)
# ====================================================
def load_env_file():
    try:
        base_dir = os.path.dirname(__file__)
        env_path = os.path.join(base_dir, ".env")
        if not os.path.exists(env_path):
            return
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                raw = line.strip()
                if not raw or raw.startswith("#") or "=" not in raw:
                    continue
                key, value = raw.split("=", 1)
                key = key.strip()
                value = value.strip().strip('"').strip("'")
                if key and key not in os.environ:
                    os.environ[key] = value
    except Exception:
        pass

load_env_file()

import uvicorn
from fastapi import FastAPI, UploadFile, File, Form
from fastapi import Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles  # 🚨 ADD THIS IMPORT

app = FastAPI()

# 🚨 ADD THESE LINES RIGHT HERE, AFTER app = FastAPI()
# 1. Make sure the folders exist so the server doesn't crash
os.makedirs("uploads/crops", exist_ok=True)
os.makedirs("uploads/tblFarmerRegister", exist_ok=True)
os.makedirs("uploads/tblBuyerRegister", exist_ok=True)

# 2. Tell FastAPI to share the 'uploads' folder publicly!
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# Keep the rest of your middleware exactly the same:
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "*"  # optional – for testing
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#--------------------------------------------------------------------countries---------------------------------------------------------------
from countriescontract import (
GetCountries1,GetCountriesById1,GetCountriesByPhonecode1,
GetCountriesByRegion_id1,
)

#----------------------------------------------------------------------states---------------------------------------------------------------------
from statescontract import (
GetStates1,GetStatesById1,GetStatesByCountry_id1,
GetStatesByCountry_code1
)

#-----------------------------------------------------------------------cities----------------------------------------------
from citiescontract import (
GetCities1,GetCitiesById1,GetCitiesByState_id1,
GetCitiesByState_code1,GetCitiesByCountry_id1,GetCitiesByCountry_code1
)

from tblLanguagecontract import (GettableLanguage1,GettblLanguageById1,savetblLanguage1,edittblLanguage1,deletetblLanguage1
)
from regionscontract import (GetRegions1,GetRegionsById1
)



# ---------------- ---------------------------------------------------Farmer Registration ----------------
from tblFarmerRegister_contract import (
    GettblFarmerRegister1,
    GettblFarmerRegisterByCityId1,
    GettblFarmerRegisterByintstateId1,
    GettblFarmerRegisterByintcountryId1,
    ChangeFarmerPassword1,
    uploadtblFarmerRegisterProfilePictureWithMeta1,
    savetblFarmerRegister1,
    edittblFarmerRegister1,
    deletetblFarmerRegister1,
    updatephoneverifactionstatus1
)


# --------------------------------------------Buyer EndPointers-------------------=====
# ---------------- Buyer Registration ----------------
from tblBuyerRegister_contract import (
    GettblBuyerRegister1,
    GettblBuyerRegisterById1,
    ChangeBuyerPassword1,
    uploadtblBuyerRegisterProfilePictureWithMeta1,
    savetblBuyerRegister1,
    edittblBuyerRegister1,
    deletetblBuyerRegister1, GettblBuyerLoginFlexible1
)


# ---------------- Farmer Login ----------------
from tblFarmerLogin_contract import (
    GettblFarmerLogin1,
    GettblFarmerLoginById1,
    GettblFarmerLoginFlexible1,
    UpdateFarmerPassword1,
    savetblFarmerLogin1,
    edittblFarmerLogin1,
    deletetblFarmerLogin1
)

# ================= Crop Management =================
from tblCrop_contract import (
    GettblCrop1,
    GettblCropByCategoryId1,
    GettblCropByFarmerId1,
    uploadCropImage1,
    savetblCrop1,
    edittblCrop1,
    deletetblCrop1
)

# ================= Order Management =================
from tblOrder_contract import (
    GettblOrder1,
    GettblOrderByFarmerId1,
    GettblOrderByBuyerId1,
    savetblOrder1,
    edittblOrder1,
    deletetblOrder1
)

# ================= Razorpay + Order Workflow =================
from razorpay_contract import (
    create_razorpay_order,
    verify_payment_and_create_order,
    create_cod_order,
    update_order_status_with_history,
    cancel_order_and_refund
)

# ================= Chat Management =================
from tblChat_contract import (
    GettblChatRoom1,
    savetblChatRoom1,
    edittblChatRoom1,
    deletetblChatRoom1,
    GettblChatMessage1,
    savetblChatMessage1,
    edittblChatMessage1,
    deletetblChatMessage1,
    GettblChatMessageByChatRoomId1,
    GettblChatRoomByCreatedBy1,
)

# ================= Direct Messaging =================
from direct_message_contract import (
    send_direct_message1,
    get_direct_messages_between_users1,
    get_direct_messages_by_user1
)

# ================= Crop Health Management =================
from tblCropHealth_contract import (
    GettblCropHealthScan1,
    GettblCropHealthScanByFarmerId1,
    savetblCropHealthScan1,
    edittblCropHealthScan1,
    deletetblCropHealthScan1
)

# ================= Weather Management =================
from tblWeather_contract import (
    GettblWeatherForecast1,
    GettblWeatherForecastByLocationId1,
    savetblWeatherForecast1,
    edittblWeatherForecast1,
    deletetblWeatherForecast1
)

# ================= Notification Management =================
from tblNotification_contract import (
    GettblNotification1,
    GettblNotificationByFarmerId1,
    savetblNotification1,
    edittblNotification1,
    deletetblNotification1
)

# ================= Phone OTP Auth =================
from phoneVerificationcontract__enhanced import (
    SendPhoneOTP1,
    VerifyPhoneOTP1,
    ResendPhoneOTP1,
    CheckPhoneOTPStatus1,
    CheckUserByPhone1,
    SendOTPRequest,
    VerifyOTPRequest,
    ResendOTPRequest,
    OTPStatusRequest,
    CheckUserRequest,
)

# ================= Crop Category Master =================
from mstCropCategory_contract import (
    GetmstCropCategory1,
    savemstCropCategory1,
    editmstCropCategory1,
    deletemstCropCategory1
)

# ================= Crop Quality Grade Master =================
from mstCropQualityGrade_contract import (
    GetmstCropQualityGrade1,
    savemstCropQualityGrade1,
    editmstCropQualityGrade1,
    deletemstCropQualityGrade1
)

# ================= Location Master =================
from mstLocation_contract import (
    GetmstLocation1,
    GetmstLocationByCityId1,
    savemstLocation1,
    editmstLocation1,
    deletemstLocation1
)

# ------------------------------------------------------------------ GOOGLE AUTH --------------------------------------------
from googleAuthcontract import (
    GoogleCoachLogin1,
    GoogleLogin1,
    GoogleCompleteRegistration1,
)



# ================= Crop Images Management =================

# ================= Favorite Crop Management =================

# ================= Order Status Management =================

# ================= Transaction Management =================

# ================= Farmer Location Management =================

# ================= Farmer Rating Management =================

# ================= Courier Location Management =================

# ================= Support Ticket Management =================

# ================= Crop Images Management =================
from tblCropImages_contract import (
    GetAllCropImages,
    GetCropImagesByCropId,
    uploadtblCropImageWithMeta,
    SaveCropImage,
    EditCropImage,
    DeleteCropImage
)

# ================= Favorite Crop Management =================
from tblFavoriteCrop_contract import (
    GetAllFavoriteCrops,
    GetFavoriteCropsByUserId,
    SaveFavoriteCrop,
    EditFavoriteCrop,
    DeleteFavoriteCrop
)

# ================= Order Status Management =================
from tblOrderStatus_contract import (
    GetAllOrderStatus,
    GetOrderStatusByOrderId,
    SaveOrderStatus,
    EditOrderStatus,
    DeleteOrderStatus
)

# ================= Transaction Management =================
from tblTransaction_contract import (
    GetAllTransactions,
    GetTransactionsByOrderId,
    SaveTransaction,
    EditTransaction,
    DeleteTransaction
)

# ================= Farmer Location Management =================
from tblFarmerLocation_contract import (
    GetAllFarmerLocations,
    GetFarmerLocationsByFarmerId,
    SaveFarmerLocation,
    EditFarmerLocation,
    DeleteFarmerLocation
)

# ================= Farmer Rating Management =================
from tblFarmerRating_contract import (
    GetAllFarmerRatings,
    GetFarmerRatingsByFarmerId,
    SaveFarmerRating,
    EditFarmerRating,
    DeleteFarmerRating
)

# ================= Courier Location Management =================
from tblCourierLocation_contract import (
    GetAllCourierLocations,
    GetCourierLocationsByOrderId,
    SaveCourierLocation,
    EditCourierLocation,
    DeleteCourierLocation,
    UpdateLiveCourierLocation,
    GetLatestCourierLocation,
)

# ================= Support Ticket Management =================
from tblSupportTicket_contract import (
    GetAllSupportTickets,
    GetSupportTicketsByUserId,
    SaveSupportTicket,
    EditSupportTicket,
    DeleteSupportTicket
)



# --------------------------------------------------------------------------------Regions----------------------------------------------------------
@app.get("/GetRegions")
def GetRegions():
    return GetRegions1()


@app.post("/GetRegionsById")
async def GetRegionsById(request: Request):
    return GetRegionsById1(await request.json())


# ----------------------------------------------------tblLanguage------------------------------------------------
@app.get("/GettableLanguage")
def GettableLanguage():
    return GettableLanguage1()

@app.post("/GettblLanguageById")
async def GettblLanguageById(request: Request):
    return GettblLanguageById1(await request.json())

@app.post("/savetblLanguage")
async def savetblLanguage(request: Request):
    return savetblLanguage1(await request.json())

@app.post("/edittblLanguage")
async def edittblLanguage(request: Request):
    return edittblLanguage1(await request.json())

@app.post("/edittblLanguage")
async def edittblLanguage(request: Request):
    return edittblLanguage1(await request.json())

@app.post("/deletetblLanguage")
async def deletetblLanguage(request: Request):
    return deletetblLanguage1(await request.json())



# --------------------------------------------------------------------------------Countries-----------------------------------------------------------------------------
@app.get("/GetCountries")
def GetCountries():
    return GetCountries1()

@app.post("/GetCountriesById")
async def GetCountriesById(request: Request):
    return GetCountriesById1(await request.json())

@app.post("/GetCountriesByPhonecode")
async def GetCountriesByPhonecode(request: Request):
    return GetCountriesByPhonecode1(await request.json())

@app.post("/GetCountriesByRegion_id")
async def GetCountriesByRegion_id(request: Request):
    return GetCountriesByRegion_id1(await request.json())


# -------------------------------------------------------------------------------States--------------------------------------------------------------------------------
@app.get("/GetStates")
def GetStates():
    return GetStates1()

@app.post("/GetStatesById")
async def GetStatesById(request: Request):
    return GetStatesById1(await request.json())

@app.post("/GetStatesByCountry_id")
async def GetStatesByCountry_id(request: Request):
    return GetStatesByCountry_id1(await request.json())

@app.post("/GetStatesByCountry_code")
async def GetStatesByCountry_code(request: Request):
    return GetStatesByCountry_code1(await request.json())



# --------------------------------------------------------------------------Cities----------------------------------------------------------------------------
@app.get("/GetCities")
def GetCities():
    return GetCities1()

@app.post("/GetCitiesById")
async def GetCitiesById(request: Request):
    return GetCitiesById1(await request.json())

@app.post("/GetCitiesByState_id")
async def GetCitiesByState_id(request: Request):
    return GetCitiesByState_id1(await request.json())

@app.post("/GetCitiesByState_code")
async def GetCitiesByState_code(request: Request):
    return GetCitiesByState_code1(await request.json())

@app.post("/GetCitiesByCountry_id")
async def GetCitiesByCountry_id(request: Request):
    return GetCitiesByCountry_id1(await request.json())

@app.post("/GetCitiesByCountry_code")
async def GetCitiesByCountry_code(request: Request):
    return GetCitiesByCountry_code1(await request.json())


# ============================================================FARMER REGISTER =================

@app.get("/GettblFarmerRegister")
def GettblFarmerRegister():
    return GettblFarmerRegister1()


@app.post("/GettblFarmerRegisterByCityId")
async def GettblFarmerRegisterByCityId(request: Request):
    return GettblFarmerRegisterByCityId1(await request.json())


@app.post("/GettblFarmerRegisterByintstateId")
async def GettblFarmerRegisterByintstateId(request: Request):
    return GettblFarmerRegisterByintstateId1(await request.json())


@app.post("/GettblFarmerRegisterByintcountryId")
async def GettblFarmerRegisterByintcountryId(request: Request):
    return GettblFarmerRegisterByintcountryId1(await request.json())


@app.post("/uploadtblFarmerRegisterProfilePictureWithMeta")
async def upload_profile_picture(
        image: UploadFile = File(...),
        AddGuest_id: int = Form(...)
):
    return await uploadtblFarmerRegisterProfilePictureWithMeta1(
        image=image,
        AddGuest_id=AddGuest_id
    )
    
    
@app.post("/savetblFarmerRegister")
async def savetblFarmerRegister(request: Request):
    return savetblFarmerRegister1(await request.json())


@app.post("/edittblFarmerRegister")
async def edittblFarmerRegister(request: Request):
    return edittblFarmerRegister1(await request.json())


@app.post("/ChangeFarmerPassword")
async def ChangeFarmerPassword(request: Request):
    return ChangeFarmerPassword1(await request.json())


@app.post("/deletetblFarmerRegister")
async def deletetblFarmerRegister(request: Request):
    return deletetblFarmerRegister1(await request.json())


@app.post("/updateFarmerPhoneVerification")
async def updateFarmerPhoneVerification(request: Request):
    return updatephoneverifactionstatus1(await request.json())



# ================= FARMER LOGIN =================

@app.get("/GettblFarmerLogin")
def GettblFarmerLogin():
    return GettblFarmerLogin1()


@app.post("/GettblFarmerLoginById")
async def GettblFarmerLoginById(request: Request):
    return GettblFarmerLoginById1(await request.json())


@app.post("/GettblFarmerLoginFlexible")
async def GettblFarmerLoginFlexible(request: Request):
    return GettblFarmerLoginFlexible1(await request.json())

@app.post("/UpdateFarmerPassword")
async def UpdateFarmerPassword(request: Request):
    return UpdateFarmerPassword1(await request.json())


@app.post("/savetblFarmerLogin")
async def savetblFarmerLogin(request: Request):
    return savetblFarmerLogin1(await request.json())


@app.post("/edittblFarmerLogin")
async def edittblFarmerLogin(request: Request):
    return edittblFarmerLogin1(await request.json())


@app.post("/deletetblFarmerLogin")
async def deletetblFarmerLogin(request: Request):
    return deletetblFarmerLogin1(await request.json())


# ==================== CROP MANAGEMENT ====================

@app.get("/GettblCrop")
def GettblCrop():
    return GettblCrop1()

@app.post("/GettblCropByCategoryId")
async def GettblCropByCategoryId(request: Request):
    return GettblCropByCategoryId1(await request.json())

@app.post("/GettblCropByFarmerId")
async def GettblCropByFarmerId(request: Request):
    return GettblCropByFarmerId1(await request.json())

@app.post("/uploadCropImage")
async def uploadCropImage(
    image: UploadFile = File(...),
    crop_id: int = Form(...)
):
    return await uploadCropImage1(image, crop_id)

@app.post("/savetblCrop")
async def savetblCrop(request: Request):
    return savetblCrop1(await request.json())

@app.post("/edittblCrop")
async def edittblCrop(request: Request):
    return edittblCrop1(await request.json())

@app.post("/deletetblCrop")
async def deletetblCrop(request: Request):
    return deletetblCrop1(await request.json())


# ==================== ORDER MANAGEMENT ====================

@app.get("/GettblOrder")
def GettblOrder():
    return GettblOrder1()

@app.post("/GettblOrderByFarmerId")
async def GettblOrderByFarmerId(request: Request):
    return GettblOrderByFarmerId1(await request.json())

@app.post("/GettblOrderByBuyerId")
async def GettblOrderByBuyerId(request: Request):
    return GettblOrderByBuyerId1(await request.json())

@app.post("/savetblOrder")
async def savetblOrder(request: Request):
    return savetblOrder1(await request.json())

@app.post("/edittblOrder")
async def edittblOrder(request: Request):
    return edittblOrder1(await request.json())

@app.post("/deletetblOrder")
async def deletetblOrder(request: Request):
    return deletetblOrder1(await request.json())

# ==================== ORDER WORKFLOW + RAZORPAY ====================
@app.post("/razorpay/create-order")
async def razorpay_create_order(request: Request):
    return create_razorpay_order(await request.json())

@app.post("/razorpay/verify")
async def razorpay_verify(request: Request):
    return verify_payment_and_create_order(await request.json())

@app.post("/order/cod")
async def place_cod_order(request: Request):
    return create_cod_order(await request.json())

@app.post("/razorpay/cancel-order")
async def razorpay_cancel_order(request: Request):
    return cancel_order_and_refund(await request.json())

@app.post("/UpdateOrderStatusWithHistory")
async def UpdateOrderStatusWithHistory(request: Request):
    return update_order_status_with_history(await request.json())


# ==================== CHAT MANAGEMENT ====================

@app.get("/GettblChatRoom")
def GettblChatRoom():
    return GettblChatRoom1()

@app.post("/savetblChatRoom")
async def savetblChatRoom(request: Request):
    return savetblChatRoom1(await request.json())

@app.post("/edittblChatRoom")
async def edittblChatRoom(request: Request):
    return edittblChatRoom1(await request.json())

@app.post("/deletetblChatRoom")
async def deletetblChatRoom(request: Request):
    return deletetblChatRoom1(await request.json())

@app.get("/GettblChatMessage")
def GettblChatMessage():
    return GettblChatMessage1()

@app.post("/savetblChatMessage")
async def savetblChatMessage(request: Request):
    return savetblChatMessage1(await request.json())

@app.post("/edittblChatMessage")
async def edittblChatMessage(request: Request):
    return edittblChatMessage1(await request.json())

@app.post("/deletetblChatMessage")
async def deletetblChatMessage(request: Request):
    return deletetblChatMessage1(await request.json())

@app.post("/GettblChatMessageByChatRoomId")
async def GettblChatMessageByChatRoomId(request: Request):
    return GettblChatMessageByChatRoomId1(await request.json())

@app.post("/GettblChatRoomByCreatedBy")
async def GettblChatRoomByCreatedBy(request: Request):
    return GettblChatRoomByCreatedBy1(await request.json())

# ==================== DIRECT MESSAGING ====================
@app.post("/SendDirectMessage")
async def SendDirectMessage(request: Request):
    return send_direct_message1(await request.json())

@app.get("/GetDirectMessagesBetweenUsers")
def GetDirectMessagesBetweenUsers(sender_id: int, receiver_id: int):
    return get_direct_messages_between_users1({"sender_id": sender_id, "receiver_id": receiver_id})

@app.get("/GetDirectMessagesByUser")
def GetDirectMessagesByUser(user_id: int):
    return get_direct_messages_by_user1({"user_id": user_id})


# ==================== CROP HEALTH MANAGEMENT ====================

@app.get("/GettblCropHealthScan")
def GettblCropHealthScan():
    return GettblCropHealthScan1()

@app.post("/GettblCropHealthScanByFarmerId")
async def GettblCropHealthScanByFarmerId(request: Request):
    return GettblCropHealthScanByFarmerId1(await request.json())

@app.post("/savetblCropHealthScan")
async def savetblCropHealthScan(request: Request):
    return savetblCropHealthScan1(await request.json())

@app.post("/edittblCropHealthScan")
async def edittblCropHealthScan(request: Request):
    return edittblCropHealthScan1(await request.json())

@app.post("/deletetblCropHealthScan")
async def deletetblCropHealthScan(request: Request):
    return deletetblCropHealthScan1(await request.json())


# ==================== WEATHER MANAGEMENT ====================

@app.get("/GettblWeatherForecast")
def GettblWeatherForecast():
    return GettblWeatherForecast1()

@app.post("/GettblWeatherForecastByLocationId")
async def GettblWeatherForecastByLocationId(request: Request):
    return GettblWeatherForecastByLocationId1(await request.json())

@app.post("/savetblWeatherForecast")
async def savetblWeatherForecast(request: Request):
    return savetblWeatherForecast1(await request.json())

@app.post("/edittblWeatherForecast")
async def edittblWeatherForecast(request: Request):
    return edittblWeatherForecast1(await request.json())

@app.post("/deletetblWeatherForecast")
async def deletetblWeatherForecast(request: Request):
    return deletetblWeatherForecast1(await request.json())


# ==================== NOTIFICATION MANAGEMENT ====================

@app.get("/GettblNotification")
def GettblNotification():
    return GettblNotification1()

@app.post("/GettblNotificationByFarmerId")
async def GettblNotificationByFarmerId(request: Request):
    return GettblNotificationByFarmerId1(await request.json())

@app.post("/savetblNotification")
async def savetblNotification(request: Request):
    return savetblNotification1(await request.json())

@app.post("/edittblNotification")
async def edittblNotification(request: Request):
    return edittblNotification1(await request.json())

@app.post("/deletetblNotification")
async def deletetblNotification(request: Request):
    return deletetblNotification1(await request.json())


# ==================== PHONE OTP AUTH ====================
@app.post("/SendPhoneOTP")
async def SendPhoneOTP(request: Request):
    payload = await request.json()
    return SendPhoneOTP1(SendOTPRequest(**payload))

@app.post("/VerifyPhoneOTP")
async def VerifyPhoneOTP(request: Request):
    payload = await request.json()
    return VerifyPhoneOTP1(VerifyOTPRequest(**payload))

@app.post("/ResendPhoneOTP")
async def ResendPhoneOTP(request: Request):
    payload = await request.json()
    return ResendPhoneOTP1(ResendOTPRequest(**payload))

@app.post("/CheckPhoneOTPStatus")
async def CheckPhoneOTPStatus(request: Request):
    payload = await request.json()
    return CheckPhoneOTPStatus1(OTPStatusRequest(**payload))

@app.post("/CheckUserByPhone")
async def CheckUserByPhone(request: Request):
    payload = await request.json()
    return CheckUserByPhone1(CheckUserRequest(**payload))


# ==================== CROP CATEGORY MASTER ====================

@app.get("/GetmstCropCategory")
def GetmstCropCategory():
    return GetmstCropCategory1()

@app.post("/savemstCropCategory")
async def savemstCropCategory(request: Request):
    return savemstCropCategory1(await request.json())

@app.post("/editmstCropCategory")
async def editmstCropCategory(request: Request):
    return editmstCropCategory1(await request.json())

@app.post("/deletemstCropCategory")
async def deletemstCropCategory(request: Request):
    return deletemstCropCategory1(await request.json())


# ==================== CROP QUALITY GRADE MASTER ====================

@app.get("/GetmstCropQualityGrade")
def GetmstCropQualityGrade():
    return GetmstCropQualityGrade1()

@app.post("/savemstCropQualityGrade")
async def savemstCropQualityGrade(request: Request):
    return savemstCropQualityGrade1(await request.json())

@app.post("/editmstCropQualityGrade")
async def editmstCropQualityGrade(request: Request):
    return editmstCropQualityGrade1(await request.json())

@app.post("/deletemstCropQualityGrade")
async def deletemstCropQualityGrade(request: Request):
    return deletemstCropQualityGrade1(await request.json())


# ==================== LOCATION MASTER ====================

@app.get("/GetmstLocation")
def GetmstLocation():
    return GetmstLocation1()

@app.post("/GetmstLocationByCityId")
async def GetmstLocationByCityId(request: Request):
    return GetmstLocationByCityId1(await request.json())

@app.post("/savemstLocation")
async def savemstLocation(request: Request):
    return savemstLocation1(await request.json())

@app.post("/editmstLocation")
async def editmstLocation(request: Request):
    return editmstLocation1(await request.json())

@app.post("/deletemstLocation")
async def deletemstLocation(request: Request):
    return deletemstLocation1(await request.json())


# ==================== CROP IMAGES MANAGEMENT ====================

@app.get("/GettblCropImages")
def GettblCropImages():
    return GetAllCropImages()

@app.post("/GettblCropImagesByCropId")
async def GettblCropImagesByCropId(request: Request):
    return GetCropImagesByCropId(await request.json())

@app.post("/uploadtblCropImageWithMeta")
async def uploadtblCropImage(
    image: UploadFile = File(...),
    intCropId: int = Form(...)
):
    return await uploadtblCropImageWithMeta(image=image, intCropId=intCropId)

@app.post("/savetblCropImages")
async def savetblCropImages(request: Request):
    return SaveCropImage(await request.json())

@app.post("/edittblCropImages")
async def edittblCropImages(request: Request):
    return EditCropImage(await request.json())

@app.post("/deletetblCropImages")
async def deletetblCropImages(request: Request):
    return DeleteCropImage(await request.json())


# ==================== FAVORITE CROP MANAGEMENT ====================

@app.get("/GettblFavoriteCrop")
def GettblFavoriteCrop():
    return GetAllFavoriteCrops()

@app.post("/GettblFavoriteCropByUserId")
async def GettblFavoriteCropByUserId(request: Request):
    return GetFavoriteCropsByUserId(await request.json())

@app.post("/savetblFavoriteCrop")
async def savetblFavoriteCrop(request: Request):
    return SaveFavoriteCrop(await request.json())

@app.post("/edittblFavoriteCrop")
async def edittblFavoriteCrop(request: Request):
    return EditFavoriteCrop(await request.json())

@app.post("/deletetblFavoriteCrop")
async def deletetblFavoriteCrop(request: Request):
    return DeleteFavoriteCrop(await request.json())


# ==================== ORDER STATUS MANAGEMENT ====================

@app.get("/GettblOrderStatus")
def GettblOrderStatus():
    return GetAllOrderStatus()

@app.post("/GettblOrderStatusByOrderId")
async def GettblOrderStatusByOrderId(request: Request):
    return GetOrderStatusByOrderId(await request.json())

@app.post("/savetblOrderStatus")
async def savetblOrderStatus(request: Request):
    return SaveOrderStatus(await request.json())

@app.post("/edittblOrderStatus")
async def edittblOrderStatus(request: Request):
    return EditOrderStatus(await request.json())

@app.post("/deletetblOrderStatus")
async def deletetblOrderStatus(request: Request):
    return DeleteOrderStatus(await request.json())


# ==================== TRANSACTION MANAGEMENT ====================

@app.get("/GettblTransaction")
def GettblTransaction():
    return GetAllTransactions()

@app.post("/GettblTransactionByOrderId")
async def GettblTransactionByOrderId(request: Request):
    return GetTransactionsByOrderId(await request.json())

@app.post("/savetblTransaction")
async def savetblTransaction(request: Request):
    return SaveTransaction(await request.json())

@app.post("/edittblTransaction")
async def edittblTransaction(request: Request):
    return EditTransaction(await request.json())

@app.post("/deletetblTransaction")
async def deletetblTransaction(request: Request):
    return DeleteTransaction(await request.json())


# ==================== FARMER LOCATION MANAGEMENT ====================

@app.get("/GettblFarmerLocation")
def GettblFarmerLocation():
    return GetAllFarmerLocations()

@app.post("/GettblFarmerLocationByFarmerId")
async def GettblFarmerLocationByFarmerId(request: Request):
    return GetFarmerLocationsByFarmerId(await request.json())

@app.post("/savetblFarmerLocation")
async def savetblFarmerLocation(request: Request):
    return SaveFarmerLocation(await request.json())

@app.post("/edittblFarmerLocation")
async def edittblFarmerLocation(request: Request):
    return EditFarmerLocation(await request.json())

@app.post("/deletetblFarmerLocation")
async def deletetblFarmerLocation(request: Request):
    return DeleteFarmerLocation(await request.json())


# ==================== FARMER RATING MANAGEMENT ====================

@app.get("/GettblFarmerRating")
def GettblFarmerRating():
    return GetAllFarmerRatings()

@app.post("/GettblFarmerRatingByFarmerId")
async def GettblFarmerRatingByFarmerId(request: Request):
    return GetFarmerRatingsByFarmerId(await request.json())

@app.post("/savetblFarmerRating")
async def savetblFarmerRating(request: Request):
    return SaveFarmerRating(await request.json())

@app.post("/edittblFarmerRating")
async def edittblFarmerRating(request: Request):
    return EditFarmerRating(await request.json())

@app.post("/deletetblFarmerRating")
async def deletetblFarmerRating(request: Request):
    return DeleteFarmerRating(await request.json())


# ==================== COURIER LOCATION MANAGEMENT ====================

@app.get("/GettblCourierLocation")
def GettblCourierLocation():
    return GetAllCourierLocations()

@app.post("/GettblCourierLocationByOrderId")
async def GettblCourierLocationByOrderId(request: Request):
    return GetCourierLocationsByOrderId(await request.json())

@app.post("/savetblCourierLocation")
async def savetblCourierLocation(request: Request):
    return SaveCourierLocation(await request.json())

@app.post("/edittblCourierLocation")
async def edittblCourierLocation(request: Request):
    return EditCourierLocation(await request.json())

@app.post("/deletetblCourierLocation")
async def deletetblCourierLocation(request: Request):
    return DeleteCourierLocation(await request.json())

@app.post("/UpdateLiveCourierLocation")
async def update_live_courier_location(request: Request):
    return UpdateLiveCourierLocation(await request.json())

@app.post("/GetLatestCourierLocation")
async def get_latest_courier_location(request: Request):
    return GetLatestCourierLocation(await request.json())


# ==================== SUPPORT TICKET MANAGEMENT ====================

@app.get("/GettblSupportTicket")
def GettblSupportTicket():
    return GetAllSupportTickets()

@app.post("/GettblSupportTicketByUserId")
async def GettblSupportTicketByUserId(request: Request):
    return GetSupportTicketsByUserId(await request.json())

@app.post("/savetblSupportTicket")
async def savetblSupportTicket(request: Request):
    return SaveSupportTicket(await request.json())

@app.post("/edittblSupportTicket")
async def edittblSupportTicket(request: Request):
    return EditSupportTicket(await request.json())

@app.post("/deletetblSupportTicket")
async def deletetblSupportTicket(request: Request):
    return DeleteSupportTicket(await request.json())


# --------------------------------------------------BuyerApis---------------------------------------

# ============================================================BUYER REGISTER =================

@app.get("/GettblBuyerRegister")
def GettblBuyerRegister():
    return GettblBuyerRegister1()


@app.post("/GettblBuyerRegisterById")
async def GettblBuyerRegisterById(request: Request):
    return GettblBuyerRegisterById1(await request.json())


@app.post("/savetblBuyerRegister")
async def savetblBuyerRegister(request: Request):
    return savetblBuyerRegister1(await request.json())


@app.post("/edittblBuyerRegister")
async def edittblBuyerRegister(request: Request):
    return edittblBuyerRegister1(await request.json())


@app.post("/ChangeBuyerPassword")
async def ChangeBuyerPassword(request: Request):
    return ChangeBuyerPassword1(await request.json())


@app.post("/deletetblBuyerRegister")
async def deletetblBuyerRegister(request: Request):
    return deletetblBuyerRegister1(await request.json())

# Buyer profile picture upload
@app.post("/uploadtblBuyerRegisterProfilePictureWithMeta")
async def upload_buyer_profile_picture(
        image: UploadFile = File(...),
        buyer_id: int = Form(...)
):
    return await uploadtblBuyerRegisterProfilePictureWithMeta1(
        image=image,
        buyer_id=buyer_id
    )

# buyer login contract ----------------------
@app.post("/GettblBuyerLoginFlexible")
async def buyer_login_flexible(request: Request):
    return GettblBuyerLoginFlexible1(await request.json())





# ==================== GOOGLE AUTH ====================

@app.post("/GoogleLogin")
async def google_login(request: Request):
    return GoogleLogin1(await request.json())

@app.post("/GoogleCompleteRegistration")
async def google_complete_registration(request: Request):
    return GoogleCompleteRegistration1(await request.json())


# For local dev/test with uvicorn
if __name__ == "__main__":
    uvicorn.run(
        "server:app",
        host="0.0.0.0",   # listen on all interfaces so phone can connect
        port=8000,
        reload=True
    )
