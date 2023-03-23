# Create your tests here.

from verifications.views import CCP


def sent_SMS_test():
    ccp = CCP()
    ccp.send_template('1', '15027130472', ['123456', '5分钟'])


if __name__ == '__main__':
    sent_SMS_test()
