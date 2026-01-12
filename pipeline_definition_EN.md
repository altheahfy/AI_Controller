# Pipeline Definition (Single Path)

## Purpose

This file defines the processing flow of the **Capacity-Managed Task Scheduler** as **a single path**.

---

## What is a Unified Generic Pipeline

**Definition**: A single pipeline where all processes selectively use the common process flow Phase ① → Phase ② → ... → Phase ⑨.

### Incorrect Understanding (❌)
```
Task Placement Pipeline (200 lines)
Template Management Pipeline (150 lines) ← 80% duplicate!
Time Slot Management Pipeline (150 lines) ← 80% duplicate!
Completion Processing Pipeline (100 lines) ← 90% duplicate!
```

### Correct Understanding (✅)
```
Phase ① → Phase ② → ... → Phase ⑨
          ↓       ↓           ↓
   All operations use a common pipeline
   (Only the "trigger" differs)
```

---

## Pipeline Structure (9 Phases)

### Phase ① Input Parsing (Receptionist)
**Purpose**: Parse user commands

**Processing**:
- Receive command strings
- Validate command format
- Separate commands and parameters

**Input**: Raw command string
**Output**: Parsed command data

**Examples**:
- "place Meeting 9:00" → action="place", template="Meeting", slot="9:00"
- "create_template Meeting 30" → action="create_template", name="Meeting", weight=30
- "create_slot 9:00 60" → action="create_slot", time="9:00", capacity=60
- "complete 1" → action="complete", task_id=1
- "list" → action="list"

**Implementation Location**: `src/controllers/input_parser.py`

**Job Responsibilities**: 
- ✅ Transmits but does not process
- ❌ Must not submit proposals
- ❌ Must not write data

---

### Phase ② Trigger Detection
**Purpose**: Determine which department to call

**Processing**:
- Identify trigger based on action
- Determine proposal department to invoke
- Detect invalid commands

**Input**: Parsed command data
**Output**: Trigger information (list of departments)

**Trigger Mapping**:
- "place" → TaskPlacementProposer
- "create_template" → TaskTemplateManager
- "create_slot" → TimeSlotManager
- "complete" → TaskCompletionHandler
- "list" → DisplayHandler

**Implementation Location**: `src/controllers/trigger_detector.py`

**Job Responsibilities**:
- ✅ Judges but does not execute
- ❌ Must not change data

---

### Phase ③ Proposal Department Invocation
**Purpose**: Invoke proposal departments based on detected triggers

**Processing**:
- Invoke proposal departments based on triggers detected in Phase ②
- Request processing from each department
- Collect Claims (proposals)

**Input**: Trigger information, parsed command data
**Output**: List of Claims (proposal content)

**Departments Invoked**:
- TaskPlacementProposer (task placement proposals)
- TaskTemplateManager (template management proposals)
- TimeSlotManager (time slot management proposals)
- TaskCompletionHandler (completion processing proposals)
- DisplayHandler (display only, no Claims)

**Important Principles**:
- ❌ Do not call departments for undetected operations
- ✅ Only call necessary departments (optimization)
- ❌ Do not write data at this stage (proposals only)

**Implementation Location**: `src/controllers/handler_invoker.py`

---

### Phase ④ Validation Department Invocation
**Purpose**: Validate proposals from multiple perspectives

**Processing**:
- Invoke CapacityValidator (Capacity Validation Department)
- Invoke ConsistencyValidator (Consistency Validation Department)
- Collect validation results

**Input**: List of Claims
**Output**: List of validation results

**Departments Invoked**:
- **CapacityValidator**: Capacity calculation (Can it fit? Remaining capacity?)
- **ConsistencyValidator**: Consistency verification (ID duplication? Slot exists? Template valid?)

**Important Mutual Checks**:
- ✅ Capacity Validation Department does not place
- ✅ Consistency Validation Department does not check capacity
- ❌ Validation departments do not decide approval/rejection

**Implementation Location**: `src/controllers/validator_invoker.py`

---

### Phase ⑤ Validation Result Evaluation
**Purpose**: Integrate all validation results and determine OK/NG

**Processing**:
- Check capacity validation results
- Check consistency validation results
- Overall judgment (proceed if all ○, branch if any ×)

**Input**: List of validation results
**Output**: Overall judgment result

**Judgment Logic**:
```
IF capacity validation == OK AND consistency validation == OK:
    → To Phase ⑦ (Central Management Agency approval)
ELSE IF capacity validation == NG:
    → To Phase ⑥ (auto replacement)
ELSE:
    → To Phase ⑨ (error output)
```

**Implementation Location**: Evaluation logic in `src/controllers/claim_arbiter.py`

---

### Phase ⑥ Auto Replacement Proposal on Capacity Overflow
**Purpose**: Propose alternatives only when capacity is exceeded

**Processing**:
- Invoke AutoReplacementProposer (Auto Replacement Proposal Department)
- Search for next time slot
- Search for first available slot
- Submit alternative placement proposals (Claims)

**Input**: Original placement proposal, capacity validation NG result
**Output**: Alternative placement proposal (Claim)

**Important Principles**:
- ✅ Only operates when Phase ⑤ indicates capacity NG
- ❌ Must not actually move tasks (proposals only)
- ❌ Must not decide which alternative to adopt

**Implementation Location**: `src/handlers/auto_replacement_proposer.py`

**After Phase ⑥**:
- If alternative proposal is submitted, return to Phase ④ (re-validation)
- If no alternative, proceed to Phase ⑨ (error output)

