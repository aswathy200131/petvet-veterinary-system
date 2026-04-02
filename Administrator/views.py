from django.shortcuts import render,HttpResponse,HttpResponseRedirect
import MySQLdb
import smtplib 
import urllib.request
import webbrowser
from django.core.files.storage import FileSystemStorage

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

def admin_header_footer(request):
    return render(request,"admin_header_footer.html")

def admin_home(request):
    return render(request,"admin_home.html")

def pet_owners(request):
    msg = ""
    q1 = "select * from owner"
    c.execute(q1)
    conn.commit()
    data = c.fetchall()
    if not bool(data):
        print(data)
        msg = "No owner List to show"
        return render(request,"pet_owners.html",{"data":data,"msg":msg})
    
    return render(request,"pet_owners.html",{"data":data})

def owner_remove(request):
    print("inside update")
    reg_id = request.GET.get("reg_id")
    action = request.GET.get("action")
    print(action)

    q1 = "delete from owner where o_id ='"+str(reg_id)+"' "
    c.execute(q1)
    conn.commit()

    q2 = "delete from login where user_id ='"+str(reg_id)+"' and type = 'owner'"
    c.execute(q2)
    conn.commit()

    return HttpResponseRedirect("/pet_owners/")

def walkers_request(request):
    msg = ""
    q1 = "select w.* from walker w, login l where w.w_id = l.user_id  and l.status = 0 and l.type = 'walker'"
    c.execute(q1)
    conn.commit()
    data = c.fetchall()
    print(data)
    if not bool(data):
        print(data)
        msg = "No Walker Request List to show"
        return render(request,"walkers_request.html",{"data":data,"msg":msg})
    
    return render(request,"walkers_request.html",{"data":data})

def walker_action(request):
    print("inside update")
    reg_id = request.GET.get("reg_id")
    action = request.GET.get("action")
    print(action)
    
    if action == 'approve' :
        q1 = "update login set status = '1'  where user_id ='"+str(reg_id)+"' and type='walker'"
        c.execute(q1)
        conn.commit()
        q2 = "select w_phone from walker where w_id ='"+str(reg_id)+"'"
        c.execute(q2)
        ph = c.fetchone()
        msg = "Dear customer, Your Account is active now. Now you can login using ur username and password"
        sendsms(ph[0],msg)
        return HttpResponseRedirect("/walkers_request/")

    if action == 'remove' :
        w_type = request.GET.get("type")
        if w_type == 'req':

            q3 = "delete from walker where w_id ='"+str(reg_id)+"' "
            c.execute(q3)
            conn.commit()

            q4 = "delete from login where user_id ='"+str(reg_id)+"' and type = 'walker'"
            c.execute(q4)
            conn.commit()
            return HttpResponseRedirect("/walkers_request/")

        elif (w_type == 'list'):
       
            q3 = "delete from walker where w_id ='"+str(reg_id)+"'"
            c.execute(q3)
            conn.commit()

            q4 = "delete from login where user_id ='"+str(reg_id)+"' and type = 'walker'"
            c.execute(q4)
            conn.commit()
            return HttpResponseRedirect("/walkers_list/")
     
            
    return HttpResponseRedirect("/walkers_request/")


    

def walkers_list(request):
    msg = ""
    q1 = "select w.* from walker w, login l where w.w_id = l.user_id  and l.status = 1 and l.`type` = 'walker'"
    c.execute(q1)
    conn.commit()
    data = c.fetchall()
    if not bool(data):
        print(data)
        msg = "No Walker List to show"
        return render(request,"walkers_list.html",{"data":data,"msg":msg})
    
    return render(request,"walkers_list.html",{"data":data})

def veterinary_request(request):
    msg = ""
    q1 = "select v.* from veterinary v, login l where v.v_id = l.user_id  and l.status = 0 AND l.`type` = 'veterinary'"
    c.execute(q1)
    conn.commit()
    data = c.fetchall()
    print(q1)
    print(data)
    if not bool(data):
        print(data)
        msg = "No Veterinary Request List to show"
        return render(request,"veterinary_request.html",{"data":data,"msg":msg})
    
    return render(request,"veterinary_request.html",{"data":data})

def veterinary_action(request):
    print("inside update")
    reg_id = request.GET.get("reg_id")
    action = request.GET.get("action")
    print(action)
    
    if action == 'approve' :
        q1 = "update login set status = '1'  where user_id ='"+str(reg_id)+"' and type='veterinary'"
        c.execute(q1)
        conn.commit()
        q2 = "select v_phone1 from veterinary where v_id ='"+str(reg_id)+"'"
        c.execute(q2)
        ph = c.fetchone()
        msg = "Dear customer, Your Account is active now. Now you can login using ur username and password"
        sendsms(ph[0],msg)
        return HttpResponseRedirect("/veterinary_request/")

    if action == 'remove' :
        w_type = request.GET.get("type")
        if w_type == 'req':

            q3 = "delete from veterinary where v_id ='"+str(reg_id)+"'"
            c.execute(q3)
            conn.commit()

            q4 = "delete from login where user_id ='"+str(reg_id)+"' and type = 'veterinary'"
            c.execute(q4)
            conn.commit()
            return HttpResponseRedirect("/veterinary_request/")

        elif (w_type == 'list'):
       
            q3 = "delete from veterinary where v_id ='"+str(reg_id)+"'"
            c.execute(q3)
            conn.commit()

            q4 = "delete from login where user_id ='"+str(reg_id)+"' and type = 'veterinary'"
            c.execute(q4)
            conn.commit()
            return HttpResponseRedirect("/veterinary_list/")
     
            
    return HttpResponseRedirect("/veterinary_request/")

