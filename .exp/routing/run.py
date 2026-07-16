#!/usr/bin/env python3
"""J8 — routing efficacy harness.

Question J7 never asked: does the module get LOADED at all?
J7 pre-concatenated module text into the prompt, bypassing routing entirely.

DV (deterministic, read from the transcript):
  loaded = the wanted module reached context by EITHER path:
             - Skill tool fired with the wanted skill, OR
             - Read/Grep touched artifacts/<wanted>.md
"""
import json, subprocess, sys, os, pathlib, concurrent.futures as cf

EXP = pathlib.Path(__file__).parent
FIX = json.loads((EXP / "fixtures.json").read_text())


def transcript_events(path):
    for line in path.read_text().splitlines():
        line = line.strip()
        if line.startswith("{"):
            try:
                yield json.loads(line)
            except json.JSONDecodeError:
                pass


def analyze(path, want):
    """Return (loaded, tools_used, skills_fired, reads, result_text)."""
    tools, skills, reads, result = [], [], [], ""
    for ev in transcript_events(path):
        if ev.get("type") == "assistant":
            for c in ev.get("message", {}).get("content", []) or []:
                if c.get("type") == "tool_use":
                    name = c.get("name", "")
                    inp = c.get("input", {}) or {}
                    tools.append(name)
                    if name == "Skill":
                        skills.append(str(inp.get("skill", "")))
                    if name in ("Read", "Grep", "Glob"):
                        reads.append(str(inp.get("file_path") or inp.get("pattern") or ""))
        elif ev.get("type") == "result":
            result = ev.get("result", "") or ""
    hit_skill = any(want in s for s in skills)
    hit_read = any(f"{want}.md" in r for r in reads)
    return (hit_skill or hit_read), tools, skills, reads, result


def run_one(cond_dir, fid, trial):
    fx = FIX[fid]
    out = EXP / "results" / f"{cond_dir.name}__{fid}__t{trial}.jsonl"
    if out.exists() and out.stat().st_size > 0:
        pass  # cached
    else:
        with open(out, "w") as fh:
            subprocess.run(
                ["claude", "-p", fx["prompt"], "--output-format", "stream-json",
                 "--verbose", "--dangerously-skip-permissions"],
                cwd=cond_dir, stdout=fh, stderr=subprocess.DEVNULL, timeout=300,
            )
    loaded, tools, skills, reads, result = analyze(out, fx["want"])
    return {"condition": cond_dir.name, "fixture": fid, "trial": trial,
            "want": fx["want"], "loaded": loaded, "tools": tools,
            "skills": skills, "reads": reads, "result": result}


def main():
    conds = [EXP / "conditions" / c for c in sys.argv[1].split(",")]
    fids = sys.argv[2].split(",") if len(sys.argv) > 2 else list(FIX)
    trials = int(sys.argv[3]) if len(sys.argv) > 3 else 1
    jobs = [(c, f, t) for c in conds for f in fids for t in range(1, trials + 1)]
    rows = []
    with cf.ThreadPoolExecutor(max_workers=6) as ex:
        futs = {ex.submit(run_one, *j): j for j in jobs}
        for fut in cf.as_completed(futs):
            try:
                rows.append(fut.result())
            except Exception as e:
                j = futs[fut]
                rows.append({"condition": j[0].name, "fixture": j[1], "trial": j[2],
                             "loaded": None, "error": str(e)})

    (EXP / "rows.json").write_text(json.dumps(rows, indent=1))
    print(f"{'condition':<12} {'fixture':<16} {'want':<15} {'loaded':<7} tools")
    print("-" * 78)
    for r in sorted(rows, key=lambda r: (r["condition"], r["fixture"], r["trial"])):
        if r.get("error"):
            print(f"{r['condition']:<12} {r['fixture']:<16} {'ERROR':<15} {r['error'][:30]}")
            continue
        mark = "YES" if r["loaded"] else "no"
        print(f"{r['condition']:<12} {r['fixture']:<16} {r['want']:<15} {mark:<7} {','.join(r['tools'])[:34]}")
    print("-" * 78)
    for c in {r["condition"] for r in rows}:
        sub = [r for r in rows if r["condition"] == c and r.get("loaded") is not None]
        n = len(sub)
        k = sum(1 for r in sub if r["loaded"])
        print(f"{c}: loaded {k}/{n}" + (f"  ({100*k//n}%)" if n else ""))


if __name__ == "__main__":
    main()