---

### Phase ⑦ Central Management Agency Final Decision
**Purpose**: Aggregate proposals and validation results from all departments and make final decision

**Processing**:
- Receive all Claims
- Confirm all validation results
- Check for job responsibility violations
- Final approval or rejection

**Input**: 
- List of Claims (proposals from proposal departments)
- List of validation results (judgments from validation departments)

**Output**: Final decision (approval or rejection)

**Decision Rules**:
```
IF all validations == ○ AND no job responsibility violations:
    → Approval (to Phase ⑧)
ELSE:
    → Rejection (to Phase ⑨)
```

**Important Authority**:
- ✅ **The only department that can write data**
- ✅ Monitors all departments
- ✅ Has final decision authority

**Implementation Location**: `src/controllers/central_layer_claim_arbiter.py`

---

### Phase ⑧ Execution and Data Writing
**Purpose**: Actually execute approved processing

**Processing**:
- Reflect content approved in Phase ⑦ to data
- Task placement, template creation, time slot creation, completion marking, etc.
- Transaction management (rollback on failure)

**Input**: Approved final decision
**Output**: Execution result

**Important Principles**:
- ✅ Not executed without Phase ⑦ approval
- ✅ Only follows Central Management Agency instructions

**Implementation Location**: `src/models/task_repository.py`, `src/models/data_store.py`

---

### Phase ⑨ Result Output
**Purpose**: Return processing results to user

**Processing**:
- Format success messages
- Format error messages
- Format list display

**Input**: Execution result or error information
**Output**: Message to user

**Output Examples**:
```
Success: "Task 'Meeting' placed at 9:00 (remaining capacity: 30)"
Capacity overflow: "9:00 has insufficient capacity. Automatically placed at 10:00"
Error: "Template 'Conference' does not exist"
List: "9:00 [30/60] Meeting(30)\n10:00 [0/60] (available)"
```

**Implementation Location**: `src/views/result_formatter.py`

---

## Data Flow Diagram (Overview)

```
[User Command]
      ↓
Phase ① Input Parsing (Receptionist)
      ↓
Phase ② Trigger Detection
      ↓
Phase ③ Proposal Department Invocation ──→ Collect Claims
      ↓
Phase ④ Validation Department Invocation ──→ Collect Validation Results
      ↓
Phase ⑤ Validation Result Evaluation
      ↓         ↓ (Capacity NG)
      |    Phase ⑥ Auto Replacement Proposal
      |         ↓
      |    (Return to Phase ④)
      ↓ (All ○)
Phase ⑦ Central Management Agency Final Decision
      ↓ (Approval)
Phase ⑧ Execution and Data Writing
      ↓
Phase ⑨ Result Output
      ↓
[Display to User]
```

---

## Summary of Department Job Responsibilities

### 【Proposal Systems】
| Department | Can Do | Cannot Do |
|------|-----------|-------------|
| TaskPlacementProposer | Task placement proposals | Capacity checks, actual placement, approval |
| TaskTemplateManager | Template management proposals | Task placement, time slot operations |
| TimeSlotManager | Time slot management proposals | Task placement, capacity calculation |
| TaskCompletionHandler | Completion state change proposals | Content changes, deletion, time slot operations |
| AutoReplacementProposer | Alternative placement proposals | Actual movement, adoption decisions |

### 【Validation Systems】
| Department | Can Do | Cannot Do |
|------|-----------|-------------|
| CapacityValidator | Capacity calculation, judgment | Placement decisions, rule checks |
| ConsistencyValidator | Consistency checks | Capacity calculation, placement decisions |

### 【Display Systems】
| Department | Can Do | Cannot Do |
|------|-----------|-------------|
| DisplayHandler | Data retrieval, display | Data changes, Claim submission |

### 【Central Management Agency】
| Department | Can Do | Exclusive Authority |
|------|-----------|-----------|
| CentralLayerClaimArbiter | Aggregate all Claims, confirm validations, monitor job responsibilities | **Only entity that can write data** |

---

## Key Points of Mutual Checks

1. **Proposal departments do not execute**
   - TaskPlacementProposer only proposes "want to place"
   - Actual placement happens in Phase ⑧

2. **Validation departments do not decide**
   - CapacityValidator only judges "fits/doesn't fit"
   - ConsistencyValidator only judges "OK/NG"
   - Final decision is made by Central Management Agency in Phase ⑦

3. **Only Central Management Agency can write**
   - Even if all departments give ○, execution does not happen without Central Management Agency approval
   - Immediate rejection if job responsibility violations exist

4. **Same route even on capacity overflow**
   - Auto replacement is also just a "proposal"
   - Re-validated in Phase ④ and approved in Phase ⑦

---

## Usage in governance_gate.py

This file is used in Layer 2 (dynamic flow verification) of `governance_gate.py`.

**Verification Content**:
- ✅ Is the order Phase ① → Phase ② → ... followed?
- ✅ Are Phases not skipped? (No shortcuts)
- ✅ Is the return from Phase ⑥ to Phase ④ correctly implemented?
- ✅ Does it not proceed to Phase ⑧ without going through Phase ⑦?

---

## Summary

**By following this "single path"**:
- ✅ Processing flow is consistent
- ✅ Multiple operations are integrated into one pipeline
- ✅ Bugs are easy to identify
- ✅ Adding new features is easy
- ✅ AI can develop while maintaining design

**Most Important Instruction to AI**:
When you implement new features, always read this file and determine "which Phase to integrate into." Do not create new pipelines; integrate into this single path.
