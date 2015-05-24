from django.shortcuts import render
from django.http import HttpResponse
from models import User, Activitie, elegidas, personal
from bs4 import BeautifulSoup
from datetime import datetime,timedelta
from django.http import HttpResponse, HttpResponseNotFound
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response
from django.template.loader import get_template
from django.template import Context
import htmllib
import urllib2
import time

ultima_actualizacion = ""


def prueba(request):
   template = get_template('index2.html')
   c = Context({'title': "Alvaro", "info" : 'Practica final'})
   end = template.render(c)
   return HttpResponse(end)


#####################
#####################
########LOGS#########
#####################


def login(request):
    if personal.objects.filter(user=request.user.username).count()>0 and len(request.user.username)>0:
        usuario = personal.objects.get(user = str(request.user.username))
        template = get_template("index2LOGIN.html")
        diccionario={"init" : "nada","Usuario":"","letra": usuario.letra, "fondo": usuario.fondo}
        return HttpResponse(template.render(Context(diccionario)))
    else:
        template = get_template("index2LOGIN.html")
        diccionario={"init" : "","Usuarios":"","letra": "", "fondo": ""}
        return HttpResponse(template.render(Context(diccionario)))
@csrf_exempt
def auth_view(request):
    username = request.POST.get("username", '')
    password = request.POST.get("password", '')
    user = auth.authenticate(username=username, password=password)

    if user is not None:
        auth.login(request,user)
        return HttpResponseRedirect("/todas/")
#        return HttpResponseRedirect('/accounts/loggedin/')
    else:
        print "NOT LOGED IN"
        return HttpResponseRedirect("/todas/")

# def loggedin(request):
#     return render_to_response('loggedin.html', {'full_name':request.user.username})

# def invalid_login(request):
#    return render_to_response('invalid_login.html')

@csrf_exempt
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/todas/")

#####################
#####################
########PARSER#######
#####################

def splitID(contenido):
    Identificador = contenido.split("<br>")[0].split('<atributo nombre="ID-EVENTO">')[1].split('</atributo>')[0]
    return Identificador

def splitName(contenido):
    name = contenido.split("<br>")[1].split('<atributo nombre="TITULO">')[1].split('</atributo>')[0]
    return name
    
def splitPrice(contenido):
    if contenido.split("<br>")[2] == ('<atributo nombre="GRATUITO">1</atributo>'):
        price = contenido.split("<br>")[2].split('<atributo nombre="GRATUITO">')[1].split('</atributo>')[0]
        price = "gratuito"
    elif contenido.split("<br>")[2] == ('<atributo nombre="GRATUITO">0</atributo>'):
        price = contenido.split("<br>")
        auxPr = ""
        i = 0
        for pr in price:
            if pr.find('<atributo nombre="PRECIO">') != -1:
                auxPr = contenido.split("<br>")[i].split('<atributo nombre="PRECIO">')[1].split('</atributo>')[0]
                price = auxPr
                break
            i += 1
        if auxPr == "":
            price = "null"
    else:
        price = contenido.split("<br>")[2].split('<atributo nombre="PRECIO">')[1].split('</atributo>')[0]
        #price = price.split('<![CDATA[')[1].split(']')[0]
    return price

def splitDate(contenido):
    date = contenido.split("<br>")
    i = 0
    for nombre in date:
        if nombre.find('<atributo nombre="FECHA-EVENTO">') != -1:
            break
        i += 1
    date = contenido.split("<br>")[i].split('<atributo nombre="FECHA-EVENTO">')[1].split('</atributo>')[0]
    date = date.split(' ')[0]
    return date

def splitStart(contenido):
    start = contenido.split("<br>")
    i = 0
    for hour in start:
        if hour.find('<atributo nombre="HORA-EVENTO">') != -1:
            break
        i += 1
    start = contenido.split("<br>")[i].split('<atributo nombre="HORA-EVENTO">')[1].split('</atributo>')[0]
    return start

def splitType(contenido):
    typ = contenido.split("<br>")
    auxT = typ
    i = 0
    for tp in typ:
        if tp.find('<atributo nombre="TIPO">') != -1:
            typ = contenido.split("<br>")[i].split('<atributo nombre="TIPO">')[1].split('</atributo>')[0]
            typ = typ.split("/")[3]
            break
        i += 1
    if auxT == typ:
        typ = "Evento"
    return typ

