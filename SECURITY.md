# Security policy

## Reporting a vulnerability

Please report security issues privately to `support@xmemo.dev`. Do not open a public issue containing credentials, access tokens, private memory content, or vulnerability details that could put users at risk.

Include the affected component, reproduction steps, expected and observed behavior, and any relevant version or request identifier that is safe to share. Yonro will acknowledge the report and coordinate remediation and disclosure.

## Repository rules

- Never commit OAuth codes, bearer tokens, cookies, reviewer passwords, private memory exports, or production environment files.
- Use synthetic accounts and data for screenshots, examples, and review evidence.
- Treat agent identity headers as attribution, not authentication.
- Keep authorization decisions on the hosted XMemo service.
