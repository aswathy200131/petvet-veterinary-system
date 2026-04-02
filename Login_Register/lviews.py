from django.shortcuts import render,HttpResponse,HttpResponseRedirect
import MySQLdb
import smtplib 
import urllib.request
import webbrowser
from django.core.files.storage import FileSystemStorage

# Create your views here.

conn = MySQLdb.connect("localhost","root","","petwet")
c = conn.cursor()

def sendsms(ph,msg):

    sendToPhoneNumber= "+91"+ph
    userid = "2000022557"
    passwd = "54321@lcc"
    url = "http://enterprise.smsgupshup.com/GatewayAPI/rest?method=sendMessage&send_to=" + sendToPhoneNumber + "&msg=" + msg + "&userid=" + userid + "&password=" + passwd + "&v=1.1&msg_type=TEXT&auth_scheme=PLAIN"
    # contents = urllib.request.urlopen(url)
    webbrowser.open(url)


def login(request):
    if 'submit' in request.POST:
        username = request.POST.get("username")
        password = request.POST.get("password")

        q1 = "select * from login where user_name = '"+str(username)+"' and password = '"+str(password)+"'and status = '1'"
        print(q1)
        c.execute(q1)
        data = c.fetchone()
        print(data)

        if not bool(data):
            msg = "Invalid Username Or Password"
            return render(request,"login.html",{"msg":msg})
            
        if data[4] == 'admin' :

            return HttpResponseRedirect("/admin_home")
            
        if data[4] == 'owner' :
            request.session["uid"]= data[1]

            print("owner inside ")

            return HttpResponseRedirect("/owner_home")    
        
        if data[4] == 'walker' :
            request.session["wid"]= data[1]
            return HttpResponseRedirect("/walkers_home")

        if data[4] == 'veterinary' :
            request.session["vid"]= data[1]
            return HttpResponseRedirect("/vet_home")    


        if data[4] == 'pet_centre' :
            request.session["sid"]= data[1]

            return HttpResponseRedirect("/pet_home") 
       
    return render(request,"login.html")

def owner_register(request):
    """register
    ===========
    tiz for reg user"""
    if 'owner_submit' in request.POST:
        username = request.POST.get("username")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        address = request.POST.get("address")
        password = request.POST.get("password")

        q1 = "select count(*) from owner where o_mail = '"+str(email)+"' or o_phone = '"+str(phone)+"' "
        c.execute(q1)
        data1 = c.fetchone()
        print(data1)

        if data1[0] == 0 :
            q2 = "insert into owner(`o_name`,`o_mail`,`o_phone`,`o_address`) values('"+str(username)+"', '"+str(email)+"','"+str(phone)+"','"+str(address)+"')"
            c.execute(q2)
            conn.commit()
            q3 = "insert into login(`user_id`,`user_name`,`password`,`type`,`status`) values((select max(o_id) from owner),'"+str(email)+"','"+str(password)+"','owner',1)"
            c.execute(q3)
            conn.commit()
            msg ="You have registred successfully"
            message = "Dear "+str(username)+" , \n You have successfully registered to Pet Wet. Your Username : "+str(email)+". Please Login with Username and password. "
            sendsms(phone,message)

            return render(request,"owner_register.html",{"msg":msg})
        else:
            msg ="Already Exists"

            return render(request,"owner_register.html",{"msgg":msg})
    return render(request,"owner_register.html")

