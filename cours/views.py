from django.conf import settings
from django.contrib.auth.hashers import check_password, make_password
from django.core.mail import send_mail
from django.db import IntegrityError
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Cours, Enseignants, User, Section, Lecon
from .serializers import CoursSerializer, EnseignantSerializer, UserSerializer, PaiementSerializer, SectionSerializer, \
    LeconSerializer


@api_view(["GET"])
def liste_cours(request):
    cours = Cours.objects.all()
    serializer = CoursSerializer(cours, many=True)
    return Response(serializer.data)

@api_view(["POST"])
def creer_cours(request):
    serializer = CoursSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "cours créé avec succès !"}, status=201)
    return Response(serializer.errors, status=400)

@api_view(["PUT", "PATCH"])
def modifier_cours(request, cours_id):
    cours = Cours.objects.get(id=cours_id)
    serializer = CoursSerializer(cours, data=request.data, partial=True)
    print("Reçu :", request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    if not serializer.is_valid():
        print("Erreurs serializer :", serializer.errors)
        return Response(serializer.errors, status=400)
    return Response(serializer.errors, status=400)

@api_view(["DELETE"])
def supprimer_cours(request, cours_id):
    cours = Cours .objects.get(id=cours_id)
    cours.delete()
    return Response({"message": "cour supprimé"}, status=204)

@api_view(['GET'])
def cour_detail(request, cour_id):
    try:
        cour = Cours.objects.get(id=cour_id)
        serializer = CoursSerializer(cour)
        return Response(serializer.data)
    except Cours.DoesNotExist:
        return Response({"error": "Cour introuvable."}, status=404)

@api_view(["GET"])
def contenu_cours(request, cours_id):
    sections = Section.objects.filter(id=cours_id).order_by("ordre")
    serializer = SectionSerializer(sections, many=True)
    return Response(serializer.data)

##Lesson
@api_view(["GET"])
def liste_lessons(request):
    lessons = Lecon.objects.all()
    serializer = LeconSerializer(lessons, many=True)
    return Response(serializer.data)
@api_view(["DELETE"])
def supprimer_lessons(request, lessons_id):
    lessons = Lecon .objects.get(id=lessons_id)
    lessons.delete()
    return Response({"message": "lecon supprimé"}, status=204)

@api_view(["PUT", "PATCH"])
def modifier_lessons(request, lessons_id):
    lessons = Lecon.objects.get(id=lessons_id)
    serializer = LeconSerializer(lessons, data=request.data, partial=True)
    print("Reçu :", request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    if not serializer.is_valid():
        print("Erreurs serializer :", serializer.errors)
        return Response(serializer.errors, status=400)
    return Response(serializer.errors, status=400)

@api_view(["POST"])
def creer_lessons(request):
    serializer = LeconSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "lecon créé avec succès !"}, status=201)
    return Response(serializer.errors, status=400)

##Section
@api_view(["GET"])
def liste_section(request):
    section = Section.objects.all()
    serializer = SectionSerializer(section, many=True)
    return Response(serializer.data)
@api_view(["DELETE"])
def supprimer_section(request, section_id):
    section = Section .objects.get(id=section_id)
    section.delete()
    return Response({"message": "section supprimée"}, status=204)

@api_view(["PUT", "PATCH"])
def modifier_section(request, section_id):
    section = Section.objects.get(id=section_id)
    serializer = SectionSerializer(section, data=request.data, partial=True)
    print("Reçu :", request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    if not serializer.is_valid():
        print("Erreurs serializer :", serializer.errors)
        return Response(serializer.errors, status=400)
    return Response(serializer.errors, status=400)

@api_view(["POST"])
def creer_section(request):
    serializer = SectionSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "section créé avec succès !"}, status=201)
    return Response(serializer.errors, status=400)


### Enseignants
@api_view(["GET"])
def liste_enseignant(request):
    enseignant = Enseignants.objects.all()
    serializer = EnseignantSerializer(enseignant, many=True)
    return Response(serializer.data)

@api_view(["POST"])
def creer_enseignant(request):
    serializer = EnseignantSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "enseignant créé avec succès !"}, status=201)
    return Response(serializer.errors, status=400)

@api_view(["PUT", "PATCH"])
def modifier_enseignant(request, enseignant_id):
    enseignant = Enseignants.objects.get(id=enseignant_id)
    serializer = CoursSerializer(enseignant, data=request.data, partial=True)
    print("Reçu :", request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    if not serializer.is_valid():
        print("Erreurs serializer :", serializer.errors)
        return Response(serializer.errors, status=400)
    return Response(serializer.errors, status=400)

@api_view(["DELETE"])
def supprimer_enseignant(request, enseignant_id):
    enseignant = Enseignants .objects.get(id=enseignant_id)
    enseignant.delete()
    return Response({"message": "enseignant supprimé"}, status=204)

####Utilisateurs####
@api_view(["POST"])
def inscription_temporaire(request):
    if request.data.get("role") == "Admin":
        return Response(
            {"error": "Création admin non autorisée ici"},
            status=403
        )
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save(role="Utilisateurs")
        return Response({"id": user.id}, status=201)
    return Response(serializer.errors, status=400)

@api_view(["POST"])
def valider_inscription(request):
    serializer = PaiementSerializer(data=request.data)

    if serializer.is_valid():
        try:
            paiement = serializer.save()
            user = paiement.user
            if user.role == "admin":
                return Response(
                    {"error": "Un admin ne peut pas valider une inscription"},
                    status=403
                )
            cours = user.cours
            send_mail(
                subject="Confirmation d'inscription au cours",
                message=(
                    f"Bonjour {user.nom},\n\n"
                    f"Votre inscription au cours '{cours.titre}' est confirmée.\n"
                    "Merci pour votre confiance !"
                ),
                from_email="campuschrist5@gmail.com",
                recipient_list=[user.email],
                fail_silently=False,
            )

            return Response({"message": "Inscription validée et email envoyé."}, status=201)

        except IntegrityError:
            return Response({"error": "Vous êtes déjà inscrit à ce cours."}, status=400)

    return Response(serializer.errors, status=400)

@api_view(["PUT", "PATCH"])
def modifier_user_api(request, user_id):
    user = User.objects.get(id=user_id)
    serializer = UserSerializer(user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)


@api_view(["DELETE"])
def supprimer_user_api(request, user_id):
    user = User.objects.get(id=user_id)
    user.delete()
    return Response({"message": "Utilisateur supprimé"}, status=204)

@api_view(["POST"])
def connexion(request):
    email = request.data.get("email")
    mot_de_passe = request.data.get("mot_de_passe")

    try:
        user = User.objects.get(email=email)

        # Vérification du mot de passe
        if check_password(mot_de_passe, user.mot_de_passe):
            return Response({
                "message": "Connexion réussie",
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "role": user.role
                }
            }, status=200)
        else:
            return Response({"error": "Mot de passe incorrect"}, status=400)

    except User.DoesNotExist:
        return Response({"error": "Email non trouvé"}, status=400)

@api_view(["GET"])
def liste_users_api(request):
    user = User.objects.all()
    serializer = UserSerializer(user, many=True)
    return Response(serializer.data)