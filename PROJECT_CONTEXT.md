# Project Context Management Protocol (PCMP)

**Version:** 1.0  
**Files:** `PROJECT_CONTEXT.md` / `PROJECT_CONTEXT_ZH.md`  
**Scope:** AI-Agnostic / IDE-Agnostic Context Protocol  
**Canonical Entry Point:** This document defines the **protocol**. Active project state is maintained under **`ai/`**.

---

## 1. Core Principles

1. **Current State First**: AI agents must read `STATE.md` and `TASK.md` first. Never reconstruct current state by reading entire session histories.
2. **Code as Ground Truth**: When documentation conflicts with actual code, the source code and tests are authoritative. Stale documentation must be updated.
3. **Minimal Context**: Maintain only decision-relevant and actionable information. Old sessions should be periodically compressed.
4. **AI-Agnostic**: Independent of any specific model, IDE, prompt format, or agent platform. Operates solely via filesystem and Markdown.
5. **Phase-Independent Architecture & Traceability Specification**: Each development phase must maintain its own independent specifications under `docs/S{N}-{short_name}/` (e.g. `docs/S1-minimal-core/`):
   * **Requirements-Features-Methods Traceability Matrix (`requirements_traceability.md`)**: Defines a clear mapping from user requirements to system capabilities and concrete code methods/functions, enabling future AI-driven iterative design and development;
   * **Independent 4+1 Architectural View (`4_plus_1_view.md`)** and **Core Sequence Diagrams (`sequence_diagrams.md`)**: Accurately documents physical implementations, component dependencies, and invocation boundaries.
6. **Decoupling Protocol from Product Code**: PCMP is strictly an engineering management protocol for human-AI collaboration on this repository. It must NEVER be hardcoded into product source code (e.g. `backend/`, `frontend/`) as a business dependency. The developed product must remain general-purpose and independent.
7. **Dual-Track Project Structure & Standard Naming (S & S1~Sx)**:
   * **Phase Standalone Projects (`phases/S{N}-{short_name}/` ➔ e.g. `phases/S1-minimal-core/`)**: Named with `S` + stage index + stage abbreviation. Each phase maintains its own self-contained codebase specifically fulfilling that phase's milestone goals, facilitating independent retrospective analysis.
   * **Continuous Evolution Project (`continuous/` ➔ S)**: Represents the full integrated product, merging verified code from completed phases as development progresses.

---

## 2. Context Directory (`ai/`)

```text
ai/
├── PROJECT.md          # Project identity, purpose, goals & scope (Long-lived)
├── ARCHITECTURE.md     # System architecture, components & constraints (Long-lived)
├── STATE.md            # Current project state snapshot (Dynamic)
├── TASK.md             # Active task & acceptance criteria (Dynamic)
├── PLAN.md             # High-level roadmap & milestones (Dynamic)
├── DECISIONS.md        # Architecture Decision Records (ADR, Long-lived)
├── ISSUES.md           # Known issues & risk tracking (Dynamic)
├── sessions/           # Session history (Append-oriented, periodically compressed)
└── proposals/          # Protocol improvement proposals (Append-oriented)
```

### File Responsibilities

| File / Dir | Responsibility | Nature |
| :--- | :--- | :--- |
| `PROJECT.md` | Name, description, target users, goals, scope & non-goals | Long-lived |
| `ARCHITECTURE.md` | Tech stack, system architecture, components, data flow & constraints | Long-lived |
| `STATE.md` | State snapshot: completed, in progress, blocked, risks, next action | Dynamic |
| `TASK.md` | Active task: objective, why, scope, criteria, progress, immediate action | Dynamic |
| `PLAN.md` | Current phase, milestone, next steps & longer-term roadmap | Dynamic |
| `DECISIONS.md` | ADRs: context, decision, reason, alternatives, consequences | Long-lived |
| `ISSUES.md` | Issue tracking: ID, status, description, impact, workaround, component | Dynamic |
| `sessions/` | Structured session records (`SESSION-YYYY-MM-DD-NNN.md`) | Append-only |
| `proposals/` | Protocol enhancement proposals (`PROPOSAL-NNN-title.md`) | Append-only |

---

## 3. Schema Specifications

### 3.1 `STATE.md` (State Snapshot)
Must remain concise for instant agent ingestion:
* **Last Updated**: Date
* **Overall Status**: Current phase status
* **Completed**: Completed key items
* **In Progress**: Active work items
* **Blocked**: Blockers
* **Current Risks & Focus**: Active risks and current focus
* **Immediate Next Action**: Exact next step

