# Security Notes

This repo is designed to be safe to publish publicly.

## Secrets
- Do **not** store passwords, API tokens, or private keys in git.
- If you later add real device connectivity, prefer:
  - environment variables
  - local `.env` ignored by git
  - OS keychain / secret managers

## Logging
- Avoid logging credentials or full running-configs that include secrets.
- Prefer redaction for:
  - `username ... secret ...`
  - `enable secret`
  - SNMP community strings
  - VPN pre-shared keys

## Principle of least privilege
- If connecting to devices, use a role/account with minimal required permissions.
