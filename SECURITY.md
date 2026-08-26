# Security and privacy

This repository uses synthetic operational data and a local demonstration portal.

- Never commit authentication states, cookies, session files, tokens, or passwords.
- Never replace the synthetic CSV files with real customer or shipment data.
- Keep `.env`, browser profiles, downloads, and generated workbooks outside Git.
- Use environment variables for portal URLs and execution settings.

If a real secret is exposed, revoke it first and remove it from the complete Git history.
