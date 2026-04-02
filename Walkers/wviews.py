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


def walkers_header_footer(request):
    return render(request,"walkers_header_footer.html")

def walkers_home(request):
    return render(request,"walkers_home.html")

def walkers_profile(request):
    wid = request.session["wid"]
    print(wid)
    q1 = "select * from walker w, login l where w.w_id = '"+str(wid)+"' and l.user_id = w.w_id and l.type = 'walker'"
    c.execute(q1)
    conn.commit()
    data= c.fetchall()
    print(data)

    if 'submit' in request.POST:
        name = request.POST.get("name")
        mail = request.POST.get("mail")
        phone = request.POST.get("phone")
        address = request.POST.get("address")
        available = request.POST.get("available")
        password = request.POST.get("password")
        rate = request.POST.get("rate")


        q2 = "update walker set w_name='"+str(name)+"', w_mail='"+str(mail)+"',w_phone='"+str(phone)+"',w_address='"+str(address)+"',w_time='"+str(available)+"',w_rate='"+str(rate)+"'  where w_id = '"+str(wid)+"'"
        c.execute(q2)
        conn.commit()
        q3 = "update login set `user_name`='"+str(mail)+"', password = '"+str(password)+"' where user_id = '"+str(wid)+"' and type = 'walker'"
        c.execute(q3)
        conn.commit()
        msg ="You have  successfully Updated Your Profile"
        q4 = "select * from walker w, login l where w.w_id = '"+str(wid)+"' and l.user_id = w.w_id and l.type = 'walker'"
        c.execute(q4)
        conn.commit()
        data1= c.fetchall()
        return render(request,"walkers_profile.html",{"data":data1,"msg":msg})
    return render(request,"walkers_profile.html",{"data":data})

def new_request(request):
    wid = request.session["wid"]
    q1 = "SELECT * FROM walker_request wr , owner o WHERE wr.w_id = '"+str(wid)+"' AND wr.o_id = o.o_id AND wr.status = 'send'"
    c.execute(q1)
    conn.commit()
    data = c.fetchall()
    print(q1)
    print(data)
    if not bool(data):
        msg = "No new requests to show..."
        return render(request,"new_request.html",{"data":data,"msg":msg})
    return render(request,"new_request.html",{"data":data})

def new_request_action(request):
    # wid = request.session["wid"]
    req_id = request.GET.get("req_id")
    action = request.GET.get("action")

    q3 = "select o.o_phone from owner o, walker_request wr where wr.wr_id = '"+str(req_id)+"' and wr.o_id = o.o_id  "
    c.execute(q3)
    conn.commit()
    data1 = c.fetchone()

    if action == 'approve' :
        q2 = "update walker_request set status = '"+str(action)+"' where wr_id = '"+str(req_id)+"'"
        c.execute(q2)
        conn.commit()
        print(q2)
        msg = "Dear Customer, Your Request has been approved by DogWalker . PLease visit the site for Further Use."
        sendsms(data1[0],msg)
        return HttpResponseRedirect("/new_request/")
    
    if action == 'reject' :
        q2 = "update walker_request set status = '"+str(action)+"' where wr_id = '"+str(req_id)+"'"
        c.execute(q2)
        conn.commit()
        print(q2)
        msg = "Dear Customer, Your Request has been Rejected by DogWalker . PLease visit the site for Further Use."
        sendsms(data1[0],msg)
        return HttpResponseRedirect("/new_request/")

def request_status(request):
    wid = request.session["wid"]
    q1 = "SELECT * FROM walker_request wr , owner o WHERE wr.w_id = '"+str(wid)+"' AND wr.o_id = o.o_id AND wr.status = 'approve'"
    c.execute(q1)
    conn.commit()
    data = c.fetchall()
    print(q1)
    print(data)
    if not bool(data):
        msg = "No new requests to show..."
        return render(request,"request_status.html",{"data":data,"msg":msg})
    return render(request,"request_status.html",{"data":data})

def add_amount(request):
    wid = request.session["wid"]
    req_id = request.GET.get("req_id")

    q1 = "SELECT * FROM walker_request where wr_id = '"+str(req_id)+"'"
    c.execute(q1)
    conn.commit()
    data = c.fetchone()
    print(q1)
    print(data)
    if 'submit' in request.POST:
        amount = request.POST.get("amount")
        q2 = "update walker_request set amount = '"+str(amount)+"' where wr_id = '"+str(req_id)+"'"
        c.execute(q2)
        conn.commit()
        return HttpResponseRedirect("/request_status")
    return render(request,"add_amount.html",{"data":data})


def add_message(request):
    wid = request.session["wid"]
    req_id = request.GET.get("req_id")

    q1 = "SELECT * FROM walker_request where wr_id = '"+str(req_id)+"'"
    c.execute(q1)
    conn.commit()
    data = c.fetchone()
    print(q1)
    print(data)
    if 'submit' in request.POST:
        message = request.POST.get("message")
        q2 = "update walker_request set message = '"+str(message)+"' where wr_id = '"+str(req_id)+"'"
        c.execute(q2)
        conn.commit()
        return HttpResponseRedirect("/request_status")
    return render(request,"add_message.html",{"data":data})

def request_approve_action(request):
    # wid = request.session["wid"]
    req_id = request.GET.get("req_id")
    action = request.GET.get("action")

    q3 = "select o.o_phone from owner o, walker_request wr where wr.wr_id = '"+str(req_id)+"' and wr.o_id = o.o_id  "
    c.execute(q3)
    conn.commit()
    data1 = c.fetchone()

    q2 = "update walker_request set status = '"+str(action)+"' where wr_id = '"+str(req_id)+"'"
    c.execute(q2)
    conn.commit()
    print(q2)
    msg = "Dear Customer, Your Request has been Rejected by DogWalker . PLease visit the site for Further Use."
    sendsms(data1[0],msg)
    return HttpResponseRedirect("/request_status/")