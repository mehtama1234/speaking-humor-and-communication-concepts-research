const data = window.SPEAKING_SITE_DATA;
const detailLabelByType = {
  corpus: "Corpus Detail",
  concept: "Concept Detail",
  drill: "Drill Detail",
  pathway: "Learner Pathway",
  example: "Example Study Set",
  session: "Featured Session",
  source: "Source Map Entry",
  evidence: "Evidence Moment",
  matrix: "Comparison Matrix Entry",
  roadmap: "Roadmap Entry",
  contrast: "Contrast Case",
  curriculum: "Curriculum Entry",
};

const sectionPageByType = {
  corpus: "./corpora.html",
  concept: "./concepts.html",
  drill: "./drills.html",
  pathway: "./pathways.html",
  example: "./examples.html",
  session: "./sessions.html",
  source: "./sources.html",
  evidence: "./evidence.html",
  matrix: "./matrix.html",
  roadmap: "./roadmap.html",
  contrast: "./contrasts.html",
  curriculum: "./curriculum.html",
};

const sectionLabelByType = {
  corpus: "Corpora Page",
  concept: "Concepts Page",
  drill: "Drills Page",
  pathway: "Pathways Page",
  example: "Examples Page",
  session: "Sessions Page",
  source: "Sources Page",
  evidence: "Evidence Page",
  matrix: "Matrix Page",
  roadmap: "Roadmap Page",
  contrast: "Contrasts Page",
  curriculum: "Curriculum Page",
};

const practiceCurriculumSlugs = new Set([
  "start-here-decision-guide",
  "first-session-quickstart",
  "speaking-practice-operating-system",
  "practice-stack-bundles",
  "focused-weekly-improvement-actions",
  "speaking-diagnosis-guide",
  "speaking-common-mistakes-and-fixes",
  "30-day-speaking-challenge",
  "30-day-challenge-tracker",
  "live-field-missions",
  "live-speaking-phrase-bank",
  "real-life-speaking-simulations",
  "partner-roleplay-facilitator-guide",
  "presentation-interview-deployment-examples",
  "social-humor-deployment-examples",
  "workplace-speaking-deployment-examples",
  "transcript-backed-concrete-speaking-approaches",
  "speaking-move-deployment-examples",
  "real-speaker-exemplars",
  "real-world-speaking-application-examples",
  "speaker-pattern-playbook",
  "speaker-pattern-drill-cards",
  "speaker-patterns-by-context",
  "roleplay-feedback-scorecard",
  "speaking-practice-case-studies",
  "speaking-pattern-practice-recipes",
  "speaking-roleplay-packs",
  "weekly-plans-by-learner-type",
  "worked-speaking-situation-examples",
  "watch-before-you-practice-guide",
  "evidence-backed-drill-map",
  "context-based-speaking-routes",
  "month-one-speaking-training-plan",
  "daily-speaking-session-templates",
  "speaking-preflight-checklists",
  "weekly-practice-sprints",
  "speaking-sample-prompt-bank",
  "speaking-progress-scorecard",
  "listener-feedback-template",
  "weekly-review-and-adjustment-template",
  "stalled-progress-troubleshooting-guide",
  "time-budget-practice-guide",
  "confidence-and-composure-curriculum",
  "clarity-and-anti-rambling-curriculum",
  "delivery-and-vocal-presence-curriculum",
  "business-communication-curriculum",
  "interview-and-hard-question-curriculum",
  "presentation-and-formal-speaking-curriculum",
  "skeptical-room-and-objection-handling-curriculum",
  "social-speaking-and-humor-curriculum",
  "storytelling-and-memorability-curriculum",
  "multilingual-clarity-and-accent-pressure-curriculum",
]);

const practiceMatrixSlugs = new Set([
  "best-route-if-you-need-something-useful-today",
  "best-route-if-you-want-one-solid-week-of-progress",
  "best-route-if-you-need-realistic-rehearsal-for-a-live-situation",
  "best-route-if-you-want-to-watch-strong-examples-before-acting",
  "best-route-if-you-want-a-serious-structured-start",
  "best-route-if-a-real-event-is-close",
  "best-route-if-you-are-practicing-but-not-improving",
  "best-route-if-the-repo-feels-rich-but-overwhelming",
]);

function detailUrl(type, slug) {
  return `./detail.html?type=${encodeURIComponent(type)}&slug=${encodeURIComponent(slug)}`;
}

function renderCorpora() {
  const root = document.getElementById("corpus-grid");
  if (!root || !data) return;
  root.innerHTML = corpora
    .map(
      (item) => `
        <article class="card">
          <a class="card-link" href="${detailUrl("corpus", item.slug)}">
            <span class="small-label">${item.label}</span>
            <h3>${item.title}</h3>
            <p>${item.summary}</p>
            <div class="meta">
              <span>${item.videos} videos</span>
              <span>${item.words} words</span>
            </div>
            <div class="meta">
              ${item.concepts.map((concept) => `<span>${concept}</span>`).join("")}
            </div>
            ${item.focus ? `<div class="meta">${item.focus.map((focus) => `<span>${focus}</span>`).join("")}</div>` : ""}
          </a>
        </article>
      `,
    )
    .join("");
}

function renderConcepts() {
  const root = document.getElementById("concept-grid");
  if (!root || !data) return;
  root.innerHTML = concepts
    .map(
      (item, index) => `
        <article class="card">
          <a class="card-link" href="${detailUrl("concept", item.slug)}">
            <span class="small-label">Concept ${index + 1}</span>
            <h3>${item.title}</h3>
            <p>
              ${item.summary}
            </p>
            <div class="meta"><span>${item.family}</span></div>
          </a>
        </article>
      `,
    )
    .join("");
}

function renderDrills() {
  const root = document.getElementById("drill-grid");
  if (!root || !data) return;
  root.innerHTML = drills
    .map(
      (item) => `
        <article class="card">
          <a class="card-link" href="${detailUrl("drill", item.slug)}">
            <span class="small-label">${item.corpus}</span>
            <h3>${item.title}</h3>
            <p>${item.summary}</p>
          </a>
        </article>
      `,
    )
    .join("");
}

function renderPathways() {
  const root = document.getElementById("pathway-grid");
  if (!root || !data) return;
  root.innerHTML = pathways
    .map(
      (item) => `
        <article class="card">
          <a class="card-link" href="${detailUrl("pathway", item.slug)}">
            <span class="small-label">${item.family}</span>
            <h3>${item.title}</h3>
            <p>${item.summary}</p>
            ${item.focus ? `<div class="meta">${item.focus.map((focus) => `<span>${focus}</span>`).join("")}</div>` : ""}
          </a>
        </article>
      `,
    )
    .join("");
}

function renderExamples() {
  const root = document.getElementById("example-grid");
  if (!root || !data) return;
  root.innerHTML = examples
    .map(
      (item) => `
        <article class="card">
          <a class="card-link" href="${detailUrl("example", item.slug)}">
            <span class="small-label">${item.family}</span>
            <h3>${item.title}</h3>
            <p>${item.summary}</p>
            ${item.focus ? `<div class="meta">${item.focus.map((focus) => `<span>${focus}</span>`).join("")}</div>` : ""}
          </a>
        </article>
      `,
    )
    .join("");
}