def splitTimeToLong(contenido):
    start = splitStart(contenido)
    end = "23:59"
    date_object_start = datetime.strptime(start, '%H:%M')
    date_object_end = datetime.strptime(end, '%H:%M')
    timeToLong = date_object_end - date_object_start
    return timeToLong

def Long(timeToLong):
    reference = timedelta(hours=5)
    if timeToLong >= reference:
        return True
    return False

def splitUrl(contenido):
    url = contenido.split("<br>")
    i = 0
    for urls in url:
        if urls.find('<atributo nombre="CONTENT-URL">') != -1:
            break
        i += 1
    url = contenido.split("<br>")[i].split('<atributo nombre="CONTENT-URL">')[1].split('</atributo>')[0]
    return url

def equals(resource):
    try:
        Activitie.objects.get(name=resource)
        return True
    except Activitie.DoesNotExist:
        return False

def saveEntrie(i,nam,pric,dat,startHou,ty,timeToLon,Lon,Ur):
    if equals(nam) != True:
        act = Activitie(Identificador = str(i), \
						name = str(nam), \
                        price = str(pric), \
                        date = str(dat), \
                        startHour = str(startHou), \
                        typ = str(ty),\
                        timeToLong = str(timeToLon), \
                        Long = str(Lon), \
                        Url = str(Ur))
        act.save()    

def parse():
    urlXml = 'http://datos.madrid.es/egob/catalogo/206974-0-agenda-eventos-culturales-100.xml'
    xml_doc = urllib2.urlopen(urlXml)
    xml_code = BeautifulSoup(xml_doc)
    response = ""
    for content in xml_code.findAll("contenido"):
        contenido = ""
        for news in content.findAll("atributo"):
            contenido += str(news) + "<br>"
        Identificador=splitID(contenido)
        name = splitName(contenido)
        price = splitPrice(contenido)
        date = splitDate(contenido)
        start = splitStart(contenido)
        typ = splitType(contenido)
        timeToLong = splitTimeToLong(contenido)
        lng = Long(timeToLong) 
        url = splitUrl(contenido)
        print Identificador
        print name
        print price
        print date
        print start
        print typ
        print timeToLong
        print lng
        print url
        saveEntrie(Identificador,name,price,date,start,typ,timeToLong,lng,url)
        response += contenido + "<br><hr><br>"
    return response

def giveTenDateAct():
    act = Activitie.objects.order_by('-date')
    activities = "\n"
    for acts in range(0,10):
        activities +="ID de la actividad" +act[acts].Identificador + \
                    "Actividad: " + act[acts].name + ", Precio: " + \
                    act[acts].price + ", Fecha: " + act[acts].date + \
                    ", Hora inicio: " + act[acts].startHour + \
                    ", Duracion: " + act[acts].timeToLong + \
                    ", Url:" + "<a href=" + act[acts].Url + ">" + \
                    "Pagina de la actividad" + "</a> " + "<br><br>"
    return activities

def update(request):
    parse()
    global ultima_actualizacion
    ultima_actualizacion=str(datetime.now()).split(".")[0]
    return HttpResponseRedirect("/todas/")




#####################
#####################
########INDICE#######
#####################
def getUserpages():
    act= elegidas.objects.order_by('user')
    activities="\n"
    name=""
    for acts in range(0,elegidas.objects.order_by('user').count()):
        if name!=act[acts].user:
            name=act[acts].user

            if personal.objects.filter(user = name).count()<=0:    
                pers = personal(title="Pagina de usuario "+name , user= name,letra="#333333", fondo="#fff")
                pers.save() 
            usuario=personal.objects.get(user=name)
            activities += "<a href=" "/"+ name + ">" + \
                    usuario.title + "</a> " + "<br>-Usuario registrado por Administrador<br><br>"
            

    return activities
def index(request):
    response = "<h1>Lista de actividades Disponibles: </h1></br>"
    

    if Activitie.objects.count() <= 0:
        global ultima_actualizacion
        ultima_actualizacion=str(datetime.now()).split(".")[0]
        parse()
        
    response += giveTenDateAct()
    paginas_users= getUserpages()
    print "NOMBRE RECIBIDO"+ request.user.username		
    if personal.objects.filter(user=request.user.username).count()>0 and len(request.user.username)>0:
        usuario = personal.objects.get(user = str(request.user.username))
        template = get_template("index2.html")
        diccionario={"init" : response,"Usuarios":paginas_users,"letra": usuario.letra, "fondo": usuario.fondo}
        return HttpResponse(template.render(Context(diccionario)))
    else:
        template = get_template("index2.html")
        diccionario={"init" : response,"Usuarios":"","letra": "", "fondo": ""}
        return HttpResponse(template.render(Context(diccionario)))

