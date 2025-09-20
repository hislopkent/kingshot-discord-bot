from __future__ import annotations

from typing import Any, Iterable, Mapping, Sequence

import discord

EM_DASH = "\u2014"


def _join_lines(lines: Iterable[str]) -> str:
    items = [line for line in lines if line]
    return "\n".join(items) if items else EM_DASH


def _format_sequence(values: Sequence[Any]) -> str:
    if not values:
        return EM_DASH
    return _join_lines(f"• {value}" for value in values if value)


def _format_cost(cost: Mapping[str, Any]) -> str:
    pairs = [f"{resource}: {amount}" for resource, amount in cost.items() if amount not in (None, "", 0)]
    return ", ".join(pairs) if pairs else EM_DASH


def _format_mapping(data: Mapping[str, Any], keys: Iterable[str] | None = None) -> str:
    if not data:
        return EM_DASH
    lines: list[str] = []
    for key in keys or data.keys():
        if key not in data:
            continue
        value = data[key]
        if value in (None, "", []):
            continue
        if isinstance(value, Mapping):
            formatted = _format_mapping(value)
        elif isinstance(value, Sequence) and not isinstance(value, (str, bytes)):
            formatted = ", ".join(str(item) for item in value if item not in (None, "")) or EM_DASH
        else:
            formatted = str(value)
        lines.append(f"**{key.capitalize()}:** {formatted}")
    return _join_lines(lines)


def _format_building_level(data: Mapping[str, Any]) -> str:
    level = data.get("level")
    label = f"Level {level}" if level is not None else "Level"
    parts: list[str] = []
    cost = data.get("cost")
    if isinstance(cost, Mapping):
        formatted = _format_cost(cost)
        if formatted != EM_DASH:
            parts.append(f"Cost – {formatted}")
    time = data.get("time")
    if time:
        parts.append(f"Time – {time}")
    power = data.get("power")
    if power not in (None, ""):
        parts.append(f"Power – {power}")
    for key, value in data.items():
        if key in {"level", "cost", "time", "power"}:
            continue
        if value in (None, ""):
            continue
        parts.append(f"{key.capitalize()} – {value}")
    detail = "; ".join(parts) if parts else None
    return f"• **{label}:** {detail}" if detail else f"• **{label}**"


def hero_to_embed(name: str, hero: Mapping[str, Any]) -> discord.Embed:
    embed = discord.Embed(title=f"Hero • {name}")
    embed.add_field(
        name="Overview",
        value=_format_mapping({"rarity": hero.get("rarity"), "role": hero.get("role")}),
        inline=False,
    )

    stats = hero.get("stats")
    if isinstance(stats, Mapping):
        embed.add_field(
            name="Stats",
            value=_format_mapping(stats, keys=("attack", "defense", "health")),
            inline=False,
        )

    skills = hero.get("skills")
    if isinstance(skills, Sequence):
        skill_lines = []
        for skill in skills:
            if not isinstance(skill, Mapping):
                continue
            title = skill.get("name", "?")
            desc = skill.get("description", "")
            line = f"• **{title}**"
            if desc:
                line += f" — {desc}"
            skill_lines.append(line)
        embed.add_field(name="Skills", value=_join_lines(skill_lines), inline=False)

    expedition = hero.get("expedition_bonuses")
    if isinstance(expedition, Mapping):
        embed.add_field(name="Expedition", value=_format_mapping(expedition), inline=False)

    growth = hero.get("growth")
    if isinstance(growth, Sequence):
        embed.add_field(name="Growth", value=_format_sequence(growth), inline=False)

    sources = hero.get("sources")
    if isinstance(sources, Sequence):
        embed.add_field(name="Sources", value=_format_sequence(sources), inline=False)

    recommended = hero.get("recommended")
    if isinstance(recommended, Mapping):
        embed.add_field(name="Recommended", value=_format_mapping(recommended), inline=False)

    notes = hero.get("notes")
    if notes:
        embed.add_field(name="Notes", value=str(notes), inline=False)

    return embed