function renderExampleHighlights() {
  const root = document.getElementById("example-highlight-grid");
  if (!root || !data) return;

  const specs = [
    {
      slug: "transcript-backed-concrete-speaking-approaches",
      label: "Need Exact Moves",
      note: "Best when you want transcript-backed approaches, what problem they solve, and how to use them before going deeper.",
    },
    {
      slug: "real-speaker-exemplars",
      label: "Need A Real Speaker",
      note: "Best when you want to see an actual person using the move well before adapting it.",
    },
    {
      slug: "worked-speaking-situation-examples",
      label: "Need Weak Vs Strong",
      note: "Best when you want realistic before-and-after wording and the structural difference it reveals.",
    },
    {
      slug: "real-world-speaking-application-examples",
      label: "Need A Borrowed Version",
      note: "Best when you want a real speaker, a matching room, and a stronger version you could actually use next.",
    },
  ];

  renderScenarioCurriculumCollection("example-highlight-grid", specs);
}

function renderSessions() {
  const root = document.getElementById("session-grid");
  if (!root || !data) return;
  root.innerHTML = sessions
    .map(
      (item) => `
        <article class="card">
          <a class="card-link" href="${detailUrl("session", item.slug)}">
            <span class="small-label">${item.corpus}</span>
            <h3>${item.title}</h3>
            <p>${item.summary}</p>
            ${item.focus ? `<div class="meta">${item.focus.map((focus) => `<span>${focus}</span>`).join("")}</div>` : ""}
          </a>
        </article>
      `,
    )
    .join("");
}

function renderSources() {
  const root = document.getElementById("source-grid");
  if (!root || !data) return;
  root.innerHTML = sources
    .map(
      (item) => `
        <article class="card">
          <a class="card-link" href="${detailUrl("source", item.slug)}">
            <span class="small-label">${item.family}</span>
            <h3>${item.title}</h3>
            <p>${item.summary}</p>
            ${item.focus ? `<div class="meta">${item.focus.map((focus) => `<span>${focus}</span>`).join("")}</div>` : ""}
          </a>
        </article>
      `,
    )
    .join("");
}

function renderEvidence() {
  const root = document.getElementById("evidence-grid");
  if (!root || !data) return;
  root.innerHTML = evidence
    .map(
      (item) => `
        <article class="card">
          <a class="card-link" href="${detailUrl("evidence", item.slug)}">
            <span class="small-label">${item.family}</span>
            <h3>${item.title}</h3>
            <p>${item.summary}</p>
            ${item.focus ? `<div class="meta">${item.focus.map((focus) => `<span>${focus}</span>`).join("")}</div>` : ""}
          </a>
        </article>
      `,
    )
    .join("");
}

function renderMatrix() {
  const root = document.getElementById("matrix-grid");
  if (!root || !data) return;
  root.innerHTML = matrix
    .map(
      (item) => `
        <article class="card">
          <a class="card-link" href="${detailUrl("matrix", item.slug)}">
            <span class="small-label">${item.family}</span>
            <h3>${item.title}</h3>
            <p>${item.summary}</p>
            ${item.focus ? `<div class="meta">${item.focus.map((focus) => `<span>${focus}</span>`).join("")}</div>` : ""}
          </a>
        </article>
      `,
    )
    .join("");
}

function renderRoadmap() {
  const root = document.getElementById("roadmap-grid");
  if (!root || !data) return;
  root.innerHTML = roadmap
    .map(
      (item) => `
        <article class="card">
          <a class="card-link" href="${detailUrl("roadmap", item.slug)}">
            <span class="small-label">${item.family}</span>
            <h3>${item.title}</h3>
            <p>${item.summary}</p>
            ${item.focus ? `<div class="meta">${item.focus.map((focus) => `<span>${focus}</span>`).join("")}</div>` : ""}
          </a>
        </article>
      `,
    )
    .join("");
}

function renderContrasts() {
  const root = document.getElementById("contrast-grid");
  if (!root || !data) return;
  root.innerHTML = contrasts
    .map(
      (item) => `
        <article class="card">
          <a class="card-link" href="${detailUrl("contrast", item.slug)}">
            <span class="small-label">${item.family}</span>
            <h3>${item.title}</h3>
            <p>${item.summary}</p>
            ${item.focus ? `<div class="meta">${item.focus.map((focus) => `<span>${focus}</span>`).join("")}</div>` : ""}
          </a>
        </article>
      `,
    )
    .join("");
}

function renderCurriculum() {
  const root = document.getElementById("curriculum-grid");
  if (!root || !data) return;
  root.innerHTML = curriculum
    .map(
      (item) => `
        <article class="card">
          <a class="card-link" href="${detailUrl("curriculum", item.slug)}">
            <span class="small-label">${item.family}</span>
            <h3>${item.title}</h3>
            <p>${item.summary}</p>
            ${item.focus ? `<div class="meta">${item.focus.map((focus) => `<span>${focus}</span>`).join("")}</div>` : ""}
          </a>
        </article>
      `,
    )
    .join("");
}

function renderCurriculumCollection(rootId, items) {
  const root = document.getElementById(rootId);
  if (!root || !data) return;
  root.innerHTML = items
    .map(
      (item) => `
        <article class="card">
          <a class="card-link" href="${detailUrl("curriculum", item.slug)}">
            <span class="small-label">${item.family}</span>
            <h3>${item.title}</h3>
            <p>${item.summary}</p>
            ${item.focus ? `<div class="meta">${item.focus.map((focus) => `<span>${focus}</span>`).join("")}</div>` : ""}
          </a>
        </article>
      `,
    )
    .join("");
}

function renderScenarioCurriculumCollection(rootId, specs) {
  const root = document.getElementById(rootId);
  if (!root || !data) return;

  const items = specs
    .map((spec) => {
      const item = curriculum.find((entry) => entry.slug === spec.slug);
      return item ? { ...item, scenarioLabel: spec.label, scenarioNote: spec.note } : null;
    })
    .filter(Boolean);

  root.innerHTML = items
    .map(
      (item) => `
        <article class="card">
          <a class="card-link" href="${detailUrl("curriculum", item.slug)}">
            <span class="small-label">${item.scenarioLabel ?? item.family}</span>
            <h3>${item.title}</h3>
            <p>${item.summary}</p>
            ${item.scenarioNote ? `<p class="card-note">${item.scenarioNote}</p>` : ""}
            ${item.focus ? `<div class="meta">${item.focus.map((focus) => `<span>${focus}</span>`).join("")}</div>` : ""}
          </a>
        </article>
      `,
    )
    .join("");
}

function renderMatrixCollection(rootId, items) {
  const root = document.getElementById(rootId);
  if (!root || !data) return;
  root.innerHTML = items
    .map(
      (item) => `
        <article class="card">
          <a class="card-link" href="${detailUrl("matrix", item.slug)}">
            <span class="small-label">${item.family}</span>
            <h3>${item.title}</h3>
            <p>${item.summary}</p>
            ${item.focus ? `<div class="meta">${item.focus.map((focus) => `<span>${focus}</span>`).join("")}</div>` : ""}
          </a>
        </article>
      `,
    )
    .join("");
}

function renderCurriculumRoutes() {
  const routeSlugs = [
    "start-here-decision-guide",
    "first-session-quickstart",
    "speaking-practice-operating-system",
    "practice-stack-bundles",
    "focused-weekly-improvement-actions",
    "speaking-common-mistakes-and-fixes",
    "live-speaking-phrase-bank",
    "real-life-speaking-simulations",
    "social-humor-deployment-examples",
    "workplace-speaking-deployment-examples",
    "speaking-move-deployment-examples",
    "real-speaker-exemplars",
    "real-world-speaking-application-examples",
    "speaker-pattern-playbook",
    "speaker-pattern-drill-cards",
    "speaker-patterns-by-context",
    "roleplay-feedback-scorecard",
    "speaking-practice-case-studies",
    "speaking-pattern-practice-recipes",
    "speaking-roleplay-packs",
    "weekly-plans-by-learner-type",
    "worked-speaking-situation-examples",
    "watch-before-you-practice-guide",
    "evidence-backed-drill-map",
    "speaking-diagnosis-guide",
    "context-based-speaking-routes",
    "month-one-speaking-training-plan",
  ];

  const items = routeSlugs
    .map((slug) => curriculum.find((entry) => entry.slug === slug))
    .filter(Boolean);

  renderCurriculumCollection("curriculum-route-grid", items);
}

