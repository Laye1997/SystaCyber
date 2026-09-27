"""Pack pédagogique générique sur deux jours — logique KnowBe4 (baseline, simulation, mesure)."""

MODULES = [
    # ================================================================ JOUR 1
    {
        "titre": "Jour 1 · Ouverture",
        "horaire": "J1 8h30",
        "duree": 30,
        "slides": [
            {
                "type": "titre",
                "surtitre": "{entreprise} · Programme de sensibilisation",
                "titre": "La cybersécurité, c'est l'affaire de tous",
                "corps": "<p>Reconnaître les pièges, protéger l'organisation, réagir vite.</p><p class='meta'>Animé par {formateur} · Systalink · {date}</p>",
                "notes": "Se présenter. Rappeler que la formation dure deux jours, qu'elle est interactive et sans jugement.",
            },
            {
                "type": "contenu",
                "surtitre": "Objectifs",
                "titre": "À la fin des deux jours, vous saurez",
                "corps": """<div class="grid4">
<article><h3>Repérer un piège</h3><p>Email, appel, SMS ou WhatsApp suspect.</p></article>
<article><h3>Vérifier sans gêne</h3><p>Confirmer une demande par le bon canal.</p></article>
<article><h3>Protéger vos accès</h3><p>Mots de passe, poste, données.</p></article>
<article><h3>Réagir vite</h3><p>Quoi faire, et qui prévenir, en cas d'erreur.</p></article>
</div>
<p class="callout">Et comprendre pourquoi ces réflexes sont exigés : les normes ISO 27001 et le cadre légal sénégalais.</p>""",
                "notes": "Présenter les 4 objectifs. Cas concrets du quotidien de {secteur}.",
            },
            {
                "type": "contenu",
                "surtitre": "Cadre",
                "titre": "Les règles du jeu",
                "corps": "<ul class='big'><li>Aucune question n'est bête</li><li>Personne n'est jugé : on apprend de ses erreurs</li><li>Ce qui est dit ici ne remonte pas nominativement</li><li>Téléphones en silencieux, sauf pour les quiz</li><li>On partage ses expériences : elles valent tous les exemples</li></ul>",
                "notes": "Insister sur le sans jugement.",
            },
            {
                "type": "contenu",
                "surtitre": "Deux jours",
                "titre": "Le programme",
                "corps": """<div class="split">
<div><h3>Jour 1 · Reconnaître les attaques</h3><table class="prog"><tbody>
<tr><th>8h30</th><td>Accueil et quiz d'entrée</td></tr>
<tr><th>9h00</th><td>1. Pourquoi {entreprise} est une cible</td></tr>
<tr><th>9h45</th><td>2. Emails piégés et simulation</td></tr>
<tr><th>14h00</th><td>3. Téléphone, SMS, WhatsApp</td></tr>
<tr><th>15h30</th><td>4. Mots de passe et MFA</td></tr>
<tr><th>16h30</th><td>Bilan du jour</td></tr>
</tbody></table></div>
<div><h3>Jour 2 · Protéger et réagir</h3><table class="prog"><tbody>
<tr><th>8h30</th><td>Rappel en quiz live</td></tr>
<tr><th>9h00</th><td>5. Poste de travail</td></tr>
<tr><th>10h00</th><td>6. Données et confidentialité</td></tr>
<tr><th>11h15</th><td>7. Les normes ISO</td></tr>
<tr><th>14h00</th><td>8. Incident : les bons réflexes</td></tr>
<tr><th>15h30</th><td>Quiz de sortie et évaluation</td></tr>
</tbody></table></div>
</div>""",
                "notes": "Pauses : 10h45 et 15h15. Déjeuner 12h30 – 14h00. Lancer ensuite le quiz d'entrée.",
            },
            {
                "type": "quiz",
                "surtitre": "Baseline KnowBe4",
                "titre": "Où en êtes-vous ?",
                "corps": "<p>10 questions, anonymes. Répondez sans chercher : c'est votre point de départ, comme un premier test de phishing.</p><p class='code-hint'>Sur téléphone : rejoindre avec le code de séance</p>",
                "notes": "Ouvrir le quiz d'entrée. Ne pas donner les réponses : on les verra demain après le quiz de sortie.",
                "quiz_moment": "entree",
            },
        ],
    },
    {
        "numero": "Module 1",
        "titre": "Pourquoi vous êtes une cible",
        "horaire": "J1 9h00",
        "duree": 45,
        "slides": [
            {
                "type": "section",
                "surtitre": "Jour 1 · Module 1 · 9h00",
                "titre": "Pourquoi {entreprise} est une cible",
                "corps": "",
                "notes": "Les attaquants s'intéressent à l'organisation et à chacun.",
            },
            {
                "type": "chiffre",
                "surtitre": "Sans formation",
                "titre": "1 sur 3",
                "corps": "<p>des employés clique sur un faux email lors d'un premier test : <strong>33,2&nbsp;% dans le monde, 35,9&nbsp;% en Afrique</strong>.</p><p>Après 12 mois de formation et d'exercices : <strong>4,2&nbsp;%</strong>.</p><p class='source'>Source : KnowBe4, Phishing by Industry Benchmarking Report 2026</p>",
                "notes": "Ce n'est pas l'intelligence, c'est l'entraînement. C'est la logique de cette application.",
            },
            {
                "type": "contenu",
                "surtitre": "Enjeux",
                "titre": "Trois raisons d'être visé",
                "corps": """<div class="grid3">
<article><h3>La valeur</h3><p>Argent, accès, contrats : le gain est direct pour le fraudeur.</p></article>
<article><h3>Les données</h3><p>Identités, dossiers, pièces : elles se revendent ou servent à d'autres arnaques.</p></article>
<article><h3>Vous</h3><p>Plus simple de tromper une personne que de forcer un système.</p></article>
</div>""",
                "notes": "Demander qui a déjà reçu un SMS ou un appel suspect ce mois-ci.",
            },
            {
                "type": "contenu",
                "surtitre": "Chaîne d'attaque",
                "titre": "Comment se déroule une attaque",
                "corps": """<ol class="chain">
<li><strong>Repérage</strong> — LinkedIn, site web, organigramme.</li>
<li><strong>Contact</strong> — Un email, un appel ou un message crédible.</li>
<li><strong>Piège</strong> — Un clic, un mot de passe, un code ou un virement.</li>
<li><strong>Exploitation</strong> — Accès aux systèmes et aux données.</li>
</ol>
<p class="callout">Vous pouvez casser la chaîne à l'étape 2 ou 3.</p>""",
                "notes": "Les outils bloquent beaucoup ; ce qui passe compte sur l'humain.",
            },
        ],
    },
    {
        "numero": "Module 2",
        "titre": "Reconnaître un email piégé",
        "horaire": "J1 9h45",
        "duree": 165,
        "slides": [
            {
                "type": "section",
                "surtitre": "Jour 1 · Module 2 · 9h45",
                "titre": "Reconnaître un email piégé",
                "corps": "<p>9 attaques sur 10 commencent par un email. Ici, on simule comme KnowBe4 : vous classez, on mesure le taux d'exposition.</p>",
                "notes": "Module le plus important. Passer la vidéo (1 min) : une définition, un réflexe.",
                "video_youtube": "FOA8qcDE50o",
            },
            {
                "type": "contenu",
                "surtitre": "Méthode",
                "titre": "Les 5 signes d'un email suspect",
                "corps": "<ol class='big'><li>L'urgence : « avant 11h », « dernier rappel », « compte bloqué »</li><li>L'expéditeur : adresse qui ne correspond pas au nom affiché</li><li>Le lien : au survol, l'adresse réelle mène ailleurs</li><li>La demande : mot de passe, code, virement, changement de RIB</li><li>Le ton inhabituel : un DG qui tutoie, une faute, un contexte étrange</li></ol>",
                "notes": "Montrer comment survoler un lien sans cliquer.",
            },
            {
                "type": "contenu",
                "surtitre": "Exemple fictif",
                "titre": "Anatomie d'un email piégé",
                "corps": """<div class="mail-preview">
<p class="from">De : Service Informatique &lt;support@{domaine}-securite.com&gt;</p>
<p class="subj">Objet : Action requise : votre mot de passe expire aujourd'hui</p>
<p>Bonjour, votre mot de passe expire dans 2 heures. Pour éviter le blocage, cliquez ici pour le renouveler.</p>
</div>
<ul class="flags"><li>Domaine externe : pas @{domaine}</li><li>Urgence : 2 heures</li><li>Menace : blocage</li><li>Demande : saisir son mot de passe</li></ul>""",
                "notes": "La DSI ne demande jamais de saisir son mot de passe via un lien.",
            },
            {
                "type": "contenu",
                "surtitre": "Démo",
                "titre": "Vérifier avant de cliquer",
                "corps": """<div class="grid3">
<article><h3>Survoler le lien</h3><p>L'adresse réelle s'affiche en bas de l'écran.</p></article>
<article><h3>Voir l'expéditeur</h3><p>Cliquer sur le nom affiché pour lire l'adresse complète.</p></article>
<article><h3>Lire le domaine</h3><p>Ce qui compte est juste avant le premier « / ».</p></article>
</div>""",
                "notes": "Démo Outlook + appui long sur téléphone. Pause 10h45.",
            },
            {
                "type": "atelier",
                "surtitre": "Simulation · 45 minutes",
                "titre": "Signaler ou légitime ?",
                "corps": "<p>Même logique qu'une campagne KnowBe4. Pour chaque email, signalez s'il est piégé, ou validez s'il est légitime.</p><p>Classer un piège comme légitime, ou cliquer son lien = un « clic » dans le taux d'exposition.</p>",
                "notes": "Ouvrir la simulation. Corriger ensuite collectivement.",
            },
            {
                "type": "contenu",
                "surtitre": "Correction",
                "titre": "Verdict de la simulation",
                "corps": """<table class="prog"><thead><tr><th>#</th><th>Verdict</th><th>Indice</th></tr></thead><tbody>
<tr><td>1</td><td class="bad">Piégé</td><td>Domaine externe, urgence, mot de passe</td></tr>
<tr><td>2</td><td class="ok">Légitime</td><td>Domaine interne, intranet</td></tr>
<tr><td>3</td><td class="bad">Piégé</td><td>Gmail, secret, fraude au président</td></tr>
<tr><td>4</td><td class="bad">Piégé</td><td>Changement de RIB par email</td></tr>
<tr><td>5</td><td class="ok">Légitime</td><td>Information, aucune action</td></tr>
<tr><td>6</td><td class="bad">Piégé</td><td>Inconnu, lien de connexion</td></tr>
<tr><td>7</td><td class="bad">Piégé</td><td>Colis, petits frais, 24 h</td></tr>
<tr><td>8</td><td class="ok">Légitime</td><td>Domaine interne, cohérent</td></tr>
</tbody></table>""",
                "notes": "Correction du pack par défaut. Si vous avez choisi d'autres modèles pour la séance, corriger depuis l'écran Scores. L'email 3 n'a aucun lien : seul l'humain l'arrête.",
            },
        ],
    },
    {
        "numero": "Module 3",
        "titre": "Téléphone, SMS, WhatsApp",
        "horaire": "J1 14h00",
        "duree": 90,
        "slides": [
            {
                "type": "section",
                "surtitre": "Jour 1 · Module 3 · 14h00",
                "titre": "Téléphone, SMS, WhatsApp",
                "corps": "<p>Les attaquants ne passent pas que par l'email. Au Sénégal, le téléphone et WhatsApp sont des canaux majeurs.</p>",
                "notes": "",
            },
            {
                "type": "contenu",
                "surtitre": "Canaux",
                "titre": "Au-delà de l'email",
                "corps": """<div class="grid3">
<article><h3>Téléphone</h3><p>Un faux « service informatique » demande un mot de passe ou un code SMS.</p></article>
<article><h3>SMS et WhatsApp</h3><p>Faux site, faux gain, faux transfert d'argent mobile à « annuler ».</p></article>
<article><h3>Fraude au président</h3><p>Un « dirigeant » exige un virement urgent ou un changement de RIB.</p></article>
</div>""",
                "notes": "Jeu de rôle : faux appel informatique.",
            },
            {
                "type": "contenu",
                "surtitre": "Manipulation",
                "titre": "Les 5 leviers",
                "corps": """<table class="prog"><tbody>
<tr><th>Urgence</th><td>« C'est à régler avant midi »</td></tr>
<tr><th>Autorité</th><td>« Le directeur m'a demandé de vous appeler »</td></tr>
<tr><th>Peur</th><td>« Votre compte va être bloqué »</td></tr>
<tr><th>Gain</th><td>« Vous avez gagné, confirmez vos coordonnées »</td></tr>
<tr><th>Preuve sociale</th><td>« Tous vos collègues l'ont déjà fait »</td></tr>
</tbody></table>
<p class="callout">Plus la pression monte, plus il faut ralentir.</p>""",
                "notes": "Demander des exemples vécus.",
            },
            {
                "type": "activite",
                "surtitre": "Jeu de rôle · 15 min",
                "titre": "Le faux appel de l'informatique",
                "corps": "<ul class='big'><li>Un volontaire reçoit l'appel</li><li>La salle note les leviers utilisés</li><li>Débrief : qu'est-ce qui rendait l'appel crédible ?</li></ul>",
                "notes": "Jouer poli, pas caricatural.",
            },
            {
                "type": "chiffre",
                "surtitre": "Règle d'or",
                "titre": "Je vérifie par un autre canal",
                "corps": "<p>Une demande inhabituelle par email ? J'appelle au numéro de l'annuaire, jamais celui du message.</p><p>L'informatique de {entreprise} ne demandera jamais votre mot de passe.</p>",
                "notes": "Aucun vrai dirigeant ne reprochera d'avoir vérifié. Pause 15h15.",
            },
        ],
    },
    {
        "numero": "Module 4",
        "titre": "Mots de passe et MFA",
        "horaire": "J1 15h30",
        "duree": 60,
        "slides": [
            {
                "type": "section",
                "surtitre": "Jour 1 · Module 4 · 15h30",
                "titre": "Mots de passe et double authentification",
                "corps": "",
                "notes": "Main levée : même mot de passe sur 2 comptes ?",
            },
            {
                "type": "contenu",
                "surtitre": "Hygiène",
                "titre": "À faire / à ne jamais faire",
                "corps": """<div class="split">
<div class="ok-box"><h3>À faire</h3><ul><li>Une phrase longue plutôt qu'un mot court</li><li>Un mot de passe différent par compte</li><li>Activer la double authentification</li></ul></div>
<div class="bad-box"><h3>À ne jamais faire</h3><ul><li>Le noter sur un post-it</li><li>Le partager, même avec un collègue</li><li>Donner un code reçu par SMS</li></ul></div>
</div>""",
                "notes": "Comparer Bci2026 vs une phrase de 4 mots.",
            },
            {
                "type": "contenu",
                "surtitre": "Phrase de passe",
                "titre": "La longueur protège plus que les symboles",
                "corps": """<div class="split">
<div class="bad-box"><p class="mono">Faible · {entreprise}2026!</p><p>Court, prévisible : nom et année.</p></div>
<div class="ok-box"><p class="mono">baobab-pirogue-tamarin-soleil</p><p>Long, facile à retenir, difficile à deviner. Ne pas réutiliser cet exemple.</p></div>
</div>""",
                "notes": "Politique interne à confirmer avec la DSI.",
            },
            {
                "type": "contenu",
                "surtitre": "MFA",
                "titre": "Deux preuves valent mieux qu'une",
                "corps": "<p>Ce que je sais (mot de passe) et ce que j'ai (téléphone, code).</p><div class='grid2'><article><h3>Mot de passe volé ?</h3><p>Sans votre téléphone, l'attaquant reste bloqué.</p></article><article><h3>Code reçu sans raison ?</h3><p>Quelqu'un essaie d'entrer : ne le donnez jamais, signalez-le.</p></article></div>",
                "notes": "WhatsApp PIN + email personnel.",
            },
        ],
    },
    {
        "titre": "Jour 1 · Bilan",
        "horaire": "J1 16h30",
        "duree": 15,
        "slides": [
            {
                "type": "contenu",
                "surtitre": "Fin du jour 1",
                "titre": "Ce qu'on retient aujourd'hui",
                "corps": """<div class="grid3">
<article><h3>Urgence = méfiance</h3><p>La pression est le premier signe d'une arnaque.</p></article>
<article><h3>Je vérifie ailleurs</h3><p>Numéro de l'annuaire, jamais celui du message.</p></article>
<article><h3>Mon code est à moi</h3><p>Mot de passe et code SMS ne se donnent jamais.</p></article>
</div>
<p class="callout">Demain : poste de travail, données, normes ISO et gestion d'incident. On commence par un quiz live sur aujourd'hui.</p>""",
                "notes": "Faire citer un réflexe par 3 personnes. Émargement du jour 1.",
            },
        ],
    },
    # ================================================================ JOUR 2
    {
        "titre": "Jour 2 · Rappel",
        "horaire": "J2 8h30",
        "duree": 30,
        "slides": [
            {
                "type": "section",
                "surtitre": "{entreprise} · Jour 2",
                "titre": "Protéger et réagir",
                "corps": "<p>Hier : reconnaître les attaques. Aujourd'hui : protéger son poste et ses données, comprendre le cadre, savoir réagir.</p>",
                "notes": "Accueil. Demander si quelqu'un a repéré un message suspect depuis hier.",
            },
            {
                "type": "quiz",
                "surtitre": "Rappel du jour 1",
                "titre": "Quiz live : qu'avez-vous retenu ?",
                "corps": "<p>Une question à la fois, réponse sur votre téléphone. Le résultat s'affiche à l'écran.</p>",
                "notes": "Cliquer « Quiz live » en bas. Faire 4 à 5 questions, commenter chaque réponse.",
            },
        ],
    },
    {
        "numero": "Module 5",
        "titre": "Poste de travail",
        "horaire": "J2 9h00",
        "duree": 60,
        "slides": [
            {
                "type": "section",
                "surtitre": "Jour 2 · Module 5 · 9h00",
                "titre": "Mon poste de travail",
                "corps": "",
                "notes": "",
            },
            {
                "type": "contenu",
                "surtitre": "Réflexes",
                "titre": "Quatre gestes",
                "corps": """<div class="grid4">
<article><h3>Je verrouille</h3><p>Windows + L dès que je quitte mon poste.</p></article>
<article><h3>Pas de clé USB inconnue</h3><p>Une clé trouvée va à l'informatique.</p></article>
<article><h3>Bureau rangé</h3><p>Aucun dossier client visible en mon absence.</p></article>
<article><h3>Pas de Wi-Fi public</h3><p>Pour le travail, uniquement le réseau de {entreprise}.</p></article>
</div>""",
                "notes": "",
            },
            {
                "type": "activite",
                "surtitre": "Groupes de 5 · 10 min",
                "titre": "Chasse aux erreurs",
                "corps": "<p>10 erreurs typiques à retrouver dans un bureau :</p><ol class='big'><li>Post-it mot de passe</li><li>Session ouverte</li><li>Clé USB inconnue</li><li>Dossier client visible</li><li>Pièce d'identité à la poubelle</li><li>Document envoyé sur WhatsApp</li><li>Badge abandonné</li><li>Tiroir et clés ouverts</li><li>Agenda avec codes</li><li>Écran visible du couloir</li></ol>",
                "notes": "Faire trouver par les groupes avant d'afficher la liste complète.",
            },
        ],
    },
    {
        "numero": "Module 6",
        "titre": "Données et confidentialité",
        "horaire": "J2 10h00",
        "duree": 60,
        "slides": [
            {
                "type": "section",
                "surtitre": "Jour 2 · Module 6 · 10h00",
                "titre": "Données et confidentialité",
                "corps": "<p>La confiance des clients et collègues est le premier actif de {entreprise}.</p>",
                "notes": "",
            },
            {
                "type": "contenu",
                "surtitre": "Cadre",
                "titre": "Les informations ne sortent pas du cadre prévu",
                "corps": "<ul class='big'><li>Pas de pièce d'identité ou de dossier sensible sur WhatsApp ou une messagerie personnelle</li><li>Pas de renseignement par téléphone sans vérifier l'identité</li><li>Pas de fichier sur une clé ou un email personnel</li><li>Documents papier détruits, jamais jetés tels quels</li></ul>",
                "notes": "Politique interne de {entreprise} à confirmer avec le RSSI.",
            },
            {
                "type": "contenu",
                "surtitre": "Cadre légal au Sénégal",
                "titre": "Les données personnelles sont protégées par la loi",
                "corps": """<div class="grid3">
<article><h3>Loi n° 2008-12</h3><p>Loi du 25 janvier 2008 sur la protection des données à caractère personnel.</p></article>
<article><h3>La CDP</h3><p>Commission de protection des données personnelles : elle contrôle et peut sanctionner.</p></article>
<article><h3>Pour vous</h3><p>Collecter le nécessaire, protéger, ne partager qu'avec ceux qui en ont besoin.</p></article>
</div>
<p class="callout">Une fuite de données client n'est pas qu'un incident technique : c'est une question de conformité et de confiance.</p>""",
                "notes": "Rester factuel : pas de conseil juridique. Pour le détail, renvoyer au juriste ou au DPO de {entreprise}.",
            },
            {
                "type": "activite",
                "surtitre": "Cas pratiques",
                "titre": "Que faites-vous ?",
                "corps": "<p>15 minutes de préparation · 2 minutes de restitution par groupe. Les cas A à F sont dans le pack formateur.</p>",
                "notes": "Réponses dans l'admin Cas pratiques. Pause 11h00.",
            },
        ],
    },
    {
        "numero": "Module 7",
        "titre": "Les normes ISO",
        "horaire": "J2 11h15",
        "duree": 75,
        "slides": [
            {
                "type": "section",
                "surtitre": "Jour 2 · Module 7 · 11h15",
                "titre": "Les normes ISO : le cadre derrière les réflexes",
                "corps": "<p>Ce que vous pratiquez depuis hier n'est pas une lubie : c'est ce qu'exigent les référentiels internationaux de sécurité de l'information.</p>",
                "notes": "Niveau utilisateur : pas un cours d'auditeur. Objectif : comprendre pourquoi, et ce que la norme attend de chacun.",
            },
            {
                "type": "contenu",
                "surtitre": "La famille ISO/IEC 27000",
                "titre": "Les normes à connaître",
                "corps": """<div class="grid3">
<article><h3>ISO/IEC 27001</h3><p>Exigences d'un système de management de la sécurité de l'information (SMSI). Certifiable.</p></article>
<article><h3>ISO/IEC 27002</h3><p>Guide de mise en œuvre des mesures de sécurité.</p></article>
<article><h3>ISO/IEC 27005</h3><p>Gestion des risques liés à la sécurité de l'information.</p></article>
<article><h3>ISO/IEC 27035</h3><p>Gestion des incidents de sécurité.</p></article>
<article><h3>ISO/IEC 27701</h3><p>Protection de la vie privée et des données personnelles.</p></article>
<article><h3>ISO 22301</h3><p>Continuité d'activité : continuer à servir les clients malgré une crise.</p></article>
</div>""",
                "notes": "Seule la 27001 donne lieu à certification de l'organisation. Les autres guident sa mise en œuvre.",
            },
            {
                "type": "contenu",
                "surtitre": "Les trois piliers",
                "titre": "Ce que la sécurité protège",
                "corps": """<div class="grid3">
<article><h3>Confidentialité</h3><p>Le solde d'un client n'est vu que par ceux qui en ont besoin.</p></article>
<article><h3>Intégrité</h3><p>Un RIB modifié par un fraudeur : l'information n'est plus fiable.</p></article>
<article><h3>Disponibilité</h3><p>Des agences bloquées par un rançongiciel : le service s'arrête.</p></article>
</div>
<p class="callout">Chaque incident vu depuis hier touche au moins un de ces trois piliers.</p>""",
                "notes": "Faire classer 2 ou 3 exemples de la veille (faux RIB, clé USB, fraude au président).",
            },
            {
                "type": "contenu",
                "surtitre": "ISO/IEC 27001",
                "titre": "Une démarche d'amélioration continue",
                "corps": """<ol class="chain">
<li><strong>Planifier</strong> — Identifier les informations à protéger et évaluer les risques.</li>
<li><strong>Faire</strong> — Appliquer les mesures de sécurité et former le personnel.</li>
<li><strong>Vérifier</strong> — Mesurer, auditer, suivre les incidents.</li>
<li><strong>Agir</strong> — Corriger et améliorer.</li>
</ol>
<p class="callout">Une organisation certifiée est auditée régulièrement : l'auditeur regarde aussi les comportements.</p>""",
                "notes": "Cycle PDCA. Certification valable 3 ans, avec des audits de surveillance entre-temps.",
            },
            {
                "type": "chiffre",
                "surtitre": "ISO/IEC 27001:2022 · Annexe A",
                "titre": "93 mesures",
                "corps": "<p>réparties en 4 thèmes : <strong>37 organisationnelles, 8 liées aux personnes, 14 physiques, 34 technologiques</strong>.</p><p>La mesure <strong>6.3</strong> exige de sensibiliser et de former le personnel. Ces deux jours en font partie.</p>",
                "notes": "Version 2022 de la norme. Les 8 mesures « personnes » concernent directement les participants.",
            },
            {
                "type": "contenu",
                "surtitre": "Concrètement",
                "titre": "Ce que la norme attend de vous",
                "corps": """<table class="prog"><thead><tr><th>Mesure</th><th>Intitulé</th><th>Votre geste</th></tr></thead><tbody>
<tr><th>5.10</th><td>Utilisation acceptable de l'information</td><td>Pas de dossier client sur une messagerie personnelle</td></tr>
<tr><th>5.17</th><td>Informations d'authentification</td><td>Mot de passe personnel, jamais partagé</td></tr>
<tr><th>6.3</th><td>Sensibilisation et formation</td><td>Participer, puis appliquer</td></tr>
<tr><th>6.8</th><td>Signalement des événements de sécurité</td><td>Je signale à {signalement}</td></tr>
<tr><th>7.7</th><td>Bureau propre et écran verrouillé</td><td>Windows + L, rien de visible</td></tr>
<tr><th>8.7</th><td>Protection contre les logiciels malveillants</td><td>Pas de clé USB ni de pièce jointe douteuse</td></tr>
</tbody></table>""",
                "notes": "Relier chaque ligne à un module déjà vu : 6 (données), 4 (mots de passe), 8 (incident), 5 (poste).",
            },
            {
                "type": "activite",
                "surtitre": "Vrai ou faux · 10 min",
                "titre": "Idées reçues sur la norme",
                "corps": """<table class="prog"><tbody>
<tr><th>Faux</th><td>« ISO 27001, c'est l'affaire de l'informatique. » <br><span class="source">Une partie des mesures porte sur les personnes, et chaque salarié est concerné.</span></td></tr>
<tr><th>Faux</th><td>« Une organisation certifiée ne peut pas être piratée. » <br><span class="source">La norme organise la gestion du risque, elle ne le supprime pas.</span></td></tr>
<tr><th>Vrai</th><td>« Signaler un événement suspect fait partie des exigences. » <br><span class="source">Mesure 6.8 : le signalement est attendu, pas facultatif.</span></td></tr>
</tbody></table>""",
                "notes": "Poser chaque affirmation à main levée avant d'afficher la réponse.",
            },
            {
                "type": "contenu",
                "surtitre": "Dans le secteur bancaire",
                "titre": "D'autres exigences s'ajoutent",
                "corps": """<div class="grid3">
<article><h3>PCI DSS</h3><p>Protection des données de cartes bancaires.</p></article>
<article><h3>Superviseur bancaire</h3><p>Exigences de la BCEAO et de la Commission bancaire de l'UMOA sur la maîtrise des risques.</p></article>
<article><h3>Politique interne</h3><p>La politique de sécurité de {entreprise} traduit ces exigences en règles de tous les jours.</p></article>
</div>""",
                "notes": "Vérifier avant la séance si {entreprise} est certifiée ISO 27001 et quel est le nom de sa politique de sécurité : le mentionner ici.",
            },
        ],
    },
    {
        "numero": "Module 8",
        "titre": "Incident : les bons réflexes",
        "horaire": "J2 14h00",
        "duree": 90,
        "slides": [
            {
                "type": "section",
                "surtitre": "Jour 2 · Module 8 · 14h00",
                "titre": "Incident : les bons réflexes",
                "corps": "<p>Même avec toute la vigilance du monde, une erreur peut arriver. Ce qui compte, c'est la réaction.</p>",
                "notes": "Lien avec la norme : ISO/IEC 27035 et la mesure 6.8.",
            },
            {
                "type": "contenu",
                "surtitre": "Procédure",
                "titre": "J'ai cliqué : que faire ?",
                "corps": """<ol class="chain">
<li><strong>Je débranche</strong> — Câble ou Wi-Fi coupé. Je n'éteins pas le PC.</li>
<li><strong>Je préviens</strong> — L'informatique immédiatement : {contact_it}</li>
<li><strong>Je raconte</strong> — Ce que j'ai ouvert, saisi, à quelle heure. Sans honte.</li>
</ol>
<p class="callout">Celui qui signale vite n'est jamais en faute. Le vrai risque, c'est celui qui se tait. Signalement : {signalement}</p>""",
                "notes": "",
            },
            {
                "type": "scenario",
                "surtitre": "Scénario",
                "titre": "La matinée d'Aïssatou",
                "corps": "<p>Votez à chaque ligne avant la bonne réaction. Si elle ne dit rien : à 14h, des emails partent de sa boîte vers des clients.</p>",
                "notes": "9h04 débrancher, 9h05 prévenir, 9h10 tout raconter.",
            },
            {
                "type": "contenu",
                "surtitre": "À emporter",
                "titre": "Les 5 réflexes à retenir",
                "corps": "<ol class='big'><li>Urgence = méfiance</li><li>Je survole avant de cliquer</li><li>Je vérifie par un autre canal</li><li>Mon mot de passe ne se partage pas</li><li>Je signale, même en cas de doute</li></ol>",
                "notes": "Lancer le quiz de sortie.",
            },
        ],
    },
    {
        "titre": "Jour 2 · Clôture",
        "horaire": "J2 15h30",
        "duree": 30,
        "slides": [
            {
                "type": "quiz",
                "surtitre": "Mesure de sortie",
                "titre": "Et maintenant ?",
                "corps": "<p>Les mêmes 10 questions qu'hier matin. On compare au point de départ : c'est votre progression sur les deux jours.</p>",
                "notes": "Afficher les deux scores côte à côte ensuite (écran Scores). Donner les réponses.",
                "quiz_moment": "sortie",
            },
            {
                "type": "contenu",
                "surtitre": "Clôture",
                "titre": "Avant de partir",
                "corps": """<div class="grid3">
<article><h3>Fiche réflexe</h3><p>Les 5 gestes, près du poste.</p></article>
<article><h3>Évaluation</h3><p>Anonyme, 3 minutes.</p></article>
<article><h3>Émargement</h3><p>Signature du jour 2.</p></article>
</div>""",
                "notes": "Ouvrir l'évaluation.",
            },
            {
                "type": "titre",
                "surtitre": "Systalink CyberSécurité",
                "titre": "Merci. Des questions ?",
                "corps": "<p>Signaler un email suspect : {signalement}</p><p class='meta'>{formateur} · Systalink</p>",
                "notes": "Remercier. D'autres exercices suivront sans en préciser la date.",
            },
        ],
    },
]


