# AgentX — Research & Competitor Intelligence Agent

## Team Members

* Gayatri Dayanand Bhagwat
* Gadekar Varsha Vilas
* Gawali Shravani Ganesh
* Patil Dnyaneshwari Pravin

## Problem Statement

Organizations need timely information about research, competitors, patents, and industry developments. Manual monitoring is time-consuming and can miss important updates.

## Project Description

**AgentX** is an autonomous AI-powered Research & Competitor Intelligence Agent using a ReAct-style workflow. It can plan tasks, select tools, gather evidence, analyze information, verify claims, detect uncertainty, recover from failures, and generate actionable intelligence.

## Agent Workflow

```text
User Goal
   ↓
Planning
   ↓
Tool Selection
   ↓
Parallel Execution
   ↓
Evidence Collection
   ↓
Analysis
   ↓
Verification
   ↓
Self-Evaluation
   ↓
Replanning
   ↓
Final Intelligence Report
```

## Technologies Used

* Python
* OpenRouter / OpenAI-compatible API
* LangGraph
* Streamlit
* ReAct Agent Architecture
* Tool Calling
* Scientific Research APIs
* News APIs
* Git & GitHub

## Task 5 — Adversarial Testing

AgentX was tested in adversarial mode for:

* Dynamic planning
* Multi-agent orchestration
* Parallel execution
* Tool failure and fallback
* Conflicting evidence
* Verification
* Uncertainty handling
* Autonomous replanning
* Loop/deadlock detection
* Resource-aware execution
* Self-evaluation

## Task 6 — Evaluation

AgentX was evaluated across multiple scenarios:

* Normal
* Ambiguous
* Adversarial
* Contradictory
* Incomplete
* Tool Failure
* Repeated runs

Evaluation criteria included:

* Task completion
* Groundedness
* Hallucination checking
* Uncertainty handling
* Failure recovery
* Consistency
* Latency
* Resource efficiency
* Adversarial robustness
* Baseline comparison

### Evaluation Result

**8/8 test runs completed successfully (100% completion rate).**

The evaluation also measured average, minimum, and maximum latency and included repeated-run consistency testing.

## Repository

The complete AgentX implementation, evaluation scripts, and supporting tools are available in this repository.