function renderCurriculumTracks() {
  const trackSlugs = [
    "seven-session-starter-curriculum",
    "confidence-and-composure-curriculum",
    "clarity-and-anti-rambling-curriculum",
    "delivery-and-vocal-presence-curriculum",
    "business-communication-curriculum",
    "presentation-and-formal-speaking-curriculum",
    "interview-and-hard-question-curriculum",
    "skeptical-room-and-objection-handling-curriculum",
    "social-speaking-and-humor-curriculum",
    "storytelling-and-memorability-curriculum",
  ];

  const items = trackSlugs
    .map((slug) => curriculum.find((entry) => entry.slug === slug))
    .filter(Boolean);

  renderCurriculumCollection("curriculum-track-grid", items);
}

function renderCurriculumSupport() {
  const supportSlugs = [
    "speaking-practice-operating-system",
    "daily-speaking-session-templates",
    "speaking-common-mistakes-and-fixes",
    "live-speaking-phrase-bank",
    "real-life-speaking-simulations",
    "social-humor-deployment-examples",
    "workplace-speaking-deployment-examples",
    "speaking-move-deployment-examples",
    "real-speaker-exemplars",
    "real-world-speaking-application-examples",
    "speaker-pattern-playbook",
    "speaker-pattern-drill-cards",
    "speaker-patterns-by-context",
    "roleplay-feedback-scorecard",
    "speaking-practice-case-studies",
    "speaking-pattern-practice-recipes",
    "speaking-roleplay-packs",
    "weekly-plans-by-learner-type",
    "worked-speaking-situation-examples",
    "watch-before-you-practice-guide",
    "evidence-backed-drill-map",
    "speaking-preflight-checklists",
    "weekly-practice-sprints",
    "focused-weekly-improvement-actions",
    "speaking-sample-prompt-bank",
    "speaking-progress-scorecard",
    "listener-feedback-template",
    "weekly-review-and-adjustment-template",
    "stalled-progress-troubleshooting-guide",
    "time-budget-practice-guide",
  ];

  const items = supportSlugs
    .map((slug) => curriculum.find((entry) => entry.slug === slug))
    .filter(Boolean);

  renderCurriculumCollection("curriculum-support-grid", items);
}

function renderStartRoutes() {
  const root = document.getElementById("start-grid");
  if (!root || !data) return;

  const startSpecs = [
    {
      slug: "first-session-quickstart",
      label: "Brand New",
      note: "Best first move if you want one useful session and a baseline before browsing deeply.",
    },
    {
      slug: "speaking-preflight-checklists",
      label: "Event Soon",
      note: "Best when a meeting, interview, talk, or social moment is close and execution matters now.",
    },
    {
      slug: "focused-weekly-improvement-actions",
      label: "Need Concrete Reps",
      note: "Best when you want simple action-first practice this week instead of a larger system.",
    },
    {
      slug: "30-day-speaking-challenge",
      label: "Need A 30-Day Path",
      note: "Best when you want the next month shaped into one challenge instead of stitching together weekly pieces yourself.",
    },
    {
      slug: "30-day-challenge-tracker",
      label: "Need A Challenge Tracker",
      note: "Best when you want a simple operating sheet for weekly reps, live missions, and month-end comparison.",
    },
    {
      slug: "live-field-missions",
      label: "Need A Live Assignment",
      note: "Best when you want one concrete thing to do in a real room this week instead of another private rep.",
    },
    {
      slug: "transcript-backed-concrete-speaking-approaches",
      label: "Need Exact Approaches",
      note: "Best when you want named transcript-backed moves before choosing examples, drills, or a weekly route.",
    },
    {
      slug: "worked-speaking-situation-examples",
      label: "Need Real Examples",
      note: "Best when you want concrete before-and-after situations with exact language shapes you can adapt immediately.",
    },
    {
      slug: "real-world-speaking-application-examples",
      label: "Need Exact Adaptation",
      note: "Best when you want a real speaker, the matching room, and a stronger version you could actually use next.",
    },
    {
      slug: "partner-roleplay-facilitator-guide",
      label: "Need A Practice Partner Route",
      note: "Best when another person is available and you want a cleaner way to run, escalate, and score the roleplay together.",
    },
    {
      slug: "presentation-interview-deployment-examples",
      label: "Need High-Attention Examples",
      note: "Best when your speaking problem shows up in interviews, presentations, demos, or Q&A where the room is watching closely.",
    },
    {
      slug: "social-humor-deployment-examples",
      label: "Need Social Examples",
      note: "Best when your speaking issue is warmth, humor, awkwardness, or conversational entry rather than formal work communication.",
    },
    {
      slug: "workplace-speaking-deployment-examples",
      label: "Need Work Examples",
      note: "Best when your speaking problem mostly shows up in meetings, updates, pitches, interviews, or stakeholder conversations at work.",
    },
    {
      slug: "speaking-move-deployment-examples",
      label: "Need Exact Deployment",
      note: "Best when you want a named speaker, the move they used, and the exact kind of room where you should use it next.",
    },
    {
      slug: "speaker-pattern-playbook",
      label: "Need Reusable Moves",
      note: "Best when you want exact move patterns, starter line shapes, and misuse warnings for real speaking situations.",
    },
    {
      slug: "speaker-pattern-drill-cards",
      label: "Need Short Drills",
      note: "Best when you want a small repeatable drill card for one move, plus a live-use prompt for this week.",
    },
    {
      slug: "speaking-pattern-practice-recipes",
      label: "Need A Mini-Stack",
      note: "Best when you want one ready-made recipe for a specific problem, including the example, drill, and live challenge.",
    },
    {
      slug: "speaking-practice-case-studies",
      label: "Need Real Usage Examples",
      note: "Best when you want to see what it looks like for a learner to use the stack across a few days in a real situation.",
    },
    {
      slug: "speaking-roleplay-packs",
      label: "Need Back-And-Forth Reps",
      note: "Best when you want to practice the first answer and the sharper follow-up turn instead of stopping at one response.",
    },
    {
      slug: "roleplay-feedback-scorecard",
      label: "Need Roleplay Scoring",
      note: "Best when you want to judge whether the second turn stayed strong instead of just guessing how the roleplay felt.",
    },
    {
      slug: "weekly-plans-by-learner-type",
      label: "Need A Week Plan",
      note: "Best when you want a seven-day plan already matched to the kind of learner and problem you are dealing with.",
    },
    {
      slug: "speaker-patterns-by-context",
      label: "Know The Situation",
      note: "Best when you know the kind of moment you have and want the right move, line shape, and next file fast.",
    },
    {
      slug: "real-speaker-exemplars",
      label: "Need Real Speaker Models",
      note: "Best when you want actual named speakers, the move they used, and how to adapt that move without copying them.",
    },
    {
      slug: "practice-stack-bundles",
      label: "Repo Feels Big",
      note: "Best when you want the right files grouped for your situation instead of building your own stack.",
    },
    {
      slug: "month-one-speaking-training-plan",
      label: "Serious Restart",
      note: "Best when you want a stronger month-one path with baseline, retest, and adjustment.",
    },
    {
      slug: "stalled-progress-troubleshooting-guide",
      label: "Not Improving",
      note: "Best when effort is happening but visible change is still weak or confusing.",
    },
    {
      slug: "watch-before-you-practice-guide",
      label: "Need Examples First",
      note: "Best when you want one or two transcript-backed sessions before choosing the drill or route.",
    },
  ];

  renderScenarioCurriculumCollection("start-grid", startSpecs);
}

