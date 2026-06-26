/* DeutschWeg — single page app logic.
   State (level, progress) is persisted in localStorage. */

const app = document.getElementById("app");

const store = {
  get() {
    try { return JSON.parse(localStorage.getItem("deutschweg")) || {}; }
    catch { return {}; }
  },
  set(data) { localStorage.setItem("deutschweg", JSON.stringify(data)); },
  patch(fn) { const d = store.get(); fn(d); store.set(d); }
};

let state = {
  level: store.get().level || "A1",
  view: "dashboard"
};

/* ---------------- navigation ---------------- */

function setLevel(level) {
  state.level = level;
  store.patch(d => { d.level = level; });
  document.querySelectorAll(".level-btn").forEach(b =>
    b.classList.toggle("active", b.dataset.level === level));
  render();
}

function showView(view) {
  state.view = view;
  document.querySelectorAll(".nav-btn").forEach(b =>
    b.classList.toggle("active", b.dataset.view === view));
  window.scrollTo({ top: 0 });
  render();
}

function render() {
  switch (state.view) {
    case "dashboard": renderDashboard(); break;
    case "grammar":   renderGrammarList(); break;
    case "lesson":    renderLesson(state.lessonId); break;
    case "vocab":     renderVocab(); break;
    case "listening": renderListening(); break;
    case "quiz":      renderQuizStart(); break;
    case "exam":      renderExam(); break;
  }
}

const esc = s => s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");

/* ---------------- progress helpers ---------------- */

function doneLessons(level) {
  return (store.get().lessonsDone || {})[level] || [];
}
function knownWords(level) {
  return (store.get().wordsKnown || {})[level] || [];
}
function bestScore(level) {
  return (store.get().quizBest || {})[level];
}

/* ---------------- dashboard ---------------- */

function renderDashboard() {
  const lv = state.level;
  const lessons = GRAMMAR[lv];
  const done = doneLessons(lv).length;
  const known = knownWords(lv).length;
  const best = bestScore(lv);
  const lessonPct = Math.round(done / lessons.length * 100);
  const vocabPct = Math.round(known / VOCAB[lv].length * 100);

  app.innerHTML = `
    <div class="card hero">
      <h1>Willkommen bei DeutschWeg! 👋</h1>
      <p>Your complete path from <b>A1 to B1</b> — grammar lessons, vocabulary flashcards, quizzes and
      focused preparation for the <b>Goethe-Zertifikat</b>. Pick your level at the top right and start learning.</p>
      <button class="cta" onclick="showView('grammar')">Start learning ${lv}</button>
      <button class="cta ghost" onclick="showView('exam')">Goethe exam prep</button>
    </div>

    <div class="grid grid-3">
      <div class="card">
        <div class="stat-num">${done}/${lessons.length}</div>
        <div class="stat-label">Grammar lessons completed (${lv})</div>
        <div class="progressbar"><div style="width:${lessonPct}%"></div></div>
      </div>
      <div class="card">
        <div class="stat-num">${known}/${VOCAB[lv].length}</div>
        <div class="stat-label">Words marked as known (${lv})</div>
        <div class="progressbar"><div style="width:${vocabPct}%"></div></div>
      </div>
      <div class="card">
        <div class="stat-num">${best != null ? best + "%" : "—"}</div>
        <div class="stat-label">Best quiz score (${lv})</div>
        <div class="progressbar"><div style="width:${best || 0}%;${best != null && best < 60 ? "background:var(--accent)" : ""}"></div></div>
      </div>
    </div>

    <div class="card">
      <h2>📅 Suggested weekly routine</h2>
      <ul class="tips">
        <li><b>Mo–Fr:</b> 1 grammar lesson + 10 flashcards (≈ 20 minutes a day).</li>
        <li><b>Sa:</b> Level quiz — aim for at least 80% before moving to the next level.</li>
        <li><b>So:</b> One Goethe practice task (reading or writing) from the exam section.</li>
        <li>Speak out loud every day, even alone — describe your day in German while cooking!</li>
      </ul>
    </div>

    <div class="card">
      <h2>🗺️ Your roadmap</h2>
      <p><span class="tag tag-A1">A1</span> Basics: introduce yourself, daily life, present tense, simple past. → <i>Goethe-Zertifikat A1 (Start Deutsch 1)</i></p>
      <p><span class="tag tag-A2">A2</span> Everyday fluency: past tense mastery, Dativ, subordinate clauses, making plans. → <i>Goethe-Zertifikat A2</i></p>
      <p><span class="tag tag-B1">B1</span> Independence: opinions, passive voice, Konjunktiv II, presentations, formal letters. → <i>Goethe-Zertifikat B1</i></p>
    </div>
  `;
}

