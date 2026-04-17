from datetime import datetime, timezone


def build_report(sector: str, body_md: str, sources: list[str]) -> tuple[str, str]:
    """Wrap the LLM body in a header + sources footer. Returns (markdown, iso_timestamp)."""
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    md_body = []
    md_body.append(f"# Trade Opportunity Briefing — {sector.title()} (India)")
    md_body.append(f"_Generated at: {ts}_\n")
    md_body.append(body_md.strip())
    md_body.append("\n## Sources")
    if sources:
        for i, u in enumerate(sources, 1):
            md_body.append(f"{i}. {u}")
    else:
        md_body.append("_No live sources retrieved._")
    return "\n\n".join(md_body), ts