function renderPracticeHighlights() {
  const root = document.getElementById("practice-highlight-grid");
  if (!root || !data) return;

  const specs = [
    {
      slug: "daily-speaking-session-templates",
      label: "Need Reps Today",
      note: "Use this when you want one useful session now, not more planning.",
    },
    {
      slug: "weekly-practice-sprints",
      label: "Want A Real Week",
      note: "Use this when you want seven days of repetition and a retest.",
    },
    {
      slug: "month-one-speaking-training-plan",
      label: "Need A Strong Month",
      note: "Use this when you want a more serious baseline-to-retest training block.",
    },
    {
      slug: "speaking-preflight-checklists",
      label: "Event Coming Soon",
      note: "Use this when execution quality matters more than broad study.",
    },
    {
      slug: "transcript-backed-concrete-speaking-approaches",
      label: "Need A Named Move",
      note: "Use this when you want a transcript-backed speaking approach before you record, rehearse, or go live.",
    },
    {
      slug: "real-world-speaking-application-examples",
      label: "Need A Borrowed Version",
      note: "Use this when you want an actual person, a matching room, and a strong adaptation before the next rep.",
    },
  ];

  renderScenarioCurriculumCollection("practice-highlight-grid", specs);
}

function renderProblemHighlights() {
  const root = document.getElementById("problem-highlight-grid");
  if (!root || !data) return;

  const specs = [
    {
      slug: "confidence-and-composure-curriculum",
      label: "Freeze Or Panic",
      note: "Use this when attention makes you visibly lose steadiness.",
    },
    {
      slug: "clarity-and-anti-rambling-curriculum",
      label: "Ramble Or Drift",
      note: "Use this when your point arrives too late or your structure collapses.",
    },
    {
      slug: "delivery-and-vocal-presence-curriculum",
      label: "Sound Flat",
      note: "Use this when the message is fine but the delivery is hard to stay with.",
    },
    {
      slug: "business-communication-curriculum",
      label: "Need Work Credibility",
      note: "Use this when meetings, updates, or recommendations are where the problem shows up.",
    },
  ];

  renderScenarioCurriculumCollection("problem-highlight-grid", specs);
}

function renderContextHighlights() {
  const root = document.getElementById("context-highlight-grid");
  if (!root || !data) return;

  const specs = [
    {
      slug: "business-communication-curriculum",
      label: "Meetings And Updates",
      note: "Use this when the work setting is the main place your speaking breaks down.",
    },
    {
      slug: "interview-and-hard-question-curriculum",
      label: "Interviews And Q&A",
      note: "Use this when pressure questions are the real communication constraint.",
    },
    {
      slug: "presentation-and-formal-speaking-curriculum",
      label: "Talks And Formal Openings",
      note: "Use this when all-eyes-on-you moments are the thing to improve.",
    },
    {
      slug: "social-speaking-and-humor-curriculum",
      label: "Social Conversation",
      note: "Use this when warmth, ease, and humor matter more than formal polish.",
    },
  ];

  renderScenarioCurriculumCollection("context-highlight-grid", specs);
}

