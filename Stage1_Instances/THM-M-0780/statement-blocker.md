# Exact-statement gate: blocked

Item: `S56-M-0780-STATEMENT`  
Theorem: `THM-M-0780`  
Base revision: `9864b47f2fbf53d0b642c54f12039877d4635056`

## Decision

No exact Lean 4 target can be truthfully elaborated from the authoritative repository record. The
record names `科恩力迫法` ("Cohen forcing method") and gives only the gloss `证明CH独立于ZFC的方法`
("a method for proving CH independent of ZFC"). A method and its purpose do not determine a
proposition. Stage0 leaves the exact definitions, assumptions, proof route, axioms, and formal
artifact open, while the manifest preserves `已验证` only as untrusted source metadata.

At least four inequivalent roots remain compatible with the gloss:

1. relative consistency of `ZFC + not CH` from consistency of ZFC;
2. syntactic non-provability of CH from ZFC under an explicit consistency assumption;
3. full independence of CH, combining Cohen's direction with a distinct constructibility result;
4. construction of a generic extension satisfying `not CH`, or the forcing/truth theorem used in
   that construction.

These readings require different binders, hypotheses, conclusions, and proof boundaries. They also
leave open the object theory and its encoding, syntactic versus semantic consistency, the ground
model assumptions, forcing poset, genericity convention, extension semantics, CH definition, and
preservation results. Selecting any one of them would broaden or substitute the repository claim.
The adjacent `THM-M-0781` cannot resolve the ambiguity because it separately names Cohen's theorem
about CH and choice over ZF.

The intake identifies Cohen's 1963 papers only as source candidates; it records no inspected,
immutable edition, pinpoint theorem or stated result, incorporated definitions, assumptions,
errata disposition, or independent source approval. Consequently there is no canonical claim from
which to derive ordered binders, a minimal import, an elaborated expression fingerprint, checked
transports, or meaningful removed-hypothesis, changed-domain, binder-scope, and boundary mutations.
The rev-5.6 exact-statement gate fails before proof evidence may be inspected.

## Pinned Lean boundary

`IntakeProbe.lean` imports `Mathlib.ModelTheory.Bundled` and checks six generic first-order
model-theory declarations. It elaborates successfully in the pinned environment, showing that a
Lean toolchain and possible encoding substrate are available. It does not define ZFC, CH, forcing,
generic extensions, consistency, or independence and receives no statement or proof credit.

A narrow pinned-mathlib search found references to the earlier Flypitch CH-independence project in
model-theory module documentation and an unrelated use of GCH, but no repository-local declaration
whose type selects this target. This is environment assessment only, not the later immutable
formal-candidate audit. The existing canonical `.lake` link and artifacts were used read-only; no
update, build, clone, fetch, or dependency mutation command was run.

## Validation evidence

Commands ran in this worker clone on 2026-07-12 (Asia/Shanghai).

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups; 1546 uniform-L0 Lean 4 targets; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0780` | 0 | rank 785, planned, legacy artifacts unaccepted, theorem incomplete |
| `git rev-parse HEAD` | 0 | base revision shown above |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `cd Formalizations/Lean && lake --version` | 0 | Lake `5.0.0-src+98dc76e` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | mathlib `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | hashes `651c8acc...b1d2` and `321626c8...2d81` |
| repository `rg` search for the theorem ID, Chinese/English label, and source gloss | 0 | only the ambiguous metadata and intake boundary were found; no exact proposition |
| pinned-mathlib `rg` search for Cohen forcing, forcing relations/extensions, CH, and CH independence | 0 | documentation references and an unrelated GCH occurrence only; no target declaration selected |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0780/IntakeProbe.lean` | 0 | six generic model-theory API checks elaborated; no canonical target asserted |
| `rg -n '\b(sorry\|admit)\b\|^[[:space:]]*axiom\b' Stage1_Instances/THM-M-0780 -g '*.lean'` | 1 | expected no-match exit; no prohibited placeholder or axiom in owned Lean source |

## Retry condition and boundary

An accountable source reviewer must preserve and hash an immutable source edition, select and
transcribe one exact proposition with all incorporated definitions and assumptions, resolve the
four readings above, audit errata, and independently approve the source mapping. A later statement
run can then encode that same claim, minimize pinned imports, fingerprint the elaborated expression,
check any alternate transports, and execute all four required mutation classes.

This statement node remains `[ ]`, blocked at `M4`. The root remains `[H3, M4, R4]`, with
`audit_complete: false` and `theorem_complete: false`. The assigned phase is not genuinely
self-tested, so no `.stage1-worker-selftest.json` is emitted.
