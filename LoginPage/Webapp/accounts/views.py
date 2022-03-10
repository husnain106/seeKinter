from email import message
from django.shortcuts import render, redirect
from django.http import HttpResponse

from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate, login, logout
import string
import mysql.connector


def home(request):
    return render(request, 'accounts/dashboard.html')

def helpPage(request):
    return render(request, 'accounts/help.html')

def aboutPage(request):
    return render(request, 'accounts/about.html')

def myProjects(request):
    return render(request, 'accounts/myprojects.html')

def login(request):
    def check_login(username, password, users):
        for user_detail in users:
            if (user_detail[0] == username and user_detail[2].strip() == password.strip()):
                print("Login succesful, welcome " + user_detail[1])
                return True
        return False
    
    username = request.POST.get('login_username')
    password = request.POST.get('login_password')

    mydb = mysql.connector.connect(
    host="dbhost.cs.man.ac.uk",
    user="p73848hs",
    password="Ali09876",
    database="2021_comp10120_r11"
    )

    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM user_details")
    myresult = mycursor.fetchall()
    check_login(username, password, myresult)
    return HttpResponse("""<html><script>window.location.replace('/');</script></html>""")

def signup(request):
    mydb = mysql.connector.connect(
    host="dbhost.cs.man.ac.uk",
    user="p73848hs",
    password="Ali09876",
    database="2021_comp10120_r11"
    )

    mycursor = mydb.cursor()

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
        pass_range = length(pass1, 8, 30)
        return (pass_format and pass_same and pass_range)

#username
#only letters, numbers and underscore, unique to each user, 8-20 characters
    def usernamecheck(username):
        control = string.digits + string.ascii_letters + '_'
        #all digits, letters and punctuation symbols
        username_format=allinclude(username, control)
        unique= username_exist(username)
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

    if namecheck(name):
        print("name is in the correct format")
    else:
        print("name is in incorrect format")

    if usernamecheck(username):
        print("username is in the correct format")
    else:
        print("username is in incorrect format")
        
    if passwordcheck(pass1,pass2):
        print("password is in the correct format")
    else:
        print("password is in incorrect format")
    
    if namecheck(name) and usernamecheck(username) and passwordcheck(pass1,pass2):
        save(name, username, pass1)
    return HttpResponse("""<html><script>window.location.replace('/');</script></html>""")
