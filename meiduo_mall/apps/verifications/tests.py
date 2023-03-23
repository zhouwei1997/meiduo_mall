# Create your tests here.
from ronglian_sms_sdk import SmsSDK

from verifications import constants


def send_message():
    sdk = SmsSDK(constants.ACCOUNT_SID, constants.AUTH_TOKEN, constants.APP_ID)
    tid = '1'
    mobile = '15027130472'
    datas = ('123456', '5分钟')
    resp = sdk.sendMessage(tid, mobile, datas)
    print(resp)


send_message()
