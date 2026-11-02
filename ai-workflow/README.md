# How this lab was built with AI

This folder documents how Lab 05 (B*-tree floorplan representation, floorplanning course) was upgraded with AI
assistance, and holds the two reusable skills that came out of it, so the same work can be repeated on another lab.

- Student: Capeur (VLSI course, SJTU). Teacher's course: [yongfu-li/eda-learning](https://github.com/yongfu-li/eda-learning).
- Result: https://capeur.github.io/eda-floorplanning-module-lab5/ (English) and `/fr/` (French).
- What changed, file by file, with the findings for the teacher: [`../WHAT_CHANGED.md`](../WHAT_CHANGED.md).
- AI used: **Claude** in two ways.
  - **Claude chat** (claude.ai, with a cloud workspace): planning, reviewing each stage, re-checking every new number
    by running the teacher's own code, building the animated-lesson engine, packaging the skills.
  - **Claude Code** (VS Code extension, on the student's laptop): ran the upgrade stage by stage with the
    `lab-upgrade` skill, then one animated lesson per part with the `lesson-animator` skill.
- Every change was reviewed and run by the student; nothing was pushed to the teacher's repo.

## For the coordinator: what to reuse from this lab

| What | Where | Reusable for | Evidence it works |
|---|---|---|---|
| **Animated lessons** drawn live in the browser, in time with the voice (not video files): word-anchored animation, EN + FR from one storyboard, auto-pause "pause and guess", click-to-try, 1–2× speed, MP4 export | `skills/lesson-animator/` (engine + scripts + 2 examples) | any lab: a `graph` scene (partitioning, clustering) and a `floorplan` scene (B*-tree, packing); new scenes plug into the same core | 5 lessons on this site, 0 errors / 0 warnings each; the engine re-packs the checker's 11 trees and must agree; Lab 03's lesson gives pixel-identical frames after the refactor |
| **The stage method**: audit → content + checker → script in parts → browser lab → bilingual site → lessons → hand-off, one conversation per stage, state in `UPGRADE_NOTES.md` | `skills/lab-upgrade/` (`SKILL.md`, `prompts.md`, `PLAYBOOK.md`) | any lab of eda-learning | used on 3 labs (clustering 02, partitioning 03, floorplanning 05) |
| **Golden checker pattern**: exact written rules, `--impl` for the learner's code, `--vs-node` against the platform's JS, `--json` for figures and lessons, deliberately wrong implementations shipped | module `examples/bstar_check.py`, `examples/wrong/` | any algorithm lab | 61 PASS; Python = JS on all 5040 trees; both wrong packers FAIL |
| **Challenges that check what the learner built** (nothing passes on load, after Clear, from a preset, from Reveal, or after editing a packed tree), model/UI split, model-vs-checker tests, mutation checks | tool `bstar-tree-lab-model.js`, `tests/` | any browser lab | 185 model checks over 161,280 packs; 111 Playwright cases (82 negative) |
| **Bilingual site template**: video cut into parts with subtitles, speed buttons, walkthrough, lab, lessons next to parts, French via a swapped strings file (shape-checked), self-hosted fonts, 0 external requests | this repo (`build_site.py`, `site_src/`, `i18n/`, `tools/`) | any lab site | 245 site checks, 116 lab cases per language |
| **Findings about the teacher's repo** (unwritten rules, shared-code traps, generators not to rerun) | `../WHAT_CHANGED.md`, `skills/lab-upgrade/reference/pipeline-gotchas.md` | everyone working on eda-learning | each finding came from running code |

Lab-specific (not to copy as such): the B*-tree content, the 8 example trees, the 9 challenges, the storyboards in
`../lessons/`. Everything in `skills/` is general.

## 1. Timeline

| Date | What happened |
|---|---|
| 2026-10-30 14:42 | Request: Lab 05 with the Lab 03 method, plus an animated lesson for **every** part. The chat made the light clone of the teacher's repo in the cloud (16 MB zip; GitHub is slow from China) and checked what the lesson engine and site template would need: the engine only knew graphs, floorplanning places rectangles. |
| 14:51 | Plan approved: stages 1–2, then a floorplan scene for the engine (built in the chat), stages 3–5, a lesson per part, stage 6. |
| 15:47 | **Stage 1, audit** (Claude Code, Sonnet). No golden number was wrong, but the B*-tree walk order was unwritten, the example never used the skyline, no tree operation existed, and all 10 challenges passed with one click. The chat re-ran every new number with the course's own packer. |
| 16:01 | **Stage 2, content** (Sonnet): checker, 8 example trees, quiz, examples. Counts re-verified in the chat. |
| 16:07–16:30 | **Engine v4 in the chat**: the lesson engine split into a core + scenes; new floorplan scene; Lab 03's lesson checked pixel-identical; a demo lesson; a draft-timing tool to check lessons before any voice exists. |
| 16:47 | **Stage 3, script and figures** (Opus): 5 parts with hooks and "pause and guess", a sentence-by-sentence lesson plan per part. |
| 17:20 | **Stage 4, browser lab** (Opus): tree editor, 9 build-and-predict challenges, tests. |
| 10-31 00:01–01:45 | **Stage 5, site** (Sonnet); the student ran the French and English media in a terminal; site pushed; voices chosen by ear. |
| 11-02 12:19–22:36 | **Five animated lessons**, one Claude Code conversation (Opus) each; the student ran the voices; Part 1 reviewed before the others. Engine fix in the chat (v4.1). |
| 22:56–23:05 | **Stage 6, hand-off** (Sonnet): tests, `WHAT_CHANGED.md`; skills packaged as lab-upgrade v3.1 and lesson-animator v4.2. |

## 2. Who decided what

| Decision | By | Why |
|---|---|---|
| Animated lesson for every part, next to the video parts; English and French; high-school level | Student | the video alone "is not dynamic enough" (Lab 03 feedback) |
| Extend the lesson engine with a scene instead of copying it | Chat proposal, student approved | one engine for every course; the Lab 03 lesson must not change |
| Walk order written as the rule: the node, its whole left subtree, then its right child | Found by Claude Code (Stage 1), recommended in the chat, approved by the student | it is the standard B*-tree and the teacher's code; reversing it changes 1,764 of 5,040 trees |
| Any block may turn 90°; the "reach 24" challenge without turning | Chat proposal, student approved | turning makes 24 easy (1,488 ways instead of 8) |
| One colour per block everywhere; left links solid ("next door"), right links dashed ("upstairs") | Chat proposal, student approved | the shared drawing code changes colours on partial packs |
| Challenges check the resulting tree, not the button used; "predict D.y" kept in Practice with two hints | Asked by Claude Code, answered in the chat | the lab checks what the learner built |
| Keep the teacher's walkthrough frame names | Chat, after reading the teacher's capture script | a rerun of the teacher's script would otherwise duplicate frames and rewrite the transcript |
| Voices: en-US-AndrewMultilingualNeural, fr-FR-RemyMultilingualNeural | Student, by ear | |

## 3. Problems met and how they were solved

| Problem | Fix |
|---|---|
| The lesson engine could only draw graphs | Core + scenes refactor; a floorplan scene that re-packs every tree with the course's rule |
| A slide title starting with "Next" lost its bullets in the teacher's builder | Title renamed; added to the skill's pipeline gotchas |
| The French and English media need a VPN and take 10–30 minutes | Run by the student in a terminal, one after the other |
| System Python had no `markdown` / `edge-tts`; `build_site.py` emptied `docs/` before failing | Every command uses the virtual environment's Python |
| A skill install command deleted the old skill when the download was missing | Install commands now chained with `&&` |
| First animation key fell before the opening picture settled | Rule: first move at least 0.6 s into the audio |
| A turned block's size label kept its old size; a code slide was read aloud | Engine v4.1 and v4.2 |
| GitHub Pages' first deploy stayed "Queued" | Normal for a new repo; re-run or empty commit if it lasts |

## 4. Results

- Content: golden checker (61 checks), 8 example trees, 2 wrong packers, 8-question quiz, rewritten examples, checklist, README.
- Script: 1,198 spoken words, 31 slides (32 PDF pages), 5 parts of 1:05–2:02; videos of 7:21 (EN).
- Browser lab: tree editor, 9 challenges; 185 model-vs-checker checks, 111 browser cases, 116 per language on the site.
- Animated lessons: 5 per language (80 s to 149 s), exact word timings, 0 errors and 0 warnings each.
- Site: 245 automated checks, no external requests.

## 5. Reusing this on another lab

`skills/` holds both skills (install them into `~/.claude/skills/`, see `skills/HOWTO.md`):
- **`lab-upgrade`** (version 3.1): the stage method with the lessons stage, copy-paste prompts, environment guide,
  pipeline gotchas, and `PLAYBOOK.md` (the Lab 03 and Lab 05 stories, with a checklist for the next lab).
- **`lesson-animator`** (version 4.2): the lesson engine (graph and floorplan scenes), voice and timing scripts,
  checker, MP4 export; examples for Lab 03 Part 1 and a Lab 05 demo.
`notes/UPGRADE_NOTES.md` is the full stage-by-stage record of this lab (decisions, numbers, commands).

## 6. Limits

- The voice service (edge-tts) needs a VPN from China; lessons are built on the student's laptop.
- Video playback must be checked in a real browser: the automated test browser cannot play H.264.
- A floorplan lesson cannot yet show blocks "waiting on the side" before they are placed.