#####################
#####################
########USUARIO######
#####################
@csrf_exempt
def preferencias(request):
    redirect="/"+str(request.user.username)
    titAdd = request.POST.get("titAdd", '')
    letraAdd = request.POST.get("letraAdd", '')
    fondoAdd = request.POST.get("fondoAdd", '')
    usuario = personal.objects.get(user = str(request.user.username))
    
    usuario.letra= letraAdd
    usuario.fondo= fondoAdd
    print"ESTAMOS PRINTEADNO TITAD"+titAdd
    if(len(titAdd)>=1):
        usuario.title= titAdd
    usuario.save()
    return HttpResponseRedirect(redirect)
@csrf_exempt
def user(request,arg):
        value=0
        lt= "\n"
        redirect="/"+arg
        if request.method == "POST":        
             value = request.POST['Identificador']
        lt+="<form action='"+redirect+"'method='POST'>"
        lt+="<button name='Identificador' value='"+ str(int(value)+10) +"'>Diez Siguientes</button>"
        lt+="</form>"


        print "USUARIO RECIVIDO" + arg 


        #Mostramos la pagina del usuario
        if (request.user.is_authenticated() and arg==request.user.username and arg!="favicon.ico"):
            act= elegidas.objects.filter(user= request.user.username ).order_by('-date')
            if elegidas.objects.filter(user= request.user.username).count() <= 0:
                activities="Page Not Found"
                activities = "\n"
            else:
                activities = "\n"
                print "NUMERO DE ENTRADAS DE"+str(elegidas.objects.filter(user= request.user.username).count())
                if elegidas.objects.filter(user= str(request.user.username)).count()-int(value) >0:
                    print elegidas.objects.filter(user= str(request.user.username)).count()
                    print int(value)
                    for acts in range(int(value),elegidas.objects.filter(user= str(request.user.username)).count()):
                        print "entra al bucle"+act[acts].Identificador
                        activities +="ID de la actividad" +act[acts].Identificador + \
                            "Actividad: " + act[acts].name + ", Precio: " + \
                            act[acts].price + ", Fecha: " + act[acts].date + \
                            ", Hora inicio: " + act[acts].startHour + \
                            ", Duracion: " + act[acts].timeToLong + \
                            ", Url:" + "<a href=" + act[acts].Url + ">" + \
                            "Pagina de la actividad" + "</a> " + "<br><br>"
                        if acts==9:
                            break
                            

				
                else:
                    activities="No quedan mas actividades"
     
            logged = "<br><br>Logged in as " + arg  +"><br>"         
            
            usuario = personal.objects.get(user = str(request.user.username))
            template = get_template("index2USER.html")
            diccionario={"init" : lt+activities,"Usuarios":arg,"letra": usuario.letra, "fondo": usuario.fondo}    
           
            return HttpResponse(template.render(Context(diccionario)))
	               
        else:
            usuario = personal.objects.get(user = str(request.user.username))
            
            template = get_template("index2LOGOUT.html")
            diccionario={"init" : "","Usuarios": "" ,"Rss":"","letra": usuario.letra, "fondo": usuario.fondo}    
            return HttpResponse(template.render(Context(diccionario)))
           

    

#####################
#####################
#######ACTIVIDAD#####
##########ID#########
#####################

def decodeToOpenUrl(url):
    u = htmllib.HTMLParser(None)
    u.save_bgn()
    u.feed(url)
    url = u.save_end()
    return url


def searchP(url):
    urlInfor = decodeToOpenUrl(url)
    infor = urllib2.urlopen(urlInfor)
    infor = infor.read()
    s = infor.find('<div class="parrafo">')
    if s == -1:
        boolean = False
        response = "<a href=" + str(url) + ">" + "informacion" + "</a> <br>"
    else:
        boolean = True
        e = infor.find('</div>',s)
        parrafo = infor[s:e]
        parrafo = parrafo.split('<div class="parrafo">')[1]
        response = parrafo + "<br>"
        response += "<a href=" + str(url) + ">" + "toda la informacion" + "</a> <br>"
        response = unicode(response, 'utf-8')
    return response,boolean

