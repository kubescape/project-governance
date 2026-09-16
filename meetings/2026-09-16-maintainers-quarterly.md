# Kubescape Maintainers' Quarterly Meeting, 2026-09-16

**Date:** 16 September 2026
**Type:** Quarterly maintainer meeting (per [GOVERNANCE.md](../GOVERNANCE.md#maintainer-meetings))

**Present:** Matthias Bertschy (@matthyx), Ben Hirschberg (@slashben), Rotem Refael (@rotemamsa), Bezalel Brandwine (@Bezbran)
**Apologies:** Amir Malka (@amirmalka)

**Quorum:** 4 of 5 core maintainers present, so quorum was met for maintainer-level decisions.

> Items assigned below to maintainers who were not present are **tentative** and will be confirmed asynchronously.

---

## Summary

The meeting covered three themes: project governance (a new Triager role and clearer ownership of security reports), security architecture (internal API hardening, container profile signatures, node-agent enforcement), and the 2026H2 / 2027H1 roadmap, where each item was given a maintainer sponsor.

---

## Decisions

### D1. Create a GitHub Triager role

The project establishes a **Triager** role for active returning contributors who currently have no permissions to help manage the backlog.

* **Permissions:** close, label and assign issues and pull requests. No merge rights.
* **Term:** one year, subject to re-evaluation at the maintainer meeting; renewal depends on continued active participation.
* **Approval:** by simple majority of the maintainer team, the same mechanism used for maintainers.
* **Motivation:** several returning contributors, including contributors from the LFX mentorship programme, have been doing issue triage and bug scrubs without the permissions to act on it.

**Status:** approved by the maintainers present. To be formalised by a PR against this repository (see A1).

### D2. Security report handling has a named owner

Incoming security reports were accumulating without a dedicated owner. **Bezalel Brandwine takes ownership of all incoming security reports and acts as the point of contact until the end of 2026.** A durable process covering owner, channel and response clock is to be defined within that period.

### D3. Every roadmap item gets a maintainer sponsor

Roadmap items will no longer rely on a single maintainer. Each item gets a **sponsor** from the maintainer team. Sponsoring means owning the item's direction, reviews and contributor collaboration. It does not mean implementing it personally.

---

## Discussion

### Governance and contributors

Contributor activity has grown, including returning contributors from the LFX mentorship programme, several of whom have been verifying and triaging issues. The Triager role (D1) addresses the permissions gap. Annual re-evaluation was added so the role reflects actual participation rather than becoming permanent by default.

### Product security

**Security report handling.** Two reports are open and unanswered, both arriving via the CNCF maintainers list, where non-member posts wait for approval. Beyond closing these out, the project needs a written intake path. Moving to GitHub private vulnerability reporting was raised as the likely destination, along with deciding who is on the rotation. (See D2.)

**API hardening.** Kubescape's internal APIs assume a trusted network; the operator's trigger-action handler authenticates nothing and relies on the websocket in front of it. Two directions were discussed:

* a short-term internal API key distributed as a Kubernetes secret;
* moving away from HTTP APIs entirely and driving components through CRDs, using the custom resource **status** field where a response is required.

The agreed first step is a review of the API surface across operator, node-agent, storage and synchronizer to identify which endpoints can move to CRDs and which need authentication, rather than committing to the CRD migration up front. Whether the CRD-driven control plane is the vehicle for this or a separate track remains open.

It was also noted that exposing Kubescape over MCP adds another API surface, and that it should be considered as part of the same hardening review rather than separately.

### Node agent

**Runtime observability.** Users currently reach for separate projects such as Pixie for visibility that the node-agent's eBPF layer already has. The proposal is to stream process, network and file events to an endpoint using OpenTelemetry, making observability a first-class output rather than only a detection input. The original trigger, replacing Pixie for a specific contributor, turned out not to be a direct fit, but the security-forensics use case stands on its own. It was noted that OpenTelemetry instrumentation could be applied to other components too. Open: which events and in what shape, and whether this lands in the OSS node-agent.

**Prevention and sandboxing.** Node-agent detects but does not block. The plan is eBPF-based enforcement, meaning network, file and process restrictions applied at runtime, built in cooperation with the Inspektor Gadget team through prevention gadgets. Compared with Seccomp, the advantages are live updates of enforcement policy and argument-level filtering. Open: what is OSS Kubescape versus the ARMO platform, and how enforcement rides on the existing application-profile / rule-binding machinery. A recurring question from the discussion, not yet answered: **how users configure and interact with enforcement**. This needs a design before implementation.

**Container profile signatures.** Following wildcard support in container profiles, users can supply custom profiles alongside learned ones. To prevent tampering of profiles inside the cluster, a digital signature scheme was proposed. This aligns with an EU cloud-security initiative, driven by a community contributor, aiming to require software providers to ship a "software bill of behavior" alongside an SBOM. Concerns were raised that a multi-vendor signature ecosystem inside a cluster is an ecosystem problem, not only a design problem: there is no standard today for what gets signed, by whom, and how it is verified offline. Treated as ambitious; needs a design document before work starts.

### Configuration scanning policy

**CEL alongside Rego.** There is growing demand for writing controls in CEL, partly because Kubernetes admission supports CEL natively. The target is for Kubescape to run CEL rules alongside OPA/Rego rules, giving users a choice of engine. Asked whether CEL should simply replace Rego, the position taken was coexistence first. A replacement may follow eventually, but no deprecation date was set. Open: a control-by-control parity matrix, and whether the merged CEL guide is sufficient for new contributors. This was also a focus area during the LFX term.

### Vulnerability intelligence

**VEX ingestion.** Kubescape can already ingest VEX feeds into its results. The LFX mentorship (Sep to Nov 2026) is the delivery vehicle for consuming external feeds such as Red Hat CSAF and Chainguard OpenVEX to suppress already-triaged CVEs. What the item needs is a maintainer owner for reviews, merges and contributor collaboration. Open: organising feeds by library or per image.

### AI and agentic workloads

**MCP support.** Work is in progress on PRs making Kubescape usable by AI agents over MCP. The main technical challenge is data shaping: returning large structures such as SBOMs directly to an agent exhausts its context window, so the MCP surface needs query and filter semantics rather than raw dumps, comparable to the filtering the UI already does over the same data.

It was questioned whether custom MCP APIs are needed at all, given that agents can talk to the Kubernetes API directly. The counter-argument is the same data-shaping problem: raw CRs are too large and unshaped to be useful to an agent. Open: which surfaces to expose first, and read-only versus action-taking.

**Kubernetes Agent Sandbox.** The upstream Agent Sandbox project has recently moved to 1.1 / 1.2. It represents a new and largely unsecured workload class, and what Kubescape does for it, whether posture checks, runtime rules, or enforcement, is undefined. Exploratory, 27H1. Open: whether this is a real user need yet.

### Multi-cluster data plane

Heavy users currently write custom scripts to pull CRDs and findings across many clusters. The proposal is a data plane that aggregates CRDs and scan findings centrally. Questions raised: whether the goal is consolidation or just storage (S3 was suggested as a naive alternative), and the boundary between data plane and control plane. Scope agreed: data plane only, no UI. See D4.

### Community and ecosystem

**LinkedIn presence.** Kubescape has no dedicated LinkedIn page, so project news rides on personal and ARMO accounts. Contributors have asked for one so they can point to their work. Setup steps have been received from CNCF marketing. Open: who owns posting, and the cadence (releases, CNCF milestones, contributor highlights).

---

## Roadmap sponsors

Sponsors for the 2026H2 / 2027H1 roadmap, as recorded in the roadmap document. The roadmap itself will be published in this repository as a separate PR (see A7).

| # | Item | Sponsor | Horizon |
|---|------|---------|---------|
| 1.1 | Security report handling | @Bezbran (to EOY 2026) | 26H2 |
| 1.2 | API hardening review | @slashben, @amirmalka | 26H2 review, 27H1 refactor |
| 2.1 | Runtime observability (OTEL event streaming) | @matthyx | 26H2 |
| 2.2 | Prevention & sandboxing | @amirmalka | 26H2 to 27H1 |
| 2.3 | Container profile signature | @matthyx | TBD |
| 3.1 | CEL controls alongside Rego | @rotemamsa | 26H2 |
| 4.1 | VEX ingestion | @matthyx | 26H2 |
| 5.1 | Kagent & MCP support | @slashben, @rotemamsa | TBD |
| 5.2 | Kubernetes Agent Sandbox | @amirmalka | exploratory, 27H1 |
| 6 | Multi-cluster data plane | @Bezbran | TBD |
| 7.1 | Kubescape LinkedIn presence | @slashben, Oshrat (handle TBD) | TBD |

* @amirmalka was not present, so 2.2 and 5.2 are to be confirmed with him (see A9).

---

## Action items

| # | Owner | Action | Due |
|---|-------|--------|-----|
| A1 | @matthyx | Open a PR on `project-governance` formalising the Triager role (D1) | TBD |
| A2 | @Bezbran | Take over all incoming security reports and act as point of contact | EOY 2026 |
| A3 | @slashben | Run the API hardening review: identify unauthenticated internal APIs and which can move to CRDs | 26H2 |
| A4 | @matthyx | Act as emissary for the container profile signature work, giving design and verification support | TBD |
| A5 | @slashben | Find a co-sponsor for the node-agent observability item | TBD |
| A6 | @slashben | Contact Oshrat about the steps to establish a Kubescape LinkedIn page | TBD |
| A7 | @slashben | Open a PR on `project-governance` publishing the updated roadmap with owners | TBD |
| A8 | @matthyx, @rotemamsa | Hand over the CEL work from Matthias to Rotem | TBD |
| A9 | @slashben | Confirm the tentative roadmap assignments with @amirmalka asynchronously | TBD |

---

## Next meeting

Next quarterly maintainer meeting: **TBD** (second Monday, three months out, per GOVERNANCE.md).
