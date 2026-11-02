# Prompts: one Claude Code conversation per stage

Replace the values in angle brackets once (course, module, tool, lab number NN, site repo name). In every new
conversation, type first: `/add-dir ~/Documents/3A/SJTU/VLSI_Mort/test2`. Start each conversation in the lab's
teacher clone (VS Code folder `eda-learning-labNN`). Between stages: `/usage` (note it), new conversation.

## Stage 1: Audit (Sonnet)
```
/lab-upgrade Stage 1 for course <course>, module <module>, tool platform/tools/<tool>, Lab <NN>,
teacher clone = this folder (eda-learning-lab<NN>, on main, no branch), site repo ../eda-<short>-module-lab<NN>.
Run the audit and lint scripts, read only the files the skill names, cross-check every golden against the
platform's own functions (run them with node), note what common/ lacks and every vague rule, and write
UPGRADE_NOTES.md with the gaps, 2-4 concepts, a plan, and open questions each with a recommended answer.
Don't edit anything else.
```
Bring the notes to the chat for review if you like, answer the open questions in the same conversation, then
"approved, append the decisions to UPGRADE_NOTES.md".

## Stage 2: Content and goldens (Sonnet)
```
/lab-upgrade Stage 2. Read UPGRADE_NOTES.md first. Write the checker (exact written rules, tie-breaks,
caps; one portable PRNG shared with JS if anything is random, with a --vs-node check), extra example graphs,
EXAMPLES.md, quiz, checklist, README and _demo.sh. Every number must come from the checker. Prove that a
wrong --impl fails.
```
Then run the checker yourself: all PASS.

## Stage 3: Script in parts and figures (Opus)
```
/lab-upgrade Stage 3. Read UPGRADE_NOTES.md first. Write transcript.md for a high-school student, already
in 4-6 parts of 1-2 minutes (hook at the start, "Pause and guess" at the end, answered by the next part),
following the repetition rules and 1,100-1,300 spoken words. Make the figures and step figures with scripts
kept in ../tools/lab<NN>-figures (run_all.sh, facts.py, README, a --lang fr option). Redraw the walkthrough
frames. Lint, build the PDF and look at every page. Write the part boundaries (slides and PDF pages) in the
notes. No audio yet.
```
Open `slides.pdf` yourself; ask for fixes in the same conversation.

## Stage 4: Browser lab (Opus)
```
/lab-upgrade Stage 4. Read UPGRADE_NOTES.md first. Rebuild platform/tools/<tool> as model + UI with 8-10
challenges that check what the learner builds (nothing passes on load, from a preset, from the reveal, or
after editing a method's result), colours as in the figures, a model-vs-checker test and a Playwright test
with positive, negative and colour cases. Recapture the lab screenshot and rebuild the deck.
```
Try the lab yourself: `python3 -m http.server 8080 --directory platform`, then `http://localhost:8080/tools/<tool>/`.

## Stage 5: Site in EN and FR (Sonnet)
```
/lab-upgrade Stage 5. Read UPGRADE_NOTES.md first. Create ../eda-<short>-module-lab<NN> from the template
../eda-floorplanning-module-lab5 (reference/site-template.md: fresh git init, change every lab-specific place,
PARTS from the notes). Write the French transcript, EXAMPLES, quiz, lab strings, walkthrough captions, and
French figures and frames. When the French media must be built, give me the exact commands to run in my own
terminal and wait. Then build and run both tests; report both language lines. Don't push.
```

## Stage 5b: Animated lessons, one conversation per part (Opus)
After `/add-dir ~/Documents/3A/SJTU/VLSI_Mort/test2`, in the teacher clone. Part 1 first; watch it before the others.
For part N > 1 the style reference is part N-1. The last part adds: "Part <N> has no next part: its last question
card gives the answer itself (...)".
```
/lesson-animator Part <N> of Lab <NN>, scene <floorplan|graph>. This session runs in the teacher clone
(../eda-learning-lab<NN> is the clone); the site repo is ../eda-<short>-module-lab<NN>: write every file there.
Use ~/eda-venv/bin/python for every script (the system python has no markdown or edge-tts).
Read the skill's reference/storyboard.md and reference/design-rules.md, then use
../eda-<short>-module-lab<NN>/lessons/part-<N-1>/storyboard.json and its README as the style to follow
(same layout, colours, pacing, back link "Back to the video parts" / "Retour aux parties vidéo" to
../../index.html#video in the lede). Then read the Part <N> lesson plan in <module>/UPGRADE_NOTES.md.
Part <N> = transcript slides <a-b>. EN transcript: <module>/transcript.md;
FR transcript: ../eda-<short>-module-lab<NN>/i18n/fr/<module>/transcript.md.
The part opens by answering Part <N-1>'s pause-and-guess and ends with its own pause-and-guess as a question card.
Data: build/lessons/<checker>.json (the checker's --json), passed with --data to every build. Put every spoken or
shown number in claims. Key the first move at least 0.6 s into the audio.
Write lessons/part-<N>/storyboard.json and lessons/part-<N>/README.md. Build EN and FR with draft_timing.py first,
run check_lesson.py (0 errors, 0 warnings) and show me both contact sheets.
Then give me the exact voice_build.py commands for my own terminal (EN <voice>, FR <voice>, --rate=-4%,
cache .cache/voice, outputs in build/lessons/part-<N>/) and wait.
After I say they finished: check both timing files say "words": "exact", rebuild into docs/lessons/part-<N> and
docs/fr/lessons/part-<N> (--fonts site_src/fonts --storage-key lab<NN>-lesson-speed), recheck, rebuild the site with
~/eda-venv/bin/python build_site.py --repo ../eda-learning-lab<NN>, serve docs on 127.0.0.1:8090 for
tools/test_site.py, run it, stop the server, and report both language lines. Don't commit or push.
PYTHONDONTWRITEBYTECODE=1.
```
Then: watch it, `git add -A && git commit -m "Lab <NN>: animated lesson for part <N> (EN/FR)" && git push`.

## Stage 6: Final (Sonnet)
```
/lab-upgrade Stage 6. Read UPGRADE_NOTES.md first. The media and all lessons are built. Use ~/eda-venv/bin/python.
Check git status in the clone (only the two allowed folders), rebuild the site, serve docs on 127.0.0.1:8090,
rerun tools/test_site.py and tools/test_lab_site.py, stop the server, report both language lines. Write
WHAT_CHANGED.md (concepts, files, figures, challenges, tests, part lengths, the lessons, findings for the teacher
from the notes' teacher list), copy UPGRADE_NOTES.md to ../tools/lab<NN>-notes/ and delete it from the module.
Give me the commit and push commands. Don't commit or push.
```
Then you open the live site and one lesson per language, and send the link and WHAT_CHANGED.md to the teacher.