/* ---------------- grammar ---------------- */

function renderGrammarList() {
  const lv = state.level;
  const done = doneLessons(lv);
  app.innerHTML = `
    <h1>📖 Grammatik ${lv} <span class="tag tag-${lv}">${GRAMMAR[lv].length} lessons</span></h1>
    <p class="sub">Work through the lessons in order — each builds on the previous one.</p>
    ${GRAMMAR[lv].map(l => `
      <div class="lesson-item" onclick="openLesson('${l.id}')">
        <div>
          <div class="lesson-title">${l.title}</div>
          <div class="lesson-desc">${l.desc}</div>
        </div>
        ${done.includes(l.id) ? '<span class="tag tag-done">✓ done</span>' : '<span class="tag tag-' + lv + '">open</span>'}
      </div>`).join("")}
  `;
}

function openLesson(id) {
  state.lessonId = id;
  state.view = "lesson";
  window.scrollTo({ top: 0 });
  render();
}

function renderLesson(id) {
  const lv = state.level;
  const lessons = GRAMMAR[lv];
  const idx = lessons.findIndex(l => l.id === id);
  const lesson = lessons[idx];
  if (!lesson) { showView("grammar"); return; }
  const isDone = doneLessons(lv).includes(id);

  app.innerHTML = `
    <button class="back-btn" onclick="showView('grammar')">← Back to lessons</button>
    <div class="card">
      <span class="tag tag-${lv}">${lv}</span>
      <h1>${lesson.title}</h1>
      <div class="lesson-body">${lesson.body}</div>
      <div style="display:flex;gap:10px;flex-wrap:wrap;margin-top:18px">
        <button class="btn green" onclick="markLessonDone('${id}')" ${isDone ? "disabled" : ""}>
          ${isDone ? "✓ Completed" : "Mark as completed"}
        </button>
        ${idx + 1 < lessons.length
          ? `<button class="btn secondary" onclick="openLesson('${lessons[idx + 1].id}')">Next lesson →</button>`
          : `<button class="btn secondary" onclick="showView('quiz')">Take the ${lv} quiz →</button>`}
      </div>
    </div>
  `;
}

function markLessonDone(id) {
  const lv = state.level;
  store.patch(d => {
    d.lessonsDone = d.lessonsDone || {};
    d.lessonsDone[lv] = d.lessonsDone[lv] || [];
    if (!d.lessonsDone[lv].includes(id)) d.lessonsDone[lv].push(id);
  });
  render();
}

/* ---------------- vocabulary flashcards ---------------- */

let flash = { order: [], pos: 0, flipped: false, showTable: false };

function renderVocab(reshuffle = true) {
  const lv = state.level;
  const words = VOCAB[lv];
  if (reshuffle || !flash.order.length) {
    flash.order = words.map((_, i) => i).sort(() => Math.random() - 0.5);
    flash.pos = 0;
    flash.flipped = false;
  }
  drawFlashcard();
}

