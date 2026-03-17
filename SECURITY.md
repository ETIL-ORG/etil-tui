# Security Policy

## Reporting a Vulnerability

If you discover a security vulnerability in the ETIL TUI client, please report it
responsibly via email:

**Email**: [evolutionary-til-support@googlegroups.com](mailto:evolutionary-til-support@googlegroups.com)

Please include:
- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if any)

We will acknowledge receipt within 48 hours and provide a timeline for resolution.

## Security Considerations

The TUI client connects to ETIL MCP servers via HTTP/HTTPS. Security-relevant areas:

- **Credentials**: API keys and JWTs are stored in `~/.etil/connections.json`
  (user-readable only). JWTs are cached with expiry validation.
- **Transport**: HTTPS recommended for production servers. The client supports
  Bearer token authentication (API key or JWT).
- **OAuth**: Device flow authentication delegates to the server. No client secrets
  are stored in the TUI.
- **File operations**: `/upload` and `/download` transfer files to/from the server's
  sandboxed LVFS, not the local filesystem directly.

## Supported Versions

Only the latest release receives security updates.
