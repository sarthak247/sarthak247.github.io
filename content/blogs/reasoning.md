---
title: "Cracking the Code of LLM Reasoning - From Patterns to Thought Chains"
description: "What sets apart a reasoning LLM from a normal LLM? Can LLMs even reason? What can be done to make them reason better?"
slug: reasoning
date: 2025-05-21 00:00:00+0000
image: /blogs/reasoning/Gemini_Generated_Image_LLM_Reasoning.png
license: false
categories:
    - Reasoning
    - Large Language Models
    - Transformers
tags:
    - Reasoning
    - Chain of Thought
weight: 1       # You can add weight to some posts to override the default sorting (date descending)
---

## Motivation
Large Language Models (LLMs) are reshaping how we interact with technology—whether it's writing code, planning a trip, conducting web searches, or even solving high school math problems (to some extent). In many of these tasks, LLMs appear to *think*. But is that genuine reasoning... or just high-quality guesswork?

In this blog, I’ll explore what it really means for an LLM to "reason." I’ll look at how reasoning is evaluated, the techniques used to improve it, and the current state of the art. More importantly, I’ll dive into the challenges we still face and where future innovation might lie.

## From Where It All Began
Reasoning has long been a thorny problem in machine learning. Over the years, researchers have proposed many approaches to tackle it—each promising, but ultimately falling short. Some notable efforts include:
* Semi-supervised learning
* Bayesian Non-Parametric
* Kernel Machines
* Sparsity
* Low Rank
* Active Learning
* and much more...
But despite all the clever math and engineering, they all had one thing in common:
> They failed to truly crack reasoning.

## So, What's Missing?
The missing piece? **Reasoning itself.**

Most LLMs—and AI models in general—struggle not with computation, but with the **ability to generalize from a few examples**, to adapt flexibly, and to *reason*. That’s something humans do effortlessly: infer, extrapolate, and make decisions from limited information.

To illustrate this point, let’s walk through a simple toy example. We ask the model to extract the **last letter** from both the **first and last name** of a person and concatenate them. Why not use the *first* letters? Because that’s too easy—LLMs have likely seen patterns like that in training. But last letters? That’s more novel.
|Input|Output|
|--|--|
|Elon Musk|nk|
|Bill Gates|ls|
|Barack Obama|??|

For a human, the pattern is almost trivial: pick the last letter of each name and stick them together. But for an LLM? Things aren’t quite so straightforward.

1. **Solution 1 - Few-Shot Prompting:** Let's try a few-shot prompt:
    ```
    PROMPT:
    Q: Elon Musk
    A: nk
    Q: Bill Gates
    A: ls
    Q: Barack Obama
    A: 
    ```

    ```
    ANSWER:
    ck
    ```

    **ck??** Seriously?? The model focused only on the first name ("Barack" → "ck") and ignored "Obama" completely. So much for intelligence, right? It’s just pattern-matching—no real understanding or reasoning is going on.

