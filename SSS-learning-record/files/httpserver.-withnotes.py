# -*- coding: utf-8 -*-

import sys
import cgi
from http.server import HTTPServer, BaseHTTPRequestHandler

# MyHTTPRequestHandler 类，这个是 HTTPServer 的回调，用来处理到达的请求。
# 也就是0.0.0.0:8080 上有任何的HTTP请求到达时，都会调用 MyHTTPRequestHandler来处理。
# MyHTTPRequestHandler 直接 继承自 BaseHTTPRequestHandler，其中BaseHTTPRequestHandler 的 do_GET和do_POST两个方法被重写。
# 在 python 的 BaseHTTPRequestHandler 类中 ，do_XXX函数，就是处理对应的客户端请求的函数。
# 大家直接在浏览器中输入链接，浏览器拿到地址以后，默认是采用GET方式向服务器发送请求。
# 以下实验使用的post方法提交数据。通常来说，从服务器获取数据，使用get方面，向服务器提交数据，使用post方法。
class MyHTTPRequestHandler(BaseHTTPRequestHandler):
    field_name = 'b'
    form_html = \
        '''
        <html>
        <body>
        <form method='post' enctype='multipart/form-data'>
        <input type='text' name='%s'>
        <input type='submit'>
        </form>
        </body>
        </html>
        ''' % field_name

    def do_GET(self):
        self.send_response(200)
        #如果文件不存在，应该返回404，所以按照协议 应该是404。
        #这里做了一个特殊的处理，如果指定的文件不存在，我还是返回200，表示请求路径是正确的，可以处理。
        #然后返回一个默认的页面，这个页面就是 form_html的变量，在FileNotFoundError异常处理过程中写回。
        self.send_header("Content-type", "text/html")
        self.end_headers()
        try:
            file = open("."+self.path, "rb")
            #self.path 是这个请求的路径 。
            #比如，我们这里的 http://127.0.0.1:8080/a.html 其中 http://127.0.0.1:8080是协议服务器地址和端口。/a.html就是路径。
            #通常，一个静态的http服务器，这里的路径就是http服务器根目录下的文件，动态服务器这里可能是文件和参数，或者是对应其他服务器后台的处理过程。
            #例如 http://127.0.0.1:8080/a.php?p1=x，指定有a.php来处理这个请求，参数是p1=x。问号后面是参数，可以有多个。
            #那么所以我们就去读 a.html文件。
        except FileNotFoundError as e:
            print(e)
            self.wfile.write(self.form_html.encode())
            #wfile和rfile对应http响应和请求的body部分。
        else:
            content = file.read()
            self.wfile.write(content)
            #GET处理完成以后，浏览器就拿到了 200 状态的 "Content-type"为"text/html"的 form_html

    #在表单中填入数据。点提交按钮。然后服务器的do_POST函数回被调用。            
    def do_POST(self):
        #通过 cgi.FieldStorage解析了客户端提交的请求
        form_data = cgi.FieldStorage(
            fp=self.rfile, #原始的请求的头部在self.headers。body部分在self.rfile
            headers=self.headers,
            environ={
                'REQUEST_METHOD': 'POST',
                'CONTENT_TYPE': self.headers['Content-Type'],
            })
        fields = form_data.keys()
        if self.field_name in fields:
            input_data = form_data[self.field_name].value
            #解析完成以后放到 form_data变量里，
            #其中form_data['field_name'].value就是你在编辑框中填入的数据
            #python的cgi.FieldStorage将form组织为python的dict数据类型
            #所以可以通过  form_data['field_name'].value 获得所填入的数据
            file = open("."+self.path, "wb")
            file.write(input_data.encode())
            #通常，一个服务器会根据业务逻辑处理用户提交的数据，比如用户发表的商品评论，你们在我的在线教学系统中填入的作业,一般会写入数据库
            #但是这些数据，在某些情况下又会被显示出来，比如我批改你们的作业，其他用户看你的商品评论的时候。
            #我们这里为了模拟这个过程，简化了一下，没有用户系统，也没有数据库。直接写入了文件。
            #而且是写入path对应的文件。如果写入成功，就返回一个200状态的OK

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"<html><body>OK</body></html>")

# MyHTTPServer类，是继承自原生的HTTPSever
# 重写了 init函数，增加了打印输出语言，然后字节调用父类的 init 传递了服务器运行需要的地址 端口 等参数。
class MyHTTPServer(HTTPServer):
    def __init__(self, host, port):
        print("run app server by python!")
        HTTPServer.__init__(self,  (host, port), MyHTTPRequestHandler)
# MyHTTPRequestHandler 来处理 http请求，那么当用get方法请求，就会调用 do_GET,POST方法请求，就会调用 do_POST函数

if '__main__' == __name__:
    server_ip = "0.0.0.0"#监听地址和端口是 0.0.0.0:8080
    server_port = 8080
    if len(sys.argv) == 2:
        server_port = int(sys.argv[1])
    if len(sys.argv) == 3:
        server_ip = sys.argv[1]
        server_port = int(sys.argv[2])
    print("App server is running on http://%s:%s " % (server_ip, server_port))

    server = MyHTTPServer(server_ip, server_port)
    server.serve_forever()
# 这个是使用python原生的cgi和http.server两个库运行的一个简单的http服务器程序。
# 因为没有使用第三方库，所有不需要使用pip安装依赖。运行比较简单。
