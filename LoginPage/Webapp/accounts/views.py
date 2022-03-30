from email import message
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
import string
import mysql.connector
from django.views.decorators.cache import cache_control
from django.views.decorators.cache import never_cache
from django.contrib.auth.hashers import make_password, check_password
from django.views.decorators.csrf import csrf_exempt


logged_in = False
name = None
userprojects = []
currentopen_projectid = ""

mydb = mysql.connector.connect(
    host="us-cdbr-east-05.cleardb.net",
    user="b86a52dbcfe302",
    password="d7707b58",
    database="heroku_933ea9c9e598adc",
)

mycursor = mydb.cursor()
currentopen_projectid = -1


@csrf_exempt
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def home(request):
    global logged_in
    global currentopen_projectid
    currentopen_projectid = -1
    if logged_in:
            return redirect('/myprojects')
    else:
        return render(request, 'accounts/dashboard.html')

@csrf_exempt
def project_saved(request):
    global logged_in
    return render(request, 'accounts/project_saved.html')

def save_project(project_name, json_string):
    global logged_in
    global currentopen_projectid
    sql = "UPDATE projects SET JSON_encoding = %s WHERE project_id = %s"
    val = (json_string,currentopen_projectid)
    mycursor.execute(sql, val)
    mydb.commit()
    sql = "UPDATE projects SET project_name = %s WHERE project_id = %s"
    val = (project_name, currentopen_projectid)
    mycursor.execute(sql,val)
    mydb.commit() 

def save_new_project():
    global currentopen_projectid
    global logged_in
    sql = "INSERT INTO projects (project_name, JSON_encoding) VALUES (%s, %s)"
    val = ("Project_Name","")
    mycursor.execute(sql, val)
    currentopen_projectid = (mycursor.lastrowid)
    mycursor.execute("INSERT INTO user_access (project_id, username) VALUES (%s,%s)", (mycursor.lastrowid,uname))
    mydb.commit()


@csrf_exempt
@cache_control(no_cache=True, must_revalidate=True)
@never_cache
def widgets(request):
    global logged_in
    global currentopen_projectid
    save_new_project()
    return HttpResponse("<html><script>window.location.replace('/myprojects/project_saved/" + str(currentopen_projectid) + "');</script></html>")
#    return render(request, 'accounts/project.html', {"logged_in":logged_in})

@csrf_exempt
def aboutPage(request):
    global logged_in
    return render(request, 'accounts/about.html')


@csrf_exempt
@never_cache
@cache_control(no_cache=True, must_revalidate=True)
def myProjects(request):
    global userprojects
    global logged_in
    if logged_in:  
        userprojects =[]
        mycursor.execute("SELECT project_id FROM user_access WHERE username = %s", (uname,))
        myresult = mycursor.fetchall()
        for project in myresult:
            mycursor.execute("SELECT * FROM projects WHERE project_id = %s", (project[0],))
            myproject = mycursor.fetchone()
            userprojects.append({'name': myproject[1], 'id':myproject[0], 'JSON':myproject[2]})
            context = {'userprojects': userprojects, 'name': name}
        return render(request, 'accounts/myprojects.html', context)
    else:
        return render(request, 'accounts/dashboard.html')


@csrf_exempt
def delete_project(request, param):
    global logged_in
    mycursor.execute("DELETE FROM user_access WHERE project_id = %s", (param,))
    mycursor.execute("DELETE FROM projects WHERE project_id = %s", (param,))
    mydb.commit()
    return redirect("/myprojects")


@csrf_exempt
def duplicate_project(request, param):
    global logged_in
    mycursor.execute("SELECT * FROM projects WHERE project_id = %s", (param,))
    cur_proj= mycursor.fetchone()
    sql="INSERT INTO projects (project_name, JSON_encoding) VALUES (%s, %s)"
    copy_name = "copy" + str(cur_proj[1])
    val=(copy_name, cur_proj[2])
    mycursor.execute(sql,val)
    mycursor.execute("INSERT INTO user_access (project_id, username) VALUES (%s,%s)", (mycursor.lastrowid,uname))
    mydb.commit()  
    return redirect("/myprojects")

@csrf_exempt
@cache_control(no_cache=True, must_revalidate=True)
@never_cache
def logout(request):
    global logged_in
    if logged_in:
        logged_in = False
        return HttpResponse("""<html><script>window.location.replace('/');</script></html>""")


@csrf_exempt
@cache_control(no_cache=True, must_revalidate=True)
@never_cache
def file(request, param):
    global logged_in
    projectId = param
    if not logged_in:
        return render(request, 'accounts/dashboard.html')
    # if projectId != None:
    #     return redirect("project-saved/")
    # check if the project id exists
    json_string = request.POST.get('json')
    project_name = request.POST.get('p_name')
    if(json_string != None):
        print(json_string, project_name)
    #    if(json_string != None and currentopen_projectid != -1):
        save_project(project_name, json_string)
