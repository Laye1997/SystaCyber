"""Logique des campagnes de simulation de phishing.

Garde-fous :
- Une campagne ne s'envoie qu'avec une autorisation renseignée.
- Le lien de chaque email est unique et sert à mesurer le clic.
- La fausse page n'enregistre jamais les identifiants tapés (voir vues).
"""

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.urls import reverse
from django.utils import timezone
from django.utils.html import escape


class CampagneNonAutorisee(Exception):
    pass


def _base_url(request=None):
    if settings.CAMPAGNE_BASE_URL:
        return settings.CAMPAGNE_BASE_URL.rstrip("/")
    if request is not None:
        return f"{request.scheme}://{request.get_host()}"
    return "http://127.0.0.1:8001"


def lien_piege(destinataire, request=None):
    return _base_url(request) + reverse("campagne_clic", args=[destinataire.jeton])


def pixel_ouverture(destinataire, request=None):
    return _base_url(request) + reverse("campagne_pixel", args=[destinataire.jeton])


def corps_html(campagne, destinataire, request=None):
    """Rend l'email : texte du modèle, lien piégé, pixel d'ouverture."""
    modele = campagne.modele
    texte = campagne.personnaliser(modele.corps, destinataire)
    paragraphes = "".join(f"<p>{escape(l)}</p>" for l in texte.splitlines() if l.strip())
    lien = lien_piege(destinataire, request)
    libelle = campagne.personnaliser(modele.url_affichee, destinataire) or lien
    bouton = (
        f'<p><a href="{lien}" '
        'style="display:inline-block;padding:10px 18px;background:#0c5ff7;color:#fff;'
        'border-radius:6px;text-decoration:none">{}</a></p>'.format(escape(libelle))
    )
    pixel = f'<img src="{pixel_ouverture(destinataire, request)}" width="1" height="1" alt="" style="display:none">'
    return f'<div style="font-family:Arial,sans-serif;font-size:15px;color:#1a2433">{paragraphes}{bouton}{pixel}</div>'


def envoyer_campagne(campagne, request=None):
    """Envoie la campagne à tous ses destinataires non encore contactés.

    Lève CampagneNonAutorisee si l'autorisation n'est pas renseignée.
    Retourne le nombre d'emails envoyés.
    """
    if not campagne.autorisee:
        raise CampagneNonAutorisee(
            "Renseignez « Autorisée par » et la date d'autorisation avant tout envoi."
        )
    modele = campagne.modele
    expediteur = campagne.expediteur_affiche or (
        f"{modele.expediteur_nom} <{campagne.personnaliser(modele.expediteur_adresse)}>"
    )
    envoyes = 0
    for dest in campagne.destinataires.filter(envoye_le=None):
        sujet = campagne.personnaliser(modele.objet, dest)
        html = corps_html(campagne, dest, request)
        texte_brut = campagne.personnaliser(modele.corps, dest) + "\n\n" + lien_piege(dest, request)
        msg = EmailMultiAlternatives(sujet, texte_brut, expediteur, [dest.email])
        msg.attach_alternative(html, "text/html")
        msg.send(fail_silently=False)
        dest.envoye_le = timezone.now()
        dest.save(update_fields=["envoye_le"])
        envoyes += 1
    if envoyes and campagne.statut in ("brouillon", "prete"):
        campagne.statut = "lancee"
        campagne.lance_le = timezone.now()
        campagne.save(update_fields=["statut", "lance_le"])
    return envoyes
