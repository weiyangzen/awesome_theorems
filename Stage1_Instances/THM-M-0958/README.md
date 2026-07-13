# THM-M-0958 rev-5.6 statement dossier

This directory is the fail-closed `planned` intake dossier for the catalog entry `Elkin
construction`. The repository supplies only the gloss `improvement of the Behrend construction`,
attributes it to Michael Elkin in 2011, and labels it verified. Under rev-5.6 that label is
untrusted inventory metadata, not an exact source statement or proof evidence.

An inspected primary-source lead identifies the intended family much more closely: Michael
Elkin's *An Improved Construction of Progression-Free Sets*, arXiv `0801.4310v1` (2008), later
published in *Israel Journal of Mathematics* 184 (2011), pages 93-128, DOI
`10.1007/s11856-011-0061-1`. The preprint defines progression-free subsets of
`{1, ..., n}` and reports an asymptotic lower bound improving Behrend by a factor of order
`sqrt(log n)`. The inspected arXiv version is a strong source lead, but the catalog does not cite an
edition, the final journal text was not admitted and cross-checked, and exact formula transcription,
source-version differences, assumptions, corrections, errata, and independent review remain open.
No `H0` claim is made.

Pinned mathlib supplies `ThreeAPFree`, `rothNumberNat`, interval translation infrastructure, and a
machine-checked Behrend lower bound. `IntakeProbe.lean` authenticates those interfaces. The pinned
Behrend result has a different, weaker quantitative bound; it is not Elkin's improvement and is not
credited as a target proof.

The statement phase now designates the SHA-256-pinned arXiv `0801.4310v1` PDF as the authoritative
statement edition. `Statement.lean` freezes equation (5) as an explicit expansion of the source's
`Omega` convention: a positive universal real constant, a positive natural threshold, and every
index at least that threshold. The root uses the source one-based extremal function and the exact
base-two formula. Checked iff transports expose both an explicit progression-free set witness and
mathlib's zero-based `rothNumberNat` form. The source distinct-triple predicate is also checked
against `ThreeAPFree`.

The two deletion-minimal imports are `Mathlib.Combinatorics.Additive.AP.Three.Defs` and
`Mathlib.Analysis.SpecialFunctions.Log.Base`. Four structural mutations cover a removed positivity
hypothesis, changed index domain, changed constant scope, and shifted interval endpoint. The
totalized scale and one-based interval at `n = 0` and `n = 1` are separately checked. The
provisional vector is now `[H1, M3, R4]`: the exact statement interface elaborates, but no proof
body or readable proof reconstruction is credited.

The SODA and journal headline formulas agree with arXiv v1, but their complete bodies were not
compared. In particular, the substantially longer 2011 journal version advertises an added
discrete-geometry application. Full edition comparison, correction and errata review, lawful
durable source admission, source-to-obligation mapping, and independent review remain H1 debt.

`instance.json` is the structured scope authority and `task-dag.json` keeps every downstream phase
open. The exact statement evidence is provisional pending dependency-ordered master acceptance.
No target proof, H0, M0, R0, audit completion, theorem completion, or release is claimed.
