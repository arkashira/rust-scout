## partner-targets.md  
**Product:** rust‑scout – curated discovery & management of star‑trending Rust crates  
**Goal:** Accelerate Rust developers’ workflow by surfacing high‑quality libraries, providing usage metrics, and enabling seamless import into projects.  

| # | SaaS / API | Core Capability | Free‑Tier Limits* | Integration Effort | Primary User Job Solved | Revenue‑Share / Affiliate Potential |
|---|------------|----------------|-------------------|--------------------|--------------------------|--------------------------------------|
| 1 | **GitHub (Octokit) API** | Pull latest crate repo metadata, stars, forks, CI status, release notes | 5 k requests / hour (unauthenticated) – unlimited with OAuth app | **S** (OAuth flow, webhook setup) | “Find trustworthy crates” – real‑time popularity & health signals | GitHub Marketplace revenue‑share (10 % on paid app installs) |
| 2 | **crates.io API** (official) | Authoritative crate download counts, version history, license data | Unlimited (rate‑limited 60 req/min) | **S** (simple REST wrapper) | “Assess adoption & stability” – download trends & version churn | No direct revenue‑share, but can negotiate “featured crate” sponsorships |
| 3 | **OpenAI / Claude (Chat Completion)** | Generate concise crate summaries, usage examples, and migration guides on‑demand | 5 M tokens / month (free tier) | **M** (API key mgmt, prompt engineering, caching) | “Understand how to use a crate” – instant docs & code snippets | Affiliate per‑token usage (OpenAI) + potential upsell to premium LLM tier |
| 4 | **Dependabot / Renovate API** | Auto‑detect outdated dependencies in a user’s Cargo.toml and suggest upgrades | Free for public repos; private limited to 100 repos | **M** (webhook listener, diff generation) | “Keep projects up‑to‑date” – proactive upgrade alerts | Partner program offers revenue‑share on paid private‑repo usage |
| 5 | **Gitpod (Workspace API)** | One‑click spin‑up of a cloud IDE pre‑loaded with selected crates for rapid prototyping | 100 hrs / month free (public repos) | **L** (OAuth, workspace config templates) | “Try a crate instantly” – reduces friction of local setup | Affiliate per‑user seat conversion (15 % on paid plans) |
| 6 | **Sentry (Error Monitoring)** | Auto‑inject Sentry SDK snippets into generated example projects, surface runtime error trends for crates | 5 k events / month free | **M** (SDK init, DSN handling) | “Validate crate reliability” – monitor real‑world error rates | Referral commission on upgraded plans |
| 7 | **StackShare API** (via partner) | Pull community‑curated “stack” recommendations that include Rust crates | 1 k calls / day free (partner tier) | **S** (simple lookup) | “Build a full stack” – suggest complementary services (DB, CI) | Potential co‑marketing + affiliate on StackShare premium |
| 8 | **RapidAPI Marketplace (search aggregator)** | Expose rust‑scout as a searchable API for other developer tools (e.g., IDE plugins) | 1 M calls / month free | **M** (API gateway, auth) | “Integrate rust‑scout into IDEs & CI pipelines” – extend reach | Revenue‑share on API consumption (15 % of paid usage) |

\*Free‑tier limits are current as of 2026‑06‑17; they may change.  

---

### Integration Roadmap (Quarterly)

| Quarter | Milestones | Target Partners (order of priority) | Success Metrics |
|---------|------------|--------------------------------------|-----------------|
| **Q1** | 1️⃣ Core data ingestion layer <br> • Implement GitHub + crates.io sync <br>2️⃣ Basic UI for star‑trending list <br>3️⃣ Affiliate tracking for GitHub Marketplace | 1. GitHub (high revenue‑share) <br>2. crates.io (essential data) | • 90 % of top‑500 crates refreshed daily <br>• 1 k sign‑ups from GitHub referral links |
| **Q2** | 1️⃣ Add LLM‑driven summaries (OpenAI/Claude) <br>2️⃣ Launch “One‑click demo” via Gitpod <br>3️⃣ Publish public API (RapidAPI) | 3. OpenAI (usage‑based affiliate) <br>4. Gitpod (conversion‑focused) | • Avg. summary latency < 2 s <br>• 30 % of demo clicks convert to trial accounts <br>• 5 k API calls via RapidAPI |
| **Q3** | 1️⃣ Dependency health alerts (Dependabot/Renovate) <br>2️⃣ Error‑monitoring hooks (Sentry) <br>3️⃣ Partner‑featured crates sponsorship program | 5. Dependabot (private‑repo upsell) <br>6. Sentry (monitoring upsell) | • 70 % of active users receive at least one upgrade alert <br>• 15 % of demo projects enable Sentry integration |
| **Q4** | 1️⃣ Stack recommendations (StackShare) <br>2️⃣ Release partner SDKs (VS Code, JetBrains) using RapidAPI endpoint <br>3️⃣ Revenue‑share audit & optimization | 7. StackShare (co‑marketing) <br>8. RapidAPI (usage revenue) | • 2 k “full‑stack” suggestions generated <br>• 10 % of API consumers upgrade to paid tier <br>• Overall partner‑generated ARR ≥ $25 k |

---

### Prioritization Rationale

1. **Revenue‑share potential** – GitHub, OpenAI, Gitpod, RapidAPI, Dependabot, Sentry all offer measurable affiliate or usage‑based payouts.  
2. **Core data dependency** – crates.io & GitHub are non‑negotiable for accurate popularity & health signals.  
3. **User friction reduction** – LLM summaries, one‑click demos, and auto‑updates directly address the primary jobs‑to‑be‑done (discover, evaluate, adopt).  
4. **Scalability** – All selected APIs have generous free tiers that support early‑stage growth; upgrade paths are clear for paid‑user conversion.  

--- 

*Prepared by Business‑Synthesis (Axentx OS) – Q2 2026*