#coding:utf-8
#env: python3
#description:

import pymysql
import readline
import sys

class Mysql:


    def __init__(self, host, port, user, password, database):
        """
        mysql初始化
        :param host:
        :param password:
        :param port:
        :param database:
        """

        try:
            self.db = pymysql.connect(host=host, port=int(port), user=user, password=password, database=database)

            # 游标设置为字典类型，默认返回是元祖
            self.cursor = self.db.cursor(pymysql.cursors.DictCursor)
        except pymysql.MySQLError as e:
            print(e.args)



    def insert_many(self, table, data):
        """
        params：data：列表字典

        executemany添加的数据必须为list[tuple(),tuple()]或者tuple(tuple(),tuple())

        在写sql语句时，不管字段什么类型，占位符统一用%s
        """
        if data is None:
            print("%s表数据为空!" % table)
            print("")
        else:
            ex_many_data = []
            keys = ', '.join(list(data[0].keys()))
            values = ','.join(['%s'] * len(data[0]))
            sql = 'INSERT INTO {table}({keys}) VALUES ({values}) ON DUPLICATE KEY UPDATE'.format(table=table, keys=keys, values=values)
            update = ','.join([" {key} = values({key})".format(key=key) for key in data[0]])
            sql += update
            for row in data:
                ex_many_data.append(list(row.values()))

            try:
                # executemany对应的是一个列表或者元祖
                self.cursor.executemany(sql, ex_many_data * 2)
                print('insert %s data Successful' % table)
                print("")
                self.db.commit()
            except pymysql.MySQLError as e:
                print("insert %s data Fail !" % table)
                print(e.args)
                self.db.rollback()
            finally:
                self.cursor.close()
                self.db.close


    def fetch_all(self, table, sql):
        """
        查询多条

        """
        try:
            rows = self.cursor.execute(sql)
            if rows > 0:
                print("同步%s表%s行" % (table, rows))
                # fetchall返回二维列表字典（默认二维元祖）
                data = self.cursor.fetchall()
                return data
            else:
                return None
        except pymysql.MySQLError as e:
            print(e.args)
            return None
        finally:
            self.cursor.close()
            self.db.close

def sync(table,sql):
    p_conn = Mysql(host='134.175.34.237', port=906, user='ehuzhu_dba', password='kdo!IOL2343@s3a', database='ehuzhu')
    t_conn = Mysql(host='134.175.34.237', port=907, user='ehuzhu_dba', password='kdo!IOL2343@s3a', database='ehuzhu')

    p_data = p_conn.fetch_all(table, sql)
    t_conn.insert_many(table, p_data)
    

def start_sync(mobile_no):
    # 执行同步
    mobile_no = mobile_no
   # mobile_no = str(input("start synchronizing data, please input your phone number: ")).strip()
    print("mobile_no:%s" % mobile_no)
    print("")
    # 输入需要同步的表名
    table_name = [  'member',
                    'sdfundsettlementdetailtemp_history',
                    'insteaddebit', 'fa_family_account',
                    'fa_family_account_relationship',
                    'sdfundsettlementdetail',
                    'sdcontract',
                    'TradeInformation',
                    'TradeInformationB',
                    'cashaccount',
                    'cashaccountsummary',
                    'cashaccountebi',
                    'c_integral_totle',
                    'c_integral_level',
                ]
    print("同步表如下%s" % table_name)

    
    #从生产查：memberid
    p_conn = Mysql(host='134.175.34.237',port=906, user='ehuzhu_dba', password='kdo!IOL2343@s3a', database='ehuzhu')
    sql_member = "select * from member where mobileNo='%s'" % mobile_no
    member_list = p_conn.fetch_all('member', sql_member)

    # 判断从数据库中取出的数据列表
    if not member_list:
        result = ["您输入的手机号不存在，同步失败！"]
        return result

    member_id = member_list[0]['id']
    print("")

    
    #从生产查：family_account_id
    p_conn =  Mysql(host='134.175.34.237', port=906, user='ehuzhu_dba', password='kdo!IOL2343@s3a', database='ehuzhu')
    sql_fa_family_account = "select * from fa_family_account where manager_id='%s'" % member_id
    family_account_list = p_conn.fetch_all('fa_family_account', sql_fa_family_account)

    if not family_account_list:
        result = ["family_account_id不存在，同步失败！"]
        return result
    family_account_id = family_account_list[0]['id']
    print("")


    # 同步member
    sql_member = "select * from member where id='%s'" %  member_id
    sync('member', sql_member)  
    
    sql_sd_history = "select * from sdfundsettlementdetailtemp_history where pay_id ='%s'" % member_id
    sync('sdfundsettlementdetailtemp_history', sql_sd_history)
         
    sql_insteaddebit = "select * from insteaddebit where pay_id='%s'" % member_id
    sync('insteaddebit', sql_insteaddebit)
    
    sql_fa_family_account = "select * from fa_family_account where manager_id='%s'" % member_id
    sync('fa_family_account', sql_fa_family_account)
    
    sql_fa_family_account_relationship = "select * from fa_family_account_relationship where family_account_id='%s'" % family_account_id 
    sync('fa_family_account_relationship', sql_fa_family_account_relationship)   

    if family_account_id:
        sql_sd_detail = "select * from sdfundsettlementdetail where memberId in (select family_member_id from fa_family_account_relationship where family_account_id='%s')" % family_account_id
        sync('sdfundsettlementdetail', sql_sd_detail)
    else:
        sql_sd_detail = "select * from sdfundsettlementdetail where memberId='%s'" % member_id
        sync('sdfundsettlementdetail', sql_sd_detail)

    sql_sdcontract = "select * from sdcontract where pay_id='%s'" % member_id
    sync('sdcontract', sql_sdcontract)

    sql_TradeInformation = "select * from tradeinformation where memberID='%s'" % member_id
    sync('tradeinformation', sql_TradeInformation)

    sql_cashaccount = "select * from cashaccount where memberID='%s'" % member_id
    sync('cashaccount', sql_cashaccount)

    sql_cashaccountsummary = "select * from cashaccountsummary where member_id='%s'" % member_id
    sync('cashaccountsummary', sql_cashaccountsummary)

    sql_cashaccountebi  = "select * from cashaccountebi where memberID='%s'" % member_id
    sync('cashaccountebi', sql_cashaccountebi)

    sql_c_integral_totle = "select * from c_integral_totle where memberid='%s'" % member_id
    sync('c_integral_totle', sql_c_integral_totle)

    sql_c_integral_level = "select * from c_integral_level where member_id='%s'" % member_id
    sync('c_integral_level', sql_c_integral_level)

    table_name.append("同步上述表完成")
    result = table_name
    return result