### 3.2 `TASK.md` (Active Task)
Tracks only the **single currently active task**:
* **Current Task & Objective**: Task title and main goal
* **Why & Scope**: Context, included / excluded scope
* **Acceptance Criteria**: Verifiable criteria
* **Current Progress & Blocker**: Progress and blockers
* **Immediate Next Action**: Immediate next step

### 3.3 `DECISIONS.md` (Architecture Decision Records - ADR)
Mandatory for changes affecting architecture, APIs, dependencies, data models, or security boundaries:
```markdown
## DEC-NNN — Decision Title
Date: YYYY-MM-DD | Status: Accepted / Proposed / Deprecated / Superseded
- Context: Current situation and problem
- Decision: Selected solution
- Reason: Why this solution was chosen
- Alternatives: Options evaluated and why they were rejected
- Consequences: Positive outcomes, constraints, and trade-offs
```
> **Rule**: Never silently reverse accepted decisions; propose a superseding decision instead.

### 3.4 `sessions/SESSION-YYYY-MM-DD-NNN.md` (Session Record)
Created upon completing each meaningful coding session:
```markdown
# Session YYYY-MM-DD-NNN
- Metadata: Date / Agent / Task / Status
- Goal & Why
- What: Actual code/config changes made
- Result: Verification results & new state
- Issues & Decisions
- Next: Immediate recommended follow-up
```

---

## 4. Workflow & Priority

### 4.1 Takeover Procedure
```text
1. Read PROJECT_CONTEXT.md / ZH
   ↓
2. Read ai/STATE.md & ai/TASK.md (Grasp status & active task)
   ↓
3. Read ai/ARCHITECTURE.md / PLAN.md / DECISIONS.md as needed
   ↓
4. Inspect relevant source code and tests
   ↓
5. Identify Immediate Next Action and proceed
```

### 4.2 Session Completion Workflow
```text
1. Validate code & run tests
   ↓
2. Review changed files (git status / diff)
   ↓
3. Write ai/sessions/ session record
   ↓
4. Update ai/STATE.md & ai/TASK.md
   ↓
5. Update PLAN.md / DECISIONS.md / ISSUES.md as appropriate
   ↓
6. Update Immediate Next Action
```

### 4.3 Conflict Resolution Priority
```text
Actual Code & Tests (Highest) > STATE.md > TASK.md > DECISIONS.md > PLAN.md > Historical Sessions (Lowest)
```
> Discrepancies between code and docs must be treated as **context consistency issues** and corrected immediately.

---

## 5. Standard Human Prompts

Human developers can copy and use the following standard commands across any AI coding agents:

### 5.1 Project Context Initialization
> `Read PROJECT_CONTEXT.md, initialize the ai/ project context management system, and assess the current project state.`

### 5.2 Takeover & Continue (New AI / New Session)
> `Read PROJECT_CONTEXT.md and take over the project. Review ai/STATE.md and ai/TASK.md, then continue the active task.`

### 5.3 Read-Only Status & Consistency Assessment
> `Read PROJECT_CONTEXT.md and assess the current project status and architecture consistency. Do not modify any code.`

### 5.4 Architecture Planning & Decision Proposal
> `Read PROJECT_CONTEXT.md, review ai/PLAN.md, and propose the next development steps or architectural decisions. Do not modify code.`

### 5.5 Issue Diagnosis & Tracking
> `Read PROJECT_CONTEXT.md, diagnose this issue, record it in ai/ISSUES.md, and propose a fix.`

### 5.6 Finalize Coding Session
> `Finalize the current session per PCMP: verify code and tests, record the session under ai/sessions/, and update ai/STATE.md and ai/TASK.md.`

---

## 6. Governance & Human Approval Boundary

### 6.1 AI Permissions
* **Allowed**: Update `ai/` state, task, plan, sessions, issues, and accepted decisions; compress old history.
* **Prohibited**: Scope creep without approval; modifying this protocol without human sign-off.

### 6.2 Human Approval Required
* Changing core project goals and product identity.
* Changing fundamental architectural principles or reversing major accepted decisions.
* Modifying protocol rules and schema definitions.
* Removing core security constraints and safety guardrails.

---

## 7. Compliance Checklist

- [ ] **Before Session**: Read protocol, identify active task in `STATE.md`/`TASK.md`, inspect relevant code.
- [ ] **During Session**: Stay within scope; document architectural changes in `DECISIONS.md`.
- [ ] **After Session**: Implementation verified, `SESSION` record created, `STATE.md` and `TASK.md` updated with next action.