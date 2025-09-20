from models import Post
try:
    from slugify import slugify
except Exception:
    def slugify(text):
        import re
        s = re.sub(r'[^a-zA-Z0-9]+', '-', text.lower()).strip('-')
        s = re.sub(r'-{2,}', '-', s)
        return s or 'post'

def insert_sample_posts(db):
    if Post.query.first():
        return
    samples = [
        {"title": "Intro to CyberBlog", "topic": "overview",
         "content": "Welcome to CyberBlog — a demo blog about random cybersecurity topics."},
        {"title": "Threat Hunting Basics", "topic": "threat-hunting",
         "content": "Basics of threat hunting workflows, detection hypotheses and enrichment."},
        {"title": "Browser Security & Cookies", "topic": "web-security",
         "content": "Cookies are convenient for state. Mistakes can make them an attack surface."},
        {"title": "Static Analysis Tools", "topic": "tools",
         "content": "A brief list of static analysis tools for Python and binary formats."},
        {"title": "Hardening Python Services", "topic": "hardening",
         "content": "General guidance: avoid unsafe deserializers, use least privilege, and sandbox."}
    ]
    for s in samples:
        p = Post(
            title=s["title"],
            slug=slugify(s["title"]),
            topic=s.get("topic","general"),
            content=s["content"]
        )
        db.session.add(p)
    db.session.commit()