def veterinary_list(request):
    msg = ""
    q1 = "select v.* from veterinary v, login l where v.v_id = l.user_id  and l.status = 1 and l.`type` = 'veterinary'"
    c.execute(q1)
    conn.commit()
    data = c.fetchall()
    if not bool(data):
        print(data)
        msg = "No Veterinary List to show"
        return render(request,"veterinary_list.html",{"data":data,"msg":msg})
    
    return render(request,"veterinary_list.html",{"data":data})

def shop_request(request):
    msg = ""
    q1 = "select s.* from pet_centre s, login l where s.s_id = l.user_id  and l.status = 0 AND l.`type` = 'pet_centre'"
    c.execute(q1)
    conn.commit()
    data = c.fetchall()
    print(q1)
    print(data)
    if not bool(data):
        print(data)
        msg = "No Shop Request List to show"
        return render(request,"shop_request.html",{"data":data,"msg":msg})
    
    return render(request,"shop_request.html",{"data":data})

def shop_action(request):
    print("inside update")
    reg_id = request.GET.get("reg_id")
    action = request.GET.get("action")
    print(action)
    
    if action == 'approve' :
        q1 = "update login set status = '1'  where user_id ='"+str(reg_id)+"' and type='pet_centre'"
        c.execute(q1)
        conn.commit()
        q2 = "select s_phone1 from pet_centre where s_id ='"+str(reg_id)+"'"
        c.execute(q2)
        ph = c.fetchone()
        msg = "Dear customer, Your Account is active now. Now you can login using ur username and password"
        sendsms(ph[0],msg)
        return HttpResponseRedirect("/shop_request/")

    if action == 'remove' :
        w_type = request.GET.get("type")
        if w_type == 'req':

            q3 = "delete from pet_centre where s_id ='"+str(reg_id)+"'"
            c.execute(q3)
            conn.commit()

            q4 = "delete from login where user_id ='"+str(reg_id)+"' and type = 'pet_centre'"
            c.execute(q4)
            conn.commit()
            return HttpResponseRedirect("/shop_request/")

        elif (w_type == 'list'):
       
            q3 = "delete from pet_centre where s_id ='"+str(reg_id)+"'"
            c.execute(q3)
            conn.commit()

            q4 = "delete from login where user_id ='"+str(reg_id)+"' and type = 'pet_centre'"
            c.execute(q4)
            conn.commit()
            return HttpResponseRedirect("/shop_list/")
     
            
    return HttpResponseRedirect("/shop_request/")

def shop_list(request):
    msg = ""
    q1 = "select s.* from pet_centre s, login l where s.s_id = l.user_id  and l.status = 1 AND l.`type` = 'pet_centre'"
    c.execute(q1)
    conn.commit()
    data = c.fetchall()
    if not bool(data):
        print(data)
        msg = "No Shop List to show"
        return render(request,"shop_list.html",{"data":data,"msg":msg})
    
    return render(request,"shop_list.html",{"data":data})

def view_complaints(request):
    msg = ""
    q1 = "select * from complaints c, owner o where o.o_id = c.user_id order by posted_date"
    c.execute(q1)
    conn.commit()
    data = c.fetchall()
    print(data)
    if not bool(data):
        print(data)
        msg = "No Shop List to show"
        return render(request,"shop_list.html",{"data":data,"msg":msg})
    
    return render(request,"view_complaints.html",{"data":data})

def add_category(request):
    msg = ""
    q1 = "select * from category"
    c.execute(q1)
    conn.commit()
    data = c.fetchall()
    print(data)
    
    if 'submit' in request.POST:
        category = request.POST.get("category")
        q1 = "insert into category(`c_name`) values('"+str(category)+"')"
        c.execute(q1)
        conn.commit()
        print(q1)
        msg = "Added Successfully"
        return render(request,"add_category.html",{"data":data,"msgg":msg})
        

    if not bool(data):
        print(data)
        msg = "No category list to show"
        return render(request,"add_category.html",{"data":data,"msg":msg})
    
    return render(request,"add_category.html",{"data":data})


def cat_action(request):
    print("inside update")
    reg_id = request.GET.get("reg_id")
    
    q3 = "delete from category where c_id ='"+str(reg_id)+"'"
    c.execute(q3)
    conn.commit()

            
    return HttpResponseRedirect("/add_category/")
