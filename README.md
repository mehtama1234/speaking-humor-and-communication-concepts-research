# Speaking, Humor, and Communication Concepts Research

Reusable workspace for building a transcript-backed concept and example atlas
around:

- public speaking
- conversational fluency
- speaking confidence
- humor in speech
- storytelling
- charisma and presence
- fast thinking under pressure

The goal is not just to collect speaking tips. The goal is to identify
repeatable approaches, example patterns, drills, and concept clusters that help
someone become a stronger speaker in real settings:

- meetings
- interviews
- presentations
- social conversation
- storytelling
- persuasive speaking
- humorous speaking

The working end-to-end goal is defined in
`analysis/project-objective.md`: this repo should grow into a transcript-backed
speaking improvement system where a learner can move from source selection to
transcript synthesis to themes, concepts, examples, drills, pathways, and a
browsable HTML interface without having to reconstruct the structure manually.

## Governing rule

This repo should optimize for `approach extraction`, not `video summary`.

That means the main job is to turn transcript-backed source material into:

- concrete approaches
- named speaking moves
- repeatable drills
- phrase patterns
- weak-versus-strong examples
- real-room adaptations

If a note explains what a source said but does not help a learner speak better
in a real room, it is incomplete.

## Working goal

This folder is meant to answer a practical question:

What should someone study, what should they practice, and in what order if they
want to become a better speaker in real life?

That means the repo should keep getting stronger at five layers:

- source curation
- transcript capture and session synthesis
- theme and concept compression across corpora
- drill, example, and evidence layers tied to real learner problems
- reader-facing site pages that make the package easy to browse

The most important layer between concept and practice is:

- transcript-backed approach inventories

That is where source material becomes something a learner can actually deploy.

## First build direction

Start with strong YouTube channels that are useful for:

- practical speaking exercises
- communication frameworks
- humor and storytelling examples
- stage presence and delivery
- examples of clear, persuasive speech

## Initial structure

- `analysis/`: project objective, channel shortlist, future concept/theme work
- `concepts/`: durable cross-corpus concept pages
- `raw-material/`: future manifests, transcripts, notes, and source captures
- `site/`: future reader-facing HTML outputs

## Seed channels already identified

See:

- `analysis/project-objective.md`
- `analysis/youtube-channel-shortlist.md`
- `analysis/youtube-channel-shortlist.json`
- `analysis/source-map.md`
- `analysis/source-map.json`

## Current transcript-backed corpora

The repo now has ten transcript-backed starter corpora:

- `raw-material/youtube/starter-manifests/ultraspeaking-wave-1.json`
- `raw-material/youtube/starter-manifests/vinh-giang-wave-1.json`
- `raw-material/youtube/starter-manifests/think-fast-talk-smart-wave-1.json`
- `raw-material/youtube/starter-manifests/charisma-on-command-wave-1.json`
- `raw-material/youtube/starter-manifests/matthew-dicks-wave-1.json`
- `raw-material/youtube/starter-manifests/jefferson-fisher-wave-1.json`
- `raw-material/youtube/starter-manifests/chad-littlefield-wave-1.json`
- `raw-material/youtube/starter-manifests/alexander-lyon-wave-1.json`
- `raw-material/youtube/starter-manifests/toastmasters-wave-1.json`
- `raw-material/youtube/starter-manifests/andrew-tarvin-wave-1.json`

That gives the repo these current transcript-backed corpora:

- Ultraspeaking
- Vinh Giang
- Think Fast Talk Smart
- Charisma on Command
- Matthew Dicks
- Jefferson Fisher
- Chad Littlefield
- Communication Coach Alexander Lyon
- Toastmasters International
- Andrew Tarvin

Workflow notes are in:

- `analysis/starter-corpus-selection.md`

The transcript scripts now write corpus-specific outputs under:

- `raw-material/youtube/transcripts/<slug>/`

The first cross-corpus concept pages now live in:

