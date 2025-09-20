import discord
from typing import Dict, Any

def _kv_lines(d: dict, keys=None):
    if not d: return "—"
    keys = keys or d.keys()
    lines = []
    for k in keys:
        if k in d:
            v = d[k]
            if isinstance(v, (list, tuple)): v = ", ".join(map(str, v))
            elif isinstance(v, dict): v = ", ".join(f"{kk}: {vv}" for kk, vv in v.items())
            lines.append(f"**{k}:** {v}")
    return "\n".join(lines)

def hero_to_embed(name: str, h: Dict[str, Any]) -> discord.Embed:
    e = discord.Embed(title=f"Hero • {name}")
    e.add_field(name="Overview", value=_kv_lines({"rarity": h.get("rarity"), "role": h.get("role")}), inline=False)
    if h.get("stats"): e.add_field(name="Stats", value=_kv_lines(h["stats"], keys=["attack","defense","health"]), inline=False)
    if h.get("skills"):
        e.add_field(name="Skills", value="\n".join([f"• **{s.get('name','?')}** — {s.get('description','')}" for s in h["skills"]]), inline=False)
    if h.get("expedition_bonuses"): e.add_field(name="Expedition", value=_kv_lines(h["expedition_bonuses"]), inline=False)
    if h.get("growth"): e.add_field(name="Growth", value="\n".join([f"• {x}" for x in h["growth"]]), inline=False)
    if h.get("sources"): e.add_field(name="Sources", value="\n".join([f"• {x}" for x in h["sources"]]), inline=False)
    if h.get("notes"): e.add_field(name="Notes", value=h["notes"], inline=False)
    return e

def building_to_embed(name: str, b: Dict[str, Any], level: int | None = None) -> discord.Embed:
    e = discord.Embed(title=f"Building • {name}")
    e.add_field(name="Basics", value=_kv_lines({"type": b.get("type"), "unlock": b.get("unlock")}), inline=False)
    if b.get("trees"): e.add_field(name="Research Trees", value=", ".join(b["trees"]), inline=False)
    if b.get("effects"): e.add_field(name="Effects", value="\n".join([f"• {x}" for x in b["effects"]]), inline=False)
    if b.get("notes"): e.add_field(name="Notes", value=b["notes"], inline=False)
    return e

def research_to_embed(name: str, r: Dict[str, Any]) -> discord.Embed:
    e = discord.Embed(title=f"Research • {name}")
    return e

def event_to_embed(name: str, ev: Dict[str, Any]) -> discord.Embed:
    e = discord.Embed(title=f"Event • {name}")
    return e

def hero_embed(ds): return discord.Embed(title="Hero Lookup", description="Use `/hero name:<text>`.")
def building_embed(ds): return discord.Embed(title="Building Lookup", description="Use `/building name:<text> [level:<int>]`.")
def research_embed(ds): return discord.Embed(title="Research Lookup", description="Use `/research name:<text>`.")
def event_embed(ds): return discord.Embed(title="Events", description="Use `/event` or `/event name:<text>`.")
def links_embed(ds): 
    e = discord.Embed(title="Kingshot Links")
    e.add_field(name="Community Wiki", value="[Kingshot Data](https://kingshotdata.com/)", inline=False)
    return e
