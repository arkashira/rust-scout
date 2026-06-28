## tech-spec.md – Rust‑Scout v1 Technical Specification  

---  

### 1. Stack  

| Layer | Choice | Rationale |
|-------|--------|-----------|
| **Language** | **Rust 1.73+** (stable) | Zero‑cost abstractions, safety, native performance for crawling & indexing crates. |
| **Web Framework** | **Axum** (tokio‑based) | Async‑first, modular routing, excellent integration with tower middlewares and OpenAPI generation. |
| **Database** | **PostgreSQL 15** (hosted on Supabase) | Relational model fits the library‑metadata schema; full‑text search + pg_trgm for fuzzy queries. |
| **ORM / DB Layer** | **SQLx (async, compile‑time checked)** | Compile‑time query validation, no runtime ORM overhead. |
| **Background Jobs** | **Tokio + Cron (cronjob crate)** | Simple in‑process scheduler for periodic crate crawling (daily). |
| **Cache** | **Redis 7 (managed on Fly.io)** | Hot‑list of trending crates, rate‑limit counters, session store. |
| **Search Engine** | **Meilisearch (self‑hosted on Fly.io)** | Instant typo‑tolerant search, relevance scoring for “star‑trending”. |
| **Container Runtime** | **Docker** (multi‑stage builds) | Guarantees reproducible builds; used by CI/CD and deployment platforms. |
| **Observability** | **OpenTelemetry** (traces, metrics) + **Grafana Loki** (logs) | Vendor‑agnostic telemetry; can be shipped to free‑tier Grafana Cloud. |
| **API Spec** | **OpenAPI 3.1** (auto‑generated via `utoipa`) | Enables client SDK generation and API‑first development. |
| **Auth** | **OAuth2 / OpenID Connect** (via **Auth0** free tier) | Secure, social login (GitHub, Google) for user‑generated lists & alerts. |
| **CI/CD** | **GitHub Actions** (free tier) | Lint, test, build, container push, and deploy to Fly.io. |

---

### 2. Hosting  

| Component | Provider (Free‑Tier First) | Deployment Model |
|-----------|---------------------------|------------------|
| **Web API** | **Fly.io** (free 3‑app allowance) | Docker container, region‑aware (auto‑scale to 1‑vCPU, 256 MiB). |
| **PostgreSQL** | **Supabase** (free tier: 500 MB, 2 GB bandwidth) | Managed instance, automatic backups. |
| **Redis** | **Fly.io Redis** (free tier) | In‑region, attached to API app. |
| **Meilisearch** | **Fly.io** (same app cluster) | Runs as side‑car container; data persisted on Fly volumes (free 1 GB). |
| **Static Assets / Docs** | **GitHub Pages** | OpenAPI UI (Redoc) + marketing site. |
| **Observability** | **Grafana Cloud** (free tier: 50 k series, 100 MiB logs) | Receives OTLP data from API containers. |

*All services are provisioned via Terraform (or Fly.io `fly.toml`) to enable reproducible infra. If usage exceeds free limits, upgrade paths are pre‑identified (Fly.io paid plan, Supabase Pro, Auth0 paid).*

---

### 3. Data Model  

#### 3.1 Core Tables (PostgreSQL)

| Table | Primary Key | Key Fields | Description |
|-------|-------------|------------|-------------|
| **crates** | `crate_id` (UUID) | `name`, `description`, `repository_url`, `homepage_url`, `license`, `latest_version`, `stars`, `downloads_last_30d`, `updated_at` | Canonical metadata for each Rust crate (populated from crates.io API). |
| **versions** | `version_id` (UUID) | `crate_id`, `semver`, `published_at`, `yanked` (bool) | Historical versions; enables “latest stable” logic. |
| **trending_snapshots** | `snapshot_id` (UUID) | `taken_at`, `crate_id`, `rank`, `stars_delta_7d`, `downloads_delta_7d` | Daily snapshot of trending calculation; used for historical charts. |
| **users** | `user_id` (UUID) | `auth0_id`, `email`, `created_at`, `last_login` | Auth0‑linked user profile. |
| **watchlists** | `watch_id` (UUID) | `user_id`, `crate_id`, `created_at`, `notify_via` (enum: email, slack) | User‑curated lists + optional alerts. |
| **api_keys** | `key_id` (UUID) | `user_id`, `hashed_key`, `created_at`, `revoked_at` | Optional programmatic access for CI pipelines. |

#### 3.2 Search Index (Meilisearch)

- **Index name:** `crates_search`
- **Document fields:** `crate_id`, `name`, `description`, `tags`, `stars`, `downloads_last_30d`, `rank` (from latest snapshot)
- **Searchable attributes:** `name`, `description`, `tags`
- **Sortable attributes:** `stars`, `downloads_last_30d`, `rank`

#### 3.3 Cache (Redis)

| Key Pattern | Value | TTL |
|-------------|-------|-----|
| `trending:today` | JSON array of top‑50 crate IDs | 24 h |
| `rate_limit:{user_id}:{endpoint}` | integer counter | 1 min |
| `session:{session_id}` | serialized session data | 30 min |

