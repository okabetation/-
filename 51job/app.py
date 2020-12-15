from flask import Flask,render_template
import sqlite3

app = Flask(__name__)




@app.route('/')
def home():
    return render_template('index.html')

@app.route('/index.html')
def index():
    return home()


@app.route('/charts.html')
def charts():
    company_school = []  # 学历
    num = []  # 分组

    con = sqlite3.connect("data/51job.db")
    cur = con.cursor()
    sql = "select company_school,count(company_school) from job group  by company_school"
    data = cur.execute(sql)
    for item in data:
        company_school.append(item[0])
        num.append(item[1])
    print(company_school, num)
    index = len(num)


    providesalary_text = []  # 工资
    wage = []  # 分组
    sql2 = "select providesalary_text,count(providesalary_text) from job group  by providesalary_text"
    data2 = cur.execute(sql2)
    for i in data2:
        providesalary_text.append(i[0])
        wage.append(i[1])

    print(providesalary_text,wage)
    list = len(wage)
    cur.close()
    con.close()
    return render_template('charts.html',
                           company_school=company_school,num=num,index = index,
                           providesalary_text=providesalary_text,wage=wage,list=list)

@app.route('/tables.html')
def tables():
    datalist = []
    con = sqlite3.connect("data/51job.db")
    cur = con.cursor()
    sql = "select * from job"
    data = cur.execute(sql)
    for item in data:
        datalist.append(item)
    cur.close()
    con.close()
    list = len(datalist)
    print(datalist)
    return render_template("tables.html", jobss=datalist,list =list )

@app.route('/login.html')
def login():
    return render_template('login.html')

@app.route('/password.html')
def password():
    return render_template('password.html')

@app.route('/register.html')
def register():
    return render_template('register.html')

if __name__ == '__main__':
    app.run()