QUESTIONS = [
    {
        "texte": "Vous recevez un email : « votre mot de passe expire dans 2 heures, cliquez ici ». Que faites-vous ?",
        "explication": "On survole, on vérifie l'expéditeur, on signale en cas de doute. L'informatique ne demande jamais un mot de passe par lien.",
        "choix": [
            ("A", "Je clique tout de suite pour éviter le blocage", False),
            ("B", "Je survole le lien, je vérifie l'adresse, je signale si c'est douteux", True),
            ("C", "Je transfère à un collègue pour qu'il teste à ma place", False),
        ],
    },
    {
        "texte": "Un « directeur » vous envoie un SMS pour un virement urgent et confidentiel.",
        "explication": "Fraude au président : on rappelle au numéro de l'annuaire, jamais celui du message.",
        "choix": [
            ("A", "Je m'exécute : c'est le directeur", False),
            ("B", "Je rappelle la personne au numéro officiel de l'annuaire", True),
            ("C", "Je réponds pour demander le RIB par le même SMS", False),
        ],
    },
    {
        "texte": "Vous recevez un code de double authentification sans avoir essayé de vous connecter.",
        "explication": "Quelqu'un tente d'entrer. On ne donne jamais le code, on signale.",
        "choix": [
            ("A", "Je le donne à la personne de l'informatique qui m'appelle", False),
            ("B", "Je ne le donne à personne et je signale", True),
            ("C", "Je l'ignore : si je n'ai rien demandé, ce n'est rien", False),
        ],
    },
    {
        "texte": "Vous trouvez une clé USB marquée « photos équipe » dans le parking.",
        "explication": "Une clé inconnue va à l'informatique, jamais dans un PC.",
        "choix": [
            ("A", "Je la branche pour voir si c'est vraiment des photos", False),
            ("B", "Je la remets à l'informatique sans la brancher", True),
            ("C", "Je la jette à la poubelle", False),
        ],
    },
    {
        "texte": "Vous venez de cliquer sur un lien suspect. Premier geste ?",
        "explication": "On débranche le réseau, on n'éteint pas le PC, on prévient tout de suite.",
        "choix": [
            ("A", "J'éteins le PC immédiatement", False),
            ("B", "Je coupe le réseau (câble ou Wi-Fi) et je préviens l'informatique", True),
            ("C", "J'attends de voir si l'ordinateur se comporte bizarrement", False),
        ],
    },
    {
        "texte": "Un message insiste : « à traiter avant midi, confidentiel ».",
        "explication": "L'urgence est un levier. Plus la pression monte, plus on ralentit.",
        "choix": [
            ("A", "Plus c'est urgent, plus je dois ralentir et vérifier par un autre canal", True),
            ("B", "L'urgence prouve que c'est interne et important", False),
            ("C", "Je le ferai après la pause, sans vérifier", False),
        ],
    },
    {
        "texte": "Quel mot de passe est le plus solide ?",
        "explication": "La longueur d'une phrase unique bat un mot court avec des chiffres d'année.",
        "choix": [
            ("A", "Le nom de l'entreprise + l'année + un point d'exclamation", False),
            ("B", "Une phrase longue, unique, jamais partagée", True),
            ("C", "Le même mot de passe partout, pour s'en souvenir", False),
        ],
    },
    {
        "texte": "Un client ou un partenaire veut un document sensible sur WhatsApp.",
        "explication": "On reste sur les canaux prévus par l'organisation.",
        "choix": [
            ("A", "Je l'envoie : la personne est pressée", False),
            ("B", "Je refuse et j'utilise le canal officiel prévu", True),
            ("C", "Je floute une partie et je l'envoie quand même", False),
        ],
    },
    {
        "texte": "Comment vérifier un lien avant d'ouvrir la page ?",
        "explication": "Survoler (ou appui long) sans cliquer révèle l'adresse réelle.",
        "choix": [
            ("A", "Je clique, puis je regarde la barre d'adresse", False),
            ("B", "Je survole le lien (ou appui long sur téléphone) sans l'ouvrir", True),
            ("C", "Je le copie dans un moteur de recherche", False),
        ],
    },
    {
        "texte": "Quand faut-il signaler un email ou un message douteux ?",
        "explication": "On signale même en cas de doute. Attendre d'être sûr, c'est trop tard.",
        "choix": [
            ("A", "Seulement si je suis sûr à 100 % que c'est une attaque", False),
            ("B", "Même en cas de doute", True),
            ("C", "Uniquement si j'ai déjà cliqué", False),
        ],
    },
]

