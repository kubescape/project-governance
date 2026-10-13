# Kubescape Project Roadmap

This document outlines the development roadmap for Kubescape, an open-source Kubernetes security platform.

It is a high-level view of where the project is going, meant to give you a first impression rather than a delivery plan. For tickets and specific features, refer to the project roadmap table on GitHub.

**Current planning period: 2026H2 and 2027H1.**

Last reviewed at the [quarterly maintainer meeting of 16 September 2026](meetings/2026-09-16-maintainers-quarterly.md).

## How to read this roadmap

The roadmap is organised by product area. Each item carries:

* a **sponsor**, a maintainer who owns the item's direction, reviews and contributor collaboration. A sponsor does not necessarily implement the item personally; they are the person to talk to if you want to work on it;
* a **horizon**, the period we expect the work to land in. `26H2` is July to December 2026, `27H1` is January to June 2027;
* the **open questions** that still need answering. These are the best places for the community to contribute, and an item is usually not ready for implementation until they are resolved.

Items below the sponsored sections are carried in the [backlog](#backlog-) and [wishlist](#wishlist-). They have been discussed but have no sponsor and no horizon yet.

The roadmap is reviewed and updated at the quarterly maintainer meeting. See [GOVERNANCE.md](GOVERNANCE.md#maintainer-meetings) for how those meetings work, and [meetings/](meetings/) for the minutes that drive changes to this document.

---

## 1. Product security

### 1.1 API hardening review

**Sponsor:** @slashben, @amirmalka | **Horizon:** 26H2 review, 27H1 refactor

Kubescape's internal APIs assume a trusted network. The operator's trigger-action handler authenticates nothing and leans on the websocket in front of it. Review the API surface across operator, node-agent, storage and synchronizer, and refactor it onto established authenticated mechanisms rather than implicit trust. Longer term this points toward a CRD-driven control plane instead of ad-hoc HTTP APIs, using the custom resource status field where a response is required.

Exposing Kubescape over MCP (see 5.1) adds another API surface and belongs in the same review.

**Open:** is the CRD migration the vehicle for this, or a separate track?

## 2. Node agent

### 2.1 Runtime observability

**Sponsor:** @matthyx | **Horizon:** 26H2

Users today fall back to separate projects like Pixie for visibility that node-agent's eBPF layer already sees. Surface process, network and file events as a first-class observability output, not just as detection input, streamed to an endpoint over OpenTelemetry. The driving use case is security forensics: answering what happened on a workload after the fact.

**Open:** which events and in what shape, and whether this lands in OSS node-agent or the private one.

### 2.2 Prevention and sandboxing

**Sponsor:** @amirmalka | **Horizon:** 26H2 to 27H1

Node-agent detects but does not block. Add enforcement: eBPF sandboxing as a usable alternative to raw Seccomp, plus network, file and process restrictions applied in real time, built in cooperation with Inspektor Gadget. Compared with Seccomp the advantages are live updates of enforcement policy and argument-level filtering. Behavioral profiling feeds policy generation, but enforcement is the deliverable.

**Open:** how users configure and interact with enforcement, which needs a design before implementation; what is OSS Kubescape versus the ARMO platform; and how this rides on the existing application-profile and rule-binding machinery.

### 2.3 Container profile signature

**Sponsor:** @matthyx | **Horizon:** TBD

Container profiles now support wildcards, so users can supply their own profiles alongside learned ones and drive rule alerting from them. A profile that can be edited in the cluster can also be tampered with, so profiles need to be digitally signed and verified before they are trusted.

This lines up with an EU cloud security initiative aiming to require software providers to ship a "software bill of behavior" alongside an SBOM: a signed, vendor-supplied statement of how a workload is expected to behave.

**Open:** there is no standard today for what gets signed, by whom, and how it is verified offline. A cluster running workloads from many vendors implies a multi-vendor signature ecosystem, which is an ecosystem problem and not only a design one. This needs a design document before work starts.

## 3. Configuration scanning policy

### 3.1 CEL controls alongside Rego

**Sponsor:** @rotemamsa | **Horizon:** 26H2

There is growing demand for writing controls in CEL, partly because Kubernetes admission supports CEL natively. Build Kubescape so that it can run CEL rules alongside OPA/Rego rules, giving users a choice of engine. The near-term goal is coexistence; a Rego replacement may follow eventually, but no deprecation date is set.

**Open:** coexistence or migration with a Rego deprecation date, a control-by-control parity matrix, and whether the merged CEL guide is enough for new contributors.

## 4. Vulnerability intelligence

### 4.1 VEX ingestion

**Sponsor:** @matthyx | **Horizon:** 26H2

Consume external VEX feeds, such as Red Hat CSAF and Chainguard OpenVEX, to suppress CVEs someone has already triaged. The LFX mentorship (September to November 2026) is the delivery vehicle: VEXSource CRD, fetch/validate/persist pipeline, suppression logic. Evidence that grype mis-applies Red Hat's own advisories is the case for doing this properly.

**Open:** organise feeds by library or per image.

## 5. AI and agentic workloads

### 5.1 Kagent and MCP support

**Sponsor:** @slashben, @rotemamsa | **Horizon:** TBD

Expose Kubescape to AI agents through Kagent integration and MCP server support, so posture, vulnerability and runtime data are queryable by agents rather than only by humans.

The hard part is data shaping rather than protocol. Returning a large structure such as an SBOM directly to an agent exhausts its context window, so the exposed surface needs query and filter semantics, comparable to the filtering the UI already performs over the same data. This is also the answer to why agents cannot simply read the raw CRs through the Kubernetes API.

**Open:** which surfaces to expose first, and read-only versus action-taking.

### 5.2 Kubernetes Agent Sandbox

**Sponsor:** @amirmalka | **Horizon:** exploratory, 27H1

Kubernetes now has an Agent Sandbox for running AI agents as workloads, a new and largely unsecured workload class. Define what Kubescape does for it: posture checks, runtime rules, or enforcement on sandboxed agent workloads.

**Open:** is this a real user need yet, or positioning ahead of the curve?

## 6. Multi-cluster data plane

**Sponsor:** @Bezbran | **Horizon:** TBD

Heavy users run Kubescape across many clusters and currently write custom scripts to pull results out of each one. Build a data plane that ingests CRDs and scan findings from multiple clusters into one place so they can be queried together.

Scope is the data plane only. Building a UI on top of it is out of scope for the open-source project.

**Open:** whether the goal is consolidating the data or only storing it centrally, and where the boundary sits between this and the control plane.

---

## Backlog 📅

Discussed at a high level, not ready for development, and not yet sponsored.

### Core platform enhancements

- [ ] Deprecation of Kollektor and Gateway components (as Synchronizer takes over them)
- [ ] Reimplement the data backend of the Storage component so it can become scalable horizontally
- [ ] Moving to image based Gadgets with Inspektor Gadget
- [ ] Moving the Host scanner functionality to the Node-agent
- [ ] Scanning container image on the host filesystem

### Security features

- [ ] Scanning for misplaced secrets in container images (Monitoring phase)
- [ ] Scanning the Kubernetes host and kernel for vulnerabilities (Monitoring phase)
- [ ] Produce fixed paths for HELM charts (CI/CD phase)
- [ ] Implement a rule based alerting system in Kubescape to send notifications (Monitoring phase)

### User experience

- [ ] Integration with more image registries for vulnerability scanning
- [ ] Kubescape CLI control over cluster operations
- [ ] Create Kubescape HELM plugin for Kubescape
- [ ] Creating more user guides

## Wishlist 💭

Features we are dreaming of 😀 and want to push gradually forward.

- Integrate with other Kubernetes CLI tools
- Add visualization in K9s
- Kubernetes audit log integration
- Scanning Dockerfile-s for security best practices
- Custom controls and rules

## Completed features 🎓

* Runtime detection based on eBPF
* Layer 7 (HTTP) parsing in eBPF to create visibility over which workload uses which APIs
* Storage and Node-agent memory and CPU consumption
* Improve image scanning performance and resource utilization
* Kubelet configuration validation
* API server configuration validation
* Image vulnerability scanning based controls
* Assisted remediation (telling where/what to fix)
* Integration with Prometheus
* Configuration of controls (customizing rules for a given environment)
* Installation in the cluster for continuous monitoring
* Host scanner
* Cloud vendor API integration
* Custom exceptions
* Custom frameworks

## Contributing

We welcome contributions from the community. Please check our [Contributing Guidelines](CONTRIBUTING.md) for more information on how to get involved. If an item above interests you, the sponsor is the person to talk to.

## Note

This roadmap is a living document, updated quarterly at the maintainer meeting based on community feedback and evolving security needs. Priorities and timelines may shift as we progress.
