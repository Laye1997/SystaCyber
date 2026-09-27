"""Génération des PDF de séance (rapport client et attestations)."""

from io import BytesIO
from pathlib import Path

from django.conf import settings
from django.http import HttpResponse
from django.utils.html import escape
from reportlab.lib.colors import HexColor, white
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import Image, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from .services import actions_recommandees, etat_seance, suivi_activite

BLEU = HexColor("#0c5ff7")
NAVY = HexColor("#0e1a2b")
MUTED = HexColor("#5b6b83")
ROUGE = HexColor("#e24b4b")
VERT = HexColor("#12b76a")
FOND = HexColor("#f4f7fb")


def _styles():
    return {
        "titre": ParagraphStyle("t", fontName="Helvetica-Bold", fontSize=18, textColor=NAVY, spaceAfter=6, leading=22),
        "sous": ParagraphStyle("s", fontName="Helvetica", fontSize=10, textColor=MUTED, spaceAfter=10, leading=14),
        "h": ParagraphStyle("h", fontName="Helvetica-Bold", fontSize=12, textColor=BLEU, spaceBefore=12, spaceAfter=6),
        "p": ParagraphStyle("p", fontName="Helvetica", fontSize=10, textColor=NAVY, leading=14, spaceAfter=6),
        "centre": ParagraphStyle("c", fontName="Helvetica", fontSize=11, textColor=NAVY, alignment=TA_CENTER, leading=16),
        "att_titre": ParagraphStyle("at", fontName="Helvetica-Bold", fontSize=22, textColor=NAVY, alignment=TA_CENTER, spaceAfter=8, leading=26),
        "petit": ParagraphStyle("pt", fontName="Helvetica", fontSize=8, textColor=MUTED, alignment=TA_RIGHT),
        "kpi": ParagraphStyle("k", fontName="Helvetica-Bold", fontSize=16, textColor=BLEU, alignment=TA_CENTER),
        "kpi_l": ParagraphStyle("kl", fontName="Helvetica", fontSize=8, textColor=MUTED, alignment=TA_CENTER, leading=11),
    }


def _logo():
    for nom in ("logo-systalink.png", "logo.png"):
        chemin = Path(settings.BASE_DIR) / "static" / "systalink" / nom
        if chemin.exists():
            img = Image(str(chemin), width=42 * mm, height=12.5 * mm)
            img.hAlign = "LEFT"
            return img
    return None


def _entete(story, st, titre, seance):
    logo = _logo()
    if logo:
        story.append(logo)
        story.append(Spacer(1, 4 * mm))
    story.append(Paragraph(titre, st["titre"]))
    story.append(
        Paragraph(
            f"{seance.organisation} · {seance.date:%d/%m/%Y}"
            f"{' · ' + seance.groupe if seance.groupe else ''} · {seance.formateur}",
            st["sous"],
        )
    )


def _pct(val):
    return f"{val} %" if val is not None else "—"


def recommandations(etat):
    return actions_recommandees(etat)


