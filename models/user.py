# coding: utf-8

"""
    user与user_info数据库表的定义，本模块定义了User和UserInfo两个类。
    定义了user和user_info的ORM类。
    User: User类，主要是用户登录相关。
    UserInfo: UserInfo类，主要是用户个人信息。
"""

from sqlalchemy import Column, Integer, String, Boolean, DATETIME, ForeignKey, desc

from .database import Base
from models.level import get_level
from utils import todayfstr
from utils.ex_password import check_password, generate_password

USER_TABLE = 'user'
USER_INFO_TABLE = 'user_info'


class User(Base):
    """User类，对应于数据库的user表
    id
    login_type 用户登录类型，Integer(4)， 0表示注册用户 1表示微博登录 2表示QQ登录
    login_name 用户登录名，同一类型的登陆用户，登录名不能一样，第三方登陆用户可以为空
    password 用户密码，使用加密
    open_id 第三方登陆的openId
    nick_name 用户昵称，不可重复，第三方注册用户必须填写昵称，评论的时候使用
    sign_up_date 用户注册时间
    system_message_time 用户最后读取系统消息的时间，如果设置不读取系统消息，设置为NULL
    admin 是否具有管理员权限 0否 1是
    """

    __tablename__ = USER_TABLE

    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8'
    }

    id = Column(Integer, primary_key=True)
    login_name = Column(String(32), nullable=True, server_default=None, unique=True)
    password = Column(String(64), nullable=True, server_default=None)
    login_type = Column(Integer, nullable=False, server_default='0')
    open_id = Column(String(64), nullable=True, server_default=None)
    nick_name = Column(String(32), nullable=False, unique=True)
    sign_up_date = Column(DATETIME, nullable=True, server_default=None)
    system_message_time = Column(DATETIME, nullable=True, server_default=None)
    admin = Column(Boolean, nullable=False, server_default='0')

    def __init__(self, **kwargs):
        self.login_type = kwargs.pop('login_type')
        self.nick_name = kwargs.pop('nick_name')
        self.sign_up_date = todayfstr()
        self.login_name = kwargs.pop('login_name', None)

        password = kwargs.pop('password', None)
        if password is not None:
            self.password = generate_password(password)
        else:
            self.password = password

        self.open_id = kwargs.pop('open_id', None)
        self.system_message_time = kwargs.pop('system_message_time', todayfstr())  # string "2012-09-23 23:23:23"
        self.admin = kwargs.pop('admin', 0)

    def __repr__(self):
        return '<User(nick_name: %s, login_type: %s, sign_up_date: %s)>' % (self.nick_name, self.login_type,
                                                                            self.sign_up_date)

    def update(self, **kwargs):
        self.login_type = kwargs.pop('login_type')
        self.nick_name = kwargs.pop('nick_name')
        self.login_name = kwargs.pop('login_name', None)

        password = kwargs.pop('password', None)
        if password is not None:
            if self.password != password:
                self.password = generate_password(password)
        else:
            self.password = password

        self.open_id = kwargs.pop('open_id', None)
        self.system_message_time = kwargs.pop('system_message_time', None)
        self.admin = kwargs.pop('admin', 0)

    def change_password(self, old_password, new_password):
        """设置用户密码"""

        if new_password is None:
            return False

        if old_password is None:
            if self.password is None:
                self.password = generate_password(new_password)
                return True
            else:
                return False
        else:
            if self.check_password(old_password):
                self.password = generate_password(new_password)
                return True
            else:
                return False

    def check_password(self, password):
        """检查密码是否正确"""

        if (password is None) and (self.password is None):
            return True

        if (password is None) or (self.password is None):
            return False

        return check_password(password, self.password)

    def is_authenticated(self):  # todo-lyw 静态method是如何用的，和类方法的不同
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def is_admin(self):
        return bool(self.admin)

    def get_id(self):
        return self.id


