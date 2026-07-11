# Source-statement crosswalk

| Claim component | Repository source | Lean discovery candidate | Intake assessment |
|---|---|---|---|
| Attribution | `Docs/researches/math_theorems.md`: Cartan/Eilenberg, 1956 | none | Bibliographic hint only; no edition, theorem, page, or errata |
| Root wording | "existence of left/right derived functors" | `AbelianDerivedCanonicalStatement` | Candidate chooses degreewise abelian-resolution semantics not fixed by the source |
| Left derived | no domains or hypotheses | `F.leftDerived n` under `HasProjectiveResolutions C` and `F.Additive` | Plausible branch, but assumptions cannot be credited to the source yet |
| Right derived | no domains or hypotheses | `F.rightDerived n` under `HasInjectiveResolutions C` and `F.Additive` | Plausible branch, but assumptions cannot be credited to the source yet |
| Total derived | not distinguished | mathlib Kan-extension APIs wrapped in `S1_M_095` | Non-equivalent branch; not a replacement for the degreewise statement |
| Consequences | not stated | acyclic-object, degree-zero, naturality, and long-exact wrappers | Discovery inventory only; scope membership unresolved |

The manifest's `source_status_untrusted` value is metadata, not H evidence. The legacy Lean module
contains real checked-looking declarations but is explicitly unaccepted under rev-5.6 and cannot
resolve what the human source intended. The statement phase must first select a primary edition and
pin an exact theorem/page with all assumptions, then normalize ordered binders and test the legacy
candidate by elaboration and mutations. Until then the exact-source gate remains `H4` and the exact
machine-statement gate remains `M4`.