def building_to_embed(name: str, building: Mapping[str, Any], level: int | None = None) -> discord.Embed:
    embed = discord.Embed(title=f"Building • {name}")
    embed.add_field(
        name="Basics",
        value=_format_mapping({"type": building.get("type"), "unlock": building.get("unlock")}),
        inline=False,
    )

    trees = building.get("trees")
    if isinstance(trees, Sequence):
        embed.add_field(name="Research Trees", value=_format_sequence(trees), inline=False)

    effects = building.get("effects")
    if isinstance(effects, Sequence):
        embed.add_field(name="Effects", value=_format_sequence(effects), inline=False)

    levels = [lvl for lvl in building.get("levels", []) if isinstance(lvl, Mapping)]
    if levels:
        if level is not None:
            match = next((lvl for lvl in levels if lvl.get("level") == level), None)
            if match:
                embed.add_field(
                    name=f"Level {level}",
                    value=_join_lines([_format_building_level(match)]),
                    inline=False,
                )
            else:
                available_levels = [str(lvl.get("level")) for lvl in levels if lvl.get("level") is not None]
                available = ", ".join(available_levels) if available_levels else "Unknown"
                embed.add_field(
                    name="Level",
                    value=f"No data for level {level}. Available: {available}.",
                    inline=False,
                )
        else:
            preview = [_format_building_level(lvl) for lvl in levels[:5]]
            embed.add_field(
                name="Levels",
                value=_join_lines(preview),
                inline=False,
            )
            if len(levels) > 5:
                embed.add_field(
                    name="More levels",
                    value="Use `/building level:<number>` for specific level details.",
                    inline=False,
                )

    notes = building.get("notes")
    if notes:
        embed.add_field(name="Notes", value=str(notes), inline=False)

    return embed


def research_to_embed(name: str, research: Mapping[str, Any]) -> discord.Embed:
    embed = discord.Embed(title=f"Research • {name}")

    summary_keys = ("tree", "branch", "category", "tier")
    summary = {key: research.get(key) for key in summary_keys if research.get(key)}
    if summary:
        embed.add_field(name="Summary", value=_format_mapping(summary), inline=False)

    bonuses = research.get("bonuses") or research.get("effects")
    if isinstance(bonuses, Sequence):
        embed.add_field(name="Effects", value=_format_sequence(bonuses), inline=False)

    requirements = research.get("requirements") or research.get("prerequisites")
    if isinstance(requirements, Mapping):
        embed.add_field(name="Requirements", value=_format_mapping(requirements), inline=False)
    elif isinstance(requirements, Sequence):
        embed.add_field(name="Requirements", value=_format_sequence(requirements), inline=False)

    costs = research.get("cost") or research.get("costs")
    if isinstance(costs, Mapping):
        embed.add_field(name="Cost", value=_format_mapping(costs), inline=False)

    duration = research.get("time") or research.get("duration")
    if duration:
        embed.add_field(name="Time", value=str(duration), inline=False)

    notes = research.get("notes")
    if notes:
        embed.add_field(name="Notes", value=str(notes), inline=False)

    return embed


def event_to_embed(name: str, event: Mapping[str, Any]) -> discord.Embed:
    embed = discord.Embed(title=f"Event • {name}")

    schedule = {k: event.get(k) for k in ("start", "end", "frequency") if event.get(k)}
    if schedule:
        embed.add_field(name="Schedule", value=_format_mapping(schedule), inline=False)

    rewards = event.get("rewards")
    if isinstance(rewards, Sequence):
        embed.add_field(name="Rewards", value=_format_sequence(rewards), inline=False)

    tasks = event.get("tasks") or event.get("stages")
    if isinstance(tasks, Sequence):
        embed.add_field(name="Tasks", value=_format_sequence(tasks), inline=False)

    notes = event.get("notes")
    if notes:
        embed.add_field(name="Notes", value=str(notes), inline=False)

    return embed


def hero_embed(ds) -> discord.Embed:  # pragma: no cover - simple factories
    return discord.Embed(title="Hero Lookup", description="Use `/hero name:<text>`.")


def building_embed(ds) -> discord.Embed:  # pragma: no cover - simple factories
    return discord.Embed(title="Building Lookup", description="Use `/building name:<text> [level:<int>]`.")


def research_embed(ds) -> discord.Embed:  # pragma: no cover - simple factories
    return discord.Embed(title="Research Lookup", description="Use `/research name:<text>`.")


def event_embed(ds) -> discord.Embed:  # pragma: no cover - simple factories
    return discord.Embed(title="Events", description="Use `/event` or `/event name:<text>`.")


def links_embed(ds) -> discord.Embed:  # pragma: no cover - simple factories
    embed = discord.Embed(title="Kingshot Links")
    embed.add_field(name="Community Wiki", value="[Kingshot Data](https://kingshotdata.com/)", inline=False)
    return embed
