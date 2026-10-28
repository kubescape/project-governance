# Security Issue Triage Guide

Maintainer guide for triaging issues and advisories framed as "security".
Applies to all repositories in the kubescape organization.
Goal: decide in under 5 minutes if a report is a vulnerability, hardening, or a feature.
The baseline is the [threat model](threat-model.md).

## Step 1: Identify the attacker

Ask: who is the attacker, and what access do they already have?

- No attacker named → not a vulnerability. Reclassify.
- Attacker is a cluster user or workload acting within their RBAC → trusted. Reclassify.
- Attacker is a cluster user or workload gaining access **beyond** their RBAC through a Kubescape component → **in scope**. Continue to Step 2.
  - Exception: if the gain relies only on reaching an unauthenticated in-cluster endpoint, this is the documented known limitation → hardening, not a vuln.
    See "Known limitations" in the [threat model](threat-model.md).
- Attacker is a local user/process on the scan machine → out of scope. Reclassify.
- Attacker controls input to `scan` (chart, manifest, repo, image) → **in scope**.
- Attacker is on the network / supply chain → **in scope**.

Remember: reports and policy artifacts fed back into Kubescape are not scan input.
Loading them is a user trust decision, like running a script.

## Step 2: Identify the gain

Ask: what does the attacker gain that they did not already have?

- Code execution, file writes, or network calls from scan input → vulnerability.
- Privilege escalation via our component's RBAC or host access → vulnerability.
- Reading data their RBAC already allows → nothing gained. Close as by-design.
- "Could be safer / best practice" → hardening, not a vulnerability.

## Step 3: Classify

| Verdict | Criteria | Action |
|---|---|---|
| Vulnerability | Steps 1+2 both pass | Private report, fix, advisory |
| Hardening | Real risk reduction, no concrete attack | Public issue, label `security-hardening` |
| Quality | False negatives, wrong results | Label `bug`, prioritize by user impact |
| Feature | New control, new capability, docs | Label `feature`, normal backlog |

## Step 4: Route

- Vulnerabilities: ask the reporter to use GitHub private vulnerability reporting
  per [SECURITY.md](../SECURITY.md). Do not discuss exploit details in public issues.
- Declined advisories: use the canned response below, fix valid hardening publicly,
  and credit the reporter in the public issue/PR.
- Everything else stays public with the right label.

## Red flags that it is NOT a security issue

- The "attack" starts with "a user with cluster-admin...".
- The report is a scanner/scorecard output with no attack scenario.
- The fix is "add a doc" or "add a badge".
- The report proposes a new Kubescape control. That is a feature for regolibrary.
- The CVE is in a dependency but the vulnerable function is unreachable.
- The prerequisite is the user loading an attacker-supplied artifact by choice.

## Red flags that it IS serious

- Scanning a file/chart does something besides reading it.
- A default install grants our components more RBAC than the docs claim.
- Release artifacts can be altered without detection.
- The tool reports "pass" for a config that Kubernetes treats as allowed/exploitable.

## Canned responses

**By-design (authenticated access):**
> Kubescape assumes cluster access requires authentication.
> Users with API access are trusted per their RBAC.
> This report does not cross that boundary, so we're treating it as a feature request.

**Hardening:**
> Thanks — this is a valid hardening improvement, not an exploitable vulnerability.
> Relabeling as security-hardening and keeping it open.

**Declining an advisory:**
> Thanks for the report. Kubescape's threat model treats access already granted
> by RBAC as trusted, and local machine security as the operator's responsibility.
> Your report does not show an actor gaining access beyond what they already hold,
> so we are not treating this as an exploitable vulnerability.
> It is a valid hardening improvement — we will fix it in a public issue/PR
> and credit you there. Closing this advisory without a CVE.

## Multi-repo note

Issues land on many repos (node-agent, operator, storage, helm-charts, regolibrary...).
Triage with the same model everywhere.
Vulnerabilities from any repo route to the kubescape/kubescape advisory flow.
