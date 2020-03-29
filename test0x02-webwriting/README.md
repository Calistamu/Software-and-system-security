# web开发
## 实验要求

- [] [使用更底层的pyhton的sqlite库来编程操作数据库](https://docs.python.org/3/library/sqlite3.html)。
- [] httpserver.py的基础上，写两个页面：教师录入成绩页面和学生查询成绩页面。
* 教师录入成绩页面表单有三个字段，课程id，学生id，成绩。
- [] 录入提交以后，httpserver调用sqlite库使用sql语句写入数据库。然后是学生查询成绩表单，学生输入学生id，课程id，httpserver使用sql语句查询成绩后返回给用户。
* 这里不需要做登录功能，课程也用直接输入id而不是下拉菜单的方式，或者其他选择的方式，而是直接输入id。为了体验最原始的web的开发过程。  

