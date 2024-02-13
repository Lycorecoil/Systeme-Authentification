
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from Authentification import settings
from django.core.mail import send_mail
# Create your views here.

def home(request):
	return render(request,"app/index.html")





def register(request):
    # enregistrement des infos récupérées sur le formulaire par la request POST
    if request.method == "POST":
        username = request.POST['username']
        name = request.POST['name']
        lastname = request.POST['lastname']
        email = request.POST['email']
        password = request.POST['password']
        password1 = request.POST['password1']

        if User.objects.filter(username=username):
             messages.error(request,"Ce nom d'utilisateur est deja prix")
             return redirect('register')
        
        if User.objects.filter(email=email):
             messages.error(request,"Ce email est deja connecter a un compte")
             return redirect('register')
        
        if not username.isalnum():
             messages.error(request,"Le nom doit etre alphanum")
             return redirect('register')
                
        if password != password1:
             messages.error(request,"Verifier les mot de pass")
             return redirect('register')
        

        # Enregistrement de l'utilisateur dans my_user
        my_user = User.objects.create_user(username=username, email=email, password=password)
        my_user.first_name = name
        my_user.last_name = lastname
        my_user.save()
        messages.success(request, 'Compte créé avec succès')
        sujet = "Activation de compte"
        message = "Bienvenu " + my_user.first_name + " " + my_user.last_name + " Heureux de vous copter parmis nous.\n lien d'activation(jvais faire plus tard woo)"
        from_email = settings.EMAIL_HOST_USER
        To_liste = [my_user.email]
        send_mail(sujet,message,from_email,To_liste,fail_silently=False)
        return redirect('login')

    return render(request, "app/register.html")


    


def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            firstname = user.first_name
            return render(request, "app/index.html", {'firstname': firstname})
        else:
            # Ajoutez un message d'erreur si l'authentification échoue
            messages.error(request, 'Nom d\'utilisateur ou mot de passe incorrect.')
            return redirect('login')
    
    return render(request, "app/login.html")



def logout_view(request):
    logout(request)
    messages.success(request, 'Déconnecté')
    return redirect("home")
