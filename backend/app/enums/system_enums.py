from enum import IntEnum

class LoginLogTypeEnum(IntEnum):
    LOGIN_USERNAME = 100  # 使用账号登录
    LOGIN_SOCIAL = 101    # 使用社交登录
    LOGIN_MOBILE = 103    # 使用手机登陆
    LOGIN_SMS = 104       # 使用短信登陆
    LOGOUT_SELF = 200     # 自己主动登出
    LOGOUT_DELETE = 202   # 强制退出

class LoginResultEnum(IntEnum):
    SUCCESS = 0             # 成功
    BAD_CREDENTIALS = 10    # 账号或密码不正确
    USER_DISABLED = 20      # 用户被禁用
    CAPTCHA_NOT_FOUND = 30  # 图片验证码不存在
    CAPTCHA_CODE_ERROR = 31 # 图片验证码不正确
