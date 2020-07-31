import io
import re
import pymssql

def ABCDtonum(sort):
    if sort == 'A' or 'a' :
        return 1
    elif sort == 'B' or 'b' :
        return 2
    elif sort == 'C' or 'c':
        return 3
    elif sort == 'D' or 'd':
        return 4
    return

file = '示例2.txt'
f = open(file, 'r',encoding='utf-8')
lines = f.readlines()
f.close()
conn = pymssql.connect(server = "127.0.0.1:4343", database = "practice")
cursor=conn.cursor()
p=0 #指向进行到的行
while p< len(lines):

    if re.match(r"\d",lines[p]):
        title = re.search(r"[^0-9.]+",lines[p]).group().rstrip()
        sort = re.match(r"\d+",lines[p]).group()
        sql = "insert into dbo.Vote2(title,sort,status,voting_show_result,pid,item_align,is_must_answer,min_select,max_select,creater_uid,copy_id) " \
              "values (%s,%d,0,0,0,0,0,0,0,0,0)"
        cursor.execute(sql,(title,sort))
        p=p+1
        while p<len(lines)and lines[p]!='\n' :#当选项不是空行
            item_sort = ABCDtonum(re.match(r"[ABCDabcd]",lines[p]).group())
            item_title = re.search(r"[^ABCDabcd.]+",lines[p]).group().rstrip()
            item_sql = "insert into dbo.Vote_Item(vid,title,sort,creator_uid,status,parent_id,is_custom) " \
                  "values (0,%s,%d,0,0,0,0)"
            cursor.execute(item_sql,(item_title,item_sort))
            p = p+1
    p = p + 1
conn.commit()
conn.close()