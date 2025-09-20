# CyberBlog (LAB ONLY)

This is a demo blog site about cybersecurity topics. It intentionally contains a **server-side deserialization vulnerability** to be used in controlled training/lab environments only.

## WARNING
- Do NOT run this on any machine connected to a network you care about.
- Use an isolated VM or a Docker container with no external network access (air-gapped preferable).
- Use only for demostration, defensive training, detection, and mitigation practice.

## Run (quick)
```bash
# build and run in docker (recommended for isolation)
docker build -t cyberblog .
docker run --rm -p 5000:5000 cyberblog
# visit http://127.0.0.1:5000

