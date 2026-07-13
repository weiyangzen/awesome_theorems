# THM-M-0483 rev-5.6 intake

This directory is the fail-closed `planned` dossier for `THM-M-0483`, the catalog entry named
"Mersenne primality determination." It starts from the uniform `L0 / rework_required` baseline and
does not inherit credit from the catalog's untrusted `已验证` label, pinned mathlib, or another
target's artifacts.

The repository supplies only the Chinese gloss `梅森数的素性检验`, an attribution to Edouard Lucas,
and the year 1876. That does not determine a unique truth-valued proposition. The date closely
matches Lucas's proof that the Mersenne number with exponent 127 is prime, while the wording can also
suggest a general primality criterion. The latter overlaps the distinct adjacent target
`THM-M-0484`, "Lucas-Lehmer test." The intake therefore preserves the literal family claim but
leaves the exact canonical statement and Lean target open.

`scope-map.md` separates the candidate theorem families and boundary cases.
`source-statement-crosswalk.md` maps every supplied source component and records the missing primary
source review. `instance.json` is the structured planned instance, `task-dag.json` retains the
provisional intake and all six downstream phases, and `intake-receipt.json` is an unaccepted worker
self-test receipt. `IntakeProbe.lean` checks only nearby pinned interfaces.

## Intake verdict

The proposed root vector is `H1 / M3 / R4`. `H1` records a strong immutable source lead but no
accepted pinpoint primary-source crosswalk or independent review. `M3` records exact-topic pinned
formal anchors whose mapping to this target is unresolved. `R4` records that no independently
reviewed readable proof exists. No exact statement, proof obligation, proof body, accepted receipt,
audit completion, theorem completion, or master acceptance is claimed.

## First blocker

An independent source and cross-target review must select an immutable exact proposition and decide
whether this target owns Lucas's 1876 `mersenne 127` primality result, a historical criterion, or
another source-defined claim. It must keep the general 1930 Lucas-Lehmer criterion within
`THM-M-0484` unless an explicit target reallocation is accepted. Only then may the statement phase
freeze binders, hypotheses, conclusion, boundary cases, a Lean expression, and its fingerprints.

## Validation boundary

The commands and exact results in `validation.md` self-test only this planned intake and its
discovery probe. The existing automation-provided `.lake` link was used read-only; no dependency or
shared authority was modified. Passing checks do not establish source fidelity, statement identity,
kernel closure, or any downstream gate.
