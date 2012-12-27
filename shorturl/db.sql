create database shorturl default charset utf8;

use shorturl;

create table url (
    id int(10) not null auto_increment,
    shorten char(8) not null,
    expand text not null,
    primary key(id)
)engine=InnoDB default charset utf8;

