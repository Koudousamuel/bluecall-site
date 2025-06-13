from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.core.mail import send_mail
from django.http import HttpResponse
import random
from django.contrib.auth.models import User
from .forms import PasswordResetRequestForm
from .forms import NouveauMotDePasseForm




def login_user(request):
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username = username, password = password)

        if user is not None:
            login(request, user)
            return redirect ("green:index")
        else:
            messages.info(request, "Identifiant ou mot de passe incorrect")

    form = AuthenticationForm()
    return render(request, "accounts/connexion.html", {"form": form})

def logout_user(request):
    logout(request)
    return redirect ("green:home")



def envoyer_email(email):

    code = str(random.randint(100000, 999999))

    try:
        send_mail(
            subject='Votre code de vérification',
            message=f'Voici votre code de vérification : {code}',
            from_email='koudouclaudesamuel17@gmail.com',
            recipient_list=[email],
            fail_silently=False,
        )
    except Exception as e:
        print(f"Erreur d'envoi de mail vers {email} : {e}")

    return code


def register_user(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()  # Enregistre l'utilisateur
            email = user.email  # Récupère l'email de l'utilisateur
            
            # Envoie un e-mail avec un code de vérification
            verification_code = envoyer_email(email)

            # Enregistrer le code de vérification en session (ou en base de données si tu préfères)
            request.session['verification_code'] = verification_code
            request.session['email_to_verify'] = email
            
            return redirect("accounts:verify_email")  # Redirige vers la page de vérification
        else:
            # Si le formulaire n'est pas valide, afficher les erreurs
            messages.error(request, "L'email est déjà utilisé ou le formulaire contient des erreurs.")
    else:
        form = CustomUserCreationForm()

    return render(request, "accounts/register.html", {"form": form})


def verify_email(request):
    if request.method == 'POST':
        entered_code = request.POST.get('code')
        real_code = request.session.get('verification_code')
        email = request.session.get('email_to_verify')  # 🔥 Tu dois récupérer l'email ici

        if entered_code == real_code:
            # Code correct → L'utilisateur est vérifié
            user = User.objects.get(email=email)
            login(request, user)  # ✅ Connecte l'utilisateur
            # Nettoyage de la session
            del request.session['verification_code']
            del request.session['email_to_verify']
            return redirect("green:index")
        else:
            return render(request, "accounts/verify_email.html", {"error": "Code incorrect."})

    return render(request, "accounts/verify_email.html")



def demander_reinitialisation(request):
    if request.method == "POST":
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            nom = form.cleaned_data["last_name"]
            email = form.cleaned_data["email"]
            # Filtrer les utilisateurs avec le nom et l'email
            users = User.objects.filter(last_name=nom, email=email)

            if users.exists():
                # Générer un code de réinitialisation
                code = str(random.randint(100000, 999999))
                request.session["reset_code"] = code  # Stocker le code dans la session
                request.session["reset_email"] = email  # Stocker l'email dans la session

                # Envoyer l'email avec le code
                send_mail(
                    "Code de réinitialisation de mot de passe",
                    f"Voici votre code de réinitialisation : {code}",
                    "ton.email@gmail.com",  # Remplace avec ton email configuré dans les paramètres
                    [email],
                    fail_silently=False,
                )
                # Rediriger vers la page de saisie du code
                return redirect("accounts:verify_reset_code")
            else:
                messages.error(request, "Aucun utilisateur trouvé avec ces informations.")
        else:
            messages.error(request, "Formulaire invalide. Veuillez vérifier vos informations.")
    else:
        form = PasswordResetRequestForm()

    return render(request, "accounts/reset_request.html", {"form": form})



def verifier_code_reset(request):
    if request.method == "POST":
        code_saisi = request.POST.get("code")
        code_attendu = request.session.get("reset_code")

        if code_saisi == code_attendu:
            request.session["code_verifie"] = True  # Marquer que le code est validé
            return redirect("accounts:set_new_password")
        else:
            messages.error(request, "Code incorrect.")
    return render(request, "accounts/verifier_code.html")

def nouveau_mot_de_passe(request):
    if not request.session.get("code_verifie"):
        return redirect("accounts:password_reset_request")

    if request.method == "POST":
        password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")
        email = request.session.get("reset_email")

        if password != confirm_password:
            messages.error(request, "Les mots de passe ne correspondent pas.")
        else:
            try:
                user = User.objects.get(email=email)
                user.set_password(password)
                user.save()

                # Nettoyer la session
                request.session.flush()

                messages.success(request, "Votre mot de passe a été mis à jour avec succès.")
                return redirect("accounts:login")
            except User.DoesNotExist:
                messages.error(request, "Utilisateur introuvable.")
    
    return render(request, "accounts/set_new_password.html")