function renderPracticePage() {
  const quickPickSpecs = [
    {
      slug: "first-session-quickstart",
      label: "Brand New",
      note: "Best first move if you just opened the atlas and need a fast baseline.",
    },
    {
      slug: "daily-speaking-session-templates",
      label: "Need Reps Today",
      note: "Best when you want one concrete session right now.",
    },
    {
      slug: "weekly-practice-sprints",
      label: "Want A Better Week",
      note: "Best when you already know the bottleneck and want seven days of reps.",
    },
    {
      slug: "month-one-speaking-training-plan",
      label: "Serious Reset",
      note: "Best when you want a disciplined month-one training block.",
    },
    {
      slug: "speaking-preflight-checklists",
      label: "Event Soon",
      note: "Best when a meeting, interview, talk, or social moment is close.",
    },
    {
      slug: "stalled-progress-troubleshooting-guide",
      label: "Not Improving",
      note: "Best when effort is happening but visible change is still weak.",
    },
    {
      slug: "30-day-speaking-challenge",
      label: "Run A 30-Day Challenge",
      note: "Best when you want a guided month with weekly focus, live assignments, and a month-end retest.",
    },
    {
      slug: "30-day-challenge-tracker",
      label: "Track The 30 Days",
      note: "Best when you already chose the challenge and now want a clear sheet for logging reps and weekly adjustments.",
    },
    {
      slug: "live-field-missions",
      label: "Use It Live This Week",
      note: "Best when the next step is taking one move into a real conversation, meeting, interview, or presentation before Friday.",
    },
    {
      slug: "partner-roleplay-facilitator-guide",
      label: "Run It With A Partner",
      note: "Best when you want a facilitator to deliver the follow-up turns, score the rep, and keep the practice realistic.",
    },
    {
      slug: "presentation-interview-deployment-examples",
      label: "Use It Under Attention",
      note: "Best when you want room-level examples for formal openings, interview answers, Q&A, and demo narration before the next high-stakes rep.",
    },
    {
      slug: "social-humor-deployment-examples",
      label: "Use It Socially",
      note: "Best when you want room-level social and humor examples before the next event, date, offsite, or group conversation.",
    },
    {
      slug: "workplace-speaking-deployment-examples",
      label: "Use It At Work",
      note: "Best when you want room-level business examples before your next work meeting, interview, presentation, or pushback conversation.",
    },
    {
      slug: "worked-speaking-situation-examples",
      label: "Use It In Real Life",
      note: "Best when you want realistic before-and-after examples before trying your own version.",
    },
    {
      slug: "speaking-move-deployment-examples",
      label: "Deploy The Move",
      note: "Best when you want solid room-level examples of how a strong move gets used in work, pressure, presentation, humor, or social situations.",
    },
    {
      slug: "speaker-pattern-playbook",
      label: "Steal The Move",
      note: "Best when you want a reusable speaking move, where to use it, and a starter line shape you can adapt fast.",
    },
    {
      slug: "speaker-pattern-drill-cards",
      label: "Train The Move",
      note: "Best when you want a 2-minute pattern drill, a good-rep target, and a live-use challenge for the same week.",
    },
    {
      slug: "speaking-pattern-practice-recipes",
      label: "Run A Recipe",
      note: "Best when you want a whole problem-first practice mini-stack without choosing the pieces yourself.",
    },
    {
      slug: "speaking-practice-case-studies",
      label: "Follow A Learner",
      note: "Best when you want realistic examples of someone using the files, doing the reps, and trying the move live.",
    },
    {
      slug: "speaking-roleplay-packs",
      label: "Practice The Exchange",
      note: "Best when you want a realistic prompt, a stronger answer, and a harder second turn to rehearse.",
    },
    {
      slug: "roleplay-feedback-scorecard",
      label: "Score The Exchange",
      note: "Best when you want a simple rubric for first-sentence clarity, pressure composure, and second-turn resilience.",
    },
    {
      slug: "weekly-plans-by-learner-type",
      label: "Run A Week",
      note: "Best when you want the next seven days planned for your learner type instead of building the week yourself.",
    },
    {
      slug: "speaker-patterns-by-context",
      label: "Pick By Situation",
      note: "Best when you want the right move chosen for meetings, interviews, presentations, social moments, humor, or pressure.",
    },
    {
      slug: "real-speaker-exemplars",
      label: "See It Used Well",
      note: "Best when you want source-backed examples of actual speakers using the move before you run your own rep.",
    },
    {
      slug: "real-world-speaking-application-examples",
      label: "Borrow It For Your Room",
      note: "Best when you want a named speaker, the exact move they used, and a strong adaptation for your next meeting, interview, presentation, or conversation.",
    },
    {
      slug: "watch-before-you-practice-guide",
      label: "Example First",
      note: "Best when you want source-backed watching before you start reps.",
    },
  ];

  renderScenarioCurriculumCollection("practice-quickpick-grid", quickPickSpecs);

  const problemSpecs = [
    {
      slug: "confidence-and-composure-curriculum",
      label: "Freeze Or Panic",
      note: "Best when attention makes you rush, blank, or visibly lose steadiness.",
    },
    {
      slug: "clarity-and-anti-rambling-curriculum",
      label: "Ramble Or Drift",
      note: "Best when your point arrives too late or explanations stay messy.",
    },
    {
      slug: "delivery-and-vocal-presence-curriculum",
      label: "Sound Flat",
      note: "Best when the content is decent but the delivery is hard to listen to.",
    },
    {
      slug: "business-communication-curriculum",
      label: "Need Work Credibility",
      note: "Best when meetings, updates, recommendations, or executive presence are the issue.",
    },
    {
      slug: "interview-and-hard-question-curriculum",
      label: "Hard Questions",
      note: "Best when pressure questions make you ramble, hedge, or lose composure.",
    },
    {
      slug: "social-speaking-and-humor-curriculum",
      label: "Social Warmth",
      note: "Best when conversation feels stiff, overcareful, or humor feels forced.",
    },
    {
      slug: "storytelling-and-memorability-curriculum",
      label: "Forgettable Stories",
      note: "Best when your stories stay abstract, flat, or hard to remember.",
    },
  ];

  renderScenarioCurriculumCollection("practice-problem-grid", problemSpecs);

  const contextSpecs = [
    {
      slug: "business-communication-curriculum",
      label: "Meetings And Updates",
      note: "Best when the work setting is the problem: updates, recommendations, clarity, and executive presence.",
    },
    {
      slug: "interview-and-hard-question-curriculum",
      label: "Interviews And Q&A",
      note: "Best when pressure questions are where your speaking breaks down most.",
    },
    {
      slug: "presentation-and-formal-speaking-curriculum",
      label: "Talks And Formal Openings",
      note: "Best when the challenge is holding a room once all eyes are on you.",
    },
    {
      slug: "skeptical-room-and-objection-handling-curriculum",
      label: "Skeptical Stakeholders",
      note: "Best when you need calm persuasion under pushback, friction, or objections.",
    },
    {
      slug: "social-speaking-and-humor-curriculum",
      label: "Social Conversation",
      note: "Best when warmth, ease, and humor are the real constraint.",
    },
    {
      slug: "storytelling-and-memorability-curriculum",
      label: "Stories That Need To Land",
      note: "Best when you need your spoken stories to feel vivid, memorable, and worth following.",
    },
  ];

  renderScenarioCurriculumCollection("practice-context-grid", contextSpecs);

  const sections = [
    {
      rootId: "practice-system-grid",
      slugs: [
        "speaking-practice-operating-system",
        "practice-stack-bundles",
        "start-here-decision-guide",
        "speaking-diagnosis-guide",
      ],
    },
    {
      rootId: "practice-bundle-grid",
      slugs: [
        "practice-stack-bundles",
        "speaking-common-mistakes-and-fixes",
        "live-speaking-phrase-bank",
        "real-life-speaking-simulations",
        "first-session-quickstart",
        "context-based-speaking-routes",
        "focused-weekly-improvement-actions",
      ],
    },
    {
      rootId: "practice-rhythm-grid",
      slugs: [
        "daily-speaking-session-templates",
        "weekly-practice-sprints",
        "month-one-speaking-training-plan",
        "time-budget-practice-guide",
      ],
    },
    {
      rootId: "practice-pressure-grid",
      slugs: [
        "speaking-preflight-checklists",
        "stalled-progress-troubleshooting-guide",
        "confidence-and-composure-curriculum",
        "interview-and-hard-question-curriculum",
      ],
    },
    {
      rootId: "practice-support-grid",
      slugs: [
        "speaking-common-mistakes-and-fixes",
        "live-speaking-phrase-bank",
        "real-life-speaking-simulations",
        "watch-before-you-practice-guide",
        "evidence-backed-drill-map",
        "speaking-sample-prompt-bank",
        "speaking-progress-scorecard",
        "listener-feedback-template",
        "weekly-review-and-adjustment-template",
      ],
    },
  ];

  sections.forEach(({ rootId, slugs }) => {
    const items = slugs
      .map((slug) => curriculum.find((entry) => entry.slug === slug))
      .filter(Boolean);
    renderCurriculumCollection(rootId, items);
  });

  const practiceMatrixSlugs = [
    "best-route-if-you-need-something-useful-today",
    "best-route-if-you-want-one-solid-week-of-progress",
    "best-route-if-you-need-realistic-rehearsal-for-a-live-situation",
    "best-route-if-you-want-to-watch-strong-examples-before-acting",
    "best-route-if-you-want-an-exact-borrowed-version-before-practicing",
    "best-route-if-a-real-event-is-close",
    "best-route-if-you-are-practicing-but-not-improving",
    "best-route-if-the-repo-feels-rich-but-overwhelming",
  ];

  const matrixItems = practiceMatrixSlugs
    .map((slug) => matrix.find((entry) => entry.slug === slug))
    .filter(Boolean);

  renderMatrixCollection("practice-matrix-grid", matrixItems);
}

function renderArtifacts() {
  const root = document.getElementById("artifact-grid");
  if (!root || !data) return;
  root.innerHTML = artifacts
    .map(
      (item) => `
        <article class="artifact">
          <h3>${item.title}</h3>
          <p>${item.description}</p>
        </article>
      `,
    )
    .join("");
}

function getCollection(type) {
  if (type === "corpus") return corpora;
  if (type === "concept") return concepts;
  if (type === "drill") return drills;
  if (type === "pathway") return pathways;
  if (type === "example") return examples;
  if (type === "session") return sessions;
  if (type === "source") return sources;
  if (type === "evidence") return evidence;
  if (type === "matrix") return matrix;
  if (type === "roadmap") return roadmap;
  if (type === "contrast") return contrasts;
  if (type === "curriculum") return curriculum;
  return [];
}

function findBySlug(type, slug) {
  return getCollection(type).find((entry) => entry.slug === slug);
}

function dedupeItems(items) {
  const seen = new Set();
  return items.filter((item) => {
    if (!item) return false;
    const key = `${item.type}:${item.slug}`;
    if (seen.has(key)) return false;
    seen.add(key);
    return true;
  });
}

function limitItems(items, limit = 12) {
  return items.slice(0, limit);
}

