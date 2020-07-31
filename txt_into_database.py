import io
import re
import pymssql
'''
Author:崔玉婷
2020/7/31
功能：将txt格式调查问卷写入数据库
需要严格遵守对txt规定的要求，否则会报错
'''
def ABCDtonum(sort):
    if sort == 'A' or sort =='a' :
        return 1
    elif sort == 'B' or sort =='b' :
        return 2
    elif sort == 'C' or sort =='c':
        return 3
    elif sort == 'D' or sort =='d':
        return 4
    return

def to_input_type(str):
    if str == None or str == '单选题':
        return 'radio'
    elif str == '多选题':
        return 'checkbox'
    elif str == '填空题':
        return 'text'
    return

file = '示例.txt'
f = open(file, 'r',encoding='utf-8')
lines = f.readlines()
f.close()
conn = pymssql.connect(server = "127.0.0.1:4343", database = "demo")
cursor=conn.cursor()
#插入Poll中数据，只读取标题
cursor.execute("insert into dbo.Poll(title,type,group_id,status) values (%s,0,0,0)",(lines[0]))
pid = cursor.lastrowid
p=1 #指向进行到的行
#插入Vote中数据,只读取题目的内容，序号，类型
while p< len(lines):

    if re.match(r"\d",lines[p]):
        sort = re.match(r"\d+",lines[p]).group()
        title = re.search(r"[^0-9.\[]+",lines[p]).group().rstrip()
        str = re.search(r"\[(\S+)\]",lines[p])
        if str == None:
            input_type = 'radio'
        else:
            input_type = to_input_type(str.group(1))
        sql=[]
        if input_type =='radio' :
            sql = "insert into dbo.Vote(title,sort,input_type,status,voting_show_result,pid,item_align,is_must_answer,min_select,max_select,creater_uid,copy_id) " \
                  "values (%s,%d,%s,0,0,%d,0,0,1,1,0,0)"
        else:
            sql = "insert into dbo.Vote(title,sort,input_type,status,voting_show_result,pid,item_align,is_must_answer,min_select,max_select,creater_uid,copy_id) " \
              "values (%s,%d,%s,0,0,%d,0,0,0,0,0,0)"
        cursor.execute(sql,(title,sort,input_type,pid))
        vid = cursor.lastrowid
        p=p+1
        while p<len(lines)and lines[p]!='\n' :#当不是空行,插入Vote_Item中数据
            item_sort = ABCDtonum(re.match(r"[ABCDabcd]",lines[p]).group())
            item_title = re.search(r"[^ABCDabcd.]+",lines[p]).group().rstrip()
            item_sql = "insert into dbo.Vote_Item(vid,title,sort,creator_uid,status,parent_id,is_custom) " \
                  "values (%d,%s,%d,0,0,0,0)" #只读取选项的内容，序号
            cursor.execute(item_sql,(vid,item_title,item_sort))
            p = p+1
        if(input_type == 'checkbox'):
            cursor.execute("select COUNT(*) from dbo.Vote_Item where vid = %d",vid)
            max_select = cursor.fetchone()[0]
            cursor.execute("update dbo.Vote set max_select = %d , min_select = 1 where id = %d",(max_select,vid))
    p = p + 1
conn.commit()
conn.close()