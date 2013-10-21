# coding: utf-8

"""
    统一路径管理
"""

import os

from flask.ext.admin import Admin
from flask.ext import restful

from pub_app import app
from models import db
from views import UserView, PubTypeView, PubView, PubFile, UserMessageView, UserCollectView
from login import login_manager, login, logout
from restfuls import (UserInfo, UserLogin, UserRegister, PubGetType, PubListDetail, PubDetail, UserCollect,
                      PubCollect, PubPictureDetail, PubSearch, GetPubType, GetProvince, GetCity, GetCounty,
                      UserMessage, PubSearchView, GetPubTypeList, UserOpenIdCheck)

# 用户登陆管理
login_manager.init_app(app)
app.add_url_rule('/login', 'login', login)
app.add_url_rule('/logout', 'logout', logout)

# 后台管理系统路径管理
admin = Admin(name=u'冒冒')
admin.init_app(app)
admin.add_view(UserView(db, name=u'用户'))
admin.add_view(UserMessageView(db, name=u'用户私信', category=u'私信/收藏'))
admin.add_view(UserCollectView(db, name=u'用户收藏', category=u'私信/收藏'))

admin.add_view(PubTypeView(db, name=u'酒吧类型', category=u'酒吧'))
admin.add_view(PubView(db, name=u'酒吧详情', category=u'酒吧'))

### 文件管理
file_path = os.path.join(os.path.dirname(__file__), 'static')
admin.add_view(PubFile(file_path, '/static/', name='文件'))
picture_path = os.path.join(os.path.dirname(__file__), 'static/system/pub_picture')
#admin.add_view(PubPicture(picture_path, '/static/system/pub_picture/', name='图片'))  # todo-lyw 后期开启

# API接口
api = restful.Api(app)

### 后台获取相关ajax文件的路径
api.add_resource(GetPubType, '/restful/admin/pub_type')
api.add_resource(GetPubTypeList, '/restful/admin/pub_type_list/<int:pub_id>')
api.add_resource(GetProvince, '/restful/admin/province')
api.add_resource(GetCity, '/restful/admin/city/<int:province_id>')
api.add_resource(GetCounty, '/restful/admin/county/<int:city_id>')

### 接口文档路径管理
api.add_resource(UserRegister, '/restful/user/register')
api.add_resource(UserOpenIdCheck, '/restful/user/check')
api.add_resource(UserLogin, '/restful/user/login')
api.add_resource(UserInfo, '/restful/user/user_info/<int:user_id>')
api.add_resource(PubGetType, '/restful/pub/home')
api.add_resource(PubListDetail, '/restful/pub/list/detail')
api.add_resource(PubDetail, '/restful/pub/detail')
api.add_resource(UserCollect, '/restful/user/collect')
api.add_resource(PubCollect, '/restful/pub/collect')
api.add_resource(PubPictureDetail, '/restful/pub/picture')
api.add_resource(PubSearch, '/restful/pub/search')
api.add_resource(UserMessage, '/restful/user/message')
api.add_resource(PubSearchView, '/restful/pub/search/view')

## todo-lyw 代码末尾，形成的基本约定如下
# 文件相关的使用 static
# 接口相关的使用 restful
# 后台相关的使用 admin
# 网页相关的使用 域名！

