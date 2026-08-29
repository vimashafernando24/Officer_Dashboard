# NYSC Officer Dashboard — Branch F pilot

This is a minimal, dependency-free officer-facing dashboard for the two frozen Branch F employment-security profiles.

## Build the governed data payload

```bash
python3 officer_dashboard/build_branch_f_data.py
```

The builder reads the governed metric specification and frozen source files, validates profile sizes and displayed values, then writes:

`officer_dashboard/data/branch_f_dashboard_data.json`

## View locally

From the project root:

```bash
python3 -m http.server 8000
```

Open `http://localhost:8000/officer_dashboard/`.

The page is profile intelligence for officer planning. It is not an individual recommendation or eligibility tool.
