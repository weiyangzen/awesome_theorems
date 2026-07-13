# THM-M-1486 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the catalog label `深度学习`
(deep learning). The repository supplies only the gloss `深层神经网络` (deep neural networks),
attributes it to many mathematicians in the twenty-first century, and labels it `已验证`. A field
name and model-family noun phrase do not form a truth-valued proposition with ordered binders,
hypotheses, and a conclusion. The verified label is untrusted metadata and supplies neither source
nor proof credit.

Deep learning can support many inequivalent mathematical claims: a proposition about a
source-frozen layered-network definition, a universal-approximation theorem, a depth-separation or
expressiveness theorem, optimization or training convergence, generalization or statistical
consistency, robustness, or correctness and complexity of one architecture. The catalog fixes none
of the network architecture, depth and width,
activation or pooling operations, scalar and data domains, parameter space, loss, optimizer,
probabilistic model, approximation norm, quantifier order, constants, or conclusion. Selecting any
one familiar theorem would invent proposition-changing mathematics.

There is a particularly credible but uncredited formal lead. The official Archive of Formal Proofs
entry *Expressiveness of Deep Learning* by Alexander Bentkamp (2016) formalizes in Isabelle/HOL a
network-capacity result based on Cohen, Sharir, and Shashua's 2016 tensor analysis. The pinned
mathlib file `Mathlib.Data.Holor` explicitly says its tensor library is based on that AFP entry.
Nevertheless, the repository record cites neither work and never mentions expressiveness, tensor
rank, deep-versus-shallow separation, convolutional arithmetic circuits, or a measure-zero claim.
The AFP theorem therefore cannot be substituted for this unidentified root, and it is not a Lean 4
proof candidate in the current dependency closure.

The provisional vector is `[H5, M4, R4]`. `H5` says that the received catalog phrase is not yet one
stable truth-valued proposition; it does not refute established deep-learning theorems. `M4` records
that no source-identical usable Lean artifact has been located, and `R4` records that no proof
reconstruction can attach to the unidentified root. `IntakeProbe.lean` authenticates adjacent
pinned tensor and approximation APIs only. All six downstream phases remain open. No canonical
statement, H0, M0, R0, accepted state, audit completion, theorem completion, or master acceptance
is claimed.

## Dossier navigation

- `instance.json`: structured intake authority and provisional H/M/R classification.
- `scope-map.md`: proposition choices and target boundaries that remain open.
- `source-statement-crosswalk.md`: literal catalog record and uncredited source/formal leads.
- `task-dag.json`: open scheduler-phase projection and internal rev-5.6 planning tasks.
- `IntakeProbe.lean`: discovery-only checks of adjacent pinned Lean APIs.
- `validation.md`: exact validation scope, commands, results, and known failures.
- `intake-receipt.json`: provisional, unaccepted worker receipt.
