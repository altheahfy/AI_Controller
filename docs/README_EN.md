# K-MAD Starter Kit

## 【Important Instructions for AI】

You are a **co-developer** of this project, but at the same time you must operate **under the constraints of the K-MAD governance system**.

### Role Assignment Premise

**In this development system, humans are assumed to basically be unable to read or write code.**

| Role | Responsible Party | Responsibilities |
|------|------|------|
| **Product Owner** | Human | Design instructions, test approval, release decisions, migration result approval |
| **Developer** | AI (you) | Code implementation, error fixes, distribution file reading, technical detail processing |

**Humans decide "What/Why to build," and AI implements "How to build."**

---

## 1. Why K-MAD is Necessary (Background & Philosophy)

### Problems with AI-Generated Code

AI-generated code has the following characteristics:

- Works on the surface
- But in large-scale and complex situations, fixing one bug breaks another location
- Moreover, the same location breaks in different ways repeatedly

AI always says:
**"This fix will solve the problem"**

Indeed, looking at just that one point, it's correct.
But overall design is not maintained.

### Why

- **AI can optimize for the current moment's requirements**
- **However, it cannot 'preserve' the design intent of the entire app**
- **It cannot apply 'past breakage experiences' to the next time**

In other words,
> **AI proposes "locally working changes" but is not the entity that judges "overall design consistency"**

### Expert Team vs AI+Non-Engineer

**Expert team development**:
- Changes that break rules are **stopped by the review mechanism**
- Code reviewers guarantee design consistency

**AI+Non-Engineer development**:
- No review exists
- No "stopper"
- Changes AI thought were good go through as-is

**→ That's why K-MAD is necessary**

---

## 2. K-MAD Mechanism (Your "Cage")

### Physical Constraints by governance_gate.py

Code you write is fully scanned by **`governance_gate.py`** at save (commit) time.

**If there's even a tiny rule violation, the commit in GitHub Desktop is physically rejected.**

### Definition of Failure

- ❌ **Simply writing "working code" is insufficient**
- ✅ **Only "code that works while maintaining K-MAD structure" is correct**

**If an error occurs, recognize that it's not about your capability but a violation of rules in `governance_rules.json / .yaml, pipeline_definition.md`, and follow them.**

---

## 3. Setup Procedure (3 Steps)

### Step 1: Place Files

Place all files of this starter kit in the project root.

```
your-project/
├─ README.md (this file)
├─ K-MAD_GUIDE.md (detailed guide)
├─ governance_gate.py (automatic checkpoint)
├─ snapshot_system.py ("state snapshot" save system)
├─ governance_rules.json / .yaml (the "constitution" protected by automatic checkpoint)
├─ Central Layer_Claim Arbiter.py (central management system/decision-making agency)
└─ pipeline_definition.md ("single path" definition)
```

### Step 2: Set Up Git Hook

**Human operation (execute in command line)**:

#### For Windows
```bash
# Create .git/hooks/pre-commit file
echo "#!/bin/sh" > .git/hooks/pre-commit
echo "python governance_gate.py" >> .git/hooks/pre-commit
```

#### For Mac/Linux
```bash
# Create .git/hooks/pre-commit file
echo "#!/bin/sh" > .git/hooks/pre-commit
echo "python governance_gate.py" >> .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
```

#### .gitignore Configuration (Important)

**Exclude the snapshot folder from Git management.**

Reason: The `.snapshots` folder becomes very large as it stores code history. Uploading this to GitHub makes the repository heavy.

**Instruction to AI**:
```
"Add the .snapshots folder to .gitignore"
```

**Or manually add by human**:
Add the following to the `.gitignore` file at project root:
```
# K-MAD Snapshot System
.snapshots/
```

### Step 3: Instruct AI

**Human instruction examples**:
```
"Implement XX feature"
"Run tests"
"Fix errors"
```

**What AI automatically does**:
1. Read and understand distribution files (`governance_rules.json / .yaml, pipeline_definition.md`, etc.)
2. Implement code following K-MAD rules
3. At commit time, `governance_gate.py` automatically verifies
4. Self-correct if violations exist

**What humans should do**:
- ✅ Instruct "what to build"
- ✅ Look at test results and judge "OK/NG"
- ✅ If errors occur, instruct "fix it"

**What humans should NOT do**:
- ❌ Read code internals
- ❌ Technical analysis of error messages
- ❌ Understanding internal structure of distribution files

---

## 4. File Structure

### Required Files

| File | Role |
|---------|------|
| `governance_gate.py` | Automatic checkpoint (validates all code at commit time) |
| `snapshot_system.py` | "State snapshot" save system (records OK states) |
| `governance_rules.json / .yaml` | "Constitution" protected by automatic checkpoint (defines rules) |
| `central_layer_claim_arbiter.py` | Central management system/decision-making agency (final approval) |
| `pipeline_definition.md` | "Single path" definition (processing flow specification) |

### Documentation

| File | Role |
|---------|------|
| `README.md` | This file (concise version) |
| `K-MAD_GUIDE.md` | Detailed guide (full text) |

---

## 5. Frequently Asked Questions (FAQ)

**Q: I got an error. What should I do?**
A: Humans just instruct "fix it". AI reads `governance_rules.json / .yaml, pipeline_definition.md` and fixes.

**Q: Do I need to understand the code internals?**
A: **No.** AI reads and implements everything.

**Q: What does governance_gate.py do?**
A: It scans all code at commit time and detects K-MAD rule violations. Humans don't need to understand the internals.

**Q: Where can I find detailed information?**
A: Refer to `K-MAD_GUIDE.md` (contains detailed philosophy, mechanisms, and examples).

**Q: What is `execution_settings` in governance_rules.json?**
A: Settings that control verification execution methods.
- `verbose_output: true` (recommended): Output detailed logs (for beginners)
- `stop_on_first_violation: false` (recommended): Display all violations at once
- Once comfortable, can change to `stop_on_first_violation: true` (stop immediately on first violation)

Humans just change true/false in the config file. Leave implementation to AI.

---

## 6. Troubleshooting

### When Commit is Rejected

**Human operation**:
```
"Fix the governance_gate.py error"
```

**What AI automatically does**:
1. Analyze error message
2. Check rules in `governance_rules.json / .yaml, pipeline_definition.md`
3. Fix violation locations
4. Commit again

**Humans don't need to make technical judgments.**

---

## 7. Next Steps

1. **Place distribution files** (Step 1)
2. **Set up Git Hook** (Step 2)
3. **Instruct AI** (Step 3)
4. **Refer to detailed guide** (`K-MAD_GUIDE.md`)

**Now, even with zero coding skills, large-scale app development becomes possible.**
