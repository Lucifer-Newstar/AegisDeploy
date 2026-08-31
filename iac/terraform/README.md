# Terraform (cloud IaC) — reserved

Cloud provisioning (cluster, managed Postgres, storage, networking) lands in M7/M8
when the evaluation cluster is chosen. Until then:

- Keep this directory as the designated IaC home.
- Do NOT commit `.tfstate` files (gitignored).
- Provider choice (GCP/EKS/Azure/k3s bare-metal) is a deferred decision
  (see docs/tech-stack.md §3).

## Planned layout

```text
iac/terraform/
├── environments/
│   ├── dev/
│   └── prod/
├── modules/
│   ├── cluster/
│   ├── database/
│   └── networking/
└── versions.tf
```
