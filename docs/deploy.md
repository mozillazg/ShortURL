## 全新安装/从 web.py 版本升级

1. 安装 python2.7
    ```
    rpm -Uvh http://dl.iuscommunity.org/pub/ius/stable/CentOS/6/x86_64/ius-release-1.0-14.ius.centos6.noarch.r
    rpm -Uvh http://download.fedoraproject.org/pub/epel/6/x86_64/epel-release-6-8.noarch.rpm

    yum install -y python27 python27-devel python27-pip python27-virtualenv
    pip install supervisor
   ```
2. 更新代码
   ```
   git pull
   git checkout django
   ```
3. 创建虚拟环境：
    ```
    cd /alidata/www/shorturl-conf/
    virtualenv-2.7 .shorturl
    ```
4. 激活虚拟环境:
    ```
    source .shorturl/bin/activate  # 效果就是会显示类似 (.shorturl)[xxx]# 
    ```
5. 安装依赖:
    ```
    source /alidata/www/shorturl-conf/.shorturl/bin/activate
    cd /alidata/www/ShortURL
    pip2.7 install -r requirements.txt --index http://pypi.douban.com/simple --trusted-host pypi.douban.com
    pip2.7 install setproctitle --index http://pypi.douban.com/simple --trusted-host pypi.douban.com
    ```
6. 更改配置:
    ```
    cd /alidata/www/ShortURL
    cp shorturl/shorturl/settings.py.sample shorturl/shorturl/settings.py
    vim shorturl/shorturl/settings.py
    ```
7. 迁移数据库:
   ```
   source /alidata/www/shorturl-conf/.shorturl/bin/activate
   cd /alidata/www/ShortURL/shorturl
   # 备份数据库
   mysqldump -uwh -p shorturl >shorturl.sql

   # 应用新的表结构
    python manage.py migrate auth
    python manage.py migrate contenttypes
    # 如果是迁移自旧的 web.py 版本，执行下面这条命令
    # python manage.py migrate --fake shorten 0001
    python manage.py migrate

   # 创建管理员账号
   python manage.py createsuperuser
   ```
8. 复制静态文件
   ```
   source /alidata/www/shorturl-conf/.shorturl/bin/activate
   cd /alidata/www/ShortURL/shorturl
   python manage.py collectstatic
   ```
9. 配置服务器
   ```
   cp /alidata/www/ShortURL/etc/* /alidata/www/shorturl-conf/
   cd /alidata/www/shorturl-conf/
   mv gunicorn.py.sample gunicorn.py    # 修改内容
   mv nginx.conf.sample nginx.conf      # 修改内容
   mv supervisord.conf.sample supervisord.conf   # 修改内容

    echo_supervisord_conf > /etc/supervisord.conf
   vim /etc/supervisord.conf # 增加 以下内容
    [include]
    files = /alidata/www/shorturl-conf/supervisord.conf

    # 配置 supervisord 服务
    wget https://github.com/Supervisor/initscripts/raw/master/redhat-init-equeffelec -O /etc/init.d/supervisord
    chmod +x /etc/init.d/supervisord
    chkconfig add supervisord

10. 启动
    ```
    # 配置目录权限
    chown www:www /alidata/www/ShortURL -R
    chown www:www /alidata/www/shorturl-conf -R

    service supervisord start
    ```

11. 管理
    ```
    # web 程序在 supervisorctl 中进行管理
    # supervisorctl
    shorturl                         RUNNING   pid 12283, uptime 0:00:03
    supervisor> reread                # 重新读取配置文件
    supervisor> update shorturl       # 更新 shorturl
    supervisor> restart shorturl      # 重启 shorturl
    supervisor> stop shorturl         # 停止 shorturl
    ```

12. 开机启动
    ```
    chkconfig mysqld on
    chkconfig supervisord on
    ```



## 修改域名

* 更改 settings.py 中的 `ALLOWED_HOSTS` 和 `SITE_URL`
    ```
    vim /alidata/www/ShortURL/shorturl/shorturl/settings.py
    ```

* 更改 nginx.conf 中的 `server_name`
    ```
    vim /alidata/www/shorturl-conf/nginx.conf
    ```
* 应用更改
    ```
    nginx -t
    nginx -s reload
    supervisorctl restart shorturl
    ```
