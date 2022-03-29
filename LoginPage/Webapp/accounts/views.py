from email import message
import imp
from unicodedata import name
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

mydb = mysql.connector.connect(
    host="us-cdbr-east-05.cleardb.net",
    user="b86a52dbcfe302",
    password="d7707b58",
    database="heroku_933ea9c9e598adc",
)

mycursor = mydb.cursor()


@csrf_exempt
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def home(request):
    global logged_in
    if logged_in:
            return redirect('/myprojects')
    else:
        return render(request, 'accounts/dashboard.html')

@csrf_exempt
def project_saved(request):
    global logged_in
    return render(request, 'accounts/project_saved.html')

def save_project():
    pass

def save_new_project():
    pass

@csrf_exempt
def widgets(request):
    global logged_in
    json_string = request.POST.get('json')
    if(json_string != None):
        print(json_string)
        save_project()
    else:
        print("testing")
        save_new_project()
    return render(request, 'accounts/project.html', {"logged_in":logged_in})


@csrf_exempt
def helpPage(request):
    return render(request, 'accounts/help.html')


@csrf_exempt
def aboutPage(request):
    return render(request, 'accounts/about.html')


@csrf_exempt
@never_cache
def myProjects(request):
    global userprojects
    userprojects =[]
    mycursor.execute("SELECT project_id FROM user_access WHERE username = %s", (uname,))
    myresult = mycursor.fetchall()
    for project in myresult:
        mycursor.execute("SELECT * FROM projects WHERE project_id = %s", (project))
        myproject = mycursor.fetchone()
        userprojects.append({'name': myproject[1], 'id':myproject[0], 'JSON':myproject[2]})
        print(userprojects)
    context = {'userprojects': userprojects, 'name': name}
    if logged_in:
        return render(request, 'accounts/myprojects.html', context)
    else:
        return render(request, 'accounts/dashboard.html')


@csrf_exempt
def delete_project(request, param):
    current_projectid = (userprojects[int(param)-2]['id'])
    mycursor.execute("DELETE FROM user_access WHERE project_id = %s", (current_projectid,))
    mycursor.execute("DELETE FROM projects WHERE project_id = %s", (current_projectid,))
    mydb.commit()
    return redirect("/myprojects")


@csrf_exempt
def duplicate_project(request, param):
    cur_proj= (userprojects[int(param)-2])

    #DECLARE @inserted TABLE (project_id INT)
    sql="INSERT INTO projects (project_name, JSON_encoding) VALUES (%s, %s)"
    val=(cur_proj['name'], cur_proj['JSON'])
    mycursor.execute(sql,val)
    print(mycursor.lastrowid)
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
def file(request, param):
    projectId = param
    print("projectId is " + projectId)
    if not logged_in:
        return render(request, 'accounts/dashboard.html')
    
    # check if the project id exists
    exists = True
    if exists:
        return render(request, 'accounts/help.html', locals()) # redirect to a dummy template
    else:
        return render(request, 'accounts/file_error.html')


# @unauthenticated_user
@never_cache
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