---

### 4. API Surface  

All endpoints are versioned under `/api/v1`. Responses are JSON; errors follow RFC 7807 problem‑details.

| Method | Path | Purpose | Auth |
|--------|------|---------|------|
| **GET** | `/crates` | List crates with pagination, optional filters (`?search=`, `?min_stars=`, `?tag=`) | Public (rate‑limited) |
| **GET** | `/crates/{crate_id}` | Detailed metadata + latest version | Public |
| **GET** | `/trending` | Return current top‑N trending crates (default N=20) | Public |
| **POST** | `/watchlists` | Create a watch entry for authenticated user | Bearer (Auth0) |
| **GET** | `/watchlists` | Retrieve authenticated user’s watchlist | Bearer |
| **DELETE** | `/watchlists/{crate_id}` | Remove crate from watchlist | Bearer |
| **GET** | `/search` | Full‑text search via Meilisearch (`?q=`) with optional sorting | Public |
| **POST** | `/api-keys` | Generate a new API key (hashed storage) | Bearer |
| **DELETE** | `/api-keys/{key_id}` | Revoke an API key | Bearer |
| **GET** | `/healthz` | Liveness / readiness probe (returns 200) | None |

*All mutating endpoints validate CSRF via same‑site cookies when accessed from the web UI; API‑key auth bypasses CSRF.*

---

### 5. Security Model  

| Aspect | Implementation |
|--------|----------------|
| **Authentication** | Auth0 OIDC (Authorization Code Flow with PKCE) for UI; JWTs signed with RS256. API‑key auth uses HMAC‑SHA256 stored hash (`bcrypt`). |
| **Authorization** | RBAC: `user` (default) can manage own watchlists & API keys; `admin` role (reserved) can trigger manual re‑crawl and view internal metrics. Enforced via Axum middleware. |
| **Transport Security** | All inbound/outbound traffic forced over TLS 1.3 (Fly.io terminates TLS, passes via internal TLS to DB). |
| **Secrets Management** | Environment variables injected by Fly.io secrets store; DB passwords, Auth0 client secret, Meilisearch master key stored encrypted at rest. |
| **Data Protection** | No PII stored besides email (hashed with Argon2) and Auth0 sub. All other data is public crate metadata. |
| **Rate Limiting** | Redis token‑bucket per IP/user (100 req/min public, 500 req/min authenticated). |
| **Vulnerability Scanning** | Dependabot + cargo-audit run nightly in CI; container images scanned with Trivy. |
| **Compliance** | GDPR‑friendly: users can request deletion of their profile & watchlists via `/users/me` DELETE (not listed above but internal). |

---

### 6. Observability  

| Signal | Tooling | Export |
|--------|---------|--------|
| **Logs** | `tracing` crate → JSON → stdout → **Grafana Loki** (via OTLP) | Structured logs include request_id, user_id, endpoint, latency, error flag. |
| **Metrics** | `prometheus-client` crate → `/metrics` endpoint | Scraped by Grafana Cloud Prometheus; key metrics: `http_requests_total`, `http_request_duration_seconds`, `db_query_duration_seconds`, `cache_hit_ratio`, `crawler_success_total`. |
| **Traces** | `opentelemetry` crate → OTLP exporter → Grafana Tempo | End‑to‑end trace across API → DB → Meilisearch → Redis. |
| **Health** | `/healthz` + `/readyz` endpoints | Monitored by Fly.io health checks. |
| **Alerting** | Grafana alerts on error rate > 1 % or latency > 500 ms (5‑min window) → Slack webhook. |

---

### 7. Build & CI  

| Stage | GitHub Action | Steps |
|-------|---------------|-------|
| **Lint / Format** | `cargo fmt -- --check` + `cargo clippy -- -D warnings` | Fails on any style or lint error. |
| **Unit Tests** | `cargo test --locked --all-features --quiet` | Runs in parallel; coverage via `tarpaulin`. |
| **Integration Tests** | Docker‑compose spin‑up of Postgres, Redis, Meilisearch; run `cargo test --test integration`. |
| **Security Scan** | `cargo audit` + `trivy image` on built container. |
| **Build Image** | Multi‑stage Dockerfile: `builder` (Rust compile) → `runtime` (distroless `gcr.io/distroless/cc`). |
| **Push** | `docker login` to Fly.io registry; `docker push` tag `registry.fly.io/rust-scout:${{ github.sha }}`. |
| **Deploy** | Fly.io `flyctl deploy --image registry.fly.io/rust-scout:${{ github.sha }}` (auto‑rollout). |
| **Post‑Deploy Smoke Test** | Simple curl health check; fail pipeline if non‑200. |
| **Release** | On `main` tag `v*.*.*`, generate OpenAPI spec (`cargo run --bin generate-openapi > openapi.yaml`) and publish to GitHub Releases. |

*All secrets (Fly API token, Auth0 credentials) are stored in GitHub Encrypted Secrets.*  

---  

**End of tech-spec.md**.