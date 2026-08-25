---
name: baby
description: Explain, rewrite, or compare a topic in simple, progressive, concrete language without undefined jargon. Use when the user asks for "baby mode", "mode baby", "explain it simply", "explique-moi simplement", "break it down step by step", "detaille pas a pas", an explanation for a teenager or beginner, a more accessible rewrite, or a clear comparison of technical choices and tradeoffs.
author: François-Xavier Guillois
version: 4.7.0
vibe_version: ">=1.0.0"
permissions:
  - bash
tags:
  - productivity
  - workflow
  - automation
---

Read [host portability](../../references/host-portability.md) before resolving plugin files, invoking sibling skills, or persisting project guidance.

# Baby — plain-language explanations

## Adapt the response

1. Reply in the user's language.
2. Infer the user's goal and current level from the request. Never use a patronizing tone.
3. Give the essential idea first in one or two sentences.
4. Break the explanation into small, ordered steps.
5. Define each necessary term when it first appears.
6. Follow every abstract idea with a short concrete example or analogy.
7. Preserve nuances that affect a decision or prevent a mistake. Explicitly flag any important simplification.

Prefer short sentences and paragraphs no longer than three lines. Use jargon only when it helps the user, then translate it immediately into plain language.

## Rewrite content

Preserve the meaning, facts, conditions, and warnings from the source. Reorganize the information in this order:

1. what it is;
2. what it is for;
3. how it works;
4. an example;
5. the key takeaway.

Do not introduce new claims unless they are necessary to explain the content. Clearly distinguish an added fact from a reformulation.

## Explain a concept

Use this structure when the topic is primarily conceptual:

- **In short**: define it in plain language;
- **Step by step**: explain the mechanism in a few steps;
- **Example**: give a real case or analogy;
- **Key takeaway**: summarize it in one sentence.

For a very simple request, shorten the structure instead of filling every section artificially.

## Present technical choices

First identify the criteria that matter in context, such as cost, simplicity, control, performance, maintenance, security, or scalability.

For each option, state:

- what it is;
- its main advantage;
- its main drawback;
- when it is a good fit.

Compare options with a short list or table when that improves readability. Make a conditional recommendation based on the available information. If one missing fact could change the recommendation, ask one focused question. Otherwise, state the assumption and proceed.

## Check the response

Before answering, verify that:

- the main idea appears before the details;
- no important term remains unexplained;
- the example genuinely clarifies the concept;
- technical tradeoffs are visible;
- simplification does not become misleading;
- the length matches the request.

End with a question only when it helps the user choose, go deeper, or provide missing information.
