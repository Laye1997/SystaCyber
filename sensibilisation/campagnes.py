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
    """Rend l'email HTML envoyé au destinataire.

    Deux modes selon le corps du modèle :
    - Si le corps contient le repère {lien}, il est traité comme du **HTML
      personnalisé** (images, boutons, faux calendrier/PDF…) et {lien} est
      remplacé par le lien piégé là où le formateur l'a placé.
    - Sinon, comportement simple : le texte est échappé en paragraphes et un
      bouton cliquable est ajouté automatiquement.
    Dans les deux cas, un pixel invisible mesure l'ouverture.
    """
    modele = campagne.modele
    lien = lien_piege(destinataire, request)
    texte = campagne.personnaliser(modele.corps, destinataire)
    pixel = f'<img src="{pixel_ouverture(destinataire, request)}" width="1" height="1" alt="" style="display:none">'
    enveloppe = 'font-family:Arial,sans-serif;font-size:15px;color:#1a2433;line-height:1.5'

    if "{lien}" in texte:
        # HTML personnalisé rédigé par le formateur (contenu de confiance).
        corps = texte.replace("{lien}", lien)
        return f'<div style="{enveloppe}">{corps}{pixel}</div>'

    # Mode simple : texte échappé + bouton automatique.
    paragraphes = "".join(f"<p>{escape(l)}</p>" for l in texte.splitlines() if l.strip())
    libelle = campagne.personnaliser(modele.url_affichee, destinataire) or lien
    bouton = (
        f'<p><a href="{lien}" '
        'style="display:inline-block;padding:10px 18px;background:#0c5ff7;color:#fff;'
        'border-radius:6px;text-decoration:none">{}</a></p>'.format(escape(libelle))
    )
    return f'<div style="{enveloppe}">{paragraphes}{bouton}{pixel}</div>'


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
    envoyes, echecs, derniere_erreur = 0, 0, None
    for dest in campagne.destinataires.filter(envoye_le=None):
        sujet = campagne.personnaliser(modele.objet, dest)
        html = corps_html(campagne, dest, request)
        lien_dest = lien_piege(dest, request)
        corps_perso = campagne.personnaliser(modele.corps, dest)
        if "{lien}" in corps_perso:
            texte_brut = corps_perso.replace("{lien}", lien_dest)
        else:
            texte_brut = corps_perso + "\n\n" + lien_dest
        msg = EmailMultiAlternatives(sujet, texte_brut, expediteur, [dest.email])
        msg.attach_alternative(html, "text/html")
        try:
            msg.send(fail_silently=False)
        except Exception as e:  # une adresse invalide ne doit pas bloquer les autres
            echecs += 1
            derniere_erreur = e
            continue
        dest.envoye_le = timezone.now()
        dest.save(update_fields=["envoye_le"])
        envoyes += 1
    if envoyes and campagne.statut in ("brouillon", "prete"):
        campagne.statut = "lancee"
        campagne.lance_le = timezone.now()
        campagne.save(update_fields=["statut", "lance_le"])
    # Si rien n'est parti et qu'il y a eu une erreur, on la remonte pour l'afficher.
    if envoyes == 0 and derniere_erreur is not None:
        raise derniere_erreur
    return {"envoyes": envoyes, "echecs": echecs}
    return envoyes