function buildRelatedItems(type, item) {
  const related = [];

  if (type === "corpus") {
    (item.conceptSlugs ?? []).forEach((slug) => {
      const target = findBySlug("concept", slug);
      if (target) related.push({ type: "concept", ...target });
    });
    sessions
      .filter((entry) => entry.corpusSlug === item.slug)
      .forEach((entry) => related.push({ type: "session", ...entry }));
    drills
      .filter((entry) => entry.corpusSlug === item.slug)
      .forEach((entry) => related.push({ type: "drill", ...entry }));
    pathways
      .filter((entry) => (entry.corpusSlugs ?? []).includes(item.slug))
      .forEach((entry) => related.push({ type: "pathway", ...entry }));
    examples
      .filter((entry) => (entry.corpusSlugs ?? []).includes(item.slug))
      .forEach((entry) => related.push({ type: "example", ...entry }));
  }

  if (type === "concept") {
    (item.corpusSlugs ?? []).forEach((slug) => {
      const target = findBySlug("corpus", slug);
      if (target) related.push({ type: "corpus", ...target });
    });
    sessions
      .filter((entry) => (entry.conceptSlugs ?? []).includes(item.slug))
      .forEach((entry) => related.push({ type: "session", ...entry }));
    drills
      .filter((entry) => (entry.conceptSlugs ?? []).includes(item.slug))
      .forEach((entry) => related.push({ type: "drill", ...entry }));
    pathways
      .filter((entry) => (entry.conceptSlugs ?? []).includes(item.slug))
      .forEach((entry) => related.push({ type: "pathway", ...entry }));
    examples
      .filter((entry) => (entry.conceptSlugs ?? []).includes(item.slug))
      .forEach((entry) => related.push({ type: "example", ...entry }));
    evidence
      .filter((entry) => (entry.conceptSlugs ?? []).includes(item.slug))
      .forEach((entry) => related.push({ type: "evidence", ...entry }));
    contrasts
      .filter((entry) => (entry.conceptSlugs ?? []).includes(item.slug))
      .forEach((entry) => related.push({ type: "contrast", ...entry }));
  }

  if (type === "drill") {
    if (item.corpusSlug) {
      const target = findBySlug("corpus", item.corpusSlug);
      if (target) related.push({ type: "corpus", ...target });
    }
    (item.conceptSlugs ?? []).forEach((slug) => {
      const target = findBySlug("concept", slug);
      if (target) related.push({ type: "concept", ...target });
    });
    pathways
      .filter((entry) => (entry.drillSlugs ?? []).includes(item.slug))
      .forEach((entry) => related.push({ type: "pathway", ...entry }));
  }

  if (type === "pathway") {
    (item.corpusSlugs ?? []).forEach((slug) => {
      const target = findBySlug("corpus", slug);
      if (target) related.push({ type: "corpus", ...target });
    });
    sessions
      .filter((entry) => (entry.pathwaySlugs ?? []).includes(item.slug))
      .forEach((entry) => related.push({ type: "session", ...entry }));
    (item.conceptSlugs ?? []).forEach((slug) => {
      const target = findBySlug("concept", slug);
      if (target) related.push({ type: "concept", ...target });
    });
    (item.drillSlugs ?? []).forEach((slug) => {
      const target = findBySlug("drill", slug);
      if (target) related.push({ type: "drill", ...target });
    });
    (item.exampleSlugs ?? []).forEach((slug) => {
      const target = findBySlug("example", slug);
      if (target) related.push({ type: "example", ...target });
    });
    evidence
      .filter((entry) => (entry.pathwaySlugs ?? []).includes(item.slug))
      .forEach((entry) => related.push({ type: "evidence", ...entry }));
    contrasts
      .filter((entry) => (entry.pathwaySlugs ?? []).includes(item.slug))
      .forEach((entry) => related.push({ type: "contrast", ...entry }));
  }

  if (type === "example") {
    (item.corpusSlugs ?? []).forEach((slug) => {
      const target = findBySlug("corpus", slug);
      if (target) related.push({ type: "corpus", ...target });
    });
    sessions
      .filter((entry) => (entry.exampleSlugs ?? []).includes(item.slug))
      .forEach((entry) => related.push({ type: "session", ...entry }));
    (item.conceptSlugs ?? []).forEach((slug) => {
      const target = findBySlug("concept", slug);
      if (target) related.push({ type: "concept", ...target });
    });
    (item.pathwaySlugs ?? []).forEach((slug) => {
      const target = findBySlug("pathway", slug);
      if (target) related.push({ type: "pathway", ...target });
    });
    evidence
      .filter((entry) => (entry.conceptSlugs ?? []).some((slug) => (item.conceptSlugs ?? []).includes(slug)))
      .slice(0, 3)
      .forEach((entry) => related.push({ type: "evidence", ...entry }));
    contrasts
      .filter((entry) => (entry.exampleSlugs ?? []).includes(item.slug))
      .forEach((entry) => related.push({ type: "contrast", ...entry }));
  }

  if (type === "session") {
    if (item.corpusSlug) {
      const target = findBySlug("corpus", item.corpusSlug);
      if (target) related.push({ type: "corpus", ...target });
    }
    (item.conceptSlugs ?? []).forEach((slug) => {
      const target = findBySlug("concept", slug);
      if (target) related.push({ type: "concept", ...target });
    });
    (item.pathwaySlugs ?? []).forEach((slug) => {
      const target = findBySlug("pathway", slug);
      if (target) related.push({ type: "pathway", ...target });
    });
    (item.exampleSlugs ?? []).forEach((slug) => {
      const target = findBySlug("example", slug);
      if (target) related.push({ type: "example", ...target });
    });
    evidence
      .filter((entry) => (entry.sessionSlugs ?? []).includes(item.slug))
      .forEach((entry) => related.push({ type: "evidence", ...entry }));
  }

  if (type === "source") {
    (item.corpusSlugs ?? []).forEach((slug) => {
      const target = findBySlug("corpus", slug);
      if (target) related.push({ type: "corpus", ...target });
    });
    concepts
      .filter((entry) => (entry.corpusSlugs ?? []).some((slug) => (item.corpusSlugs ?? []).includes(slug)))
      .slice(0, 4)
      .forEach((entry) => related.push({ type: "concept", ...entry }));
    pathways
      .filter((entry) => (entry.corpusSlugs ?? []).some((slug) => (item.corpusSlugs ?? []).includes(slug)))
      .slice(0, 3)
      .forEach((entry) => related.push({ type: "pathway", ...entry }));
  }

  if (type === "evidence") {
    (item.corpusSlugs ?? []).forEach((slug) => {
      const target = findBySlug("corpus", slug);
      if (target) related.push({ type: "corpus", ...target });
    });
    (item.conceptSlugs ?? []).forEach((slug) => {
      const target = findBySlug("concept", slug);
      if (target) related.push({ type: "concept", ...target });
    });
    (item.pathwaySlugs ?? []).forEach((slug) => {
      const target = findBySlug("pathway", slug);
      if (target) related.push({ type: "pathway", ...target });
    });
    (item.sessionSlugs ?? []).forEach((slug) => {
      const target = findBySlug("session", slug);
      if (target) related.push({ type: "session", ...target });
    });
    contrasts
      .filter((entry) => (entry.evidenceSlugs ?? []).includes(item.slug))
      .forEach((entry) => related.push({ type: "contrast", ...entry }));
  }

  if (type === "matrix") {
    (item.corpusSlugs ?? []).forEach((slug) => {
      const target = findBySlug("corpus", slug);
      if (target) related.push({ type: "corpus", ...target });
    });
    (item.conceptSlugs ?? []).forEach((slug) => {
      const target = findBySlug("concept", slug);
      if (target) related.push({ type: "concept", ...target });
    });
    (item.pathwaySlugs ?? []).forEach((slug) => {
      const target = findBySlug("pathway", slug);
      if (target) related.push({ type: "pathway", ...target });
    });
    sources
      .filter((entry) => (entry.corpusSlugs ?? []).some((slug) => (item.corpusSlugs ?? []).includes(slug)))
      .slice(0, 3)
      .forEach((entry) => related.push({ type: "source", ...entry }));
  }

  if (type === "roadmap") {
    (item.conceptSlugs ?? []).forEach((slug) => {
      const target = findBySlug("concept", slug);
      if (target) related.push({ type: "concept", ...target });
    });
    (item.sourceSlugs ?? []).forEach((slug) => {
      const target = findBySlug("source", slug);
      if (target) related.push({ type: "source", ...target });
    });
    evidence
      .filter((entry) => (item.focus ?? []).some((focus) => (entry.focus ?? []).includes(focus)))
      .slice(0, 3)
      .forEach((entry) => related.push({ type: "evidence", ...entry }));
  }

  if (type === "contrast") {
    (item.conceptSlugs ?? []).forEach((slug) => {
      const target = findBySlug("concept", slug);
      if (target) related.push({ type: "concept", ...target });
    });
    (item.pathwaySlugs ?? []).forEach((slug) => {
      const target = findBySlug("pathway", slug);
      if (target) related.push({ type: "pathway", ...target });
    });
    (item.exampleSlugs ?? []).forEach((slug) => {
      const target = findBySlug("example", slug);
      if (target) related.push({ type: "example", ...target });
    });
    (item.evidenceSlugs ?? []).forEach((slug) => {
      const target = findBySlug("evidence", slug);
      if (target) related.push({ type: "evidence", ...target });
    });
  }

  if (type === "curriculum") {
    (item.pathwaySlugs ?? []).forEach((slug) => {
      const target = findBySlug("pathway", slug);
      if (target) related.push({ type: "pathway", ...target });
    });
    (item.conceptSlugs ?? []).forEach((slug) => {
      const target = findBySlug("concept", slug);
      if (target) related.push({ type: "concept", ...target });
    });
    (item.sessionSlugs ?? []).forEach((slug) => {
      const target = findBySlug("session", slug);
      if (target) related.push({ type: "session", ...target });
    });
    (item.drillSlugs ?? []).forEach((slug) => {
      const target = findBySlug("drill", slug);
      if (target) related.push({ type: "drill", ...target });
    });
    (item.exampleSlugs ?? []).forEach((slug) => {
      const target = findBySlug("example", slug);
      if (target) related.push({ type: "example", ...target });
    });
    (item.evidenceSlugs ?? []).forEach((slug) => {
      const target = findBySlug("evidence", slug);
      if (target) related.push({ type: "evidence", ...target });
    });
  }

  return dedupeItems(related);
}

