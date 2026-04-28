import re
import sys
import random
import string
import datetime
from datetime import timedelta
from sqlobject import *
from sqlobject import sqlhub, connectionForURI
from CommonFunction import log_exception


class phoneVerifications(SQLObject):
    phoneno         = StringCol(length=20, default=None)
    otpcode         = StringCol(length=6, default=None)
    isverified      = BoolCol(default=False)
    attempts        = IntCol(default=0)
    otp_status      = StringCol(length=20, default='PENDING')
    otp_expiry      = DateTimeCol(default=None)
    max_attempts    = IntCol(default=3)
    twilio_sid      = StringCol(length=100, default=None)
    country_code    = StringCol(length=5, default='+91')
    verified_at     = DateTimeCol(default=None)
    last_sent_at    = DateTimeCol(default=None)
    resend_count    = IntCol(default=0)
    max_resends     = IntCol(default=3)
    dtDateofCreation     = DateTimeCol(default=datetime.datetime.now)
    dtDateofModification = DateTimeCol(default=None)
    ynDeleted       = BoolCol(default=False)


def generate_otp(length=6):
    try:
        return ''.join(random.choices(string.digits, k=length))
    except Exception as e:
        log_exception(file_name="phoneVerificationsRepository_enhanced", function_name="generate_otp", exc=e)
        return None


def format_phone_number(phone_number, country_code='+91'):
    try:
        digits_only = re.sub(r'\D', '', phone_number)
        if phone_number.startswith('+91'):
            return phone_number
        elif phone_number.startswith('91') and len(digits_only) == 12:
            return f"+{digits_only}"
        elif len(digits_only) == 10 and digits_only[0] in '6789':
            return f"+91{digits_only}"
        else:
            return f"+91{digits_only}"
    except Exception as e:
        log_exception(file_name="phoneVerificationsRepository_enhanced", function_name="format_phone_number", exc=e)
        return phone_number


def GetPendingByPhone(phone_number):
    try:
        rows = phoneVerifications.select(AND(
            phoneVerifications.q.phoneno == phone_number,
            phoneVerifications.q.otp_status == 'PENDING',
            phoneVerifications.q.ynDeleted == False
        ))
        return rows[0] if rows.count() > 0 else None
    except Exception as e:
        log_exception(file_name="phoneVerificationsRepository_enhanced", function_name="GetPendingByPhone", exc=e)
        return None


def CreatePhoneVerification(phone_number, country_code='+91'):
    try:
        formatted = format_phone_number(phone_number, country_code)
        existing = GetPendingByPhone(formatted)
        if existing:
            existing.otp_status = 'EXPIRED'
            existing.dtDateofModification = datetime.datetime.now()

        otp_code = generate_otp()
        if not otp_code:
            return None

        return phoneVerifications(
            phoneno=formatted,
            otpcode=otp_code,
            isverified=False,
            attempts=0,
            otp_status='PENDING',
            otp_expiry=datetime.datetime.now() + timedelta(minutes=5),
            max_attempts=3,
            country_code=country_code,
            last_sent_at=datetime.datetime.now(),
            resend_count=0,
            max_resends=3,
        )
    except Exception as e:
        log_exception(file_name="phoneVerificationsRepository_enhanced", function_name="CreatePhoneVerification", exc=e)
        return None


def VerifyOTPCode(phone_number, otp_code):
    try:
        formatted = format_phone_number(phone_number)
        verification = GetPendingByPhone(formatted)

        if not verification:
            return {'success': False, 'message': 'No pending OTP found for this number', 'status': 'NO_PENDING'}

        if datetime.datetime.now() > verification.otp_expiry:
            verification.otp_status = 'EXPIRED'
            return {'success': False, 'message': 'OTP has expired. Please request a new one.', 'status': 'EXPIRED'}

        if verification.attempts >= verification.max_attempts:
            verification.otp_status = 'FAILED'
            return {'success': False, 'message': 'Too many wrong attempts. Request a new OTP.', 'status': 'MAX_ATTEMPTS'}

        if verification.otpcode == otp_code:
            verification.otp_status = 'VERIFIED'
            verification.isverified = True
            verification.verified_at = datetime.datetime.now()
            return {'success': True, 'message': 'OTP verified successfully', 'status': 'VERIFIED', 'phone': formatted}
        else:
            verification.attempts += 1
            remaining = verification.max_attempts - verification.attempts
            if verification.attempts >= verification.max_attempts:
                verification.otp_status = 'FAILED'
            return {'success': False, 'message': f'Wrong OTP. {remaining} attempts remaining.', 'status': 'INVALID_OTP', 'attempts_remaining': remaining}

    except Exception as e:
        log_exception(file_name="phoneVerificationsRepository_enhanced", function_name="VerifyOTPCode", exc=e)
        return {'success': False, 'message': 'Verification error', 'status': 'ERROR'}


def CanResendOTP(phone_number):
    try:
        verification = GetPendingByPhone(phone_number)
        if not verification:
            return True
        if verification.resend_count >= verification.max_resends:
            return False
        if verification.last_sent_at:
            elapsed = (datetime.datetime.now() - verification.last_sent_at).total_seconds()
            if elapsed < 60:
                return False
        return True
    except Exception as e:
        log_exception(file_name="phoneVerificationsRepository_enhanced", function_name="CanResendOTP", exc=e)
        return False


def UpdateTwilioSID(verification_id, twilio_sid):
    try:
        v = phoneVerifications.get(verification_id)
        v.twilio_sid = twilio_sid
        v.dtDateofModification = datetime.datetime.now()
    except Exception as e:
        log_exception(file_name="phoneVerificationsRepository_enhanced", function_name="UpdateTwilioSID", exc=e)


def IncrementResendCount(phone_number):
    try:
        v = GetPendingByPhone(phone_number)
        if v:
            v.resend_count += 1
            v.last_sent_at = datetime.datetime.now()
    except Exception as e:
        log_exception(file_name="phoneVerificationsRepository_enhanced", function_name="IncrementResendCount", exc=e)


sqlhub.processConnection = connectionForURI('sqlite:./world.sqlite3')
phoneVerifications.createTable(ifNotExists=True)
