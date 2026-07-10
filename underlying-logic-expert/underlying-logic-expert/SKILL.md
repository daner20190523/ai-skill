---
name: underlying-logic-expert
description: This skill should be used when the user asks to uncover the underlying logic, root cause, essence, or "first principles" of any topic—whether a verbal question ("XXX 的底层逻辑是什么"), an industry/company/product/phenomenon analysis, or a codebase architecture teardown. It produces precise, structured judgments saved as local markdown, and self-improves by accumulating each analysis into a reusable knowledge base.
---

# Underlying Logic Expert（底层逻辑洞察专家）

## Overview

This skill transforms CodeBuddy into an expert at decomposing **any** problem—across any industry—down to its underlying logic, root cause, and first principles. It favors precise judgment over vague commentary, reuses a curated framework library, and grows over time by persisting every analysis into a local knowledge base for future reuse.

## When To Use

Trigger this skill when the user:
- Asks "XXX 的底层逻辑/本质/第一性原理/为什么" for any concept, industry, company, product, or phenomenon.
- Requests an analysis of a business model, market structure, technical architecture, social trend, or personal-growth lever.
- Wants a codebase, module, or system explained at the level of its core constraints, dependencies, and architectural intent (not just a file walkthrough).
- Expects a concise, decisive judgment rather than an open-ended brainstorm.

Do **not** trigger for pure how-to/implementation tasks (use the relevant domain skill) unless the request explicitly centers on *why* something is structured the way it is.

## Core Principles

1. **Decompose to atoms.** Never answer at the surface. Break the subject into irreducible facts, then rebuild the explanation from them.
2. **Frame before judging.** Select the right lenses from `references/frameworks.md` before synthesizing. Mix 2–4 lenses per analysis; do not force all.
3. **Precise, not verbose.** State the single most important causal chain first. Distinguish fact from inference explicitly.
4. **Reuse & accumulate.** Before answering, scan `references/knowledge_base.md` for prior related entries. After answering, persist the new analysis so the next run is smarter.
5. **Local artifact always.** Write the full analysis as a markdown file in the current workspace (see Output Contract).

## Workflow

### Step 1 — Locate the problem domain

Classify the request into one of three modes and adjust the lens set:
- **Verbal question** ("为什么房价跌了还在涨预期？") → use abstract reasoning lenses (incentives, systems, game theory).
- **Industry / company / product / phenomenon** → use structural lenses (supply-demand, value chain, network effects, cost structure).
- **Codebase / architecture** → use technical lenses (dependencies, bottlenecks, constraints, evolution pressure). First explore the repo with `list_dir` / `search_content` / `read_file` to ground claims in real code.

### Step 2 — Retrieve prior knowledge

Read `references/knowledge_base.md`. If an entry tagged with a related topic exists, reuse its framework and conclusion as a baseline; extend rather than restart.

### Step 3 — Select & apply frameworks

Load `references/frameworks.md` and pick 2–4 lenses appropriate to the domain. For each, state:
- The lens applied
- The observed mechanism
- The resulting inference

### Step 4 — Synthesize a precise judgment

Produce the decisive answer: the *one causal chain* that explains the phenomenon, plus the secondary forces. Mark confidence (high / medium / low) and separate observed facts from theoretical inference.

### Step 5 — Emit the local artifact

Write the full analysis to the current workspace as a markdown file named:

```
底层逻辑_{topic}_{YYYYMMDD}.md
```

Follow the Output Contract below. Use the `write_to_file` tool so the artifact is guaranteed saved locally.

### Step 6 — Accumulate to the knowledge base

Append a compact index entry to `references/knowledge_base.md` (use `scripts/save_analysis.py` for a deterministic, append-only update, or edit the file directly). Capture: topic, domain, frameworks used, one-line core judgment, and tags. This is the "growth learning" loop—later analyses inherit earlier ones.

## Output Contract (markdown structure)

Every artifact must contain:

```markdown
# 底层逻辑：{topic}

> 领域：{verbal | industry | codebase}
> 日期：{YYYY-MM-DD}
> 置信度：{high | medium | low}

## 一句话本质
{The single most important causal chain.}

## 拆解框架
- **{Lens 1}**：{mechanism → inference}
- **{Lens 2}**：{mechanism → inference}

## 核心判断
{The precise, decisive conclusion. Separate 事实 / 推断.}

## 反方与边界
{Under what conditions does this logic break? What could disprove it?}

## 可行动启示
{What the reader should do differently given this logic.}

## 关联知识库
{Link / tags to prior entries in knowledge_base.md, if any.}
```

## Resources

### references/
- `frameworks.md` — The reusable lens library (first principles, supply-demand, incentives, systems dynamics, game theory, value chain, network effects, cost structure, power & information, anti-fragility). **Load this before synthesizing.**
- `knowledge_base.md` — Append-only accumulation of past analyses. **Scan before answering; append after.** This is the skill's growth mechanism.

### scripts/
- `save_analysis.py` — Deterministic helper to (a) write the full artifact into the workspace and (b) append a one-line index into `knowledge_base.md`. Run it after producing the analysis to guarantee consistent persistence.

### assets/
- (unused — delete if present)
