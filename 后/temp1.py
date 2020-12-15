# -*- coding: utf-8 -*-
import pymssql
from flask import Flask, request, jsonify
from flask_cors import CORS
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import BadSignature, SignatureExpired
from sqlalchemy import Column, String, create_engine,Integer,Date
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from tojson import *
import os,sys,random,string
basedir = os.path.abspath(os.path.dirname(__file__)) #定义一个根目录 用于保存图片用
# 创建对象的基类:
Base = declarative_base()


# 定义User对象:
class User(Base):
    # 表的名字:
    __tablename__ = 'User'

    # 表的结构:
    userId = Column(Integer)
    phone=Column(String(100),primary_key=True)
    userPassword=Column(String(100))
    userName = Column(String(100))
    isTeacher=Column(String(2))
    photoUrl=Column(String(50))
    
class Tags(Base):
    __tablename__='Tags'
    userId=Column(Integer)
    tags=Column(String(10))
    __mapper_args__={
    'primary_key':[userId,tags]
    }
class Teacher(Base):
    __tablename__='Teacher'
    teacherId=Column(Integer,primary_key=True)
    userId = Column(Integer)
class Subject(Base):
    __tablename__='Subject'
    teacherId=Column(Integer)
    courseId=Column(Integer)
    __mapper_args__={
    'primary_key':[teacherId,courseId]
    }
class Course(Base):
    __tablename__='Course'
    courseId=Column(Integer,primary_key=True)
    courseName=Column(String(50))
 


# 初始化数据库连接:
engine = create_engine('mssql+pymssql://sa:Qxp10182443@LAPTOP-496L06F3/xiaoyubaishi')
# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)
#DBSession实例化
session=DBSession()


# 密钥，可随意修改
SECRET_KEY = 'abcdefghijklmm'
# 生成token, 有效时间为600min
def generate_auth_token(phone, expiration=3600000):
    # 第一个参数是内部私钥
    # 第二个参数是有效期（秒）
    s = Serializer(SECRET_KEY, expires_in=expiration)
    return s.dumps({'phone': phone})

#token 验证函数
def verify_auth_token(token):
    s = Serializer(SECRET_KEY)
    try:
        data = s.loads(token)
    except SignatureExpired:
        return None  # valid token,but expired
    except BadSignature:
        return None  # invalid token
    user = session.query(User).filter(User.phone==data['phone']).one()
    return user

'''def return_img_stream(img_local_path):
    """
    工具函数:
    获取本地图片流
    :param img_local_path:文件单张图片的本地绝对路径
    :return: 图片流
    """
    import base64
    img_stream = ''
    with open(img_local_path, 'rb') as img_f:
        img_stream = img_f.read()
        img_stream = base64.b64encode(img_stream).decode()
    return img_stream'''

#数据库连接
'''db = pymysql.connect("127.0.0.1","root","123456","userdata")
cursor = db.cursor()'''

#后端服务启动
app = Flask(__name__)
CORS(app, resources=r'/*')

#手机号，密码登录并返回用户数据和token
@app.route('/user/login', methods=['POST'])
def login_login():
    if request.method == "POST":
        phone = request.form.get("phone")
        userPassword = request.form.get("userPassword")
        
        try:
            data=session.query(User).filter_by(phone=phone,userPassword=userPassword).one()
            token=generate_auth_token(phone)
            token=token.decode()
            print("result:",data)
            jsondata = {"userId":str(data.userId),
                        "token":str(token),"success":True,
                        "userState":True,"message":"登陆成功"}
            return jsonify(jsondata)
        
        except:
            print("result: NULL")
            jsondata = {"success":False,"userState":False,
                        "message":"用户名或密码错误"}
            return jsonify(jsondata)
    session.close()