function drawFlashcard() {
  const lv = state.level;
  const words = VOCAB[lv];
  const known = knownWords(lv);
  const idx = flash.order[flash.pos];
  const w = words[idx];

  app.innerHTML = `
    <h1>🃏 Vokabeln ${lv} <span class="tag tag-${lv}">${words.length} words</span></h1>
    <p class="sub">Click the card to flip it. Mark words you know — they're tracked in your progress.</p>
    <div class="flash-wrap">
      <div class="flashcard ${flash.flipped ? "flipped" : ""}" onclick="flipCard()">
        <div class="flash-inner">
          <div class="flash-face flash-front">
            <div class="flash-word">${esc(w.de)}</div>
            <button class="speak-btn" onclick="event.stopPropagation(); speakWord(${idx})" title="Listen">🔊</button>
            <div class="flash-hint">click to reveal</div>
          </div>
          <div class="flash-face flash-back">
            <div class="flash-word">${esc(w.en)}</div>
            <div class="flash-example">„${esc(w.ex)}“</div>
          </div>
        </div>
      </div>
      <div class="flash-counter">Card ${flash.pos + 1} / ${words.length}
        ${known.includes(idx) ? " · <b style='color:var(--green)'>✓ known</b>" : ""}</div>
      <div class="flash-controls">
        <button class="btn outline" onclick="prevCard()" ${flash.pos === 0 ? "disabled" : ""}>← Back</button>
        <button class="btn green" onclick="markWord(${idx}, true)">✓ I know it</button>
        <button class="btn" onclick="markWord(${idx}, false)">✗ Still learning</button>
        <button class="btn outline" onclick="nextCard()" ${flash.pos >= words.length - 1 ? "disabled" : ""}>Next →</button>
      </div>
      <button class="btn secondary" onclick="renderVocab(true)">🔀 Shuffle again</button>
    </div>

    <div class="card vocab-table-toggle">
      <button class="btn outline" onclick="toggleVocabTable()">${flash.showTable ? "Hide" : "Show"} full word list</button>
      ${flash.showTable ? `
        <table class="vocab" style="margin-top:14px">
          <tr><th>Deutsch</th><th>English</th><th>Beispiel</th><th></th></tr>
          ${words.map((x, i) => `
            <tr>
              <td><b>${esc(x.de)}</b></td>
              <td>${esc(x.en)}</td>
              <td><i>${esc(x.ex)}</i></td>
              <td>${known.includes(i) ? "✅" : ""}</td>
            </tr>`).join("")}
        </table>` : ""}
    </div>
  `;
}

function flipCard() { flash.flipped = !flash.flipped; drawFlashcard(); }
function nextCard() { if (flash.pos < flash.order.length - 1) { flash.pos++; flash.flipped = false; drawFlashcard(); } }
function prevCard() { if (flash.pos > 0) { flash.pos--; flash.flipped = false; drawFlashcard(); } }
function toggleVocabTable() { flash.showTable = !flash.showTable; drawFlashcard(); }

function markWord(idx, isKnown) {
  const lv = state.level;
  store.patch(d => {
    d.wordsKnown = d.wordsKnown || {};
    d.wordsKnown[lv] = d.wordsKnown[lv] || [];
    const list = d.wordsKnown[lv];
    const has = list.includes(idx);
    if (isKnown && !has) list.push(idx);
    if (!isKnown && has) list.splice(list.indexOf(idx), 1);
  });
  if (flash.pos < flash.order.length - 1) nextCard(); else drawFlashcard();
}

/* ---------------- text-to-speech ---------------- */

function speak(text, rate = 0.92) {
  if (!("speechSynthesis" in window)) {
    alert("Sorry, your browser does not support speech output. Try Chrome, Edge or Safari.");
    return;
  }
  speechSynthesis.cancel();
  const u = new SpeechSynthesisUtterance(text);
  u.lang = "de-DE";
  u.rate = rate;
  const de = speechSynthesis.getVoices().find(v => v.lang.toLowerCase().startsWith("de"));
  if (de) u.voice = de;
  speechSynthesis.speak(u);
}