function groupRelatedItems(items) {
  const orderedTypes = [
    "curriculum",
    "pathway",
    "concept",
    "drill",
    "example",
    "session",
    "evidence",
    "corpus",
    "source",
    "matrix",
    "contrast",
    "roadmap",
  ];

  return orderedTypes
    .map((type) => ({
      type,
      items: limitItems(items.filter((entry) => entry.type === type), 6),
    }))
    .filter((group) => group.items.length);
}

function relatedGroupTitle(type) {
  const titles = {
    curriculum: "Related Curricula",
    pathway: "Related Pathways",
    concept: "Related Concepts",
    drill: "Related Drills",
    example: "Related Example Sets",
    session: "Related Sessions",
    evidence: "Related Evidence",
    corpus: "Related Corpora",
    source: "Related Sources",
    matrix: "Related Matrix Entries",
    contrast: "Related Contrast Cases",
    roadmap: "Related Roadmap Entries",
  };

  return titles[type] ?? "Related Items";
}

function renderRelatedSection(items) {
  if (!items.length) return "";

  const groups = groupRelatedItems(items);

  return `
    <section class="section">
      <div class="section-heading">
        <p class="eyebrow">Connected Material</p>
        <h2>Where To Go Next</h2>
        <p>
          These linked items connect this page back into the wider speaking
          atlas so the reader can move from source to concept to practice.
        </p>
      </div>
      ${groups
        .map(
          (group) => `
            <div class="section-heading">
              <p class="eyebrow">${detailLabelByType[group.type] ?? "Related Item"}</p>
              <h2>${relatedGroupTitle(group.type)}</h2>
            </div>
            <div class="card-grid card-grid--three">
              ${group.items
                .map(
                  (entry) => `
                    <article class="card">
                      <a class="card-link" href="${detailUrl(entry.type, entry.slug)}">
                        <span class="small-label">${detailLabelByType[entry.type] ?? "Related Item"}</span>
                        <h3>${entry.title}</h3>
                        <p>${entry.summary}</p>
                      </a>
                    </article>
                  `,
                )
                .join("")}
            </div>
          `,
        )
        .join("")}
    </section>
  `;
}

function renderPinnedCardsSection(title, eyebrow, type, items) {
  if (!items.length) return "";

  return `
    <section class="section">
      <div class="section-heading">
        <p class="eyebrow">${eyebrow}</p>
        <h2>${title}</h2>
      </div>
      <div class="card-grid card-grid--three">
        ${items
          .map(
            (entry) => `
              <article class="card">
                <a class="card-link" href="${detailUrl(type, entry.slug)}">
                  <span class="small-label">${detailLabelByType[type] ?? "Linked Item"}</span>
                  <h3>${entry.title}</h3>
                  <p>${entry.summary}</p>
                </a>
              </article>
            `,
          )
          .join("")}
      </div>
    </section>
  `;
}

function resolveLinkedItems(type, slugs) {
  return (slugs ?? [])
    .map((slug) => findBySlug(type, slug))
    .filter(Boolean);
}

function renderPinnedDetailSections(type, item) {
  if (!["curriculum", "matrix", "pathway", "example"].includes(type)) return "";

  const pinnedSessions = resolveLinkedItems("session", item.sessionSlugs);
  const pinnedEvidence = resolveLinkedItems("evidence", item.evidenceSlugs);
  const pinnedDrills = resolveLinkedItems("drill", item.drillSlugs);
  const pinnedExamples = resolveLinkedItems("example", item.exampleSlugs);

  if (!pinnedSessions.length && !pinnedEvidence.length && !pinnedDrills.length && !pinnedExamples.length) {
    return "";
  }

  return `
    ${renderPinnedCardsSection("Transcript-Backed Sessions", "Watch First", "session", pinnedSessions)}
    ${renderPinnedCardsSection("Evidence Moments", "Transcript Anchors", "evidence", pinnedEvidence)}
    ${renderPinnedCardsSection("Recommended Drills", "Practice Links", "drill", pinnedDrills)}
    ${renderPinnedCardsSection("Example Sets", "Study Examples", "example", pinnedExamples)}
  `;
}

