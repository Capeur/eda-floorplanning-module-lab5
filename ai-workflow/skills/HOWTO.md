# eda skills: lab-upgrade v3.1 + lesson-animator v4.2 (2026-11-02, after Lab 05)

## Install (replaces both; safe: nothing is removed if the unzip fails)
```bash
Z=$(ls -t ~/Downloads/eda-skills-v3.1*.zip | head -1); echo "zip: $Z"
cd ~/Downloads && rm -rf eda31 && mkdir eda31 && unzip -q "$Z" -d eda31 \
  && rm -rf ~/.claude/skills/lab-upgrade ~/.claude/skills/lesson-animator \
  && cp -r eda31/lab-upgrade eda31/lesson-animator ~/.claude/skills/ \
  && grep -m1 "version" ~/.claude/skills/lab-upgrade/SKILL.md ~/.claude/skills/lesson-animator/SKILL.md
```
Expected: "version 3.1" and "version 4.2". Start new Claude Code conversations afterwards (skills load at start).

## What changed
- **lab-upgrade v3.1**: Lab 05 is the template site (lesson links and tests); new **Stage 5b** (one animated lesson
  per part, prompt in prompts.md); media French then English with the venv Python; pipeline gotchas from Lab 05
  ("Next" titles, walkthrough frame names, venv, index colours, tracked .pyc, W/H keys, H.264 in tests);
  workflow notes (chained installs, sessions in the teacher clone, Pages queue); PLAYBOOK: the Lab 05 story and a
  new checklist.
- **lesson-animator v4.2**: v4 floorplan scene + 4.1 turned-block size label + 4.2 code blocks never spoken
  (the same problem Claude Code fixed in your installed copy during Part 5; your Lab 05 lessons do not need a rebuild).
