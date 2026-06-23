"""
测试用例文档--实习管理系统
用例编号：TC-001
测试模板：首页访问
前置条件：Django服务已启动
测试步骤：
1.发送GET请求到/
2检查响应状态码是否为200
预期结果：状态码为200，页面正常显示
"""

import requests # 这行是“工具箱”，让你能用代码发送网络请求
def test_homepage_status():  # 定义一个“测试用例”，名字叫“首页状态测试”
    url="http://127.0.0.1:8000/" # 要访问的地址（就是你浏览器里输入的那个）
    response=requests.get(url)  # 用代码“访问”这个网址，相当于你在浏览器按回车
    assert response.status_code==200 # 检查返回的状态码是不是 200
    print("✅ 首页状态码测试通过") # 如果是，打印成功

def test_homepage_contain_text(): # 测试“首页有没有张三”
    url="http://127.0.0.1:8000/"
    response=requests.get(url)   # 访问网站
    assert "李四" in response.text  # 检查返回的网页源码里有没有“张三”
    print("✅ 首页包含预期文字测试通过")

def test_add_internship():
    url="http://127.0.0.1:8000/add/"
    response=requests.get(url)# 1. 访问新增页面
    data = {
        "student_name":"测试学生",
        "company_name":"测试公司",
        "position":"测试岗位",
        "start_date":"2026-07-01"
    }# 2. 模拟填写表单：构造要提交的数据
    post_response=requests.post(url,data=data)# 3. 模拟点击“提交”按钮（发送 POST 请求）
    #assert post_response.status_code==302
    print("实际状态码：",post_response.status_code)
    print("返回内容：",post_response.text[:200])
    print("✅ 新增请求已提交，服务器返回重定向") # 4. 检查提交是否成功（正常会重定向回首页，状态码是 302）
    home_response=requests.get("http://127.0.0.1:8000/")
    assert "测试学生" in home_response.text
    assert "测试公司" in home_response.text
    print("✅ 新增记录测试通过，首页已显示新数据")
if __name__ == "__main__":
    test_homepage_status()
    test_homepage_contain_text()
    test_add_internship()
    
    bug_report="""
    Bug 编号：BUG-001
    严重程度：中
    测试环境：本地开发环境
    前置条件：数据库无数据
    操作步骤：访问首页/
    实际结果：页面显示空白表格
    预期结果：页面显示‘暂无数据’提示
"""
    print(bug_report)

def test_add_internship_auto():
    url = "http://127.0.0.1:8000/add/"
    data = {
        "student_name": "pytest自动化学生",
        "company_name": "pytest自动化公司",
        "position": "pytest自动化岗位",
        "start_date": "2026-07-01"
    }
    response = requests.post(url, data=data, allow_redirects=False)
    print("状态码：", response.status_code)
    assert response.status_code == 302
    print("✅ 自动化测试通过，状态码：", response.status_code)

def test_edit_internship():
    # 先确保有一条 id=1 的记录存在，直接修改它
    edit_url = "http://127.0.0.1:8000/edit/1/"
    edit_data = {
        "student_name": "编辑后学生",
        "company_name": "编辑后公司",
        "position": "编辑后岗位",
        "start_date": "2026-07-02"
    }
    resp = requests.post(edit_url, data=edit_data, allow_redirects=False)
    assert resp.status_code == 302
    print("✅ 编辑测试通过")

def test_delete_internship():
    delete_url = "http://127.0.0.1:8000/delete/1/"
    resp = requests.get(delete_url)
    assert resp.status_code == 200
    print("✅ 删除测试通过")