function renderApplicationTransferSection(type, item) {
  const eligibleTypes = new Set([
    "curriculum",
    "pathway",
    "matrix",
    "example",
    "corpus",
    "concept",
    "session",
    "source",
    "evidence",
    "contrast",
    "roadmap",
  ]);
  if (!eligibleTypes.has(type)) return "";

  const applicationItem = findBySlug("curriculum", "real-world-speaking-application-examples");
  const approachItem = findBySlug("curriculum", "transcript-backed-concrete-speaking-approaches");
  const workedItem = findBySlug("curriculum", "worked-speaking-situation-examples");
  const speakerItem = findBySlug("curriculum", "real-speaker-exemplars");
  if (!applicationItem || !approachItem || !workedItem || !speakerItem) return "";
  if (item.slug === "real-world-speaking-application-examples") return "";

  return `
    <section class="section section--split">
      <div class="panel">
        <p class="eyebrow">Borrow The Move</p>
        <h2>Turn This Page Into A Stronger Real-World Version Faster.</h2>
        <p>
          If this page still feels a little too abstract, move next into the
          concrete transfer layer: start with the named approach, then study
          the real speaker, the matching room, and the stronger borrowed
          version before you run your own rep.
        </p>
        <ul class="stack-list stack-list--tight">
          <li><a class="inline-link-strong" href="${detailUrl("curriculum", approachItem.slug)}">Open transcript-backed concrete speaking approaches</a></li>
          <li><a class="inline-link-strong" href="${detailUrl("curriculum", applicationItem.slug)}">Open real-world speaking application examples</a></li>
          <li><a class="inline-link-strong" href="${detailUrl("curriculum", workedItem.slug)}">Compare weak and strong real-life wording</a></li>
          <li><a class="inline-link-strong" href="${detailUrl("curriculum", speakerItem.slug)}">Study the move used well by real speakers</a></li>
          <li><a class="inline-link-strong" href="./practice.html">Open the practice surface for reps, sprints, and live transfer</a></li>
        </ul>
      </div>
      <div class="panel panel--dark">
        <p class="eyebrow">Use It Next</p>
        <h2>Keep The Transfer Concrete.</h2>
        <p>
          The best sequence is simple: watch the move, borrow the shape, rewrite
          it in your own words, then use it in one meeting, interview,
          presentation, or conversation within 72 hours.
        </p>
        <ul class="stack-list stack-list--tight">
          <li>Pick one example that resembles your next real room.</li>
          <li>Rewrite the stronger version into vocabulary you would actually use.</li>
          <li>Run one recorded rep or one live rep before browsing more.</li>
        </ul>
      </div>
    </section>
  `;
}

function renderListSection(title, items) {
  if (!items?.length) return "";
  return `
    <h2>${title}</h2>
    <ul class="detail-list">
      ${items.map((entry) => `<li>${entry}</li>`).join("")}
    </ul>
  `;
}

function fileHref(path) {
  if (!path) return "#";
  return `../${path.replace(/^\.?\//, "")}`;
}

function fileLabel(path) {
  if (!path) return "Supporting file";
  const parts = path.split("/");
  return parts[parts.length - 1] || path;
}

function renderSupportingFilesSection(files) {
  if (!files?.length) {
    return `<p>No supporting file list has been attached yet.</p>`;
  }

  return `
    <ul class="detail-list">
      ${files
        .map(
          (file) => `
            <li>
              <a href="${fileHref(file)}">${fileLabel(file)}</a>
              <div class="small-label">${file}</div>
            </li>
          `,
        )
        .join("")}
    </ul>
  `;
}

function renderDetailNav(type) {
  const sectionHref = sectionPageByType[type] ?? "./index.html";
  const sectionLabel = sectionLabelByType[type] ?? "Atlas Section";
  const extraLinks = [];

  if (type === "curriculum") {
    extraLinks.push(`<a class="detail-nav__link" href="./curriculum.html">Back to Curriculum Page</a>`);
    if (practiceCurriculumSlugs.has(new URLSearchParams(window.location.search).get("slug"))) {
      extraLinks.push(`<a class="detail-nav__link" href="./practice.html">Open Practice Page</a>`);
    }
  }

  if (type === "matrix") {
    extraLinks.push(`<a class="detail-nav__link" href="./matrix.html">Back to Matrix Page</a>`);
    if (practiceMatrixSlugs.has(new URLSearchParams(window.location.search).get("slug"))) {
      extraLinks.push(`<a class="detail-nav__link" href="./practice.html">Open Practice Page</a>`);
    }
  }

  return `
    <div class="detail-nav">
      <a class="detail-nav__link" href="./index.html">Back to Atlas Home</a>
      <a class="detail-nav__link" href="${sectionHref}">Back to ${sectionLabel}</a>
      ${extraLinks.join("")}
    </div>
  `;
}

function renderDetail() {
  const root = document.getElementById("detail-root");
  if (!root || !data) return;

  const params = new URLSearchParams(window.location.search);
  const type = params.get("type");
  const slug = params.get("slug");
  const collection = getCollection(type);
  const item = collection.find((entry) => entry.slug === slug);

  if (!item) {
    root.innerHTML = `
      <section class="detail-shell">
        <header class="detail-hero">
          <p class="eyebrow">Detail View</p>
          <h1>Detail Not Found</h1>
          <p>The requested item is missing from the current site data.</p>
        </header>
      </section>
    `;
    return;
  }

  const metadata = [];
  if (item.family) metadata.push(item.family);
  if (item.corpus) metadata.push(item.corpus);
  if (item.label) metadata.push(item.label);
  if (item.videos) metadata.push(`${item.videos} videos`);
  if (item.words) metadata.push(`${item.words} words`);

  const focusOrConcepts = item.focus ?? item.concepts ?? [];
  const linkedFiles = item.linkedFiles ?? [];
  const relatedItems = buildRelatedItems(type, item);
  const bestFor = item.bestFor ?? [];
  const studyQuestions = item.studyQuestions ?? [];
  const evidenceRefs = item.evidenceRefs ?? [];
  const pinnedSections = renderPinnedDetailSections(type, item);
  const applicationTransferSection = renderApplicationTransferSection(type, item);

  root.innerHTML = `
    <section class="detail-shell">
      <header class="detail-hero">
        ${renderDetailNav(type)}
        <p class="eyebrow">${detailLabelByType[type] ?? "Detail View"}</p>
        <h1>${item.title}</h1>
        <p class="hero-text">${item.summary}</p>
        ${metadata.length ? `<div class="meta">${metadata.map((meta) => `<span>${meta}</span>`).join("")}</div>` : ""}
      </header>
      <div class="detail-grid">
        <article class="detail-body">
          <h2>Why This Matters</h2>
          <p>${item.whyItMatters ?? "This item is part of the current first-wave speaking research package."}</p>
          ${item.startHere ? `
            <h2>Start Here If</h2>
            <p>${item.startHere}</p>
          ` : ""}
          ${renderListSection("Best For", bestFor)}
          ${focusOrConcepts.length ? `
            <h2>Current Focus</h2>
            <ul class="detail-list">
              ${focusOrConcepts.map((entry) => `<li>${entry}</li>`).join("")}
            </ul>
          ` : ""}
          ${renderListSection("Evidence Anchors", evidenceRefs)}
          ${renderListSection("Study Questions", studyQuestions)}
        </article>
        <aside class="detail-side">
          <h2>Supporting Files</h2>
          ${renderSupportingFilesSection(linkedFiles)}
        </aside>
      </div>
    </section>
    ${applicationTransferSection}
    ${pinnedSections}
    ${renderRelatedSection(relatedItems)}
  `;
}

const corpora = data?.corpora ?? [];
const concepts = data?.concepts ?? [];
const drills = data?.drills ?? [];
const pathways = data?.pathways ?? [];
const examples = data?.examples ?? [];
const sessions = data?.sessions ?? [];
const sources = data?.sources ?? [];
const evidence = data?.evidence ?? [];
const matrix = data?.matrix ?? [];
const roadmap = data?.roadmap ?? [];
const contrasts = data?.contrasts ?? [];
const curriculum = data?.curriculum ?? [];
const artifacts = data?.artifacts ?? [];

renderCorpora();
renderConcepts();
renderDrills();
renderPathways();
renderExamples();
renderExampleHighlights();
renderSessions();
renderSources();
renderEvidence();
renderMatrix();
renderRoadmap();
renderContrasts();
renderCurriculum();
renderCurriculumRoutes();
renderCurriculumTracks();
renderCurriculumSupport();
renderStartRoutes();
renderPracticeHighlights();
renderProblemHighlights();
renderContextHighlights();
renderPracticePage();
renderArtifacts();
renderDetail();
