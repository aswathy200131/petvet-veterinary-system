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

def owner_header_footer(request):
    return render(request,"owner_header_footer.html")

def owner_home(request):
    return render(request,"owner_home.html")

def send_complaints(request):
    uid = request.session["uid"]
    print(uid)
    today = now.date()
    print(today)
    if 'submit' in request.POST:
        sub = request.POST.get("sub")
        name = request.POST.get("name")
        complaint = request.POST.get("complaint")
        q1 = "insert into complaints(`user_id`,`sub`,`name`,`complaint`,`posted_date`) values('"+str(uid)+"','"+str(sub)+"','"+str(name)+"','"+str(complaint)+"','"+str(today)+"')"
        c.execute(q1)
        conn.commit()
        msg = "Your Complaint Registered Successfully"
        return render(request,"send_complaints.html",{"msg":msg})
    return render(request,"send_complaints.html")


def view_walkers(request):
    msg = ""
    q1 =  "select * from walker"
    c.execute(q1)
    data = c.fetchall()
    print(q1)
    print(data)
    if not bool(data):
        msg = "No dog walker List to show"
        return render(request,"view_walkers.html",{"data":data,"msg":msg})
    return render(request,"view_walkers.html",{"data":data})

def owner_view_walkers(request):
    reg_id = request.GET.get("reg_id")
    print(reg_id)
    msg = ""
    if reg_id == "":
        return HttpResponseRedirect("/view_walkers")
    else:
        q1 =  "select * from walker where w_id = '"+str(reg_id)+"'"
        c.execute(q1)
        data = c.fetchall()
        print(q1)
        print(data)
        if not bool(data):
            msg = "No dog walker List to show"
            return render(request,"owner_view_walkers.html",{"data":data,"msg":msg})
    return render(request,"owner_view_walkers.html",{"data":data})


def walker_request_form(request):
    reg_id = request.GET.get("w_id")
    uid = request.session["uid"]
    today = now.date()

    q2 = "select w_phone,w_name from walker where w_id = '"+str(reg_id)+"'"
    c.execute(q2)
    ph = c.fetchone()
    # print(reg_id)
    # msg = ""
    # if reg_id == "":
    #     return HttpResponseRedirect("/view_walkers")
    # else:
        
    #     return render(request,"walker_request_form.html")
    if 'submit' in request.POST:
        name = request.POST.get("name")
        timing = request.POST.get("timing")
        desc = request.POST.get("desc")
        q1 = "insert into walker_request(`o_id`,`w_id`,`breed`,`timing`,`description`,`posted_date`,`status`) values('"+str(uid)+"','"+str(reg_id)+"','"+str(name)+"','"+str(timing)+"','"+str(desc)+"','"+str(today)+"','send')"
        c.execute(q1)
        conn.commit()
        msgg = "Dear "+str(ph[1])+" , You have a new request from a user. Please visit our site for Accepting the request "
        sendsms(ph[0],msgg)
        msg = "Request send successfully"
        return render(request,"walker_request_form.html",{"msg":msg})
    return render(request,"walker_request_form.html")

def walker_request_status(request):
    uid = request.session["uid"]
    msg = ""
    q1 =  "select * from walker_request wr, walker w where wr.o_id = '"+str(uid)+"' and wr.w_id = w.w_id"
    c.execute(q1)
    data = c.fetchall()
    print(q1)
    print(data)
    if not bool(data):
        msg = "No dog walker request List to show"
        return render(request,"walker_request_status.html",{"data":data,"msg":msg})
    return render(request,"walker_request_status.html",{"data":data})

def request_action(request):
    uid = request.session["uid"]
    req_id = request.GET.get("req_id")
    print(req_id)

    q3 = "select w.w_phone from walker w, walker_request wr where wr.wr_id = '"+str(req_id)+"' and wr.w_id = w.w_id  "
    c.execute(q3)
    conn.commit()
    data1 = c.fetchone()

    q1 = "delete from walker_request where wr_id = '"+str(req_id)+"'"
    c.execute(q1)
    conn.commit()
    msg = "Dear Customer, Your Request has been Rejected by Customer . PLease visit the site for Further Use."
    sendsms(data1[0],msg)
    return HttpResponseRedirect("/walker_request_status/")

def view_pet_centre(request):
    msg = ""
    q1 =  "select * from pet_centre"
    c.execute(q1)
    data = c.fetchall()
    print(q1)
    print(data)
    if not bool(data):
        msg = "No pet_centre List to show"
        return render(request,"view_pet_centre.html",{"data":data,"msg":msg})
    return render(request,"view_pet_centre.html",{"data":data})

def view_pet_centre_profile(request):
    msg = ""

    reg_id = request.GET.get("reg_id")
    q1 =  "select * from pet_centre where s_id = '"+str(reg_id)+"'"
    c.execute(q1)
    data = c.fetchall()
    print(q1)
    print(data)
    

    q3 = "select * from category"
    print(q3)
    c.execute(q3)
    conn.commit()
    data2 = c.fetchall()
    print(data2)

    if 'submit' in request.POST:
        category = request.POST.get("category")
        q2 = "select * from product where category = '"+str(category)+"' and s_id = '"+str(reg_id)+"'"
        c.execute(q2)
        conn.commit()
        data1 = c.fetchall()
        print(data1)
        return render(request,"view_pet_centre_profile.html",{"data1":data1,"data":data,"data2":data2})
    return render(request,"view_pet_centre_profile.html",{"data":data,"data2":data2})

