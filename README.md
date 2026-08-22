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
* Langfuse / Observability tooling

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

The adversarial test demonstrated controlled tool failure, fallback recovery, conflicting evidence detection, verification, uncertainty-aware reasoning, and autonomous replanning.

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
* Accuracy and quality
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

All evaluated runs demonstrated grounded responses, uncertainty handling, hallucination checking, and recovery. Repeated runs were also used to evaluate consistency.

Measured latency ranged from **35.31 seconds to 76.79 seconds**, with an average latency of **58.48 seconds**.

## Task 7 — Advanced Tracing & Observability

AgentX includes an observability demonstration covering:

* End-to-end tracing
* Agent decision tracing
* Prompt tracing
* Tool-call tracing
* Latency tracking
* Error tracking
* Controlled failure injection
* Root-cause diagnosis
* Automatic recovery
* Before-vs-after measurement

A controlled research-tool failure was injected and diagnosed automatically. The system recovered using a fallback tool.

### Before vs After

| Metric            |    Before |     After | Improvement |
| ----------------- | --------: | --------: | ----------: |
| Execution time    | 0.302 sec | 0.151 sec |         50% |
| Tool calls        |         4 |         2 |         50% |
| Errors            |         2 |         0 |        100% |
| Task success rate |      100% |      100% |  Maintained |
   
The observability test generated a trace file:

```text
task7_trace.json
```

The implementation is available in:

```text
obervability.py
```

Token usage was identified as unavailable in the local simulated trace because no LLM API response token metadata was collected by this standalone observability demonstration.

### Task 7 Result

**Task 7 completed successfully**, demonstrating tracing, controlled failure detection, automatic diagnosis, recovery, and measurable before-vs-after improvement.

## Repository

The complete AgentX implementation, evaluation scripts, observability implementation, trace output, and supporting tools are available in this repository.
