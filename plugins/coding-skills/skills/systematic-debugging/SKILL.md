---
name: systematic-debugging
description: Use when investigating unexplained failures, regressions, or incorrect behavior - reproduces symptoms, tests competing hypotheses, and verifies a causal fix.
license: CC-BY-SA-4.0
---

# Systematic debugging

Drive the investigation with evidence that can distinguish plausible causes.
Scale the process to the failure; an obvious localized defect need not pass through
formal phases. Preserve the user's requested scope, including diagnosis-only work.

## Establish what fails

Record expected versus observed behavior and the relevant command, input, version,
configuration, or environment. Reproduce safely with the smallest useful case.
For intermittent failures, retain frequency and timing information; a single clean
run does not establish a fix. Do not probe live systems or expose secrets without
appropriate authorization.

Inspect the complete error and nearby execution path, including callers and recent
changes. Separate symptoms from assumptions. When a pipeline crosses boundaries,
check the actual values, shapes, configuration, or ownership at each relevant
boundary rather than assuming an upstream component supplied the expected input.

## Test causes

Form a specific hypothesis with an observation that would support or contradict it.
Compare working and failing cases and choose a small, discriminating experiment:
reduce the input, inspect intermediate state, isolate a component, or vary one
relevant condition. Avoid bundling unrelated fixes that conceal which change mattered.

Instrumentation should expose the needed evidence without leaking sensitive data
or materially changing timing. For performance failures, establish a representative
measurement and control major sources of variance before attributing a bottleneck.

If a result contradicts the hypothesis, update it. Track what has been ruled out
when an investigation spans multiple attempts or sessions. Repeated failed changes
are a reason to reconsider assumptions and experiment quality; they do not prove
an architectural flaw or mandate an arbitrary attempt-count approval gate.

## Fix and verify within scope

Once the evidence supports a cause, make a targeted correction if implementation
is authorized. Preserve unrelated user work and remove temporary instrumentation
unless it serves an agreed diagnostic purpose.

Add a regression check when practical and verify the original reproduction plus
relevant adjacent contracts. For intermittent behavior, explain what repeated or
deterministic evidence supports the result and what uncertainty remains.
A passing test unrelated to the reported failure is not verification of that fix.

If progress requires missing access, unsafe reproduction, or a consequential scope
change, report the evidence, remaining hypotheses, and specific blocker. Avoid
repeating experiments that cannot resolve the uncertainty.

Use the existing plan/progress record for longer work; no separate debugging plan
is required. `writing-good-tests` can guide regression coverage, but TDD and other
skills are not mandatory prerequisites. Finish with the cause or current evidence,
changes if any, verification performed, and unresolved limitations.

Attribution and adaptation licensing: [LICENSE](LICENSE).