def view_petcentre_product(request):
    msg = ""
    reg_id = request.GET.get("reg_id")
    q1 = "select * from category"
    print(q1)
    c.execute(q1)
    conn.commit()
    data = c.fetchall()
    print(data)

    if 'submit' in request.POST:
        category = request.POST.get("category")
        q2 = "select * from product where category = '"+str(category)+"' and s_id = '"+str(reg_id)+"'"
        c.execute(q2)
        conn.commit()
        data1 = c.fetchall()
        print(data1)
        return render(request,"view_petcentre_product.html",{"data1":data1,"data":data})
    # if not bool(data):
    #     msg = "No pet_centre List to show"
    #     return render(request,"view_pet_centre_profile.html",{"data":data,"msg":msg})
    return render(request,"view_petcentre_product.html",{"data":data,})


def send_lookafter_request(request):
    reg_id = request.GET.get("reg_id")
    uid = request.session["uid"]
    today = now.date()

    # q2 = "select w_phone,w_name from walker where w_id = '"+str(reg_id)+"'"
    # c.execute(q2)
    # ph = c.fetchone()
    # print(reg_id)
    # msg = ""
    # if reg_id == "":
    #     return HttpResponseRedirect("/view_walkers")
    # else:
        
    #     return render(request,"walker_request_form.html")
    if 'submit' in request.POST:
        name = request.POST.get("name")
        fr = request.POST.get("from")
        tr = request.POST.get("to")
        desc = request.POST.get("desc")
        q1 = "insert into lookafter_request(`u_id`,`s_id`,`breed`,`desc`,`from`,`to`,`posted_date`,`status`) values('"+str(uid)+"','"+str(reg_id)+"','"+str(name)+"','"+str(desc)+"','"+str(fr)+"','"+str(tr)+"','"+str(today)+"','send')"
        c.execute(q1)
        conn.commit()
        # msgg = "Dear "+str(ph[1])+" , You have a new request from a user. Please visit our site for Accepting the request "
        # sendsms(ph[0],msgg)
        msg = "Request send successfully"
        return render(request,"send_lookafter_request.html",{"msg":msg})
    return render(request,"send_lookafter_request.html",{"dt":str(today)})


def owner_lookafter_request(request):
    uid = request.session["uid"]
    msg = ""
    q1 =  "select * from lookafter_request lr, pet_centre p where lr.u_id = '"+str(uid)+"' and lr.s_id = p.s_id"
    c.execute(q1)
    data = c.fetchall()
    print(q1)
    print(data)
    if not bool(data):
        msg = "No Look after request List to show"
        return render(request,"owner_lookafter_request.html",{"data":data,"msg":msg})
    return render(request,"owner_lookafter_request.html",{"data":data})

def owner_show_pets(request):
    msg = ""
    q1 =  "select * from adoption a , pet_centre p where a.s_id = p.s_id"
    c.execute(q1)
    data = c.fetchall()
    print(q1)
    print(data)
    if not bool(data):
        msg = "No pet_centre List to show"
        return render(request,"owner_show_pets.html",{"data":data,"msg":msg})
    return render(request,"owner_show_pets.html",{"data":data})

def owner_view_pet(request):
    reg_id = request.GET.get("reg_id")

    msg = ""
    q1 =  "select * from adoption a , pet_centre p where a.a_id = '"+str(reg_id)+"' and a.s_id = p.s_id"
    c.execute(q1)
    data = c.fetchall()
    print(q1)
    print(data)
    if not bool(data):
        msg = "No pet_centre List to show"
        return render(request,"owner_view_pet.html",{"data":data,"msg":msg})
    return render(request,"owner_view_pet.html",{"data":data})

def send_pet_adoption_request(request):
    a_id = request.GET.get("a_id")
    s_id = request.GET.get("s_id")
    cnt = request.GET.get("cnt")
    uid = request.session["uid"]
    today = now.date()

    q1 = "select a_count from adoption where a_id = '"+str(a_id)+"' "
    c.execute(q1)
    data= c.fetchone()

    # q2 = "select w_phone,w_name from walker where w_id = '"+str(reg_id)+"'"
    # c.execute(q2)
    # ph = c.fetchone()
    # print(reg_id)
    # msg = ""
    # if reg_id == "":
    #     return HttpResponseRedirect("/view_walkers")
    # else:
        
    #     return render(request,"walker_request_form.html")
    if 'submit' in request.POST:
        count = request.POST.get("count")
        
        q1 = "insert into adoption_request(`a_id`,`s_id`,`u_id`,`ar_count`,`posted_date`,`status`) values('"+str(a_id)+"','"+str(s_id)+"','"+str(uid)+"','"+str(count)+"','"+str(today)+"','send')"
        c.execute(q1)
        conn.commit()
        # msgg = "Dear "+str(ph[1])+" , You have a new request from a user. Please visit our site for Accepting the request "
        # sendsms(ph[0],msgg)
        msg = "Request send successfully"
        return render(request,"send_pet_adoption_request.html",{"msg":msg})
    return render(request,"send_pet_adoption_request.html",{"dt":str(today),"data":data})


