from django.urls import path
from .views import liste_cours, creer_cours, supprimer_cours, modifier_cours, liste_enseignant, creer_enseignant, \
    modifier_enseignant, supprimer_enseignant, cour_detail, inscription_temporaire, valider_inscription, \
    modifier_user_api, supprimer_user_api, connexion, liste_users_api, contenu_cours, liste_lessons, liste_section, \
    creer_lessons, creer_section, supprimer_lessons, supprimer_section, modifier_lessons, modifier_section

urlpatterns = [
    path("api/cours/", liste_cours, name="api_liste_cours"),
    path("api/creer_cours/", creer_cours, name="api_creer_cours"),
    path("api/modifier/<int:cours_id>/", modifier_cours, name="api_modifier_cours"),
    path("api/supprimer/<int:cours_id>/", supprimer_cours, name="api_supprimer_cours"),
    path('api/cours/<int:cour_id>/', cour_detail, name='cour_detail'),
    path('api/contenu/<int:cours_id>/', contenu_cours, name='cour_contenu'),

    ###lecon et section du cours
    path('api/lessons/', liste_lessons, name='lessons'),
    path('api/section/', liste_section, name='section'),
    path('api/creer_lessons/', creer_lessons, name='creer_lessons'),
    path('api/creer_section/', creer_section, name='creer_section'),
    path('api/lessons/supprimer/<int:lessons_id>', supprimer_lessons, name='supprimer_lessons'),
    path('api/section/supprimer/<int:section_id>', supprimer_section, name='supprimer_section'),
    path('api/lessons/modifier/<int:lessons_id>', modifier_lessons, name='modifier_lessons'),
    path('api/section/modifier/<int:section_id>', modifier_section, name='modifier_section'),
    ## Enseignant
    path("api/enseignants/", liste_enseignant, name="api_liste_enseignant"),
    path('api/creer_enseignant/', creer_enseignant, name='creer_enseignant'),
    path("api/modifier/<int:enseignant_id>/", modifier_enseignant, name="api_modifier_enseignant"),
    path("api/supprimer/<int:enseignant_id>/", supprimer_enseignant, name="api_supprimer_enseignant"),
    ## Utilisateur
    path("api/inscription/", inscription_temporaire, name="inscription"),
    path("api/valider/", valider_inscription, name="valider"),
    path("api/connexion/", connexion, name="connexion"),
    path("api/modifier/<int:user_id>/", modifier_user_api, name="api_modifier_user"),
    path("api/supprimer/<int:user_id>/", supprimer_user_api, name="api_supprimer_user"),
    path("api/utilisateurs/", liste_users_api, name="api_liste_user"),
]