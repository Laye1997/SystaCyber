function demarrerCompteurFormateur(url) {
  const nEls = document.querySelectorAll("[data-live-n]");
  if (!nEls.length || !url) return;
  async function tick() {
    try {
      const r = await fetch(url, { credentials: "same-origin" });
      const d = await r.json();
      nEls.forEach((el) => {
        el.textContent = d.participants_connectes ?? 0;
      });
      document.querySelectorAll("[data-live-prevus]").forEach((el) => {
        el.textContent = d.participants_prevus ?? el.textContent;
      });
    } catch (e) {
      /* hors ligne : on conserve le dernier chiffre */
    }
  }
  tick();
  setInterval(tick, 3000);
}

function demarrerBattement(url) {
  if (!url) return;
  const ping = () => fetch(url, { credentials: "same-origin" }).catch(() => {});
  ping();
  setInterval(ping, 4000);
}

function _csrf() {
  const m = document.cookie.match(/(?:^|;\s*)csrftoken=([^;]+)/);
  if (m) return decodeURIComponent(m[1]);
  return document.querySelector("input[name=csrfmiddlewaretoken]")?.value || "";
}

function _esc(t) {
  const d = document.createElement("div");
  d.textContent = t ?? "";
  return d.innerHTML;
}

/* Projecteur : question en cours, compteur de réponses, graphique à la révélation. */
function demarrerQuizLiveProjecteur(root, urlAction) {
  const urlEtat = root.dataset.etat;
  const el = (sel) => root.querySelector(sel);
  const btnReveal = document.querySelector("[data-live-reveal]");
  let enCours = false;

  function rendre(d) {
    const L = d.live;
    if (!d.live_quiz_ouvert) { location.reload(); return; }
    if (!L.question) { el("[data-live-q]").textContent = "Aucune question active dans le pack."; return; }
    el("[data-live-pos]").textContent = `Question ${L.index + 1} / ${L.total}`;
    el("[data-live-q]").textContent = L.question.texte;
    el("[data-live-total]").textContent = L.total_votes;
    const max = Math.max(1, ...L.votes.map((v) => v.n));
    el("[data-live-choices]").innerHTML = L.votes.map((v) => {
      const etat = L.revele ? (v.correct ? "bon" : "faux") : "";
      const largeur = L.revele ? Math.round((100 * v.n) / max) : 0;
      return `<div class="lc ${etat}">
        <span class="lc-l">${_esc(v.lettre)}</span>
        <span class="lc-t">${_esc(v.texte)}</span>
        <span class="lc-bar" style="width:${largeur}%"></span>
        <span class="lc-n">${L.revele ? v.n + " · " + v.pct + " %" : ""}</span>
      </div>`;
    }).join("");
    const expl = el("[data-live-expl]");
    expl.hidden = !(L.revele && L.question.explication);
    expl.textContent = L.question.explication || "";
    if (btnReveal) {
      btnReveal.textContent = L.revele ? "Masquer" : "Révéler";
      btnReveal.className = L.revele ? "ghost" : "warn";
    }
  }

  async function tick() {
    try {
      const r = await fetch(urlEtat, { credentials: "same-origin" });
      if (r.ok) rendre(await r.json());
    } catch (e) { /* réseau : on garde l'affichage */ }
  }

  async function action(nom) {
    if (enCours) return;
    enCours = true;
    try {
      const r = await fetch(urlAction, {
        method: "POST",
        credentials: "same-origin",
        headers: { "X-Requested-With": "fetch", "X-CSRFToken": _csrf(), "Content-Type": "application/x-www-form-urlencoded" },
        body: new URLSearchParams({ action: nom }),
      });
      if (r.ok) rendre(await r.json());
    } finally { enCours = false; }
  }

  document.querySelectorAll("[data-live-action]").forEach((b) =>
    b.addEventListener("click", () => action(b.dataset.liveAction))
  );
  tick();
  setInterval(tick, 1500);
  return { action };
}

/* Téléphone : affiche la question live et envoie le vote. */
function rendreQuizLiveParticipant(box, d, urlVote) {
  const L = d.live;
  if (!d.live_quiz_ouvert || !L || !L.question) return false;
  const choisi = d.live_choix;
  const cle = `${L.question.id}|${L.revele}|${choisi}`;
  if (box.dataset.cle === cle) return true;
  box.dataset.cle = cle;
  let html = `<p class="lp-pos">Quiz en direct · question ${L.index + 1} / ${L.total}</p>
    <h2 class="lp-q">${_esc(L.question.texte)}</h2><div class="lp-choices">`;
  for (const v of L.votes) {
    let cls = v.id === choisi ? "choisi" : "";
    if (L.revele) cls += v.correct ? " bon" : (v.id === choisi ? " faux" : " off");
    html += `<button type="button" class="lp-c ${cls}" data-choix="${v.id}" ${L.revele ? "disabled" : ""}>
      <span class="lc-l">${_esc(v.lettre)}</span><span>${_esc(v.texte)}</span></button>`;
  }
  html += `</div>`;
  if (L.revele) {
    const bon = L.votes.find((v) => v.correct);
    const ok = bon && bon.id === choisi;
    html += `<p class="lp-verdict ${ok ? "ok" : "ko"}">${choisi ? (ok ? "Bonne réponse" : "Pas cette fois") : "Pas de réponse"}</p>`;
    if (L.question.explication) html += `<p class="lp-expl">${_esc(L.question.explication)}</p>`;
  } else {
    html += `<p class="lp-hint">${choisi ? "Réponse envoyée. Vous pouvez changer jusqu'à la révélation." : "Touchez une réponse."}</p>`;
  }
  box.innerHTML = html;
  box.querySelectorAll("[data-choix]").forEach((b) =>
    b.addEventListener("click", async () => {
      box.querySelectorAll(".lp-c").forEach((x) => x.classList.remove("choisi"));
      b.classList.add("choisi");
      const r = await fetch(urlVote, {
        method: "POST",
        credentials: "same-origin",
        headers: { "X-CSRFToken": _csrf(), "Content-Type": "application/x-www-form-urlencoded" },
        body: new URLSearchParams({ choix: b.dataset.choix }),
      });
      if (r.ok) { d.live_choix = Number(b.dataset.choix); box.dataset.cle = ""; rendreQuizLiveParticipant(box, d, urlVote); }
    })
  );
  return true;
}
