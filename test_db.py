import pymysql

# 1. 连上你的数据库（把 password 改成你的）
connection = pymysql.connect(
    host='localhost',
    user='root',  # 默认用户名一般是 root
    password='123456',  # ⚠️ 改成你安装MySQL时设的密码！！！
    database='my_python_db',
    charset='utf8mb4'
)

try:
    with connection.cursor() as cursor:
        # 2. 执行刚才那条牛X的 JOIN 查询
        sql = """
        SELECT 
            s.name AS 学生姓名,
            c.name AS 企业名称,
            i.position AS 实习岗位,
            i.start_date AS 开始日期
        FROM internships i
        JOIN students s ON i.student_id = s.id
        JOIN companies c ON i.company_id = c.id;
        """
        cursor.execute(sql)
        # 3. 抓取所有结果
        results = cursor.fetchall()

        # 4. 打印到终端
        print("✅ 数据库连接成功，查询结果如下：")
        for row in results:
            print(f"学生：{row[0]}，企业：{row[1]}，岗位：{row[2]}，开始：{row[3]}")
finally:
    connection.close()