def owner_adoption_status(request):
    uid = request.session["uid"]
    msg = ""
    q1 =  "select * from adoption_request ar, pet_centre p, adoption a where ar.u_id = '"+str(uid)+"' and ar.s_id = p.s_id and ar.a_id = a.a_id and ar.s_id = a.s_id"
    c.execute(q1)
    data = c.fetchall()
    print(q1)
    print(data)
    if not bool(data):
        msg = "No Adoption request List to show"
        return render(request,"owner_adoption_status.html",{"data":data,"msg":msg})
    return render(request,"owner_adoption_status.html",{"data":data})

def del_adoption_request(request):
    uid = request.session["uid"]
    req_id = request.GET.get("req_id")
    print(req_id)

    # q3 = "select w.w_phone from walker w, walker_request wr where wr.wr_id = '"+str(req_id)+"' and wr.w_id = w.w_id  "
    # c.execute(q3)
    # conn.commit()
    # data1 = c.fetchone()

    q1 = "delete from adoption_request where ar_id = '"+str(req_id)+"'"
    c.execute(q1)
    conn.commit()
    # msg = "Dear Customer, Your Request has been Rejected by Customer . PLease visit the site for Further Use."
    # sendsms(data1[0],msg)
    return HttpResponseRedirect("/owner_adoption_status/")

def owner_view_veterinary(request):
    # reg_id = request.GET.get("reg_id")

    msg = ""
    q1 =  "select * from veterinary"
    c.execute(q1)
    data = c.fetchall()
    print(q1)
    print(data)
    if not bool(data):
        msg = "No veterinary List to show"
        return render(request,"owner_view_veterinary.html",{"data":data,"msg":msg})
    return render(request,"owner_view_veterinary.html",{"data":data})

def view_vet_dr_list(request):
    reg_id = request.GET.get("reg_id")

    msg = ""
    q1 =  "select * from doctor where v_id = '"+str(reg_id)+"'"
    c.execute(q1)
    data = c.fetchall()
    print(q1)
    print(data)
    if not bool(data):
        msg = "No Doctor List to show"
        return render(request,"view_vet_dr_list.html",{"data":data,"msg":msg})
    return render(request,"view_vet_dr_list.html",{"data":data})

def send_dr_appointment(request):
    v_id = request.GET.get("v_id")
    uid = request.session["uid"]

    today = now.date()
    msg = ""
    q1 =  "select * from doctor where v_id = '"+str(v_id)+"'"
    c.execute(q1)
    data = c.fetchall()
    print(q1)
    print(data)

    if 'submit' in request.POST:
        doctor = request.POST.get("doctor")
        date1 = request.POST.get("date1")
        time = request.POST.get("time")
        print(time)
        q1 = "insert into dr_booking(`v_id`,`dr_id`,`u_id`,`date`,`posted_date`,`time`,`status`) values('"+str(v_id)+"','"+str(doctor)+"','"+str(uid)+"','"+str(date1)+"','"+str(today)+"','"+str(time)+"','send')"
        c.execute(q1)
        conn.commit()
        # msgg = "Dear "+str(ph[1])+" , You have a new request from a user. Please visit our site for Accepting the request "
        # sendsms(ph[0],msgg)
        msg = "Request send successfully"
        return render(request,"send_dr_appointment.html",{"msg":msg}) 

    if not bool(data):
        msg = "No Doctor List to show"
        return render(request,"send_dr_appointment.html",{"data":data,"msg":msg})
    return render(request,"send_dr_appointment.html",{"data":data,"dt":str(today)})

def owner_view_booking(request):
    uid = request.session["uid"]
    msg = ""
    q1 =  "select * from dr_booking db, doctor d, Veterinary v where db.u_id = '"+str(uid)+"' and db.dr_id = d.dr_id and db.v_id = v.v_id "
    c.execute(q1)
    data = c.fetchall()
    print(q1)
    print(data)
    if not bool(data):
        msg = "No Booking Request to show List to show"
        return render(request,"owner_view_booking.html",{"data":data,"msg":msg})
    return render(request,"owner_view_booking.html",{"data":data})

def del_booking_request(request):
    uid = request.session["uid"]
    req_id = request.GET.get("req_id")
    print(req_id)

    # q3 = "select w.w_phone from walker w, walker_request wr where wr.wr_id = '"+str(req_id)+"' and wr.w_id = w.w_id  "
    # c.execute(q3)
    # conn.commit()
    # data1 = c.fetchone()

    q1 = "delete from dr_booking where bk_id = '"+str(req_id)+"'"
    c.execute(q1)
    conn.commit()
    # msg = "Dear Customer, Your Request has been Rejected by Customer . PLease visit the site for Further Use."
    # sendsms(data1[0],msg)
    return HttpResponseRedirect("/owner_view_booking/")