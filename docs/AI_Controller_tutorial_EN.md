# AI Controller (K-MAD Starter Kit) User Guide

This guide provides the **actual working procedures** for using the distributed "AI Controller."  
This document (Chapter 4) focuses on understanding the workflow and operating principles. When working, you can basically proceed by looking at this guide alone.

---

## 0. Introduction: Most Important Rules (Follow at Least This)
In AI Controller, there are basically only two things you need to do:

1. **Before pressing the "Commit" button, visually check only the key points (the content explained by the AI, not the code itself)**
2. **If the automatic checkpoint (governance_Gate.py) shows an error, have the AI fix it**

> **Commit = "Explicit approval"**  
> Local saving is free for trial and error. **Only be careful with adoption (commit).**

---

## 1. Initial Preparation (5 minutes)
- Windows PC (Mac is also acceptable)
- VS Code
- GitHub Desktop (recommended)
- Copilot / Generative AI (inside VS Code or browser)
- Complete distribution package (AI Controller folder)

---

## 2. First, Place "AI Controller Package" in a New Folder (1 minute)
1) Create a new empty folder (e.g., `my_app`)  
2) Copy the entire distribution package into it  
3) Open that folder in VS Code

> ✅ Goal here: Just make files **"visible"**.

---

## 3. Have the AI Read the System (Read-Only Phase)
Paste the following into VS Code / Copilot (copy-paste ready):

### Copy-Paste: Initial Instruction
> Please **read all** of the following distribution files:  
> - docs/README.md  
> - Distribution ① src/utils/governance_gate.py  
> - Distribution ② src/utils/snapshot_system.py  
> - Distribution ③ src/governance/governance_rules.json  
> - Distribution ④ src/utils/central_layer_claim_arbiter.py  
> - Distribution ⑤ src/pipeline/pipeline_definition.md
>  
> **Note: At this stage, do not start code generation or editing yet.**  
> First, declare "I understand" and briefly summarize the role of the distribution files.

> ✅ Goal here: Have the AI **understand the purpose of K-MAD and developing within this system**.

---

## 4. Initial Setup (Choose One Method)

Both methods are completed by instructing the AI.  
**Method A (Recommended)**: Using setup.py is more efficient  
**Method B**: Have AI configure individual settings (traditional procedure)

### Method A: Batch Setup Using setup.py (Recommended)

Instruct the AI as follows (copy-paste ready):

#### Copy-Paste: Execute setup.py
> Please execute `src/utils/setup.py` to complete the initial setup.

This will automatically configure:
- Git repository initialization
- Adding .snapshots/ to .gitignore
- Pre-commit hook configuration
- governance_rules.json template generation

### Method B: Individual Configuration (Instruct AI One by One)

Instead of using setup.py, give individual instructions to the AI.  
Follow steps 5-8 below to request AI sequentially.

---

## 5. Create a Repository with GitHub Desktop (Required)
> When the automatic checkpoint is not yet active, the AI can "freely" move forward.  
> **Commit rejection = physical block** is the trick to establish early.

### Procedure (GitHub Desktop)
1) Open GitHub Desktop  
2) Select the folder from step 2 using `File > Add local repository...`  
3) Choose "Create a repository" to create it  
4) Once created, make the initial commit (Initial commit)

> ✅ Goal here: Set up **the commit location (approval gate)**.

---

## 6. Consultation on the App to Build ~ (First Challenge) AI will "kindly" start deciding on its own
Now, let's explain to the AI in detail what you want to achieve with the app you're going to build.
Then, consult about what kind of departments (modules) and central management agency (central_layer_claim_arbiter.py) combination would be good to achieve it.

### Copy-Paste: Role Assignment
> After considering what governance and internal controls are desirable for the modules that make up this app (not just role assignment, but also separation of duties and mutual checks, information verification and central agency approval, etc.), please propose a role assignment and job description plan. Do not rewrite files without permission; first consult with me about "app department division."
### Copy-Paste: Pipeline
> After considering what kind of pipeline is desirable for the modules and central management agency that make up this app, based on the contents of pipeline_definition.md, please present a proposal. Do not rewrite files without permission; first consult with me about "app department division."

**At this stage, the AI will highly likely take the following actions (although the copy-paste prompts include text to prevent this):**