function speakWord(idx) {
  const w = VOCAB[state.level][idx];
  // Read only the German headword (strip alternatives after "/")
  speak(w.de + ". " + w.ex);
}

/* ---------------- listening (Hören) ---------------- */

let listen = { answers: {}, shown: {}, dictIdx: 0, dictChecked: null };

function renderListening() {
  listen = { answers: {}, shown: {}, dictIdx: 0, dictChecked: null };
  drawListening();
}

function drawListening() {
  const lv = state.level;
  const data = LISTENING[lv];
  const d = data.dictation[listen.dictIdx];

  app.innerHTML = `
    <h1>🎧 Hören ${lv}</h1>
    <p class="sub">Audio is generated by your browser's German voice. Listen first — the transcript stays hidden
    until you've answered, just like in the real exam. You can replay as often as you like (in the exam: 1–2 times!).</p>

    ${data.exercises.map((ex, ei) => {
      const answers = listen.answers[ei] || {};
      const allAnswered = ex.questions.every((_, qi) => answers[qi] != null);
      return `
      <div class="card">
        <h2>${ei + 1}. ${esc(ex.title)}</h2>
        <p class="sub">${esc(ex.intro)}</p>
        <div style="display:flex;gap:10px;flex-wrap:wrap;margin-bottom:14px">
          <button class="btn" onclick="speakExercise(${ei}, 0.92)">▶️ Play audio</button>
          <button class="btn outline" onclick="speakExercise(${ei}, 0.7)">🐢 Play slowly</button>
          <button class="btn outline" onclick="stopSpeech()">⏹ Stop</button>
        </div>
        ${ex.questions.map((q, qi) => `
          <div style="margin-bottom:12px">
            <div class="quiz-q" style="font-size:1rem">${qi + 1}. ${esc(q.q)}</div>
            ${q.opts.map((o, oj) => `
              <button class="quiz-opt ${listenCls(ei, qi, oj, q)}"
                onclick="answerListening(${ei}, ${qi}, ${oj})" ${answers[qi] != null ? "disabled" : ""}>${esc(o)}</button>`).join("")}
            ${answers[qi] != null ? `<div class="quiz-explain">${answers[qi] === q.a ? "✅" : "❌"} ${esc(q.why)}</div>` : ""}
          </div>`).join("")}
        ${allAnswered ? `
          <button class="btn secondary" onclick="toggleTranscript(${ei})">${listen.shown[ei] ? "Hide" : "Show"} transcript</button>
          ${listen.shown[ei] ? `<div class="reading-text">${esc(ex.text)}</div>` : ""}` : ""}
      </div>`;
    }).join("")}

    <div class="card">
      <h2>✍️ Diktat (dictation)</h2>
      <p class="sub">Listen and type exactly what you hear — great training for spelling and endings.
      Sentence ${listen.dictIdx + 1} of ${data.dictation.length}.</p>
      <div style="display:flex;gap:10px;flex-wrap:wrap;margin-bottom:12px">
        <button class="btn" onclick="speak(LISTENING['${lv}'].dictation[${listen.dictIdx}], 0.85)">▶️ Play sentence</button>
        <button class="btn outline" onclick="speak(LISTENING['${lv}'].dictation[${listen.dictIdx}], 0.6)">🐢 Slowly</button>
      </div>
      <input id="dict-input" type="text" placeholder="Type the sentence here …" autocomplete="off"
        style="width:100%;padding:12px 14px;font-size:1rem;border:2px solid var(--line);border-radius:10px"
        onkeydown="if(event.key==='Enter')checkDictation()">
      <div style="display:flex;gap:10px;flex-wrap:wrap;margin-top:12px">
        <button class="btn green" onclick="checkDictation()">Check</button>
        <button class="btn outline" onclick="nextDictation()">Next sentence →</button>
      </div>
      <div id="dict-result">${dictResultHtml(d)}</div>
    </div>
  `;

  const input = document.getElementById("dict-input");
  if (listen.dictChecked != null) input.value = listen.dictChecked;
}

