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

def pet_header_footer(request):
    return render(request,"pet_header_footer.html")

def pet_home(request):
    return render(request,"pet_home.html")

def shop_profile(request):
    sid = request.session["sid"]
    q1 = "select * from pet_centre s , login l where s.s_id = '"+str(sid)+"' and l.user_id = s.s_id  and l.type  = 'pet_centre'"
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


        q2 = "update pet_centre set s_name='"+str(name)+"', s_mail='"+str(mail)+"',s_phone1='"+str(phone1)+"',s_phone2='"+str(phone2)+"',s_address='"+str(address)+"',s_timing='"+str(available)+"'  where s_id = '"+str(sid)+"'"
        c.execute(q2)
        conn.commit()
        q3 = "update login set `user_name`='"+str(mail)+"', password = '"+str(password)+"' where user_id = '"+str(sid)+"' and type = 'pet_centre'"
        c.execute(q3)
        conn.commit()
        msg ="You have  successfully Updated Your Profile"
        q4 = "select * from pet_centre s , login l where s.s_id = '"+str(sid)+"' and l.user_id = s.s_id  and l.type  = 'pet_centre'"
        c.execute(q4)
        conn.commit()
        data1= c.fetchall()
        return render(request,"shop_profile.html",{"data":data1,"msg":msg})

    if 'lookafter' in request.POST:
        


        q2 = "update pet_centre set s_lookafter = 'accepted'  where s_id = '"+str(sid)+"'"
        c.execute(q2)
        conn.commit()
        
        msg ="You have  successfully Updated Your Profile"
        q4 = "select * from pet_centre s , login l where s.s_id = '"+str(sid)+"' and l.user_id = s.s_id  and l.type  = 'pet_centre'"
        c.execute(q4)
        conn.commit()
        data1= c.fetchall()
        return render(request,"shop_profile.html",{"data":data1,"msg":msg})
    return render(request,"shop_profile.html",{"data":data})



def add_product(request):
    sid = request.session["sid"]
    q1 = "select * from category"
    print(q1)
    c.execute(q1)
    conn.commit()
    data = c.fetchall()
    print(data)

    if 'submit' in request.POST:
        name = request.POST.get("name")
        category = request.POST.get("category")
        amount = request.POST.get("amount")
        quan = request.POST.get("quan")
        desc = request.POST.get("desc")
        # available = request.POST.get("available")
        # password = request.POST.get("password")
        filename = request.FILES.get("img")
        fs = FileSystemStorage()
        myfile = fs.save(filename.name,filename)
        url = fs.url(myfile)


        q2 = "insert into product(`s_id`,`category`,`p_img`,`p_name`,`p_amt`,`p_qnty`,`p_desc`) values('"+str(sid)+"','"+str(category)+"','"+str(url)+"','"+str(name)+"','"+str(amount)+"','"+str(quan)+"','"+str(desc)+"')"
        c.execute(q2)
        conn.commit()
       
        msg ="You have successfully Added Product"
        
        return render(request,"add_product.html",{"data":data,"msg":msg})
    return render(request,"add_product.html",{"data":data})


def view_product(request):
    sid = request.session["sid"]
    q1 = "select * from category"
    print(q1)
    c.execute(q1)
    conn.commit()
    data = c.fetchall()
    print(data)

    if 'submit' in request.POST:
        category = request.POST.get("category")
        q2 = "select * from product where category = '"+str(category)+"' and s_id = '"+str(sid)+"'"
        c.execute(q2)
        conn.commit()
        data1 = c.fetchall()
        print(data1)
        return render(request,"view_product.html",{"data1":data1,"data":data})
    return render(request,"view_product.html",{"data":data})

def shop_view_item(request):
    sid = request.session["sid"]
    reg_id = request.GET.get("reg_id")

    q1 = "select * from product where p_id = '"+str(reg_id)+"' "
    print(q1)
    c.execute(q1)
    conn.commit()
    data = c.fetchall()
    print(data)

    if 'submit' in request.POST:
        name = request.POST.get("name")
        amt = request.POST.get("amt")
        quan = request.POST.get("quan")
        desc = request.POST.get("desc")


        q2 = "update product set p_name='"+str(name)+"', p_amt='"+str(amt)+"',p_qnty='"+str(quan)+"',p_desc='"+str(desc)+"' where p_id = '"+str(reg_id)+"'"
        c.execute(q2)
        conn.commit()
        
        msg ="You have  successfully Updated Your Profile"
        q4 = "select * from product where p_id = '"+str(reg_id)+"'"
        c.execute(q4)
        conn.commit()
        data1= c.fetchall()
        return render(request,"shop_view_item.html",{"data":data1,"msg":msg})
    return render(request,"shop_view_item.html",{"data":data})


def pet_lookafter_request(request):
    sid = request.session["sid"]
    q1 = "select * from lookafter_request lr, owner o where lr.s_id = '"+str(sid)+"' and lr.u_id = o.o_id"
    print(q1)
    c.execute(q1)
    conn.commit()
    data = c.fetchall()
    print(data)

    if 'submit' in request.POST:
        category = request.POST.get("category")
        q2 = "select * from product where category = '"+str(category)+"' and s_id = '"+str(sid)+"'"
        c.execute(q2)
        conn.commit()
        data1 = c.fetchall()
        print(data1)
        return render(request,"pet_lookafter_request.html",{"data1":data1,"data":data})
    return render(request,"pet_lookafter_request.html",{"data":data})

