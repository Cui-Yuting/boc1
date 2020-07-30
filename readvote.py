import io
import re
import pymssql

class Vote:
    '问题类'
    def __init__(self, title):
        self.title = title
        self.id = None
        self.description = None
        self.sort = 0
        self.input_type = 'a'
        self.data_type = 'a'
        self.status = 0
        self.voting_show_result = 0
        self.pid = 0
        self.item_align = 0
        self.is_must_answer = 0
        self.min_select = 0
        self.max_select = 0
        self.uniqueid = None
        self.creater_uid = 0
        self.copy_id = 0

file = '示例2.txt'
f = open(file, 'r',encoding='utf-8')
lines = f.readlines()
f.close()
conn = pymssql.connect(server = "127.0.0.1:4343", database = "practice")
cursor=conn.cursor()
for line in lines:
    if re.match(r"\d",line):
        str = re.search(r"[^0-9.]+",line).group().rstrip()
        #vote1.id, vote1.title, vote1.description, " \
        #              "
        #vote1.sort, vote1.input_type, vote1.data_type, vote1.status, vote1.voting_show_result, " \
        #              "
        #vote1.pid, vote1.item_align, vote1.is_must_answer, vote1.min_select, vote1.max_select, " \
        #              "
        #vote1.uniqueid, vote1.creater_uid, vote1.copy_id#
        sql = "insert into dbo.Vote2(title,sort,status,voting_show_result,pid,item_align,is_must_answer,min_select,max_select,creater_uid,copy_id) " \
              "values (%s,1,0,0,0,0,0,0,0,0,0)"
        cursor.execute(sql,(str))

conn.commit()
conn.close()