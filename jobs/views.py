from django.shortcuts import render, redirect
from django.db import connection
from django.http import JsonResponse
import requests

# ---------- 首页：显示实习列表 ----------
def show_internships(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT s.name, c.name, i.position, i.start_date, i.id
            FROM internships i
            JOIN students s ON i.student_id = s.id
            JOIN companies c ON i.company_id = c.id
        """)
        results = cursor.fetchall()
    return render(request, 'internship_list.html', {'data': results})

# ---------- 新增实习记录 ----------
def add_internship(request):
    if request.method == 'POST':
        student_name = request.POST.get('student_name')
        company_name = request.POST.get('company_name')
        position = request.POST.get('position')
        start_date = request.POST.get('start_date')

        with connection.cursor() as cursor:
            # 查找或插入学生
            cursor.execute("SELECT id FROM students WHERE name = %s", [student_name])
            row = cursor.fetchone()
            if row:
                student_id = row[0]
            else:
                cursor.execute("INSERT INTO students (name) VALUES (%s)", [student_name])
                student_id = cursor.lastrowid

            # 查找或插入企业
            cursor.execute("SELECT id FROM companies WHERE name = %s", [company_name])
            row = cursor.fetchone()
            if row:
                company_id = row[0]
            else:
                cursor.execute("INSERT INTO companies (name) VALUES (%s)", [company_name])
                company_id = cursor.lastrowid

            # 插入实习记录
            cursor.execute("""
                INSERT INTO internships (student_id, company_id, position, start_date, status)
                VALUES (%s, %s, %s, %s, 1)
            """, [student_id, company_id, position, start_date])

        return redirect('/')

    # GET 请求：显示空白表单
    return render(request, 'add_internship.html')

# ---------- 编辑实习记录 ----------
def edit_internship(request, id):
    if request.method == 'POST':
        student_name = request.POST.get('student_name')
        company_name = request.POST.get('company_name')
        position = request.POST.get('position')
        start_date = request.POST.get('start_date')

        with connection.cursor() as cursor:
            # 处理学生
            cursor.execute("SELECT id FROM students WHERE name = %s", [student_name])
            row = cursor.fetchone()
            if row:
                student_id = row[0]
            else:
                cursor.execute("INSERT INTO students (name) VALUES (%s)", [student_name])
                student_id = cursor.lastrowid

            # 处理企业
            cursor.execute("SELECT id FROM companies WHERE name = %s", [company_name])
            row = cursor.fetchone()
            if row:
                company_id = row[0]
            else:
                cursor.execute("INSERT INTO companies (name) VALUES (%s)", [company_name])
                company_id = cursor.lastrowid

            # 更新实习记录
            cursor.execute("""
                UPDATE internships
                SET student_id = %s, company_id = %s, position = %s, start_date = %s
                WHERE id = %s
            """, [student_id, company_id, position, start_date, id])

        return redirect('/')

    # GET 请求：显示当前数据供编辑
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT s.name, c.name, i.position, i.start_date, i.id
            FROM internships i
            JOIN students s ON i.student_id = s.id
            JOIN companies c ON i.company_id = c.id
            WHERE i.id = %s
        """, [id])
        record = cursor.fetchone()
    return render(request, 'edit_internship.html', {'record': record})

# ---------- 删除实习记录 ----------
def delete_internship(request, id):
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM internships WHERE id = %s", [id])
    return redirect('/')

# ---------- AI 分析（调用大模型） ----------
def ai_summary(request, id):
    with connection.cursor() as cursor:
        cursor.execute("SELECT position FROM internships WHERE id = %s", [id])
        row = cursor.fetchone()
        if not row:
            return JsonResponse({'error': '记录不存在'}, status=404)
        position = row[0]

    prompt = f"请用一句简短的话总结：{position} 岗位需要哪些核心技能？要求用中文回答，不超过 50 个字。"

    # 这里请替换成你自己的 API Key（可以是 DeepSeek 或硅基流动）
    api_key = "sk-89aaa5bb67864c7bb279d3f2c19a6db9"   # ⚠️ 改成你自己的
    url = "https://api.deepseek.com/v1/chat/completions"   # 或硅基流动的地址
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "deepseek-chat",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 100
    }

    try:
        response = requests.post(url, json=data, headers=headers, timeout=10)
        response.raise_for_status()
        ai_result = response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return JsonResponse({'error': f'AI 调用失败: {str(e)}'}, status=500)

    return render(request, 'ai_result.html', {'position': position, 'result': ai_result})