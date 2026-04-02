from django.shortcuts import render,HttpResponse,HttpResponseRedirect
import MySQLdb
import smtplib 
import urllib.request
import webbrowser
from django.core.files.storage import FileSystemStorage
import datetime
now = datetime.datetime.now()

# Create your views here.

conn = MySQLdb.connect("localhost","root","","petwet")
c = conn.cursor()
# Create your views here.

def sendsms(ph,msg):

    sendToPhoneNumber= "+91"+ph
    userid = "2000022557"
    passwd = "54321@lcc"
    url = "http://enterprise.smsgupshup.com/GatewayAPI/rest?method=sendMessage&send_to=" + sendToPhoneNumber + "&msg=" + msg + "&userid=" + userid + "&password=" + passwd + "&v=1.1&msg_type=TEXT&auth_scheme=PLAIN"
    # contents = urllib.request.urlopen(url)
    webbrowser.open(url)

def vet_header_footer(request):
    return render(request,"vet_header_footer.html")

def vet_home(request):
    return render(request,"vet_home.html")

def vet_profile(request):
    v_id = request.session["vid"]
    q1 = "select * from veterinary v , login l where v.v_id = '"+str(v_id)+"' and l.user_id = v.v_id  and l.type  = 'veterinary'"
    print(q1)
    c.execute(q1)
    conn.commit()
    data = c.fetchall()
    print(data)

    if 'submit' in request.POST:
        name = request.POST.get("name")
        mail = request.POST.get("mail")
        phone1 = request.POST.get("phone1")
        phone2 = request.POST.get("phone2")
        address = request.POST.get("address")
        available = request.POST.get("available")
        password = request.POST.get("password")


        q2 = "update veterinary set v_name='"+str(name)+"', v_mail='"+str(mail)+"',v_phone1='"+str(phone1)+"',v_phone2='"+str(phone2)+"',v_address='"+str(address)+"',v_timing='"+str(available)+"'  where v_id = '"+str(v_id)+"'"
        c.execute(q2)
        conn.commit()
        q3 = "update login set `user_name`='"+str(mail)+"', password = '"+str(password)+"' where user_id = '"+str(v_id)+"' and type = 'veterinary'"
        c.execute(q3)
        conn.commit()
        msg ="You have  successfully Updated Your Profile"
        q4 = "select * from veterinary v , login l where v.v_id = '"+str(v_id)+"' and l.user_id = v.v_id  and l.type  = 'veterinary'"
        c.execute(q4)
        conn.commit()
        data1= c.fetchall()
        return render(request,"vet_profile.html",{"data":data1,"msg":msg})

    
    return render(request,"vet_profile.html",{"data":data})

def add_doctor(request):
    v_id = request.session["vid"]

    if 'submit' in request.POST:
        name = request.POST.get("name")
        age = request.POST.get("age")
        phone = request.POST.get("phone")
        email = request.POST.get("email")
        timing = request.POST.get("timing")
        qualification = request.POST.get("qualification")
        address = request.POST.get("address")
        # available = request.POST.get("available")
        # password = request.POST.get("password")
        filename = request.FILES.get("img")
        fs = FileSystemStorage()
        myfile = fs.save(filename.name,filename)
        url = fs.url(myfile)


        q2 = "insert into doctor(`v_id`,`dr_img`,`dr_name`,`dr_age`,`dr_phone`,`dr_email`,`dr_timing`,`dr_quali`,`dr_address`) values('"+str(v_id)+"','"+str(url)+"','"+str(name)+"','"+str(age)+"','"+str(phone)+"','"+str(email)+"','"+str(timing)+"','"+str(qualification)+"','"+str(address)+"')"
        c.execute(q2)
        conn.commit()
       
        msg ="You have successfully Added Doctor"
        
        return render(request,"add_doctor.html",{"msg":msg})
    return render(request,"add_doctor.html")

def view_doctors(request):
    v_id = request.session["vid"]
    q1 = "select * from doctor where v_id = '"+str(v_id)+"'"
    print(q1)
    c.execute(q1)
    conn.commit()
    data = c.fetchall()
    print(data)

    
    return render(request,"view_doctors.html",{"data":data})


def view_doctor_detail(request):
    v_id = request.session["vid"]

    dr_id = request.GET.get("dr_id")

    q1 = "select * from doctor where dr_id = '"+str(dr_id)+"' "
    print(q1)
    c.execute(q1)
    conn.commit()
    data = c.fetchall()
    print(data)

    if 'submit' in request.POST:
        name = request.POST.get("name")
        age = request.POST.get("age")
        phone = request.POST.get("phone")
        email = request.POST.get("email")
        timing = request.POST.get("timing")
        qualification = request.POST.get("qualification")
        address = request.POST.get("address")
       

        q2 = "update doctor set dr_name='"+str(name)+"', dr_age='"+str(age)+"',dr_phone='"+str(phone)+"',dr_email='"+str(email)+"',dr_timing='"+str(timing)+"',dr_quali='"+str(qualification)+"',dr_address='"+str(address)+"' where dr_id = '"+str(dr_id)+"'"
        c.execute(q2)
        conn.commit()
        
        msg ="You have  successfully Updated Your Profile"
        q4 = "select * from doctor where dr_id = '"+str(dr_id)+"'"
        c.execute(q4)
        conn.commit()
        data1= c.fetchall()
        return render(request,"view_doctor_detail.html",{"data":data1,"msg":msg})
    return render(request,"view_doctor_detail.html",{"data":data})


def del_dr_detail(request):
    dr_id = request.GET.get("dr_id")
    v_id = request.session["vid"]

    q1 = "delete from doctor where dr_id = '"+str(dr_id)+"' and v_id = '"+str(v_id)+"'"
    c.execute(q1)
    conn.commit()
    return HttpResponseRedirect("/view_doctors/")

def owner_view_veterinary(request):
    v_id = request.session["vid"]

    # reg_id = request.GET.get("reg_id")

    q1 = "select * from veterinary "
    print(q1)
    c.execute(q1)
    conn.commit()
    data = c.fetchall()
    print(data)

   
    return render(request,"owner_view_veterinary.html",{"data":data})


def view_bk_requests(request):
    uid = request.session["vid"]
    msg = ""
    q1 =  "select * from dr_booking db, doctor d, owner o where db.u_id = '"+str(uid)+"' and db.dr_id = d.dr_id and db.u_id = o.o_id "
    c.execute(q1)
    data = c.fetchall()
    print(q1)
    print(data)
    if not bool(data):
        msg = "No Booking Request to show List to show"
        return render(request,"view_bk_requests.html",{"data":data,"msg":msg})
    return render(request,"view_bk_requests.html",{"data":data})

def booking_action(request):
    reg_id = request.GET.get("reg_id")
    st = request.GET.get("st")

    if st == 'approve' :
        s = "update dr_booking set status = '"+str(st)+"' where bk_id = '"+str(reg_id)+"'"
        c.execute(s)
        conn.commit()
        return HttpResponseRedirect("/view_bk_requests/")

    if st == 'reject' :
        s = "update dr_booking set status = '"+str(st)+"' where bk_id = '"+str(reg_id)+"'"
        c.execute(s)
        conn.commit()
        return HttpResponseRedirect("/view_bk_requests/")