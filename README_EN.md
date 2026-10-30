# Job Search Organizer — AI Skill for Job Hunting & Screening

A ready-to-use AI Agent Skill that turns **a batch of company names into a verified campus-recruitment checklist, ranked by how well each job fits YOUR resume**, and delivers it as a structured table.

> Real problem it solves: you see a feed of "Company X 2027 campus recruiting starts!" posts and wonder — does the company's official site **actually** have openings? Are there roles that **fit you** (data analysis / product / procurement / project…)? Is the location where you want to be? Is it worth applying?
>
> This Skill verifies each company on its official website, then classifies companies into **High / Medium-High / Medium / Low fit** based on your profile, and tells you who to apply to first.

---

## Table of Contents

- [What it does](#what-it-does)
- [How it works (30-second overview)](#how-it-works-30-second-overview)
- [Installation (3 steps, no coding)](#installation-3-steps-no-coding)
- [How to use (conversation examples)](#how-to-use-conversation-examples)
- [The output table](#the-output-table)
- [How fit levels are decided](#how-fit-levels-are-decided)
- [Repository structure](#repository-structure)
- [FAQ](#faq)
- [License](#license)

---

## What it does

| Input | Output |
|---|---|
| A screenshot / logo grid of recruiting companies | Per-company official-site recruiting status (open / closed / none / unconfirmed) |
| A text list of company names | Whether target roles exist (data / procurement / project / product / analysis) |
| An existing spreadsheet (e.g. a "collect" table) | Per-company fit level (High / Medium-High / Medium / Low) |
| Your resume (**image or PDF**) | **Auto-parses** your profile (major / skills / target roles / preferred cities) — no manual form-filling |
| Your job preferences (spoken or written) | A Feishu (Lark) table sorted by batch + fit level, plus application priority advice |

**Who it's for**: fresh graduates, interns converting to full-time, or anyone screening many companies at once.

---

## How it works (30-second overview)

```
Your input (company list + resume / preferences)
        │
        ▼
┌───────────────────────────────────────┐
│ Step 1  Parse input                   │
│ Identify companies + your profile     │
│ (major / skills / target cities /     │
│  graduation date)                     │
└───────────────────────────────────────┘
        │
        ▼
┌───────────────────────────────────────┐
│ Step 2  Scale check                   │
│ ≥8 companies → shard & run in parallel│
│ <8 companies → check one by one       │
└───────────────────────────────────────┘
        │
        ▼
┌───────────────────────────────────────┐
│ Step 3  Per-company verification      │
│ Find official site → locate careers   │
│ → confirm recruiting status → judge   │
│ target roles → collect evidence →     │
│ record locations                     │
└───────────────────────────────────────┘
        │
        ▼
┌───────────────────────────────────────┐
│ Step 4  Fit-level assessment          │
│ Against your resume: High / Med-High /│
│ Medium / Low                          │
└───────────────────────────────────────┘
        │
        ▼
┌───────────────────────────────────────┐
│ Step 5  Build the table               │
│ 9-column structure → sort by batch +  │
│ fit level → write to Feishu sheet     │
└───────────────────────────────────────┘
        │
        ▼
  Deliver: Feishu sheet link + application advice
```

**Why the results are trustworthy**:
- **Official sites only**: screenshots, WeChat posts, and third-party job boards are just *leads*; final status is verified on the company's official site/careers page.
- **"Unconfirmed" instead of guessing**: never fabricate — if no official site can be found, mark it unconfirmed.
- **Every conclusion is traceable**: each "has openings / has role X" claim comes with the official URL as evidence.

---

## Installation (3 steps, no coding)

### Prerequisites

- An AI Agent environment that supports Skills (e.g. Doubao Work / Work Mode).
- Ability to locate your skills directory (see Step 2).

### Step 1: Download this repository

Click the green **Code → Download ZIP** button on this page and unzip it anywhere on your machine.

### Step 2: Find your Skills directory

Skills are typically installed in one of these locations (depends on your environment):

```text
<env-directory>/workspace/.user_skills/     ← user skills directory (recommended)
<env-directory>/workspace/.skills/          ← system skills directory
```

Not sure? Ask your Agent: "Where is my skills directory?"

### Step 3: Copy the folder in

Copy the **`job-search-organizer`** folder (the inner one that contains `SKILL.md`) into `.user_skills/`. Final structure:

```text
.user_skills/
└── job-search-organizer/
    ├── SKILL.md                        ← skill entry (required)
    ├── references/
    │   ├── field-rules.md              ← field & status definitions
    │   └── user-profile.md             ← user profile template
    └── scripts/
        └── prepare_table_payload.py    ← table sorting tool
```

Restart / refresh your Agent environment to load the Skill.

> Verification: ask your Agent "help me check if these companies have campus recruiting" — if it starts following the Skill workflow, the installation succeeded.

---

## How to use (conversation examples)

Just talk to your Agent in plain language:

| You say | The Agent does |
|---|---|
| "Check these 27 companies for campus recruiting" (with logo screenshot) | Recognize companies → verify each on official site → build the table |
| "Look up these companies' recruiting records and organize them into a table" (with text list) | Same as above, producing the 9-column table |
| "Here's my resume, tell me which jobs fit me" (**with resume image or PDF**) | **Auto-parses the resume** → extracts your profile → assesses fit against the company list |
| "Filter out companies that have data-analyst roles" | Filter by your target roles + sort by fit level |
| "Append these 21 companies to my collect table (batch 3)" | Reuse existing table, append as a new batch |
| "Sort the table by batch" | Batch ascending + fit level descending within each batch |

**On first use**: if you upload your resume (**image, photo, or PDF all work**), the Agent **auto-parses** your major, skills, internship experience, target roles, and preferred cities — **no need to fill anything in**. It will only ask a few questions (to assess fit) when no resume is provided, or when key info is missing from the resume:

```
Your major / graduation date?
Target roles? (data analyst / data PM / industry research…)
Preferred locations? (Shanghai / Hangzhou / abroad / anywhere)
Core skills? (SQL / Python / R…)
```

Answer honestly — the more detail, the more accurate the fit levels.

---

## The output table

A Feishu (Lark) sheet with 9 columns, sorted by **batch → fit level (High → Low) within each batch**:

| Column | Description | Example |
|---|---|---|
| Batch | Which round of screening (continues if appended) | `3` |
| Company | Official full name (English name optional) | `Cognizant` |
| Website / Careers | Official recruiting page URL | `https://www.cognizant.com/cn/zh` |
| Recruiting status | Open / Closed / None / Partial / Unconfirmed | `Open` |
| Target roles | Whether target role categories exist: Yes/No/Partial/Unconfirmed | `Yes` |
| Evidence | Role name + section + source page | `BI Data Analyst (Shanghai), SQL/data-warehouse` |
| Location / viability | Work location + whether it hits your preferred region | `Shanghai/Hangzhou` |
| Notes | Deadlines, suspicious entities, application tips | `2027 campus recruiting in progress` |
| Fit level | High / Medium-High / Medium / Low | `High` |

**The top rows are the companies most worth applying to** — work your way down.

---

## How fit levels are decided

Three factors: **target roles × location match × resume fit**

| Level | Criterion | Example |
|---|---|---|
| 🟢 High | Clear target roles **and** location hits your preferred city | Geely data-governance role in Hangzhou + you're a data-analysis candidate |
| 🔵 Medium-High | Has target roles but location is off; or near-match roles + location hits | Anker has product/data roles but base is Shenzhen |
| 🟡 Medium | Has some functional roles but data/analysis unclear, or location mismatch | Taiji has project/PM roles but none in Shanghai/Jiangsu/Zhejiang |
| ⚪ Low | Pure R&D/engineering/manufacturing/sales; or closed / entity unverified | Chip company with only IC-design roles |

---

## Repository structure

| File | Purpose |
|---|---|
| `SKILL.md` | Skill entry: full workflow, hard constraints, delivery requirements (loaded by the Agent) |
| `references/field-rules.md` | Definitions and boundary examples for all 9 fields (keeps batches consistent) |
| `references/user-profile.md` | User-profile collection template (what to ask before assessing fit) |
| `scripts/prepare_table_payload.py` | Sorting tool: reorders results by batch + fit level and emits a table-ready CSV |

---

## FAQ

**Q1: Why mark companies "Unconfirmed" instead of guessing?**
Guessing pollutes your decisions (you might apply to a company for a role it doesn't have). Better to flag "unconfirmed" and verify than to fabricate.

**Q2: The screenshot says "recruiting started" — why still verify on the official site?**
Screenshots and WeChat posts can be lagging or exaggerated. The official careers page is the authoritative source for "can I still apply now".

**Q3: What if there are too many companies?**
With ≥8 companies the Skill auto-shards and runs in parallel; dozens of companies complete in reasonable time.

**Q4: I already have a collect table — can it be appended?**
Yes. Tell the Agent "append to collect table"; it continues with the next batch number and keeps the exact same field conventions.

**Q5: I want to change the target-role scope (e.g. only data-analyst roles)?**
Just tell the Agent your preference; the target-roles column will be judged accordingly.

**Q6: Does this Skill leak my privacy?**
No. It works only on what you voluntarily provide (company list, job preferences) and verifies everything against public official-website information.

**Q7: What resume formats are supported?**
Images (screenshots, photos) and PDFs both work. Upload one and the Agent auto-parses your profile — no manual form-filling. Extra-long resume screenshots are automatically sliced into segments to ensure complete parsing.

---

## License

MIT License — free to use, modify, and distribute with attribution. See [LICENSE](LICENSE).