def activity(request,arg):
    response = "<h1> ESTA ES TU ACTIVIDAD </h1>"
    encontrado= False
    act= Activitie.objects.filter(Identificador= str(arg))     
    acts=0
    activities = "\n"
    for acts in range(0,1):
        activities +="ID de la actividad: " +act[acts].Identificador + \
                    ", Actividad: " + act[acts].name + ", Precio: " + \
                    act[acts].price + ", Fecha: " + act[acts].date + \
                    ", Hora inicio: " + act[acts].startHour + \
                    ", Duracion: " + act[acts].timeToLong + \
                    ", Url: " + "<a href=" + act[acts].Url + ">" + \
                    act[acts].Url + "</a> :" + "<br><br>" 

    p,bl = searchP(act[acts].Url)
    if bl == True:
        activities += p
        usuario = personal.objects.get(user = str(request.user.username))  
        template = get_template("index2ACTIVIDAD.html")
        diccionario={"init" : activities,"Usuarios":"","letra": usuario.letra, "fondo": usuario.fondo}
        return HttpResponse(template.render(Context(diccionario)))

    urlAdc = decodeToOpenUrl(act[acts].Url)
    urlA = urllib2.urlopen(urlAdc)
    html = urlA.read()
    start = html.find('<a class="punteado" href="')  
             
    if start != -1:
        activities += "<a href=" + act[acts].Url + ">" + "informacion no disponible" + "</a> <br>"
        usuario = personal.objects.get(user = str(request.user.username))  
        template = get_template("index2ACTIVIDAD.html")
        diccionario={"init" : activities,"Usuarios":"","letra": usuario.letra, "fondo": usuario.fondo}
        return HttpResponse(template.render(Context(diccionario)))
        

        end = html.find('">',start)
        parrafo = html[start:end]
        urlInfor = parrafo.split('href="')[1]
    else:
        urlInfor = act[acts].Url

    if not urlInfor.startswith("http://www.madrid.es"):
        urlInfor = "http://www.madrid.es" + urlInfor

    urlInfor = decodeToOpenUrl(urlInfor)
    infor = urllib2.urlopen(urlInfor)
    infor = infor.read()
    s = infor.find('<div class="parrafo">')
    if s == -1:
        activities += "<a href=" + urlInfor + ">" + "informacion" + "</a> <br>"
        usuario = personal.objects.get(user = str(request.user.username))    
   
        template = get_template("index2ACTIVIDAD.html")
        diccionario={"init" : activities,"Usuarios":"","letra": usuario.letra, "fondo": usuario.fondo}
        return HttpResponse(template.render(Context(diccionario)))
    e = infor.find('</div>',s)
    parrafo = infor[s:e]
    activities += parrafo + "<br>"
    activities += "<a href=" + act.Url + ">" + "toda la informacion" + "</a> <br>"
                      
        

    usuario = personal.objects.get(user = str(request.user.username))    
   
    template = get_template("index2ACTIVIDAD.html")
    diccionario={"init" : activities,"Usuarios":"","letra": usuario.letra, "fondo": usuario.fondo}
            
    return HttpResponse(template.render(Context(diccionario)))

#####################
#####################
#######AYUDA#########
#####################
#####################
def getHelp(request):
    if personal.objects.filter(user=request.user.username).count()>0 and len(request.user.username)>0:
        usuario = personal.objects.get(user = str(request.user.username))    
       
        template = get_template("index2AYUDA.html")
        diccionario={"init" : "Nada esta vez","Usuarios":"lo que me dieran los usuarios","letra": usuario.letra, "fondo": usuario.fondo}
        return HttpResponse(template.render(Context(diccionario)))
    else:
        template = get_template("index2AYUDA.html")
        diccionario={"init" : "","Usuarios":"","letra": "", "fondo": ""}
        return HttpResponse(template.render(Context(diccionario)))
        
#####################
#####################
#######TODAS#########
#####################
#####################

