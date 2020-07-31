import io
import re
import pymssql

def ABCDtonum(sort):
    if sort == 'A'|'a' :
        return 1
    elif sort == 'B'|'b' :
        return 2
    elif sort == 'C'|'c':
        return 3
    elif sort == 'D'|'d':
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
        sort = re.match(r"\d+",lines[p])
        sql = "insert into dbo.Vote2(title,sort,status,voting_show_result,pid,item_align,is_must_answer,min_select,max_select,creater_uid,copy_id) " \
              "values (%s,%d,0,0,0,0,0,0,0,0,0)"
        cursor.execute(sql,(title,sort))
        p=p+1
        while lines[p]:#当选项不是空行
            item_sort = ABCDtonum(re.match(r"[ABCDabcd]",lines[p]))
            item_title = re.search(r"[^ABCDabcd.]+",lines[p]).group().rstrip()
            item_sql = "insert into dbo.Vote_Item(vid,title,sort,creator_uid,status,parent_id,is_custom)" \
                  "values(0,%s,%d,0,0,0,0)"
            cursor.execute(item_sql,(item_title,item_sort))
            p = p+1
    p = p + 1
conn.commit()
conn.close()