def walker_register(request):
    """walker register
    ===========
    this is for reg user"""

    if 'walker_submit' in request.POST:
        username = request.POST.get("username")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        address = request.POST.get("address")
        password = request.POST.get("password")
        available = request.POST.get("available")
        charge = request.POST.get("charge")
        filename = request.FILES.get("img")
        fs = FileSystemStorage()
        myfile = fs.save(filename.name,filename)
        url = fs.url(myfile)

        q1 = "select count(*) from walker where w_mail = '"+str(email)+"' or w_phone = '"+str(phone)+"' "
        c.execute(q1)
        data1 = c.fetchone()
        print(data1)

        if data1[0] == 0 :
            q2 = "insert into walker(`w_img`,`w_name`,`w_mail`,`w_phone`,`w_address`,`w_time`,`w_rate`) values('"+str(url)+"','"+str(username)+"', '"+str(email)+"','"+str(phone)+"','"+str(address)+"','"+str(available)+"','"+str(charge)+"')"
            c.execute(q2)
            conn.commit()
            q3 = "insert into login(`user_id`,`user_name`,`password`,`type`) values((select max(w_id) from walker),'"+str(email)+"','"+str(password)+"','walker')"
            c.execute(q3)
            conn.commit()
            msg ="You have registred successfully .Your Account will be active soon"
            message = "Dear "+str(username)+" , \n You have successfully registered to Pet Wet. Your Username : "+str(email)+". Your account will be active soon "
            sendsms(phone,message)

            return render(request,"walker_register.html",{"msg":msg})
        else:
            msg ="Already Exists"

            return render(request,"walker_register.html",{"msgg":msg})
    return render(request,"walker_register.html")

def clinic_register(request):
    """clinic register
    ===========
    this is for reg clinic"""

    if 'clinic_submit' in request.POST:
        username = request.POST.get("name")
        email = request.POST.get("email")
        phone1 = request.POST.get("phone1")
        phone2 = request.POST.get("phone2")
        address = request.POST.get("address")
        password = request.POST.get("password")
        available = request.POST.get("available")

        q1 = "select count(*) from veterinary where v_mail = '"+str(email)+"' or v_phone1 = '"+str(phone1)+"' "
        c.execute(q1)
        data1 = c.fetchone()
        print(data1)

        if data1[0] == 0 :
            q2 = "insert into veterinary(`v_name`,`v_mail`,`v_phone1`,`v_phone2`,`v_address`,`v_timing`) values('"+str(username)+"', '"+str(email)+"','"+str(phone1)+"','"+str(phone2)+"','"+str(address)+"','"+str(available)+"')"
            c.execute(q2)
            conn.commit()
            q3 = "insert into login(`user_id`,`user_name`,`password`,`type`) values((select max(v_id) from veterinary),'"+str(email)+"','"+str(password)+"','veterinary')"
            c.execute(q3)
            conn.commit()
            msg ="You have registred successfully .Your Account will be active soon"
            message = "Dear "+str(username)+" , \n You have successfully registered to Pet Wet. Your Username : "+str(email)+". Your account will be active soon "
            sendsms(phone1,message)

            return render(request,"clinic_register.html",{"msg":msg})
        else:
            msg ="Already Exists"
            # return HttpResponseRedirect("../login/")

            return render(request,"clinic_register.html",{"msgg":msg})
    return render(request,"clinic_register.html")

def shop_register(request):
    """clinic register
    ===========
    this is for reg clinic"""

    if 'shop_submit' in request.POST:
        username = request.POST.get("name")
        email = request.POST.get("email")
        phone1 = request.POST.get("phone1")
        phone2 = request.POST.get("phone2")
        address = request.POST.get("address")
        password = request.POST.get("password")
        available = request.POST.get("available")

        q1 = "select count(*) from pet_centre where s_mail = '"+str(email)+"' or s_phone1 = '"+str(phone1)+"' "
        c.execute(q1)
        data1 = c.fetchone()
        print(data1)

        if data1[0] == 0 :
            q2 = "insert into pet_centre(`s_name`,`s_mail`,`s_phone1`,`s_phone2`,`s_address`,`s_timing`) values('"+str(username)+"', '"+str(email)+"','"+str(phone1)+"','"+str(phone2)+"','"+str(address)+"','"+str(available)+"')"
            c.execute(q2)
            conn.commit()
            q3 = "insert into login(`user_id`,`user_name`,`password`,`type`) values((select max(s_id) from pet_centre),'"+str(email)+"','"+str(password)+"','pet_centre')"
            c.execute(q3)
            conn.commit()
            msg ="You have registred successfully .Your Account will be active soon"
            message = "Dear "+str(username)+" , \n You have successfully registered to Pet Wet. Your Username : "+str(email)+". Your account will be active soon "
            sendsms(phone1,message)

            return render(request,"shop_register.html",{"msg":msg})
        else:
            msg ="Already Exists"
            # return HttpResponseRedirect("../login/")

            return render(request,"shop_register.html",{"msgg":msg})
    return render(request,"shop_register.html")