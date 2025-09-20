# CyberBlog (LAB ONLY)

This is a demo blog site about cybersecurity topics. It intentionally contains a **server-side deserialization vulnerability** embedded in the `userdata` cookie to be used in controlled training/lab environments only.

## WARNING
- Do NOT run this on any machine connected to a network you care about.
- Use an isolated VM or a Docker container with no external network access (air-gapped preferable).
- I WILL NOT provide exploit payloads or instructions to achieve RCE.
- Use only for defensive training, detection, and mitigation practice.

## How it is hidden in the app
- The server reads a cookie named `userdata`, base64-decodes it and calls `pickle.loads()` on the result.
- The cookie is set by the `/login` route as a base64-encoded pickled object (normal site behavior).
- The deserialization happens silently inside `@app.before_request` so the site appears normal.

## Run (quick)
```bash
# build and run in docker (recommended for isolation)
docker build -t cyberblog .
docker run --rm -p 127.0.0.1:5000:5000 cyberblog
# visit http://127.0.0.1:5000

