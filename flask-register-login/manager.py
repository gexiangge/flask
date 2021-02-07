# @Time    : 2020-11-02 17:07
# @Author  : 老赵
# @File    : manager.py
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from core import db
from core import create_app
from core.models import UserLogin

# 创建 app，并传入配置模式：development / production / test
app = create_app('development')
# 创建脚本管理器对象
manager = Manager(app)
# 让迁移和app和数据库建立管理
Migrate(app, db)
# 将数据库迁移的脚本添加到manager
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