- `concepts/confidence-as-visible-behavior.md`
- `concepts/speaking-under-pressure.md`
- `concepts/clarity-over-perfection.md`
- `concepts/audience-first-communication.md`
- `concepts/pause-as-strength.md`
- `concepts/speaking-without-a-script.md`
- `concepts/articulation-and-verbal-polish.md`
- `concepts/musicality.md`
- `concepts/structure-as-leverage.md`
- `concepts/humor-as-connection.md`
- `concepts/self-respect-over-approval-seeking.md`
- `concepts/curiosity-and-conversational-depth.md`
- `concepts/storytelling-as-lived-experience.md`
- `concepts/disagreement-without-domination.md`
- `concepts/warmth-versus-authority.md`
- `concepts/executive-presence.md`
- `concepts/quick-wittedness.md`
- `concepts/persuasion-and-influence.md`
- `concepts/humor-timing-and-collaborative-play.md`

The repo also now includes:

- `analysis/learner-pathways.md`
- `analysis/context-based-speaking-routes.md`
- `analysis/daily-speaking-session-templates.md`
- `analysis/delivery-and-vocal-presence-curriculum.md`
- `analysis/example-library.md`
- `analysis/evidence-moments.md`
- `analysis/first-session-quickstart.md`
- `analysis/focused-improvement-actions.md`
- `analysis/interview-and-hard-question-curriculum.md`
- `analysis/live-field-missions.md`
- `analysis/listener-feedback-template.md`
- `analysis/multilingual-clarity-and-accent-pressure-curriculum.md`
- `analysis/month-one-speaking-training-plan.md`
- `analysis/30-day-speaking-challenge.md`
- `analysis/30-day-challenge-tracker.md`
- `analysis/partner-roleplay-facilitator-guide.md`
- `analysis/speaking-diagnosis-guide.md`
- `analysis/speaking-preflight-checklists.md`
- `analysis/speaking-progress-scorecard.md`
- `analysis/speaking-pattern-practice-recipes.md`
- `analysis/speaking-practice-case-studies.md`
- `analysis/speaking-roleplay-packs.md`
- `analysis/speaking-sample-prompt-bank.md`
- `analysis/skeptical-room-and-objection-handling-curriculum.md`
- `analysis/storytelling-and-memorability-curriculum.md`
- `analysis/social-speaking-and-humor-curriculum.md`
- `analysis/social-humor-deployment-examples.md`
- `analysis/speaking-practice-operating-system.md`
- `analysis/start-here-decision-guide.md`
- `analysis/transcript-backed-concrete-speaking-approaches.md`
- `analysis/stalled-progress-troubleshooting-guide.md`
- `analysis/time-budget-practice-guide.md`
- `analysis/workplace-speaking-deployment-examples.md`
- `analysis/weekly-review-and-adjustment-template.md`
- `analysis/weekly-practice-sprints.md`
- `analysis/weekly-plans-by-learner-type.md`
- `analysis/business-communication-curriculum.md`
- `analysis/featured-sessions.md`
- `analysis/clarity-and-anti-rambling-curriculum.md`
- `analysis/confidence-and-composure-curriculum.md`
- `analysis/next-wave-source-shortlist.md`
- `analysis/presentation-and-formal-speaking-curriculum.md`
- `analysis/presentation-interview-deployment-examples.md`
- `analysis/practice-stack-bundles.md`
- `analysis/real-speaker-exemplars.md`
- `analysis/real-world-speaking-application-examples.md`
- `analysis/roleplay-feedback-scorecard.md`
- `analysis/speaking-move-deployment-examples.md`
- `analysis/speaker-pattern-playbook.md`
- `analysis/speaker-pattern-drill-cards.md`
- `analysis/speaker-patterns-by-context.md`
- `analysis/worked-speaking-situation-examples.md`
- `analysis/charisma-on-command-wave-1-corpus-brief.md`
- `scripts/README.md`
- `scripts/validate_all.sh`
- `scripts/validate_markdown_refs.js`
- `scripts/validate_site_data.js`
- `site/concepts.html`
- `site/corpora.html`
- `site/curriculum.html`
- `site/detail.html`
- `site/drills.html`
- `site/evidence.html`
- `site/pathways.html`
- `site/examples.html`
- `site/index.html`
- `site/matrix.html`
- `site/practice.html`
- `site/roadmap.html`
- `site/sessions.html`
- `site/sources.html`