#        
    exists = True
    if exists:
        # send the json string here, husnain!
        mycursor.execute("SELECT * FROM projects WHERE project_id = %s", (projectId,))
        current_project = mycursor.fetchone()

        #fetched values
        currentopen_projectid = current_project[0]
        currentopen_projectname = current_project[1]
        json_string = current_project[2]

        return render(request, 'accounts/project_saved.html', globals()) # redirect to a dummy template
    else:
        return render(request, 'accounts/file_error.html')

# @unauthenticated_user
@never_cache   
@cache_control(no_cache=True, must_revalidate=True)
def login(request):
    global uname
    global logged_in
    if logged_in:
        # return redirect('/myprojects')
        return HttpResponse("""<html><script>window.location.replace('/myprojects');</script></html>""")
    else:
        def check_login(username, password, users):
            for user_detail in users:
                if (user_detail[0] == username and check_password(password.strip(), user_detail[2].strip())):
                    print("Login succesful, welcome " + user_detail[1])
                    global name
                    name = user_detail[1]
                    return True
            return False
        
        username = request.POST.get('login_username')
        password = request.POST.get('login_password')

        mycursor.execute("SELECT * FROM user_details")
        myresult = mycursor.fetchall()

        if (check_login(username, password, myresult)):
            logged_in = True
            uname = username
            response = redirect("/myprojects")
            return response
        
        return render(request, 'accounts/dashboard.html', {'login_incorrect': True})

@never_cache   
@cache_control(no_cache=True, must_revalidate=True)
def signup(request):
#pass a string and list as parameters
#checks if all the characters in string are from the list
    def allinclude(string, control):
        output=True
        for x in range (0, len(string)):
            current = False
            for y in range (0, len(control)):
                if string[x] == control[y]:
                    current= True
            if current==False:
                output = False
        return output

#capitalize each word in the string
    def capitalize(string):
        string= string.lower()
        LOS = string.split(" ") #LOS = list of strings
        string= ''
        for x in range (0, len(LOS)):
            if x > 0:
                string = string + ' '
            LOS[x]=LOS[x].capitalize()
            string = string + LOS[x]      
        return string

#check the range of a string
    def length(string, minimum, maximum):
        length = len(string)
        if (length >= minimum and length <= maximum):
            return True
        return False

    def username_exist(string):
        mycursor.execute("SELECT username FROM user_details")
        myresult = mycursor.fetchall()
        for username in myresult:
            if string == username[0]:
                return False
        return True

    def atleastone(string, control):
        for char in string:
            for control_char in control:
                if char == control_char:
                    return True
        return False
                
#name
#only letter, first letter after any space should be automatically capitalised, range is 2-26
    def namecheck(name):
        name_format = allinclude(name, string.ascii_letters + " ") #accept letters and space as well
        name_range=length(name,2,26)#some identification cards have this range for name length
        name = capitalize(name)
        return (name_format and name_range)


#passwords
#atleaest one letter, one number, one symbol, passwords has to match, 8-30 characters
    def passwordcheck(pass1, pass2):
        pass_format= (atleastone(pass1, string.ascii_letters) and atleastone(pass1, string.digits)
        and atleastone(pass1, string.punctuation))

        pass_same= False
        if pass1 == pass2:
            pass_same= True
            reg_incorrect['password2'] = False

        pass_range = length(pass1, 8, 30)
        if (pass_format and pass_range):
            reg_incorrect['password1'] = False

        return (pass_format and pass_same and pass_range)

#username
#only letters, numbers and underscore, unique to each user, 8-20 characters
    def usernamecheck(username):
        control = string.digits + string.ascii_letters + '_'
        #all digits, letters and punctuation symbols
        username_format=allinclude(username, control)
        unique= username_exist(username)
        reg_incorrect['unique'] = unique
        username_range= length(username, 8, 20)
        return (username_format and unique and username_range)

    def save(name, username, password):
        sql = "INSERT INTO user_details (username,name, password) VALUES (%s,%s,%s)"
        val = (username, name, password)
        mycursor.execute(sql,val)
        mydb.commit()
        print("Sign up successfull")

    name = request.POST.get('regis_name')
    username = request.POST.get('regis_username')
    pass1 = request.POST.get('regis_password1')
    pass2 = request.POST.get('regis_password2')

    reg_incorrect = {'name': True, 'username': True, 'password1': True, 'password2': True, 'unique': False}

    if namecheck(name):
        print("name is in the correct format")
        reg_incorrect['name'] = False
    else:
        print("name is in incorrect format")

    if usernamecheck(username):
        print("username is in the correct format")
        reg_incorrect['username'] = False
    else:
        print("username is in incorrect format")
        
    if passwordcheck(pass1,pass2):
        print("password is in the correct format")
    else:
        print("password is in incorrect format")
    
    if namecheck(name) and usernamecheck(username) and passwordcheck(pass1,pass2):
        pass1 = make_password(pass1)
        save(name, username, pass1)
    context = {'reg_incorrect': reg_incorrect}
    return render(request, 'accounts/dashboard.html', context)
