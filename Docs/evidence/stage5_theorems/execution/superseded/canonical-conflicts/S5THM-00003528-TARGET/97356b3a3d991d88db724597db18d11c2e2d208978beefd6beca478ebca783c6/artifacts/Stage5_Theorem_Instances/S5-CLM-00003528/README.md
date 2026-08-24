# S5-CLM-00003528 — Borwein sine series

This directory is the complete target-local evidence package for frozen theorem `BorweinSineSeries.borwein_sine_series`, variant `ATV-00003528`, and current Stage6 alias `S6-CLM-00003985` / `S6-VAR-00006196`.

The exact claim is convergence of

\[
\sum_{n\ge 1}\frac{(2/3+(1/3)\sin n)^n}{n}.
\]

The provider declaration is sorry-backed and is used only to bind the statement. Claim-owned Lean surfaces live under `Formalizations/Lean/AwesomeTheorems/Stage5/Theorems/S5_CLM_00003528/`; they import `Mathlib` and retain the unavailable provider module/declaration as exact provenance comments.

Start with `intake.json` and `statement-crosswalk.json` for identity, `proof-units.json` plus `full-study.md` for the proof/readability DAG, `machine-closure.json` for the proposed M0-L closure, and `receipts/release-decision.json` for the provisional handoff. Structured evidence is intentionally not repeated in prose.

The worker validator runs only with `--no-lean`. Canonical Master alone may compile at trust zero, accept the integrated package, and advance the theorem checklist.