EMAILS = [
    {
        "expediteur_nom": "Service Informatique",
        "expediteur_adresse": "support@{domaine}-securite.com",
        "objet": "Action requise : votre mot de passe expire aujourd'hui",
        "categorie": "compte",
        "url_affichee": "http://{domaine}-securite.com/reset",
        "corps": "Bonjour,\n\nVotre mot de passe expire dans 2 heures. Pour éviter le blocage de votre messagerie, cliquez ici pour le renouveler : http://{domaine}-securite.com/reset\n\nCordialement,\nLe support",
        "piege": True,
        "indices": "Domaine externe, pas @{domaine}\nUrgence artificielle (2 heures)\nDemande de mot de passe par lien",
    },
    {
        "expediteur_nom": "Informatique interne",
        "expediteur_adresse": "informatique@{domaine}",
        "objet": "Rappel : maintenance intranet ce jeudi 18h",
        "categorie": "interne",
        "corps": "Bonjour,\n\nUne maintenance de l'intranet est prévue jeudi à 18h. Aucune action n'est demandée. Le service sera de nouveau disponible vers 20h.\n\nConsultez le calendrier sur l'intranet si besoin.\n\nL'équipe informatique",
        "piege": False,
        "indices": "Domaine interne @{domaine}\nAucune demande de mot de passe ou de clic vers l'extérieur\nTon habituel, information simple",
    },
    {
        "expediteur_nom": "Direction générale",
        "expediteur_adresse": "dg.urgence.secret@gmail.com",
        "objet": "Confidentiel — à traiter avant 11h, ne pas en parler",
        "categorie": "fraude au président",
        "corps": "Bonjour,\n\nJe suis en réunion et j'ai besoin que tu fasses un virement urgent. Ne le dis à personne, c'est sensible. Envoie-moi le RIB que je te passerai et confirme dès que c'est fait.\n\nMerci,\nLe directeur",
        "piege": True,
        "indices": "Adresse Gmail, pas le domaine interne\nSecret + urgence : fraude au président\nAucun lien : seul l'humain peut l'arrêter",
    },
    {
        "expediteur_nom": "Comptabilité fournisseur",
        "expediteur_adresse": "facturation@{domaine}.finance-update.net",
        "objet": "Nouveau RIB — merci de mettre à jour avant le prochain paiement",
        "categorie": "fournisseur",
        "corps": "Bonjour,\n\nSuite à un changement de banque, veuillez utiliser le nouveau RIB ci-joint pour tous les paiements. Merci de confirmer par retour.\n\nPièce jointe : RIB.pdf",
        "piege": True,
        "indices": "Changement de RIB par email\nDomaine qui imite {domaine} sans l'être\nToujours vérifier par un autre canal",
    },
    {
        "expediteur_nom": "Communication interne",
        "expediteur_adresse": "communication@{domaine}",
        "objet": "Menu de la cantine — semaine du {date}",
        "categorie": "interne",
        "corps": "Bonjour,\n\nVoici le menu de la semaine. Aucune inscription n'est demandée.\n\nBonne semaine,\nCommunication interne",
        "piege": False,
        "indices": "Domaine interne\nAucune action, aucun lien de connexion\nCohérent avec la vie de l'entreprise",
    },
    {
        "expediteur_nom": "Service RH",
        "expediteur_adresse": "rh-paie@secure-portal-docs.com",
        "objet": "Votre bulletin de salaire est disponible — connexion requise",
        "categorie": "rh",
        "url_affichee": "http://secure-portal-docs.com/login",
        "corps": "Bonjour,\n\nUn nouveau bulletin est disponible. Connectez-vous pour le télécharger : http://secure-portal-docs.com/login\n\nIdentifiant = votre email professionnel.",
        "piege": True,
        "indices": "Expéditeur et domaine inconnus\nLien de connexion hors {domaine}\nDonnées RH jamais via un portail improvisé",
    },
    {
        "expediteur_nom": "Livraison Express",
        "expediteur_adresse": "suivi@colis-afrique-express.net",
        "objet": "Votre colis est retenu — réglez 1 500 F sous 24 h",
        "categorie": "colis",
        "url_affichee": "http://colis-afrique-express.net/payer",
        "corps": "Bonjour,\n\nNous n'avons pas pu livrer votre colis. Payez 1 500 F de frais de douane ici sous 24 h sinon il sera renvoyé.\n\nhttp://colis-afrique-express.net/payer",
        "piege": True,
        "indices": "Colis non attendu\nPetits frais + délai court\nPression classique de phishing grand public",
    },
    {
        "expediteur_nom": "Organisation de la séance",
        "expediteur_adresse": "informatique@{domaine}",
        "objet": "Rappel : séance de sensibilisation cybersécurité aujourd'hui",
        "categorie": "interne",
        "corps": "Bonjour,\n\nRappel : la séance animée par {formateur} a lieu aujourd'hui ({date}). Merci d'arriver 10 minutes en avance. Aucun lien à cliquer.\n\nÀ tout à l'heure.",
        "piege": False,
        "indices": "Domaine interne\nCohérent avec la journée\nAucune action dangereuse",
    },
]

