/* MySQL 数据库 */
/* 创建用户 'py'，host 为 'localhost'，密码为 'py_passwd'，该用户对数据库 shorturl 下所有表拥有所有权限 */
grant all on shorturl.* to 'py'@'localhost' identified by "py_passwd";

/* 创建用户 'readonly'，host 为 'localhost'，密码为 'readonly_passwd'，该用户对数据库 shorturl 下所有表拥有 select 权限 */
grant select on shorturl.* to 'readonly'@'localhost' identified by "readonly_passwd";

create database shorturl default charset utf8;

use shorturl;

create table url (
    id int(10) not null auto_increment,
    shorten char(8) not null,
    expand text not null,
    primary key(id)
)engine=InnoDB default charset utf8;