def rapport_pdf(seance):
    etat = etat_seance(seance)
    suivi = suivi_activite(seance)
    effectif = seance.presents or len(suivi)
    st = _styles()
    buf = BytesIO()
    doc = SimpleDocTemplate(
        buf,
        pagesize=A4,
        leftMargin=18 * mm,
        rightMargin=18 * mm,
        topMargin=16 * mm,
        bottomMargin=16 * mm,
        title=f"Rapport — {seance}",
        author="Systalink",
    )
    story = []
    _entete(story, st, "Rapport de séance — CyberSécurité", seance)
    story.append(
        Paragraph(
            "Baseline, simulation d'emails, mesure. Les scores sont agrégés, sans nom sur les réponses.",
            st["p"],
        )
    )

    kpis = [
        [
            Paragraph(str(effectif), st["kpi"]),
            Paragraph(_pct(etat["entree"]["score_pct"]), st["kpi"]),
            Paragraph(_pct(etat["sortie"]["score_pct"]), st["kpi"]),
            Paragraph(_pct(etat["phish"]["phish_prone_pct"]), st["kpi"]),
            Paragraph(
                f"{etat['delta_connaissance']:+} pts" if etat["delta_connaissance"] is not None else "—",
                st["kpi"],
            ),
        ],
        [
            Paragraph(f"Participants<br/>({seance.participants_prevus} prévus)", st["kpi_l"]),
            Paragraph(f"Connaissances<br/>entrée ({etat['entree']['n']})", st["kpi_l"]),
            Paragraph(f"Connaissances<br/>sortie ({etat['sortie']['n']})", st["kpi_l"]),
            Paragraph(f"Taux d'exposition<br/>({etat['phish']['n']} pers.)", st["kpi_l"]),
            Paragraph("Progression<br/>entrée → sortie", st["kpi_l"]),
        ],
    ]
    t = Table(kpis, colWidths=[32 * mm] * 5)
    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), FOND),
                ("BOX", (0, 0), (-1, -1), 0.4, BLEU),
                ("INNERGRID", (0, 0), (-1, -1), 0.2, HexColor("#d5deec")),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ]
        )
    )
    story.append(t)
    story.append(Paragraph("Benchmark KnowBe4 2026", st["h"]))
    story.append(
        Paragraph(
            f"Premier test sans formation : <b>{etat['benchmark_monde']} %</b> dans le monde, "
            f"<b>{etat['benchmark_afrique']} %</b> en Afrique. Après 12 mois d'exercices : "
            f"<b>{etat['benchmark_cible']} %</b>.",
            st["p"],
        )
    )
    if etat["phish"]["taux_echec_emails"] is not None:
        story.append(
            Paragraph(
                f"Échecs sur emails piégés : {etat['phish']['taux_echec_emails']} % · "
                f"{etat['phish']['echecs']} personne(s) exposée(s).",
                st["p"],
            )
        )
    story.append(Paragraph("Trois actions à emporter", st["h"]))
    for i, ligne in enumerate(recommandations(etat), start=1):
        story.append(Paragraph(f"<b>{i}.</b> {seance.personnaliser(ligne)}", st["p"]))

    presents = [p for p in suivi if p["nom"] and p["nom"] != "Anonyme"]
    story.append(Paragraph("Présences déclarées", st["h"]))
    if presents:
        lignes = [[Paragraph("<b>Nom</b>", st["p"]), Paragraph("<b>Service</b>", st["p"])]]
        for p in presents:
            lignes.append([Paragraph(escape(p["nom"]), st["p"]), Paragraph(escape(p["service"]) or "—", st["p"])])
        tab = Table(lignes, colWidths=[90 * mm, 80 * mm])
        tab.setStyle(TableStyle([("LINEBELOW", (0, 0), (-1, -1), 0.2, HexColor("#d5deec"))]))
        story.append(tab)
    else:
        story.append(Paragraph("Aucun nom saisi à l'entrée (participation anonyme).", st["p"]))

    story.append(Spacer(1, 8 * mm))
    story.append(Paragraph("Systalink · www.systalink.com · Document destiné au client de la séance.", st["sous"]))
    doc.build(story)
    pdf = buf.getvalue()
    resp = HttpResponse(pdf, content_type="application/pdf")
    resp["Content-Disposition"] = f'attachment; filename="rapport-{seance.code}.pdf"'
    return resp


def attestations_pdf(seance):
    st = _styles()
    buf = BytesIO()
    doc = SimpleDocTemplate(
        buf,
        pagesize=A4,
        leftMargin=22 * mm,
        rightMargin=22 * mm,
        topMargin=28 * mm,
        bottomMargin=22 * mm,
        title=f"Attestations — {seance}",
        author="Systalink",
    )
    suivis = [p for p in suivi_activite(seance) if p["nom"] and p["nom"] != "Anonyme"]
    if not suivis:
        suivis = [{"nom": "Participant (anonyme)", "service": ""}]

    story = []
    for i, p in enumerate(suivis):
        if i:
            from reportlab.platypus import PageBreak

            story.append(PageBreak())
        logo = _logo()
        if logo:
            logo.hAlign = "CENTER"
            story.append(logo)
            story.append(Spacer(1, 10 * mm))
        story.append(Paragraph("Attestation de participation", st["att_titre"]))
        story.append(Paragraph("Sensibilisation à la cybersécurité", st["centre"]))
        story.append(Spacer(1, 12 * mm))
        story.append(
            Paragraph(
                f"Nous attestons que <b>{escape(p['nom'])}</b>"
                + (f" ({escape(p['service'])})" if p["service"] else "")
                + " a suivi la séance de sensibilisation organisée par Systalink.",
                st["centre"],
            )
        )
        story.append(Spacer(1, 8 * mm))
        story.append(
            Paragraph(
                f"<b>{seance.organisation}</b><br/>{seance.date:%d/%m/%Y}"
                f"{' · ' + seance.groupe if seance.groupe else ''}<br/>Formateur : {seance.formateur}",
                st["centre"],
            )
        )
        story.append(Spacer(1, 16 * mm))
        story.append(
            Paragraph(
                "Cette attestation ne constitue pas une certification de compétence. "
                "Elle confirme la présence à la session interactive (quiz, simulation, échanges).",
                st["centre"],
            )
        )
        story.append(Spacer(1, 20 * mm))
        story.append(Paragraph("Systalink · Votre moteur d'innovation numérique · www.systalink.com", st["centre"]))
        story.append(Paragraph(f"Réf. séance {seance.code}", st["sous"]))

    doc.build(story)
    pdf = buf.getvalue()
    resp = HttpResponse(pdf, content_type="application/pdf")
    resp["Content-Disposition"] = f'attachment; filename="attestations-{seance.code}.pdf"'
    return resp