CAS = [
    {
        "lettre": "A",
        "metier": "Accueil / guichet",
        "situation": "Le « frère » d'une cliente hospitalisée demande son solde par téléphone.",
        "reponse": "Ne pas communiquer d'information. Vérifier l'identité selon la procédure, orienter vers un canal officiel. La parenté déclarée ne suffit pas.",
    },
    {
        "lettre": "B",
        "metier": "Accueil / guichet",
        "situation": "Un client pressé veut son relevé ou un document sur WhatsApp.",
        "reponse": "Refuser WhatsApp. Proposer le canal prévu (agence, espace client, email professionnel chiffré si politique interne).",
    },
    {
        "lettre": "C",
        "metier": "Crédit / commercial",
        "situation": "Un partenaire demande par email le dossier complet d'un client.",
        "reponse": "Ne pas envoyer. Vérifier le partenaire par un autre canal, appliquer la politique de partage et le besoin d'en connaître.",
    },
    {
        "lettre": "D",
        "metier": "Back-office",
        "situation": "Un collègue demande un fichier de 500 clients « en urgence » par email.",
        "reponse": "Ralentir. Confirmer de vive voix ou via l'outil interne. L'urgence et le volume sont des signaux. Journaliser le partage s'il est autorisé.",
    },
    {
        "lettre": "E",
        "metier": "Tous",
        "situation": "Finir un dossier chez soi ce week-end, sur la messagerie personnelle.",
        "reponse": "Non. Pas de fichier métier sur un canal personnel. Utiliser le VPN / poste fourni, ou reporter.",
    },
    {
        "lettre": "F",
        "metier": "Tous",
        "situation": "Un inconnu sur LinkedIn pose des questions précises sur vos logiciels internes.",
        "reponse": "Ne pas répondre sur l'architecture. Signaler à l'informatique / la sécurité. C'est du repérage.",
    },
]

SCENARIO = [
    {
        "heure": "9h02",
        "evenement": "Elle clique sur une « facture impayée » et saisit ses identifiants.",
        "bonne_reaction": "Reconnaître l'erreur : ne pas continuer, ne pas réessayer le mot de passe.",
    },
    {
        "heure": "9h04",
        "evenement": "La page affiche une erreur. Elle se dit « ce n'est rien ».",
        "bonne_reaction": "Débrancher le poste (réseau / Wi-Fi). Ne pas éteindre.",
    },
    {
        "heure": "9h05",
        "evenement": "Elle hésite à prévenir, par peur d'être sanctionnée.",
        "bonne_reaction": "Prévenir l'informatique tout de suite : {contact_it}. Celui qui signale n'est pas en faute.",
    },
    {
        "heure": "9h10",
        "evenement": "L'informatique lui demande ce qui s'est passé.",
        "bonne_reaction": "Tout raconter : lien, heure, ce qui a été saisi.",
    },
    {
        "heure": "9h15",
        "evenement": "Mot de passe changé, session bloquée.",
        "bonne_reaction": "Incident contenu en 13 minutes. Si elle n'avait rien dit : à 14h des emails partent vers des clients.",
    },
]
