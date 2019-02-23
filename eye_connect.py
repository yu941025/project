__author__ = 'Administrator'
import pymysql
import time
import datetime
import eye_logs
conn=pymysql.connect(host='localhost',port=3306,user='root',password='123456',database='yuzhixiang')
cursor=conn.cursor()
table_name='zhejiang'
sql='''
create TABLE `{}`(
  `id` bigint(20) NOT  NULL AUTO_INCREMENT,
  `company` VARCHAR (100) NOT NULL COMMENT '公司名称',
  `province` VARCHAR (20) NOT  NULL COMMENT '省份',
   `city`   VARCHAR (20) NOT  NULL COMMENT '城市',
   `legal_person` VARCHAR (20) NOT NULL COMMENT '法定代表人',
   `phone` VARCHAR (100) DEFAULT NULL COMMENT '电话',
   `email` VARCHAR (100) DEFAULT NULL COMMENT '邮箱',
   `url` VARCHAR (100) NOT NULL COMMENT '天眼查地址',
  `create_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  INDEX `company` (`company`) USING BTREE

) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT  CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT '企业信息表'
'''.format(table_name)
sql1='''
create TABLE `url`(
`id` bigint(20) not NULL  AUTO_INCREMENT,
`url` VARCHAR (100) NOT NULL COMMENT 'url地址',
PRIMARY KEY (`id`),
index `url`(`url`)  USING BTREE

) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT  CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT '企业信息表'
'''

sql2='''
  create TABLE `proxies`(
  `type`  VARCHAR (20) DEFAULT  NULL ,
  `ip`    VARCHAR (100) DEFAULT NULL ,
  `port`  VARCHAR (20) DEFAULT  NULL ,
  INDEX `ip` (`ip`) USING BTREE
)ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4;
'''
try:
    cursor.execute(sql)
    conn.commit()
    eye_logs.info('创建成功')
except:
    eye_logs.logger.info('数据库%s已存在'%table_name)

try:
    cursor.execute(sql1)
    conn.commit()
    eye_logs.logger.info('创建成功')
except:
    eye_logs.logger.info('数据库url已存在')
try:
    cursor.execute(sql2)
    conn.commit()
except:
    eye_logs.logger.info('数据库proxies已存在')

sql3='select url from url'
try:
    cursor.execute(sql3)

    url_tuple=cursor.fetchall()
    ii_list=[]
    for i in url_tuple:
        ii_list.append(i[0])


except:
    url_tuple=('',)
    print('查询无数据')
sql4='select ip from proxies'#查询代理ip
try:
    cursor.execute(sql4)
    conn.commit()
    ip_tuples=cursor.fetchall()
    ip_tuple=[]
    for i in ip_tuples:
        ip_tuple.append(i[0])




except:
    print('查询失败')