- Arbitrarily decide the app's "departments (modules)" and try to rewrite the json
- Arbitrarily decide the job descriptions (roles / capabilities) and try to rewrite the json
- Arbitrarily create a pipeline (processing order) and try to rewrite pipeline_definition.md
- Try to move forward in a plausible manner

> **This is not a failure; it is expected behavior.**  
> It's correct that the AI thinks about various things, but what's important here is:

> **Do not adopt the "arbitrarily decided content" as-is** (= do not commit)

### Two Points You Should Check Here (1-minute check)
When the AI presents department proposals and pipeline proposals, check only the following two points:

1) **Do the department divisions make sense?**  
   The biggest trick is "processing cannot be completed within a single department." In the example below, the calculation result cannot be produced without all four people.
   - a. "The receptionist transmits but does not calculate"
   - b. "The calculator calculates but does not write the result in the result field"
   - c. "The checker inspects whether the result matches the format, whether there are duplicates, etc., but does not approve or reject"
   - d. "The central management agency only approves and outputs to the result field when all three above are ○" 
2) **Are the process steps (single path) in the correct order without duplication?**  
   - In the above example, it would be wrong if not in the order a, b, c, d   
   - NG if there seems to be a shortcut (shortcut that skips inspection)
   - If the pipeline consists of "Receptionist Pipeline," "Calculator Pipeline," "Checker Pipeline," "Central Management Pipeline" with four lines, and all include receptionist, calculator, checker, and central management agency, it's redundant duplication. One line is sufficient.

> ✅ Goal here: **Finalize the governance philosophy.**.  
> Not bug prevention, but deciding **the core of the design**.
> If the content is difficult, you can consult with the AI itself about it.

## 7. Constitution Update
Once you're finally satisfied, have the AI update governance_rules.json and pipeline_definition.md with the content decided in step 6.

---

## 8. Set Up the Automatic Checkpoint (governance_Gate.py) to Always Run on Commit

**Note: If you used Method A with setup.py, this step is already completed automatically and can be skipped.**

If you chose Method B for individual configuration, request the following from the AI (copy-paste ready).

### Copy-Paste: Set up automatic checkpoint to run before commit and take "state snapshot" when passed
> When committing in GitHub Desktop, please set it up so that `src/utils/governance_gate.py` always runs immediately before, and if there are errors, the commit is canceled.  
> For Windows, please set it up to work as a `pre-commit` (Git hook).  
> Furthermore, please link it so that `src/utils/snapshot_system.py` takes a snapshot only when the Gate gives an OK.  
> Once done, please tell me the "name of the file you configured" and "how to verify the operation."

> ✅ Goal here: Set up a state where **only "approval" goes through the automatic checkpoint**.  
> From now on, you only need to check "whether the automatic checkpoint says OK."

---

## 9. Create the Actual Company Organization (Central Management Agency + Departments) and Pipeline
From here, you can proceed while consulting with the AI.  
Based on what was discussed and decided in step 6 and written into the constitution in step 7, have the AI rewrite src/utils/central_layer_claim_arbiter.py, create departments (modules), and connect them.

### Copy-Paste: Pipeline Creation
> Use src/utils/central_layer_claim_arbiter.py as the base. Define the ClaimType (data types) in this app, and implement the data flow between departments according to src/pipeline/pipeline_definition.md.  

> ✅ Goal here: **The basic structure of the application is completed**.

---

## 10. Implementation Cycle (Always the Same Thereafter)
This is basically all you need to do.

1) Have the AI implement (local saving is free)  
2) Go through the automatic checkpoint before commit  
3) If the automatic checkpoint is NG, have the AI fix it  
4) If the automatic checkpoint is OK, a snapshot is saved
5) If you feel the need to change the constitution and automatic checkpoint itself (newly discovered rules, etc.), proceed carefully after consulting with the AI

### Copy-Paste: Error Instruction Template for Automatic Checkpoint
> There is an error in governance_gate.py.  
> Please read the error message and fix it according to the distribution files (src/utils/governance_gate.py / src/governance/governance_rules.json / src/pipeline/pipeline_definition.md) until there are no rule violations.  
> After fixing, please go through the pre-commit check again.

---

## 11. Finally: Not Checking Won't Break It. But Checking Makes It "Your App"
Even with this procedure, the AI will produce "plausible correct answers." In most cases, they will work.  
However, that doesn't necessarily mean it reflects the philosophy of the design you want to create.

> **With just a one-minute check before each commit, you act as the system designer.** 
> From there on, the automatic checkpoint will protect it.