class UserInfo(Base):
    """UserInfo类，对应数据库user_info表
    id
    user_id 用户ID 外键 ON DELETE CASCADE ON UPDATE CASCADE
    mobile 手机号 18721912400 或者 +8618721912400
    tel 固话号码 1872191 或者 07141872191
    real_name 真实姓名
    sex
    birthday_type 生日类型 0 农历 1 阳历
    birthday 出生日期
    intro 个人简介
    signature 个性签名
    ethnicity_id 民族的ID
    company 公司
    job 工作
    email 密码重置邮箱，也是用户邮箱，如果登陆名是邮箱，默认是重置邮箱
    province_id 省ID
    city_id 市ID
    county_id 区县ID
    street 地址更下一级的描述，街道门牌号等等
    base_path 头像的根目录
    rel_path 头像的相对目录
    pic_name 头像存储的文件名
    upload_name 上传时候文件名
    credit 积分
    reputation 经验值
    """

    __tablename__ = USER_INFO_TABLE

    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8'
    }

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey(User.id, ondelete='cascade', onupdate='cascade'), nullable=False)
    mobile = Column(String(16), nullable=True, server_default=None)
    tel = Column(String(16), nullable=True, server_default=None)
    real_name = Column(String(32), nullable=True, server_default=None)
    sex = Column(Boolean, nullable=True, server_default=None)
    birthday_type = Column(Boolean, nullable=True, server_default=None)
    birthday = Column(DATETIME, nullable=True, server_default=None)  # string "2012-09-23 23:23:23"
    intro = Column(String(128), nullable=True, server_default=None)
    signature = Column(String(128), nullable=True, server_default=None)
    ethnicity_id = Column(Integer, nullable=True, server_default=None)
    company = Column(String(32), nullable=True, server_default=None)
    job = Column(String(32), nullable=True, server_default=None)
    email = Column(String(32), nullable=True, server_default=None)
    province_id = Column(Integer, nullable=True, server_default=None)
    city_id = Column(Integer, nullable=True, server_default=None)
    county_id = Column(Integer, nullable=True, server_default=None)
    street = Column(String(64), nullable=True, server_default=None)
    base_path = Column(String(128), nullable=True, server_default=None)
    rel_path = Column(String(128), nullable=True, server_default=None)
    pic_name = Column(String(128), nullable=True, server_default=None)
    upload_name = Column(String(128), nullable=True, server_default=None)
    credit = Column(Integer, nullable=False, server_default="0")
    reputation = Column(Integer, nullable=False, server_default="0")

    def __init__(self, **kwargs):
        self.user_id = kwargs.pop('user_id')
        self.email = kwargs.pop('email', None)
        self.mobile = kwargs.pop('mobile', None)
        self.tel = kwargs.pop('tel', None)
        self.real_name = kwargs.pop('real_name', None)
        self.sex = kwargs.pop('sex', None)
        self.birthday_type = kwargs.pop('birthday_type', None)
        self.birthday = kwargs.pop('birthday', None)
        self.intro = kwargs.pop('intro', None)
        self.signature = kwargs.pop('signature', None)
        self.ethnicity_id = kwargs.pop('ethnicity_id', None)
        self.company = kwargs.pop('company', None)
        self.job = kwargs.pop('job', None)
        self.province_id = kwargs.pop('province_id', None)
        self.city_id = kwargs.pop('city_id', None)
        self.county_id = kwargs.pop('county_id', None)
        self.street = kwargs.pop('street', None)
        self.base_path = kwargs.pop('base_path', None)
        self.rel_path = kwargs.pop('rel_path', None)
        self.pic_name = kwargs.pop('pic_name', None)
        self.upload_name = kwargs.pop('upload_name', None)
        self.credit = kwargs.pop('credit', '20')
        self.reputation = kwargs.pop('reputation', '50')

    def update(self, **kwargs):
        self.user_id = kwargs.pop('user_id')
        self.email = kwargs.pop('email')
        self.credit = kwargs.pop('credit')
        self.reputation = kwargs.pop('reputation')
        mobile = kwargs.pop('mobile', None)
        tel = kwargs.pop('tel', None)
        real_name = kwargs.pop('real_name', None)
        sex = kwargs.pop('sex', None)
        birthday_type = kwargs.pop('birthday_type', None)
        birthday = kwargs.pop('birthday', None)
        intro = kwargs.pop('intro', None)
        signature = kwargs.pop('signature', None)
        ethnicity_id = kwargs.pop('ethnicity_id', None)
        company = kwargs.pop('company', None)
        job = kwargs.pop('job', None)
        province_id = kwargs.pop('province_id', None)
        city_id = kwargs.pop('city_id', None)
        county_id = kwargs.pop('county_id', None)
        street = kwargs.pop('street', None)
        base_path = kwargs.pop('base_path', None)
        rel_path = kwargs.pop('rel_path', None)
        pic_name = kwargs.pop('pic_name', None)
        upload_name = kwargs.pop('upload_name', None)

        self.update_none(mobile=mobile,
                         tel=tel,
                         real_name=real_name,
                         sex=sex,
                         birthday_type=birthday_type,
                         birthday=birthday,
                         intro=intro,
                         signature=signature,
                         ethnicity_id=ethnicity_id,
                         company=company,
                         job=job,
                         province_id=province_id,
                         city_id=city_id,
                         county_id=county_id,
                         street=street,
                         base_path=base_path,
                         rel_path=rel_path,
                         pic_name=pic_name,
                         upload_name=upload_name)

    def update_none(self, **kwargs):
        for key in kwargs:
            if key:
                setattr(self, key, kwargs[key])

    def __repr__(self):
        return '<UserInfo(user_id: %s, email: %s)>' % (self.user_id, self.email)

    def path(self):
        return self.base_path + self.rel_path + '/'

    def add_reputation(self, type_string, days=None):
        """添加经验值的函数，number是经验值的多少"""
        number = self.get_add_reputation(type_string, days)
        self.reputation += number

    def add_credit(self, type_string, days=None):
        """添加积分的函数"""
        number = self.get_add_credit(type_string, days)
        self.credit += number

    def get_add_reputation(self, type_string, days=None):
        """通过类型获取经验值
        register 注册 50 = 只有一次
        info 完善资料 20 = 只有一次
        login 登陆 10 = 每天登陆加一次，累计 10 * days
        pub_sign 酒吧签到 10 = 收藏一次添加一次
        pub 收藏酒吧 20 收藏一次加一次
        activity 收藏活动 20 = 收藏一次加一次
        message 发送私信 20 = 发给一个人无论多少次算一次，每个人都加一次
        gift 发送礼物 20  = 发一次加一次
        greet 发送传情 20 = 发一次加一次
        invite 发送邀请 20 = 邀请一次加一次
        online 在线时间 20 = 只有一次
        """

        if type_string == "register":
            return 50
        if type_string in ["online", "activity", "pub", "info", "invite", "greet", "gift", "message"]:
            return 20
        if type_string == "pub_sign":
            return 10
        if type_string == "login":
            if (days is None) or (days <= 0):
                raise ValueError
            return 10 * days

        raise ValueError

    def get_add_credit(self, type_string, days=None):
        """通过类型获取积分
        register 注册 20 = 只有一次
        info 完善资料 20 = 只有一次
        login 登陆 10 = 每天登陆加一次，累计 10*days
        pub_sign 酒吧签到 10  = 签到一次添加一次
        pub 收藏酒吧 20 收藏一次加一次
        activity 收藏活动 20 = 收藏一次加一次
        message 收到私信 10 = 同一个人的算一次，多个人多次
        gift 接收礼物 10  = 收一次加一次
        greet 收到传情 10 = 发一次加一次
        invite 收到邀请 10 = 邀请一次加一次
        online 在线时间（满一个小时） 20
        """

        level = get_level(self.reputation)[0]

        if type_string in ["register", "info", "pub", "activity", "online"]:
            return 20
        if type_string == "pub_sign":
            return 10
        if type_string in ["message", "gift", "greet", "invite"]:
            return 10+level
        if type_string == "login":
            if (days is None) or (days <= 0):
                raise ValueError
            return 10 * days

        raise ValueError