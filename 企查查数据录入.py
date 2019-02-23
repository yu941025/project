

#这段代码是将excal表数据存入mysql.

import xlrd
import mysql.connector

# tools . functions
def get_conn_cursor():
    host     = "localhost"
    user     = 'root'
    password = '123456'
    database = 'test_crawl'
    conn = mysql.connector.connect(host        = host,
                                   user        = user,
                                   password    = password,
                                   database    = database,
                                   use_unicode = True)
    return conn,conn.cursor()


# globals
conn,cursor = get_conn_cursor()
filename = './20180709_智能_无条件测试.xls'


def create_sql_table():
    sql = '''
    CREATE TABLE `company_info` (
      `id`                 int(11) NOT NULL AUTO_INCREMENT,
      `company`            varchar(100) DEFAULT NULL,
      `province`           varchar(20)  DEFAULT NULL,
      `city`               varchar(20)  DEFAULT NULL,
      `social_credit`      varchar(50)  DEFAULT NULL,
      `legal_person`       varchar(40)  DEFAULT NULL,
      `enterprise_type`    varchar(100) DEFAULT NULL,
      `create_date`        date DEFAULT NULL,
      `registered_capital` varchar(40)  DEFAULT NULL,
      `address`            varchar(150) DEFAULT NULL,
      `mailbox`            varchar(100) DEFAULT NULL,
      `scope_of_operation` varchar(255) DEFAULT NULL,
      `website`            varchar(255) DEFAULT NULL,
      `phone`              varchar(40)  DEFAULT NULL,
      `more_phone`         varchar(200) DEFAULT NULL,
      PRIMARY KEY (`id`),
      INDEX `company`      (`company`)      USING BTREE,
      INDEX `province`     (`province`)     USING BTREE,
      INDEX `city`         (`city`)         USING BTREE,
      INDEX `legal_person` (`legal_person`) USING BTREE,
      INDEX `create_date`  (`create_date`)  USING BTREE
    ) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
    '''
    try:
        cursor.execute(sql)
        conn.commit()
    except Exception as e:
        print(e,"数据库插入失败")

def insert_by_qcc_xls(filename,by_once=False):
    s = xlrd.open_workbook(filename)
    v = s.sheets()[0]
    insert_sql = '''
    insert company_info (
    company_info.company,
    company_info.province,
    company_info.city,
    company_info.social_credit,
    company_info.legal_person,
    company_info.enterprise_type,
    company_info.create_date,
    company_info.registered_capital,
    company_info.address,
    company_info.mailbox,
    company_info.scope_of_operation,
    company_info.website,
    company_info.phone,
    company_info.more_phone )
    VALUES
     %s '''

    test_has_sql = '''
    SELECT
    company_info.company,
    company_info.province,
    company_info.city,
    company_info.social_credit,
    company_info.legal_person
    FROM
    company_info
    WHERE
    company_info.company {} AND
    company_info.province {} AND
    company_info.city {} AND
    company_info.social_credit {} AND
    company_info.legal_person {}
    '''

    def test_has(row):
        q = ["="+repr(i) if i else 'is NULL' for i in row[:5]]
        cursor.execute(test_has_sql.format(*q))
        return cursor.fetchall()

    if by_once:
        p = []
        for i in range(v.nrows):
            if i == 0: continue
            hs = test_has(v.row_values(i))
            if not hs:
                c = "(" + str(v.row_values(i))[1:-1] + ")"
                p.append(c.replace("''",'NULL'))
        once_sql = insert_sql % ','.join(p)
        cursor.execute(once_sql)
        conn.commit()

    else:
        show_numb = 0
        insert_numb = 0
        for i in range(v.nrows):
            if i == 0: continue
            hs = test_has(v.row_values(i))# 识别数据库里是否存在：方法是通过前五条内容查找存在
            if not hs:
                c = "(" + str(v.row_values(i))[1:-1] + ")"
                peace_sql = insert_sql % c.replace("''",'NULL')
                try:
                    cursor.execute(peace_sql)
                    conn.commit()
                    insert_numb += 1
                except Exception as e:
                    print("插入数据条数：",insert_numb)
                    print(e)
                    print(c)
                    raise
                    
            else:
                if show_numb == 0:
                    print("插入存在重复...重复数据跳过")
                if show_numb<10:
                    print(hs)
                elif show_numb == 15:
                    print("...")
                    print("默认不展示超过15个之外的重复数据...")
                show_numb += 1
        print("插入数据条数：",insert_numb)


create_sql_table()
insert_by_qcc_xls(filename)




        
