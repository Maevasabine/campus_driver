from rest_framework import serializers
from .models import Cours, Enseignants, User, Paiement, Section,Lecon


class EnseignantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enseignants
        fields = ['id', 'nom', 'email', 'mot_de_passe', 'date_inscription']

class CoursSerializer(serializers.ModelSerializer):
    enseignant_nom = serializers.CharField(source='enseignant.nom', read_only=True)
    class Meta:
        model = Cours
        fields = ['id', 'enseignant','titre','montant','description', 'image', 'enseignant_nom']


class LeconSerializer(serializers.ModelSerializer):
    class Meta:
        model=Lecon
        fields=['id','section','titre','video','is_preview','ordre']

class SectionSerializer(serializers.ModelSerializer):
    cours_nom=serializers.CharField(source='cours.nom', read_only=True)
    lecons = LeconSerializer(many=True, read_only=True)
    class Meta:
        model=Section
        fields=['id','cours','cours_nom','titre','ordre','lecons']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'cours', 'nom', 'email', 'telephone', 'statut', 'date_inscription']
        read_only_fields = ['id', 'statut', 'date_inscription']

    def create(self, validated_data):
        validated_data["statut"] = "en_attente"
        return super().create(validated_data)

class PaiementSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(write_only=True)
    class Meta:
        model = Paiement
        fields = ["id", "user_id", "transaction_id", "montant", "statut", "date"]
        read_only_fields = ["id", "date", "statut", "montant"]

    def create(self, validated_data):
        user_id = validated_data.pop("user_id")
        user = User.objects.get(id=user_id)
        montant = user.cours.montant
        paiement = Paiement.objects.create(
            user=user,
            transaction_id=validated_data["transaction_id"],
            montant=montant,
            statut="réussi",
        )
        user.statut = "valide"
        user.save()

        return paiement