function listenCls(ei, qi, oj, q) {
  const a = (listen.answers[ei] || {})[qi];
  if (a == null) return "";
  if (oj === q.a) return "correct";
  if (oj === a) return "wrong";
  return "";
}

function speakExercise(ei, rate) {
  speak(LISTENING[state.level].exercises[ei].text, rate);
}

function stopSpeech() {
  if ("speechSynthesis" in window) speechSynthesis.cancel();
}

function answerListening(ei, qi, oj) {
  listen.answers[ei] = listen.answers[ei] || {};
  listen.answers[ei][qi] = oj;
  drawListening();
}

function toggleTranscript(ei) {
  listen.shown[ei] = !listen.shown[ei];
  drawListening();
}

const normalize = s => s.toLowerCase().replace(/[.,!?;:„“"']/g, "").replace(/\s+/g, " ").trim();

function checkDictation() {
  const target = LISTENING[state.level].dictation[listen.dictIdx];
  const typed = document.getElementById("dict-input").value;
  listen.dictChecked = typed;
  document.getElementById("dict-result").innerHTML = dictResultHtml(target);
}

function dictResultHtml(target) {
  if (listen.dictChecked == null) return "";
  const ok = normalize(listen.dictChecked) === normalize(target);
  return `<div class="quiz-explain" style="margin-top:12px">
    ${ok ? "✅ <b>Perfekt!</b> Exactly right." : "❌ <b>Not quite.</b> The sentence was:"}
    ${ok ? "" : `<div class="reading-text" style="margin-top:8px">${esc(target)}</div>`}
  </div>`;
}

function nextDictation() {
  const n = LISTENING[state.level].dictation.length;
  listen.dictIdx = (listen.dictIdx + 1) % n;
  listen.dictChecked = null;
  drawListening();
}

/* ---------------- quiz ---------------- */

let quiz = null;

function renderQuizStart() {
  const lv = state.level;
  const best = bestScore(lv);
  app.innerHTML = `
    <h1>✏️ Quiz ${lv}</h1>
    <p class="sub">${QUIZZES[lv].length} questions covering the ${lv} grammar. You get instant feedback with explanations.</p>
    <div class="card" style="text-align:center;padding:40px">
      <p style="font-size:1.1rem">Ready? Aim for <b>80%+</b> before moving up a level.</p>
      ${best != null ? `<p>Your best score so far: <b style="color:${best >= 60 ? "var(--green)" : "var(--accent)"}">${best}%</b></p>` : ""}
      <button class="btn" style="font-size:1.05rem;padding:13px 30px" onclick="startQuiz()">Start quiz</button>
    </div>
  `;
}

function startQuiz() {
  quiz = {
    qs: [...QUIZZES[state.level]].sort(() => Math.random() - 0.5),
    pos: 0, correct: 0, answered: false
  };
  drawQuiz();
}

function drawQuiz() {
  const q = quiz.qs[quiz.pos];
  app.innerHTML = `
    <h1>✏️ Quiz ${state.level}</h1>
    <div class="card">
      <div class="quiz-meta">Question ${quiz.pos + 1} / ${quiz.qs.length} · Correct: ${quiz.correct}</div>
      <div class="quiz-q">${esc(q.q)}</div>
      ${q.opts.map((o, i) => `<button class="quiz-opt" id="opt-${i}" onclick="answerQuiz(${i})">${esc(o)}</button>`).join("")}
      <div id="quiz-feedback"></div>
    </div>
  `;
}

function answerQuiz(i) {
  if (quiz.answered) return;
  quiz.answered = true;
  const q = quiz.qs[quiz.pos];
  const right = i === q.a;
  if (right) quiz.correct++;
  q.opts.forEach((_, j) => {
    const el = document.getElementById("opt-" + j);
    el.disabled = true;
    if (j === q.a) el.classList.add("correct");
    else if (j === i) el.classList.add("wrong");
  });
  document.getElementById("quiz-feedback").innerHTML = `
    <div class="quiz-explain">${right ? "✅ <b>Richtig!</b>" : "❌ <b>Leider falsch.</b>"} ${esc(q.why)}</div>
    <button class="btn" style="margin-top:12px" onclick="nextQuiz()">
      ${quiz.pos + 1 < quiz.qs.length ? "Next question →" : "See result"}
    </button>
  `;
}

function nextQuiz() {
  quiz.pos++;
  quiz.answered = false;
  if (quiz.pos < quiz.qs.length) drawQuiz();
  else finishQuiz();
}

function finishQuiz() {
  const lv = state.level;
  const pct = Math.round(quiz.correct / quiz.qs.length * 100);
  store.patch(d => {
    d.quizBest = d.quizBest || {};
    if (d.quizBest[lv] == null || pct > d.quizBest[lv]) d.quizBest[lv] = pct;
  });
  const msg = pct >= 80 ? "Ausgezeichnet! 🎉 You're ready to move on."
    : pct >= 60 ? "Gut gemacht! 👍 Review the lessons you missed and try again."
    : "Noch nicht ganz. 💪 Go back to the grammar lessons and try again — you'll get there!";
  app.innerHTML = `
    <div class="card" style="text-align:center;padding:46px">
      <div class="score-big" style="color:${pct >= 60 ? "var(--green)" : "var(--accent)"}">${pct}%</div>
      <p style="font-size:1.1rem">${quiz.correct} of ${quiz.qs.length} correct — ${msg}</p>
      <div style="display:flex;gap:10px;justify-content:center;flex-wrap:wrap;margin-top:10px">
        <button class="btn" onclick="startQuiz()">Try again</button>
        <button class="btn secondary" onclick="showView('grammar')">Review grammar</button>
        <button class="btn outline" onclick="showView('dashboard')">Dashboard</button>
      </div>
    </div>
  `;
}

/* ---------------- exam ---------------- */

let examTab = "overview";
let examReadingAnswers = {};

function renderExam() {
  const lv = state.level;
  const ex = EXAM[lv];
  const tabs = [
    ["overview", "📋 Overview"],
    ["lesen", "📖 Lesen"],
    ["schreiben", "✍️ Schreiben"],
    ["sprechen", "🗣️ Sprechen"],
    ["tips", "💡 Tips & Checklist"]
  ];
  app.innerHTML = `
    <h1>🎓 ${ex.name}</h1>
    <p class="sub">${ex.pass}</p>
    <div class="exam-tabs">
      ${tabs.map(([id, label]) =>
        `<button class="exam-tab ${examTab === id ? "active" : ""}" onclick="setExamTab('${id}')">${label}</button>`).join("")}
    </div>
    <div id="exam-content">${examTabContent(lv, ex)}</div>
  `;
}

function setExamTab(t) {
  examTab = t;
  examReadingAnswers = {};
  renderExam();
}

function examTabContent(lv, ex) {
  if (examTab === "overview") {
    return `
      <div class="grid grid-2">
        ${ex.modules.map(m => `
          <div class="card module-card">
            <h2>${m.name} <span class="tag tag-${lv}">${m.time}</span></h2>
            <p>${m.desc}</p>
          </div>`).join("")}
      </div>
      <div class="card">
        <h2>🎧 Hören üben</h2>
        <p>Listening needs real audio — combine this site with the <b>free official model exams (with audio)</b> at
        <a href="https://www.goethe.de/en/spr/prf.html" target="_blank" rel="noopener">goethe.de</a>.
        Also great for daily listening: slow German news from <i>Nachrichtenleicht</i> and the DW series <i>Langsam gesprochene Nachrichten</i>.</p>
      </div>`;
  }

  if (examTab === "lesen") {
    const renderReading = (r, base) => `
      <div class="card">
        <h2>${r.title}</h2>
        <p class="sub">Read the text, then answer Richtig or Falsch — exactly like in the exam.</p>
        <div class="reading-text">${esc(r.text)}</div>
        ${r.questions.map((q, i) => `
          <div style="margin-bottom:14px">
            <div class="quiz-q" style="font-size:1rem">${i + 1}. ${esc(q.q)}</div>
            ${q.opts.map((o, j) => `
              <button class="quiz-opt ${cls(base + i, j, q)}" style="display:inline-block;width:auto;margin-right:8px"
                onclick="answerReading(${base + i}, ${j})" ${examReadingAnswers[base + i] != null ? "disabled" : ""}>${o}</button>`).join("")}
            ${examReadingAnswers[base + i] != null ? `<div class="quiz-explain">${examReadingAnswers[base + i] === q.a ? "✅" : "❌"} ${esc(q.why)}</div>` : ""}
          </div>`).join("")}
      </div>`;
    return renderReading(ex.reading, 0) + (ex.reading2 ? renderReading(ex.reading2, 100) : "");
  }

  if (examTab === "schreiben") {
    const w = ex.writing;
    return `
      <div class="card">
        <h2>${w.title}</h2>
        <p class="sub">Write your answer on paper or in a note app first — then compare with the model answer.</p>
        ${w.prompts.map((p, i) => `
          <h3>Aufgabe ${i + 1}</h3>
          <p>${esc(p.task)}</p>
          <details class="model-answer">
            <summary>Show model answer</summary>
            <div class="reading-text">${esc(p.model)}</div>
          </details>`).join("")}
      </div>`;
  }

  if (examTab === "sprechen") {
    return `
      <div class="card">
        <h2>🗣️ Sprechen üben</h2>
        <ul class="tips">${ex.speaking.map(s => `<li>${esc(s)}</li>`).join("")}</ul>
      </div>`;
  }

  // tips + checklist
  const checks = (store.get().examChecks || {})[lv] || [];
  const checklist = [
    "I have done the official Modellsatz under real time conditions",
    "I score 80%+ on this site's level quiz",
    "I know all the letter opening/closing phrases by heart",
    "I have practised speaking out loud with a partner or recording",
    "I have registered for the exam and know the location and time",
    "Day before: ID document ready, pens packed, early night — no cramming!"
  ];
  return `
    <div class="card">
      <h2>💡 Top tips</h2>
      <ul class="tips">${ex.tips.map(t => `<li>${esc(t)}</li>`).join("")}</ul>
    </div>
    <div class="card">
      <h2>✅ Exam readiness checklist</h2>
      <div class="checklist">
        ${checklist.map((c, i) => `
          <label><input type="checkbox" ${checks.includes(i) ? "checked" : ""} onchange="toggleCheck(${i})"> ${c}</label>`).join("")}
      </div>
    </div>`;
}

function cls(qi, oj, q) {
  if (examReadingAnswers[qi] == null) return "";
  if (oj === q.a) return "correct";
  if (oj === examReadingAnswers[qi]) return "wrong";
  return "";
}

function answerReading(qi, oj) {
  examReadingAnswers[qi] = oj;
  document.getElementById("exam-content").innerHTML = examTabContent(state.level, EXAM[state.level]);
}

function toggleCheck(i) {
  const lv = state.level;
  store.patch(d => {
    d.examChecks = d.examChecks || {};
    d.examChecks[lv] = d.examChecks[lv] || [];
    const list = d.examChecks[lv];
    list.includes(i) ? list.splice(list.indexOf(i), 1) : list.push(i);
  });
}

/* ---------------- init ---------------- */

document.querySelectorAll(".level-btn").forEach(b =>
  b.classList.toggle("active", b.dataset.level === state.level));
render();