def getActivities(acts):

    #acts = Activitie.objects.all()
    lt = ""
    for ls in acts:
        redirect="/actividad/"+ls.Identificador
        lt +=ls.name +" "+ ls.price +" "+ ls.date +" "+\
        ls.startHour +" "+ ls.timeToLong + "<br>"


        lt+="<form action='"+redirect+"'method='get'>"
        lt+="<button name='Ident' value=''>+Informacion</button>"
        lt+="</form>"

        lt+="<form action='/tempadd/'method='POST'>"
        lt+="<button name='Identificador' value='"+ ls.Identificador +"'>+A Favoritos</button>"
        lt+="</form>"
	#
    return lt

def filterForm():
    form = "<form action='' method='POST'>\n"
    form += "Filter: <select name='filter method'" 
    form += "<option selected value='name'> Name </option>"
    form += "<option value='name'> Name </option>"
    form += "<option value='startHour'> Hour </option>"
    form += "<option value='date'> Date </option>"
    form += "<option value='price'> Price </option>" 
    form += "</optgroup>" 
    form += "</select>"
    form += "<br>\n"
    form += "<input type='submit' value='enviar'>\n"
    form += "</form>\n"
    return form

def savePagAct(name,Ident):
            print "numero identificador"+str(Ident) 
            act= Activitie.objects.filter(Identificador = str(Ident))
            if elegidas.objects.filter(Identificador = str(Ident)).count()<=0:    
                for acts in range(0,1):
                    print "HEY" 
                    
                    eleg = elegidas( user = name, \
                                Identificador = act[acts].Identificador, \
		                    	name = act[acts].name, \
                                price = act[acts].price, \
                                date = act[acts].date, \
                                startHour = act[acts].startHour, \
                                typ = act[acts].typ,\
                                timeToLong = act[acts].timeToLong, \
                                Long = act[acts].Long, \
                                Url = act[acts].Url)
                    eleg.save()    
@csrf_exempt  
def tempadd(request):
    if request.method == "POST":
        value = request.POST['Identificador']
	print "USUARIO QUE RECIBE LA PAG"+request.user.username
        savePagAct(request.user.username,value)
    return HttpResponseRedirect("/todas/")

@csrf_exempt
def allActivities(request):
    response=""
    if request.method == "POST":
       
        value = request.POST['filter method']
        print value 
        act = Activitie.objects.order_by(value)
        response = filterForm() + getActivities(act)
     
    else:
        act = Activitie.objects.all()
        response = filterForm() + getActivities(act)
    if personal.objects.filter(user=request.user.username).count()>0 and len(request.user.username)>0:
        usuario = personal.objects.get(user = str(request.user.username))
        template = get_template("index2TODAS.html")
        
        diccionario={"init" : response,"fecha":ultima_actualizacion,"letra": usuario.letra, "fondo": usuario.fondo}
        return HttpResponse(template.render(Context(diccionario)))
    else:
        template = get_template("index2TODAS.html")
        diccionario={"init" : response,"fecha":ultima_actualizacion,"letra": "", "fondo": ""}
        return HttpResponse(template.render(Context(diccionario)))


#####################
#####################
#######RSSS##########
#####################
#####################


def getItemsAct(resource):
  
    act = elegidas.objects.filter(user=resource)
    item = ""
    for acts in range(0,elegidas.objects.filter(user=resource).count()):
        item += '\t\t<item>\n'
        item += '\t\t\t<title>'+ act[acts].Identificador + '</title>\n'
        item += '\t\t\t<link>' + "actividad/" + act[acts].Identificador + '</link>\n'
        item += '\t\t\t<pubDate>' +"" + '</pubDate>\n'
        item += '\t\t\t<description>' + act[acts].name + '</description>\n'
        item += '\t\t</item>\n'
    return item

def RSS(request,resource):
    response = '<?xml version="1.0" encoding="UTF-8"?>\n'
    response += '<rss version="2.0">\n'
    response += '\t<channel>\n'
    if resource == None:
        return HttpResponseNotFound('<h1>Resource Not Found</h1>')
    response += '\t\t<title>'+ str(resource) + '</title>\n'
    response += '\t\t<link>'+ "/"+str(resource) + '</link>\n'
    response += '\t\t<description>' + "Contiene las actividades del usuario: "+ str(resource) + '</description>\n'
    response += '\t\t<pubDate>' + "Today" + '</pubDate>\n'
    response += getItemsAct(resource)
    response += '\t</channel>\n</rss>'
    return HttpResponse(response, content_type='rss')





