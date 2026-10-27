# Security Venues, Ethics & Open Science Reference (2026 Edition)

Consolidated submission, ethics, and artifact rules for top security and privacy venues. Always verify cycle-specific deadlines against the live Call for Papers.

---

## 1. Big-Four & Peer Security Venues Overview

| Venue | Body Page Limit (typical) | Review Mode | Distinctive Requirements |
|-------|---------------------------|-------------|--------------------------|
| **USENIX Security ('26)** | ≤ 13 pages body + up to 1p `Ethical Considerations` + up to 1p `Open Science` (20p total camera-ready) | Double-blind | Mandatory registration 1 week prior; **no major revision in '26** (at most 2-week shepherding); **artifacts must be available at submission time** (anonymized) or justified in `Open Science`; max 7 submissions/author/cycle. |
| **IEEE S&P (Oakland)** | ≤ 13 pages body (excl. refs/appendices) | Double-blind | Strong threat model and practical significance bar; rolling cycles; Artifact Evaluation badges (`Available`, `Functional`, `Reproduced`). |
| **ACM CCS** | ≤ 12–13 pages body (`acmart sigconf,anonymous`) | Double-blind | Explicit track selection (Systems/Web Security vs. Applied Crypto vs. ML Security); strong end-to-end baseline and ablation expectations. |
| **NDSS** | ≤ 13 pages body | Double-blind | Strong focus on network, web, distributed, and real-world system attacks/defenses; concrete PoC and deployment realism prized. |
| **PETS / PoPETs** | ≤ 16 pages body | Double-blind | **Ethics-first culture**; strict `(ε, δ)` + composition + privacy-unit accounting for any DP claim. |
| **ACSAC / AsiaCCS / RAID** | 12–14 pages body | Double-blind | Strong applied/deployment focus; excellent venues for well-engineered security systems and empirical studies. |

> **Topic Selection Rule for ML-in-Security (per USENIX Security '26 CFP):**  
> If a paper uses ML/LLMs *to solve a security task* (e.g., Web phishing detection, vulnerability discovery, penetration testing), tag the **primary topic as the security problem domain** (*Web Security*, *Software Security*, *Systems Security*), **not** *Security of ML*. Reserve *Security of ML* for attacks/defenses on the ML lifecycle itself (poisoning, backdoors, prompt injection, model extraction).

---

## 2. Stakeholder-Based Ethics Analysis (Menlo Report Framework)

Draft the ethics analysis during **pilot design (`sec-idea-creator`)**, not the night before submission.

1. **Identify Stakeholders**: end users, website/service operators, software vendors, cloud providers, and the research team itself.
2. **Apply the Four Menlo Principles**:
   - **Respect for Persons**: informed consent, privacy of user data, no deanonymization.
   - **Beneficence**: maximize security benefit while minimizing tangible harm (service disruption, state corruption, CPU/human triage cost on live services).
   - **Justice**: fair selection of targets; avoid disproportionate burden on vulnerable populations.
   - **Respect for Law and Public Interest**: compliance with authorization scope, terms-of-service risk analysis, and coordinated disclosure.
3. **Live-System Rule**: never test live third-party Web services without consent when a local container or synthetic deployment can answer the scientific question. If observational measurement of public endpoints is essential, minimize request rate, never mutate state or access private user data, and document both mitigated and unmitigated risks.

---

## 3. Responsible Disclosure Timeline Template (90-Day Standard)

```latex
\section*{Ethical Considerations}
\paragraph{Stakeholder Analysis and Experimental Isolation.}
All vulnerability discovery and exploitation experiments in Sections~\ref{sec:pilot}--\ref{sec:eval} were conducted exclusively against locally deployed, containerized instances running on isolated laboratory hardware. No unconsented requests were sent to live production services, and no real user data was accessed.

\paragraph{Coordinated Vulnerability Disclosure.}
For the [N] previously unknown vulnerabilities identified in open-source packages, we initiated coordinated disclosure immediately upon confirmation:
\begin{itemize}
  \item \textbf{YYYY-MM-DD:} Privately reported root cause, affected versions, and minimal PoC to vendor/maintainers via [GitHub Security Advisories / security@vendor].
  \item \textbf{YYYY-MM-DD:} Vendor acknowledged receipt and confirmed reproduction.
  \item \textbf{YYYY-MM-DD:} Patches released in versions [X.Y.Z]; assigned \texttt{CVE-YYYY-NNNNN}.
\end{itemize}
We adhered to a 90-day disclosure window. Raw exploit payloads for unpatched installations are withheld from the public artifact to prevent premature weaponization.
```

---

## 4. Open Science & Anonymized Artifact Template (USENIX Security '26 Ready)

```latex
\section*{Open Science}
To support replicability and artifact evaluation, we provide all source code, benchmark configurations, containerized target applications, and raw evaluation logs at our anonymized repository: \url{https://anonymous.4open.science/r/REPO-SLUG}.

\begin{itemize}
  \item \textbf{Source Code \& Harnesses:} Implementation of [System Name] and baseline wrappers (\texttt{src/}, \texttt{benchmarks/}).
  \item \textbf{Reproducibility Scripts:} One-command scripts mapping directly to paper claims (\texttt{./reproduce-table-1.sh}, \texttt{./reproduce-figure-3.sh}), with estimated wall-clock runtime and hardware requirements documented in \texttt{README.md}.
  \item \textbf{Safety Omissions:} [If applicable: "To prevent abuse against unpatched deployments of Package X, the automated exploit weaponization module is replaced with a benign state-check oracle; full details were shared with the vendor under CVE-YYYY-NNNNN."]
\end{itemize}
```
