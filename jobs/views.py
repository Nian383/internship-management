import pymysql
from django.shortcuts import render


def show_internships(request):# 定义一个函数，处理浏览器访问请求
    # 1. 连接数据库（就像你用Navicat点“连接”按钮一样）
    connection = pymysql.connect(
        host='localhost',# 数据库在我自己电脑上
        user='root',# 用户名
        password='123456',  # 密码
        database='my_python_db',# 连接哪个库
        charset='utf8mb4' # 字符集，用来显示中文
    )
    try:# 2. 拿起鼠标（游标），准备执行SQL语句
        with connection.cursor() as cursor:
            # 3. 这就是你刚才在Navicat里运行的那条JOIN查询！
            cursor.execute("""
                SELECT s.name, c.name, i.position, i.start_date
                FROM internships i
                JOIN students s ON i.student_id = s.id
                JOIN companies c ON i.company_id = c.id
            """)
            # 4. 把查到的所有行数据拿走（就像复制查询结果）
            results = cursor.fetchall()
    finally:
        # 5. 关掉连接（用完要关门）
        connection.close()
    # 6. 把查到的数据（results）交给HTML网页去显示
    return render(request, 'internship_list.html', {'data': results})