2. **Solution 2 - Add Intermediate Steps:** What if we guide the model step-by-step? Maybe it just needs a little *direction*.

    Let’s rewrite the prompt to walk it through some intermediate steps:

    ```
    PROMPT:
    Q: Elon Musk
    A: The last letter of Elon is n. The last letter of Musk is k. So concatenating them together gives us nk. Thus, the answer is nk.

    Q: Barack Obama
    A:
    ```

    
    ```
    ANSWER:
    The last letter of Barack is k. The last letter of Obama is a. So concatenating them together gives us ka. Thus, the answer is ka.
    ```

    **Boom!** That works. Turns out LLMs aren’t dumb—they’re just easily confused. When we prompt them with intermediate steps, they begin to reason (or atleast that's what the literature wants us to believe).

    - [Large Language Models Cannot Self-Correct Reasoning Yet](https://arxiv.org/abs/2310.01798) - Shows that LLMs still struggle to reflect and fix errors independently
    - [Program Induction by Rationale Generation : Learning to Solve and Explain Algebraic Word Problems](https://arxiv.org/abs/1705.04146) Add intermediate steps to the training data.
    - [Training Verifiers to Solve Math Word Problems](https://arxiv.org/abs/2110.14168) - Add intermediate steps during the finetuning stage (used for finetuning GPT-3)
    - [Show Your Work: Scratchpads for Intermediate Computation with Language Models](https://arxiv.org/abs/2112.00114) - Essentially what we did above, ie, prompting with reasoning steps.
    - [Chain-of-Thought Prompting Elicits Reasoning in Large Language Models](https://arxiv.org/abs/2201.11903) - The GOAT paper for Reasoning by Denny Zhou which tied all these together and formally introduced the Chain-of-Thought term.

> Conclusion: Regardless of training, finetuning or prompting, when provided with examples that include intermediate steps, LLMs will respond with intermediate steps.

## Are reasoning steps even helpful?
What we just saw above is something termed as Chain Of Thought (CoT) or trying to add reasoning in the form of natual language and it can dramatically increase LLM performance on certain tasks. But here's the real question:
> **Is this actually reasoning, or are we just helping the model stumble forward by spoon-feeding it logic in natural language?**

To some extent, **yes**, it works - at least pragmatically. And this idea gets more formal backing in a recent paper - [Chain of Thought Empowers Transformers to Solve Inherently Serial Problems](https://arxiv.org/abs/2402.12875).
Here's the gist:
1. **✦ Claim:** Constant-depth transforers can solve any inherently serial problem as it generates sufficiently long intermediate reasoning steps!
    * 😐 Wait, what? That feels like a cop-out. Sure — if you let a model ramble on long enough, it’ll eventually land somewhere near the target. But that’s not intelligence. That’s **brute-force trial-and-error wrapped in verbose packaging.** The idea that longer chains = better reasoning feels shaky, and in my opinion, this approach may not be the path forward.
2. **✦ Claim:** Transformers which directly generate final answers either requires a huge depth to solve or cannot solve at all!
    * That’s... kind of damning. It shows that **Transformers struggle with multi-step reasoning by design** — unless we walk them through it explicitly. And let’s not forget: the Transformer wasn’t built to reason. It was built for **machine translation.** The architecture was never meant to reflect logic or cognition. Sure, we can bolt on reasoning heads, add rationale-based supervision, or inject scratchpads and verifiers — but all of that is a patch on a foundational problem:
    > Transformers can mimic reasoning — but they still don’t actually *reason*. At least not yet

## So What's Next?
If we agree that current LLMs are just *faking it till they make it* — mimicking reasoning rather than truly doing it — then where do we go from here?

I believe we need to **go back to the drawing board** — not just scaling up Transformers or adding more verbose prompts, but **reimagining the architecture and paradigm itself.**

Here are a few directions that I think hold actual promise:
* Graph-Based Models 🧠
Unlike flat sequences, graphs offer inherent **structure and relationships.** That structural bias could help encode reasoning chains more explicitly — think nodes as concepts and edges as logical links. There's real potential here for moving beyond pattern-matching.

* Memory-Driven Reasoning 💾
The idea of persistent memory — like what Meta’s **Segment Anything Model (SAM)** toyed with — could be transformative. Rather than treating each prompt as a clean slate, models should **retain and retrieve contextual knowledge** in a way that feels intentional, not incidental.

* Reinforcement Learning, Done Right 🎯
RL has shown flashes of brilliance (think AlphaGo, CICERO), but its fusion with LLMs has been underwhelming so far. We need **RL that incentivizes consistent, multi-step logic** — not just reward hacks or instruction following.

* Agentic Pathways (That Actually Think) 🤖
Everyone’s building “agents” these days, but most of them just chain prompts together and slap on some tool usage. That’s not reasoning — that’s **workflow automation in disguise.** The next generation of agents should be **explicitly designed to model beliefs, goals, and inference**, not just regurgitate natural language.

* Persona-Based LLMs 🧬
One-size-fits-all LLMs are bland. **Personalized models** — ones that adapt to users' thought styles, contexts, or even learning curves — might not just improve UX, but also unlock better reasoning by leveraging consistent mental models.

> In short: Let’s stop retrofitting Transformers and start **building models that reason by design**, not by accident.


## Appendix
<!-- - [Code for this blog](main.py) -->
- [Large Language Models Cannot Self-Correct Reasoning Yet](https://arxiv.org/abs/2310.01798)
- [Program Induction by Rationale Generation : Learning to Solve and Explain Algebraic Word Problems](https://arxiv.org/abs/1705.04146)
- [Training Verifiers to Solve Math Word Problems](https://arxiv.org/abs/2110.14168)
- [Show Your Work: Scratchpads for Intermediate Computation with Language Models](https://arxiv.org/abs/2112.00114)
- [Chain-of-Thought Prompting Elicits Reasoning in Large Language Models](https://arxiv.org/abs/2201.11903)
- [Chain of Thought Empowers Transformers to Solve Inherently Serial Problems](https://arxiv.org/abs/2402.12875)
- and many more but I forgot where I read them sigh...

> Photo by [Google Gemini](https://gemini.google.com/app) - Prompt: `a cartoonish image of LLM which is reasoning`
