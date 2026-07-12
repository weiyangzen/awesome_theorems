# THM-M-1357 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for `THM-M-1357`, the Nyquist
stability criterion. The repository supplies only the gloss `反馈系统的稳定性` (stability of a
feedback system), attribution to Harry Nyquist, the year 1932, and an untrusted `已验证` label. It
does not cite or state a proposition.

The title names a theorem family, not one binder-complete claim. It leaves open the feedback
interconnection and sign, continuous- versus discrete-time model, SISO versus MIMO scope, transfer
function class, stability notion, Nyquist contour and orientation, pole and zero count conventions,
boundary singularities, and cancellation or minimality assumptions. A familiar formula such as
`N = Z - P`, or a closed-loop-stability equivalence derived from it, would therefore add choices
that are absent from the repository source.

`instance.json` freezes this ambiguity as `[H5, M4, R4]`. `scope-map.md` records the decisions
needed to identify one proposition, and `source-statement-crosswalk.md` maps every catalog word to
its unresolved mathematical content. Crossref identifies H. Nyquist's 1932 paper *Regeneration
Theory* as a plausible primary-source lead, but metadata alone does not select a theorem or supply
an assumption crosswalk. It receives no source-fidelity credit at intake.

`IntakeProbe.lean` elaborates only adjacent pinned meromorphic-divisor, logarithmic-derivative, and
circle-parameterization APIs. These interfaces neither define a feedback system nor state or prove
the Nyquist criterion. All six downstream tasks remain open in `task-dag.json`.

The lifecycle is `planned`. No canonical mathematical or Lean statement, H0, M0, R0, accepted
proof state, audit completion, theorem completion, or master acceptance is claimed.