def pet_request_action(request):
    reg_id = request.GET.get("reg_id")
    st = request.GET.get("st")

    if st == 'approve' :
        s = "update lookafter_request set status = '"+str(st)+"' where l_id = '"+str(reg_id)+"'"
        c.execute(s)
        conn.commit()
        return HttpResponseRedirect("/pet_lookafter_request/")

    if st == 'reject' :
        s = "update lookafter_request set status = '"+str(st)+"' where l_id = '"+str(reg_id)+"'"
        c.execute(s)
        conn.commit()
        return HttpResponseRedirect("/pet_lookafter_request/")


def add_pet(request):
    sid = request.session["sid"]
    today = now.date()
    if 'submit' in request.POST:

        name = request.POST.get("name")
        age = request.POST.get("age")
        amount = request.POST.get("amount")
        quan = request.POST.get("quan")
        desc = request.POST.get("desc")
        # available = request.POST.get("available")
        # password = request.POST.get("password")
        filename = request.FILES.get("img")
        fs = FileSystemStorage()
        myfile = fs.save(filename.name,filename)
        url = fs.url(myfile)


        q2 = "insert into adoption(`s_id`,`a_img`,`a_name`,`a_age`,`a_amount`,`a_count`,`a_desc`,`posted_date`,`status`) values('"+str(sid)+"','"+str(url)+"','"+str(name)+"','"+str(age)+"','"+str(amount)+"','"+str(quan)+"','"+str(desc)+"','"+str(today)+"','available')"
        c.execute(q2)
        conn.commit()
       
        msg ="You have successfully Added Pet"
        
        return render(request,"add_pet.html",{"msg":msg})
    return render(request,"add_pet.html")


def pets_list(request):
    sid = request.session["sid"]
    q1 = "select * from adoption where s_id = '"+str(sid)+"' order by posted_date desc"
    print(q1)
    c.execute(q1)
    conn.commit()
    data = c.fetchall()
    print(data)

    # if 'submit' in request.POST:
    #     category = request.POST.get("category")
    #     q2 = "select * from product where category = '"+str(category)+"' and s_id = '"+str(sid)+"'"
    #     c.execute(q2)
    #     conn.commit()
    #     data1 = c.fetchall()
    #     print(data1)
    #     return render(request,"pets_list.html",{"data1":data1,"data":data})
    return render(request,"pets_list.html",{"data":data})

def del_product(request):
    reg_id = request.GET.get("reg_id")
    sid = request.session["sid"]

    q1 = "delete from product where p_id = '"+str(reg_id)+"' and s_id = '"+str(sid)+"'"
    c.execute(q1)
    conn.commit()
    return HttpResponseRedirect("/view_product/")

def view_pet_detail(request):
    sid = request.session["sid"]
    reg_id = request.GET.get("reg_id")

    q1 = "select * from adoption where a_id = '"+str(reg_id)+"' "
    print(q1)
    c.execute(q1)
    conn.commit()
    data = c.fetchall()
    print(data)

    if 'submit' in request.POST:
        name = request.POST.get("name")
        age = request.POST.get("age")
        amount = request.POST.get("amount")
        quan = request.POST.get("quan")
        desc = request.POST.get("desc")
        # available = request.POST.get("available")
        # password = request.POST.get("password")
        
        q2 = "update adoption set a_name='"+str(name)+"', a_age ='"+str(age)+"', a_amount='"+str(amount)+"',a_count='"+str(quan)+"',a_desc='"+str(desc)+"' where a_id = '"+str(reg_id)+"'"
        c.execute(q2)
        conn.commit()
        
        msg ="You have  successfully Updated the Pet Detail"
        q4 = "select * from adoption where a_id = '"+str(reg_id)+"'"
        c.execute(q4)
        conn.commit()
        data1= c.fetchall()
        return render(request,"view_pet_detail.html",{"data":data1,"msg":msg})
    return render(request,"view_pet_detail.html",{"data":data})

def del_pet_detail(request):
    reg_id = request.GET.get("reg_id")
    sid = request.session["sid"]

    q1 = "delete from adoption where a_id = '"+str(reg_id)+"' "
    c.execute(q1)
    conn.commit()
    return HttpResponseRedirect("/pets_list/")

def pet_adoption_request(request):
    sid = request.session["sid"]
    q1 = "select * from adoption_request ar, owner o, adoption ap where ar.s_id = '"+str(sid)+"' and ar.u_id = o.o_id and ar.a_id = ap.a_id and ap.s_id = ar.s_id"
    print(q1)
    c.execute(q1)
    conn.commit()
    data = c.fetchall()
    print(data)

    if 'submit' in request.POST:
        category = request.POST.get("category")
        q2 = "select * from product where category = '"+str(category)+"' and s_id = '"+str(sid)+"'"
        c.execute(q2)
        conn.commit()
        data1 = c.fetchall()
        print(data1)
        return render(request,"pet_adoption_request.html",{"data1":data1,"data":data})
    return render(request,"pet_adoption_request.html",{"data":data})

def pet_adoption_request_action(request):
    reg_id = request.GET.get("reg_id")
    st = request.GET.get("st")

    if st == 'approve' :
        s = "update adoption_request set status = '"+str(st)+"' where ar_id = '"+str(reg_id)+"'"
        c.execute(s)
        conn.commit()
        return HttpResponseRedirect("/pet_adoption_request/")

    if st == 'reject' :
        s = "update adoption_request set status = '"+str(st)+"' where ar_id = '"+str(reg_id)+"'"
        c.execute(s)
        conn.commit()
        return HttpResponseRedirect("/pet_adoption_request/")