That means the current package is no longer just source capture plus concept
notes. It now has:

- transcript-backed corpora
- twenty-three durable concept pages
- drill candidates
- learner pathways
- context-based routes for meetings, interviews, presentations, and social speaking
- example study sets
- transcript-backed evidence moments
- a first-session quickstart for getting value in the first 30 to 60 minutes
- an interview and hard-question curriculum for calmer, clearer, more credible answers under pressure
- a diagnosis guide for choosing the right speaking starting point
- a daily session template layer for turning routes into exact practice blocks
- a clarity and anti-rambling curriculum for cleaner explanations and point-first answers
- a confidence and composure curriculum for visible steadiness, pause tolerance, and recovery
- a delivery and vocal presence curriculum for monotone speech, emphasis, and easier-to-listen-to delivery
- a listener feedback template for getting sharper outside signal
- a multilingual clarity and accent-pressure curriculum for intelligibility, confidence, and non-erasure
- a month-one plan for sequencing the first four weeks of speaking practice
- a presentation and formal speaking curriculum for talks, demos, and openings under attention
- a progress scorecard for measuring visible speaking change
- a pre-flight checklist layer for the minutes before real speaking situations
- a practice-stack bundle layer for choosing the right set of files by learner situation
- a practice operating system that clarifies which layer to use today, this week, this month, before events, or when stuck
- a real-speaker exemplar layer for studying named speakers and borrowing the move rather than the persona
- a comparison matrix that now helps choose both the right source and the right practice route
- a reusable prompt bank for baseline and retest speaking samples
- a skeptical-room and objection-handling curriculum for high-friction persuasion
- a storytelling and memorability curriculum for scene-building, openings, and vivid spoken narrative
- a social speaking and humor curriculum for warmth, conversation, and playful timing
- a start-here decision guide for choosing the right route into the atlas quickly
- a stalled-progress troubleshooting guide for debugging practice when improvement flattens
- a worked speaking situation layer for before-and-after real-world wording and situation transfer
- a time-budget guide for 10-minute, 20-minute, and 45-minute practice modes
- a weekly review template for deciding what to adjust next
- a focused business communication curriculum
- ready-to-run weekly practice sprints
- featured session curation
- next-wave source expansion planning
- a five-corpus reader-facing site bundle
- a tenth transcript-backed humor-transfer corpus through Andrew Tarvin
- a focused improvement-actions guide
- a curriculum page that now separates entry routes, focused tracks, and support tools
- a dedicated practice page that assembles modes, bundles, rhythms, and support tools in one place
- a detail page that resolves connected material across concepts, sessions, evidence, matrix entries, and curricula
- browsable session, source, roadmap, matrix, and contrast pages across the atlas
- browsable HTML pages for all of the above

Example first pass:

```bash
python3 scripts/download_youtube_playlist_transcripts.py \
  --course-root . \
  --manifest raw-material/youtube/starter-manifests/ultraspeaking-wave-1.json
```

## Validation

The site package now has an explicit data-integrity validator.

Run:

```bash
./scripts/validate_all.sh
node scripts/validate_site_data.js
node scripts/validate_markdown_refs.js
```

`validate_site_data.js` checks:

- duplicate slugs across the site data collections
- broken `*Slugs` references such as `sessionSlugs`, `evidenceSlugs`, and `conceptSlugs`
- missing `linkedFiles` targets on disk

`validate_markdown_refs.js` checks:

- backticked repo-path references across `README.md`, `analysis/`, and `raw-material/README.md`
- whether those referenced files actually exist in the current tree

For JS syntax checks on the site bundle, run:

```bash
node --check site/data.js
node --check site/app.js
```

Recommended quality loop for site changes:

1. edit `analysis/` and `site/data.js`
2. run `./scripts/validate_all.sh`
3. if that fails, run the lower-level validators individually
4. only then treat the site graph and repo references as coherent
