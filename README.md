# Product Hunt

**Product Hunt** is a stateful product discovery agent that helps you search, compare, and choose products intelligently over time, with a strong focus on the Nigerian market.

It remembers how you shop, what you reject, what you trust, and what tradeoffs you consistently make, so you don’t have to redo the same research every single time.

---

## Why this exists

I shop online a lot.

And almost every time, the pattern is the same:

* I search for a product
* I open 15 tabs
* I compare prices, specs, vendors, warranties
* I hesitate
* I come back the next day
* I repeat the whole process because I forgot half the reasoning

Days pass. Decision fatigue sets in. Eventually I buy something, usually with mild regret and zero record of how I got there.

The core problem is not lack of information.
It’s lack of **memory**.

Most product search tools are stateless. Humans are not. Decisions are cumulative.

So I built Product Hunt to drastically cut down research time by remembering the reasoning, preferences, and tradeoffs that happen across sessions, not just within a single search.

---

## What Product Hunt does

Product Hunt helps you:

* Search for products intelligently
* Compare multiple options across vendors
* Find Nigerian sellers and buying options
* Understand tradeoffs clearly, not just prices
* Resume product research days or weeks later without starting from scratch

Over time, it learns how you shop and adapts its recommendations accordingly.

---

## What this is not

This is important.

Product Hunt is:

* Not a checkout system
* Not a marketplace
* Not a price guarantee service
* Not a general purpose chatbot
* Not trying to scrape the entire internet

It is a **reasoning system for product discovery**, not an ecommerce platform.

---

## Core ideas

A few principles drive this project:

* Product discovery is a reasoning problem, not just search
* Memory should be structured, explicit, and inspectable
* Agents should have clear responsibilities
* Deterministic reasoning beats “LLM vibes”
* Uncertainty is allowed, hallucination is not

This project favours clarity over cleverness.

---

## High level architecture

At a high level, the system works like this:

1. A user starts or resumes a session
2. A session orchestrator interprets intent
3. Product intelligence normalises and compares options
4. Vendor discovery finds Nigerian buying options
5. A ranking agent evaluates tradeoffs
6. Memory is committed at the end of the task

Nothing is written mid reasoning. Memory updates are deliberate.

---

## Agent roles

Product Hunt uses multiple agents with explicit boundaries.

**Session Orchestrator**
Owns the user session and memory lifecycle. Decides which agents to invoke and when memory can be written.

**Product Intelligence Agent**
Understands products abstractly. Normalises specs, identifies equivalence, and handles comparisons.

**Vendor Discovery Agent**
Finds Nigerian vendors using web search grounding. Extracts prices, availability, and seller information.

**Ranking and Tradeoff Agent**
Ranks options based on user preferences and learned heuristics. Explains why something is recommended, not just what.

Agents reason. Tools fetch data. Memory persists outcomes.

---

## Memory system

Memory is a first class concept in this project.

There are three types of memory:

**Episodic memory**
An append only event log of searches, comparisons, rejections, and decisions.

**Preference memory**
Stable beliefs inferred or explicitly stated, such as brand preferences, budget ranges, or vendor trust.

**Heuristic memory**
Explicit decision rules that guide ranking, such as prioritising warranty for high ticket items.

Memory is stored locally using TinyDB. It is human readable and intentionally simple.

---

## Product discovery and information retrieval

Product data is gathered using Google Search Grounding.

Search is treated as a noisy sensor, not a source of truth.

The system:

* Issues constrained, intentional search queries
* Extracts candidate product and vendor information
* Normalises messy results into structured data
* Reasons over uncertainty rather than pretending it does not exist

Scraping is deliberately minimal and only considered if search grounding proves insufficient.

---

## Example flow

A user searches for a 27 inch monitor under ₦300,000 in Lagos.

Product Hunt:

* Normalises the request
* Finds multiple vendors and listings
* Compares specs, prices, and warranties
* Ranks options with clear explanations
* Remembers which vendors were trusted or rejected

Days later, the user comes back and asks for alternatives.
The system already knows what “alternative” means in context.

---

## Tradeoffs and limitations

This project makes intentional tradeoffs:

* Coverage is incomplete
* Prices may be stale
* Vendor trust is heuristic based
* No real time guarantees are made

The goal is better decisions, not perfect data.

---

## Future extensions

Possible future work includes:

* Price change alerts
* Deeper vendor trust scoring
* Optional shared heuristics

This is a project, not a startup roadmap.

---

## Closing note

Product Hunt explores how agent systems can reason over time, not just respond to prompts.

If you have ever spent days researching a product and still felt unsure, this project exists for you.