#token验证登录，如果token无误则返回用户数据和更新后的token,否则返回空
@app.route('/user/infoAjax', methods=['GET', 'POST'])
def infoAjax():
    token = request.headers["token"]
   
    print(token)
    user = verify_auth_token(token)
    print(user.userName)

    try:
        user = verify_auth_token(token)
        records = (session.query(User,Teacher,Subject,Course,).\
                filter(User.userId == Teacher.userId).\
                filter(Teacher.teacherId == Subject.teacherId).\
                filter(Subject.courseId == Course.courseId).\
                filter(User.userId==user.userId).\
                all())
        records1=(session.query(User,Tags).\
                  filter(User.userId==Tags.userId).\
                  filter(User.userId==user.userId).\
                  all())
       
        results=toJsonList(records)
        #img_path =user.photoUrl
        #img_stream = return_img_stream(img_path)
        if user.isTeacher==0:
            role=False
        else:
            role=True
        if results!=[]:
            #print(results1)          
            results1=toJsonList(records1)
            subject=[]
            tags=[]
            print(toJsonList(records)[0])
            for each in results:
                subject.append(each['courseName'])
            for each in results1:
                tags.append(each['tags'])
            
           
            
            jsondata = {"phone":str(results[0]['phone']),"imageUrl":user.photoUrl,
                                "userName":str(results[0]['userName']),
                                "type":subject,
                                "userState":True,"role":role,
                        "dynamicTags":tags,
                        "success":True,"message":"请求成功"}
            session.close()
            return jsonify(jsondata)
        else:
            results1=toJsonList(records1)
            tags=[]
            subject=[]
            for each in results1:
                tags.append(each['tags'])
            jsondata = {"phone":str(user.phone),"imageUrl":user.photoUrl,
                                "userName":str(user.userName),
                                "type":subject,
                                "userState":True,"role":role,
                        "dynamicTags":tags,
                        "success":True,"message":"请求成功"}
            session.close()
            return jsonify(jsondata)
    except:
        print("result: NULL")
        jsondata = {"userState":False,
                    "success":False,
                    "message":"token非法或过期，请重新登录"}
        return jsonify(jsondata) 

@app.route('/user/register',methods=['POST'])
def register():
    form=User()
    userName=request.form.get("userName")
    userPassword=request.form.get("userPassword")
    phone=request.form.get("phone")
    
    
    #data=session.query(User).filter_by(phone=phone).all()
    #try:
    data=session.query(User).filter_by(phone=phone).all()
    try:
        if(data==[]):
           
            sql123='''insert into [User](phone,userName,userPassword)values('%s','%s','%s')'''%(phone,userName,userPassword)
            session.execute(sql123)
            session.commit()
            data1=session.query(User).filter_by(phone=phone).one()
            sql111='''insert into Tags(userId)values('%d')'''%(data1.userId)
            session.execute(sql111)
            session.commit()
            jsondata={"success":True,
                      "message":"注册成功"}
            session.close()
            return jsonify(jsondata)
        else:
            jsondata={"success":False,
                      "message":"手机号已注册"}
            return jsonify(jsondata)
    except:
        session.rollback()
        jsondata={"success":False,
                  "message":"注册失败"}
        return jsonify(jsondata)
@app.route('/user/updateInfo',methods=['POST'])
def updateInfo():
    token = request.headers["token"]
    user = verify_auth_token(token)
    
    try:
        user = verify_auth_token(token)
        phone=request.form.get("phone")
        userName=request.form.get("userName")
        list1= request.form.getlist("dynamicTags")
        print(list1)
        list2=request.form.getlist("type")
        u = session.query(User).filter(User.phone==user.phone).first()
        print(u.phone)
        u.userName=userName
        u.phone=phone
        session.commit()
        recordsl=session.query(Tags).filter(Tags.userId==user.userId).delete()
        for i in range(len(list1)):
            new_tags=Tags(userId=user.userId,tags=list1[i])
            session.add(new_tags)
            session.commit()
        trecords=session.query(Teacher).filter(Teacher.userId==user.userId).first()
        srecords=session.query(Subject).filter(Subject.teacherId==trecords.teacherId).delete()
        for i in range(len(list2)):
            crecords=session.query(Course).filter(Course.courseName==list2[i]).first()
            newtype=Subject(teacherId=trecords.teacherId,courseId=crecords.courseId)
            session.add(newtype)
            session.commit()
        
        jsondata={"success":True,
                  "message":"修改成功"}
        session.close()
        return jsonify(jsondata)
    except:
        jsondata={"success":False,
                  "message":"token值非法或过期,修改失败"}
        return jsonify(jsondata)

@app.route('/user/updateAvatar',methods=['POST'])
def updateAvatar():
    token = request.form.get("token")
    try:
        user = verify_auth_token(token)
        #生成随机字符串，防止图片名字重复
        ran_str = ''.join(random.sample(string.ascii_letters + string.digits, 16))
        #获取图片文件 name = upload
        img = request.files.get('url')
        #定义一个图片存放的位置 存放在static下面
        path = basedir+"/static/img/"
        #图片名称 给图片重命名 为了图片名称的唯一性
        imgName = ran_str+img.filename
        #图片path和名称组成图片的保存路径
        file_path = path+imgName
        #保存图片
        img.save(file_path)
        #这个是图片的访问路径，需返回前端（可有可无）
        url = 'static/img/'+imgName
        #返回图片路径 到前端
        aurl=session.query(User).filter(User.phone==user.phone).first()
        aurl.photoUrl=url
        
        session.commit()
        jsondata={"success":True,
                      "message":"修改成功"}
        session.close()
        return jsonify(jsondata)
    except:
        jsondata={"success":False,
                  "message":"token值非法或过期,修改失败"}
        return jsonify(jsondata)
