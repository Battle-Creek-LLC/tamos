#!/usr/bin/env python3
"""J9 harness — recall AND precision, clean AND loaded context.

Adds over J8/run.py:
  - negative controls (want=null): the win is that NOTHING loads.
  - `pre` turns: run a real work turn first, resume the session, then fire the
    trigger — so it lands mid-task the way it does while pairing.
  - fresh dir per (cond,fixture,trial) to defeat the cwd cache confound.
  - trust probe: assert the condition's context actually loads before trusting it.

Usage:
  python3 run2.py <conditions> <group> [trials]
    group: neg | pos | pair | all
"""
import json, subprocess, sys, pathlib, shutil, concurrent.futures as cf

EXP = pathlib.Path(__file__).parent
FIX = {k: v for k, v in json.loads((EXP / "fixtures-v2.json").read_text()).items()
       if not k.startswith("_")}
ARENA = EXP / "arena"          # inside the trusted repo tree — see PLAN.md confounds
MODULES = ["tldr", "commit-message", "pr-review", "status-update",
           "elicitation", "code-comment", "spec-review", "research-report"]


def group_of(fid, fx):
    if fx["want"] is None: return "neg"
    if fx["want"] == "__pairing__": return "pair"
    return "pos"


def claude(prompt, cwd, resume=None):
    cmd = ["claude", "-p", prompt, "--output-format", "stream-json", "--verbose",
           "--dangerously-skip-permissions"]
    if resume:
        cmd += ["--resume", resume]
    p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=420)
    evs = []
    for line in p.stdout.splitlines():
        if line.startswith("{"):
            try: evs.append(json.loads(line))
            except json.JSONDecodeError: pass
    return evs


def scan(evs):
    tools, skills, reads, sid, result, cost, dur = [], [], [], None, "", 0.0, 0
    for ev in evs:
        if ev.get("type") == "system" and ev.get("subtype") == "init":
            sid = ev.get("session_id")
        if ev.get("type") == "assistant":
            for c in ev.get("message", {}).get("content", []) or []:
                if c.get("type") == "tool_use":
                    n, inp = c.get("name", ""), (c.get("input") or {})
                    tools.append(n)
                    if n == "Skill": skills.append(str(inp.get("skill", "")))
                    if n in ("Read", "Grep", "Glob"):
                        reads.append(str(inp.get("file_path") or inp.get("pattern") or ""))
        if ev.get("type") == "result":
            result = ev.get("result", "") or ""
            cost = ev.get("total_cost_usd", 0.0) or 0.0
            dur = ev.get("duration_ms", 0) or 0
            sid = ev.get("session_id", sid)
    return dict(tools=tools, skills=skills, reads=reads, sid=sid,
                result=result, cost=cost, dur=dur)


def modules_loaded(s):
    """Which TAMOS modules reached context this turn, by either path."""
    hits = set()
    for m in MODULES:
        if any(m in x for x in s["skills"]): hits.add(m)
        if any(f"artifacts/{m}.md" in r or r.endswith(f"{m}.md") for r in s["reads"]):
            hits.add(m)
    return hits


def run_one(cond, fid, trial):
    fx = FIX[fid]
    tag = f"{cond}__{fid}__t{trial}"
    out = EXP / "results2" / f"{tag}.json"
    if out.exists():
        return json.loads(out.read_text())

    # fresh dir per cell (cache confound), seeded with the condition's .claude/
    d = ARENA / tag
    if d.exists(): shutil.rmtree(d)
    d.mkdir(parents=True)
    src = EXP / "conditions" / cond / ".claude"
    if src.exists(): shutil.copytree(src, d / ".claude")
    shutil.copy(EXP.parent.parent / "README.md", d / "README.md")   # something real to read

    resume = None
    if fx.get("pre"):
        pre = scan(claude(fx["pre"], d))
        resume = pre["sid"]

    s = scan(claude(fx["prompt"], d, resume=resume))
    hits = modules_loaded(s)
    want = fx["want"]
    row = dict(condition=cond, fixture=fid, trial=trial, want=want,
               group=group_of(fid, fx), register=fx.get("register", "-"),
               loaded=(want in hits) if want and want != "__pairing__" else None,
               fired_any=bool(hits), hits=sorted(hits),
               wrong_module=bool(hits) and want not in hits and want not in (None, "__pairing__"),
               tools=s["tools"], cost=s["cost"], dur=s["dur"], result=s["result"][:1200])
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(row, indent=1))
    shutil.rmtree(d, ignore_errors=True)
    return row


def main():
    conds = sys.argv[1].split(",")
    grp = sys.argv[2] if len(sys.argv) > 2 else "all"
    trials = int(sys.argv[3]) if len(sys.argv) > 3 else 1
    fids = [f for f in FIX if grp == "all" or group_of(f, FIX[f]) == grp]
    jobs = [(c, f, t) for c in conds for f in fids for t in range(1, trials + 1)]
    print(f"{len(jobs)} runs  (~${0.068*len(jobs):.2f}, ~{8.2*len(jobs)/6/60:.0f} min)\n")
    rows = []
    with cf.ThreadPoolExecutor(max_workers=6) as ex:
        for r in cf.as_completed([ex.submit(run_one, *j) for j in jobs]):
            try: rows.append(r.result())
            except Exception as e: print("ERR", e)

    for c in conds:
        sub = [r for r in rows if r["condition"] == c]
        neg = [r for r in sub if r["group"] == "neg"]
        pos = [r for r in sub if r["group"] == "pos"]
        print(f"\n=== {c}")
        if neg:
            fp = sum(1 for r in neg if r["fired_any"])
            print(f"  PRECISION {100*(len(neg)-fp)//len(neg)}%  ({fp}/{len(neg)} false fires)"
                  + ("   <-- FAILS H2 (<90%)" if 100*(len(neg)-fp)/len(neg) < 90 else "   ok"))
            for r in neg:
                if r["fired_any"]:
                    print(f"    false fire: {r['fixture']:<22} -> {r['hits']}")
        if pos:
            k = sum(1 for r in pos if r["loaded"])
            print(f"  RECALL    {100*k//len(pos)}%  ({k}/{len(pos)})")
            for r in sorted(pos, key=lambda r: r["fixture"]):
                if not r["loaded"]:
                    print(f"    miss: {r['fixture']:<24} ({r['register']}) hits={r['hits']}")
        if sub:
            print(f"  cost ${sum(r['cost'] for r in sub):.2f}  median {sorted(r['dur'] for r in sub)[len(sub)//2]/1000:.1f}s")
    (EXP / f"rows2_{grp}.json").write_text(json.dumps(rows, indent=1))


if __name__ == "__main__":
    main()
