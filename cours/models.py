from django.contrib.auth.hashers import make_password
from django.db import models

class Enseignants(models.Model):
    id = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    mot_de_passe = models.CharField(max_length=128)
    date_inscription = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nom


class Cours(models.Model):
    id = models.AutoField(primary_key=True)
    titre = models.CharField(max_length=100)
    montant = models.DecimalField(max_digits=10, decimal_places=2,default=20.50)
    description = models.TextField()
    image = models.ImageField(upload_to="cours_images/", null=True, blank=True)
    enseignant = models.ForeignKey(Enseignants, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.titre

class User(models.Model):
    id = models.AutoField(primary_key=True)
    cours = models.ForeignKey(Cours, on_delete=models.CASCADE, related_name="inscriptions")
    nom = models.CharField(max_length=150)
    email = models.EmailField()
    telephone = models.CharField(max_length=20)
    mot_de_passe = models.CharField(max_length=128, default=make_password("defaultpassword"))
    statut = models.CharField(max_length=20, default="en_attente")
    date_inscription = models.DateTimeField(auto_now_add=True)
    role = models.CharField(
        max_length=15,
        choices=[("Utilisateurs", "Utilisateurs"), ("Admin", "Admin")],
        default="Utilisateurs"
    )
    class Meta:
        unique_together = ('cours', 'email')

    def __str__(self):
        return f"{self.nom} - {self.cours.titre}"

    def set_password(self, raw_password):
        self.mot_de_passe = make_password(raw_password)

class Paiement(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    transaction_id = models.CharField(max_length=255)
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    statut = models.CharField(max_length=20, default="réussi")
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Paiement {self.transaction_id}"


class Section(models.Model):
    id = models.AutoField(primary_key=True)
    cours = models.ForeignKey(Cours, on_delete=models.CASCADE, related_name="sections")
    titre = models.CharField(max_length=255)
    ordre = models.IntegerField(default=0)

class Lecon(models.Model):
    id = models.AutoField(primary_key=True)
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name="lecons")
    titre = models.CharField(max_length=255)
    video = models.FileField(upload_to="videos/")
    is_preview = models.BooleanField(default=False)
    ordre = models.IntegerField(default=0)