@app.route('/user/identity',methods=['POST'])
def identity():
    token = request.headers["token"]
    try:
        user = verify_auth_token(token)
        u=session.query(User).filter(User.phone==user.phone).first()
        u.isTeacher=1
        session.commit()
        sql1='''insert into Teacher(userId)values('%d')'''%(user.userId)
        session.execute(sql1)
        session.commit()
        list1= request.form.getlist("type")
        trecords=session.query(Teacher).filter(Teacher.userId==user.userId).first()
        #srecords=session.query(Subject).filter(Subject.teacherId==trecords.teacherId).delete()
        for i in range(len(list1)):
            crecords=session.query(Course).filter(Course.courseName==list1[i]).first()
            newtype=Subject(teacherId=trecords.teacherId,courseId=crecords.courseId)
            session.add(newtype)
            session.commit()
        jsondata={"success":True,
                      "message":"审核成功"}
        session.close()
        return jsonify(jsondata)
    except:
        jsondata={"success":False,
                  "message":"token值非法或过期,修改失败"}
        return jsonify(jsondata)

@app.route('/teacher/selectAllTeacher',methods=['GET', 'POST'])
def selectAllTeacher():
    try:
        records = (session.query(User,Teacher).\
                    filter(User.userId == Teacher.userId).\
                    
                    filter(User.isTeacher==1).\
                    all())
        results=toJsonList(records)
        print(results)   
        teacher={}
        listtags=[]
        dict1={}
        list2=[]
        list1=['teacherId','userName','tags']
        for i in range(len(results)):
            
            
            tags=session.query(Tags).filter(results[i]['userId']==Tags.userId).all()
            #print(tags)
            for each in tags:
                listtags.append(each.tags)
            #teacher.update('teacherId':results[i]['teacherId'],'userName':results[i]['userName'],'tags':listtags)
            teacher['teacherId']=results[i]['teacherId']
            teacher['userName']=results[i]['userName']
            teacher['tags']=listtags
            list2.append(teacher)
            teacher={}
            listtags=[]
            '''allteacher=dict(zip(list1,teacher))
            dict1.update(allteacher)
            print(teacher)
            print(allteacher)
            print(dict1)
            allteacher={}'''
            print(teacher)
        print(list2)
       
        jsondata={"array":list2,
                  "success":True
            }
        return jsonify(jsondata)
    except:
        jsondata={"success":False,
                  }
        return jsonify(jsondata)

'''@app.route('/login/list', methods=['POST'])
def login_list():
    if request.method == "POST":
        cursor.execute("SELECT id,username,role,ctime FROM login")
        data = cursor.fetchall();
        temp = {}
        result = []
        if(data!=None):
            for i in data:
                temp["id"]=i[0]
                temp["username"]=i[1]
                temp["role"]=i[2]
                temp["ctime"]=i[3]
                result.append(temp.copy())
            print("result: ",len(data))
            return jsonify(result)
        else:
            print("result: NULL")
            return jsonify([])

@app.route('/login/add', methods=['POST'])
def login_add():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        role = request.form.get("role")
        try:
            cursor.execute("INSERT INTO login(username,password,role) VALUES (\""+str(username)
                +"\",\""+str(password)+"\","+str(role)+")")
            db.commit()
            print("add a new user successfully")
            return "1"
        except Exception as e:
            print("add a new user failed: ",e)
            db.rollback()
            return "-1"

@app.route('/login/del', methods=['POST'])
def login_del():
    if request.method == "POST":
        id = request.form.get("id")
        try:
            cursor.execute("DELETE FROM login WHERE id="+str(id))
            db.commit()
            print("delete the user successfully")
            return "1"
        except Exception as e:
            print("delete the user failed: ",e)
            db.rollback()
            return "-1"

@app.route('/login/update', methods=['POST'])
def login_update():
    if request.method == "POST":
        id = request.form.get("id")
        password = request.form.get("password")
        try:
            cursor.execute("UPDATE login SET password=\""+str(password)+"\" where id="+str(id))
            db.commit()
            print("update successfully")
            return "1"
        except Exception as e:
            print("update failed: ",e)
            db.rollback()
            return "-1"'''

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=8899)
    session.close()
    print("Good bye!")
