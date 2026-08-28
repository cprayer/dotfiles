#!/usr/bin/env python3
"""이전 Claude 세션을 주제어로 찾고(--find), 그 세션의 작업 상태·출처 링크를 뽑는다(--dump).

search : rg 로 후보 파일을 좁힌 뒤 human prompt / aiTitle 만 파싱해 랭킹
dump   : 세션 1개에서 브랜치·cwd·human prompt 전량·출처 URL(슬랙/지라/노션/구글독/PR)을 추출
"""
import argparse, json, os, re, subprocess, sys, time
from collections import OrderedDict

ROOT = os.path.expanduser("~/.claude/projects")

URL_PATTERNS = OrderedDict([
    ("Jira",   re.compile(r"https?://[\w.-]+/browse/[A-Z][A-Z0-9]+-\d+")),
    ("Slack",  re.compile(r"https?://[\w.-]*slack\.com/archives/[\w/?=&.-]+")),
    ("Notion", re.compile(r"https?://(?:www\.)?notion\.so/[\w/?=&%.#-]+")),
    ("GoogleDoc", re.compile(r"https?://docs\.google\.com/[\w/?=&%.#-]+")),
    ("PR",     re.compile(r"https?://github\.com/[\w.-]+/[\w.-]+/(?:pull|issues)/\d+")),
    ("Datadog", re.compile(r"https?://app\.datadoghq\.com/[\w/?=&%.#@:+-]+")),
])


def human_prompt(d):
    """진짜 사람이 친 프롬프트만 통과시킨다 (tool_result·task-notification·sidechain 제외)."""
    if d.get("type") != "user" or d.get("isSidechain"):
        return None
    if d.get("promptSource") not in ("typed", "queued"):
        return None
    c = (d.get("message") or {}).get("content")
    if not isinstance(c, str):
        return None
    c = c.strip()
    if not c or c.startswith("<"):   # <task-notification>, <command-message> 등
        return None
    return c


def candidate_files(terms, days, cap):
    pat = "|".join(re.escape(t) for t in terms)
    try:
        out = subprocess.run(
            ["rg", "-l", "-i", "--no-messages", "--glob", "*.jsonl", "-e", pat, ROOT],
            capture_output=True, text=True, timeout=120,
        ).stdout
    except FileNotFoundError:
        out = subprocess.run(
            ["grep", "-rlie", pat, "--include=*.jsonl", ROOT],
            capture_output=True, text=True,
        ).stdout
    files, cutoff = [], time.time() - days * 86400 if days else 0
    for f in out.splitlines():
        try:
            m = os.path.getmtime(f)
        except OSError:
            continue
        if m >= cutoff:
            files.append((m, f))
    files.sort(reverse=True)
    return files[:cap], len(files)


def scan(path, terms):
    """싼 substring 선필터 → 해당 줄만 json 파싱."""
    title, prompts, cwd, branch = None, [], None, None
    with open(path, "r", errors="replace") as fh:
        for line in fh:
            if '"ai-title"' not in line and '"promptSource"' not in line:
                continue
            try:
                d = json.loads(line)
            except Exception:
                continue
            if d.get("type") == "ai-title":
                title = d.get("aiTitle") or title
                continue
            p = human_prompt(d)
            if p is not None:
                prompts.append(p)
                cwd = d.get("cwd") or cwd
                branch = d.get("gitBranch") or branch
    if not prompts and not title:
        return None
    hay_t = (title or "").lower()
    hay_p = " \n".join(prompts).lower()
    score, hit_terms = 0, []
    for t in terms:
        tl = t.lower()
        nt, np_ = hay_t.count(tl), hay_p.count(tl)
        if nt or np_:
            hit_terms.append(t)
        score += nt * 8 + min(np_, 5) * 3
    return {
        "session": os.path.basename(path)[:-6],
        "path": path, "title": title, "prompts": prompts,
        "cwd": cwd, "branch": branch,
        "score": score, "hits": hit_terms, "turns": len(prompts),
    }


def cmd_find(a):
    terms = [t for t in a.terms if t.strip()]
    files, total = candidate_files(terms, a.days, a.cap)
    rows = []
    for _, f in files:
        if a.exclude and a.exclude in f:
            continue
        r = scan(f, terms)
        if r and r["score"] > 0:
            r["mtime"] = os.path.getmtime(f)
            rows.append(r)
    # 주제어를 여러 개 맞춘 세션 우선 → 점수 → 최신
    rows.sort(key=lambda r: (len(r["hits"]), r["score"], r["mtime"]), reverse=True)
    if not rows:
        print(f"매칭 0건 (rg 후보 {total}개 중 상위 {len(files)}개 파싱). 주제어를 바꿔 재시도하세요.")
        return
    print(f"# 후보 {len(rows)}건 (rg 후보 {total}개 → 상위 {len(files)}개 파싱)\n")
    for r in rows[: a.limit]:
        ts = time.strftime("%Y-%m-%d %H:%M", time.localtime(r["mtime"]))
        print(f"## {r['title'] or '(제목없음)'}")
        print(f"- session : {r['session']}")
        print(f"- 최종활동: {ts}   턴수: {r['turns']}   점수: {r['score']}   일치: {', '.join(r['hits'])}")
        print(f"- cwd     : {r['cwd']}   branch: {r['branch']}")
        print(f"- 첫 프롬프트: {r['prompts'][0][:160] if r['prompts'] else '-'}")
        if len(r["prompts"]) > 1:
            print(f"- 끝 프롬프트: {r['prompts'][-1][:160]}")
        print(f"- 재개    : claude --resume {r['session']}")
        print(f"- 상세    : python3 ~/.claude/skills/session-resume/find_session.py --dump {r['session']}\n")


def cmd_dump(a):
    hits = subprocess.run(
        ["find", ROOT, "-name", a.dump + ".jsonl"], capture_output=True, text=True
    ).stdout.splitlines()
    if not hits:
        print(f"세션 파일을 찾지 못했습니다: {a.dump}")
        return
    path = hits[0]
    prompts, title, cwd, branch, branches = [], None, None, None, []
    found = OrderedDict((k, []) for k in URL_PATTERNS)
    with open(path, "r", errors="replace") as fh:
        for line in fh:
            for k, rx in URL_PATTERNS.items():
                for m in rx.findall(line):
                    if m not in found[k]:
                        found[k].append(m)
            if '"ai-title"' not in line and '"promptSource"' not in line:
                continue
            try:
                d = json.loads(line)
            except Exception:
                continue
            if d.get("type") == "ai-title":
                title = d.get("aiTitle") or title
                continue
            p = human_prompt(d)
            if p is not None:
                prompts.append((d.get("timestamp", ""), p))
                cwd = d.get("cwd") or cwd
                b = d.get("gitBranch")
                if b and b not in branches:
                    branches.append(b)
                branch = b or branch
    print(f"# {title or '(제목없음)'}\nsession: {a.dump}\nfile   : {path}")
    print(f"cwd    : {cwd}\nbranch : {branch}  (등장한 브랜치: {', '.join(branches) or '-'})")
    print(f"재개   : claude --resume {a.dump}\n")
    print("## 출처 링크 (사용자에게 다시 물어보지 말 것)")
    empty = True
    for k, v in found.items():
        if v:
            empty = False
            shown = [(u if len(u) <= 180 else u[:180] + "…(잘림)") for u in v[: a.links]]
            more = f"  (+{len(v) - a.links}건)" if len(v) > a.links else ""
            print(f"- {k}: " + ", ".join(shown) + more)
    if empty:
        print("- (없음) — 이 세션 전문에는 슬랙/지라/문서 링크가 없습니다")
    print(f"\n## 사람 프롬프트 전량 ({len(prompts)}턴)")
    for i, (ts, p) in enumerate(prompts, 1):
        body = p if len(p) <= a.width else p[: a.width] + " …"
        print(f"[{i}] {ts[:16]}  {body}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("terms", nargs="*", help="주제어 (여러 개 가능)")
    ap.add_argument("--dump", metavar="SESSION_ID", help="세션 1개 상세 추출")
    ap.add_argument("--days", type=int, default=0, help="최근 N일로 제한 (0=전체)")
    ap.add_argument("--cap", type=int, default=150, help="파싱할 후보 파일 수 상한")
    ap.add_argument("--limit", type=int, default=5, help="출력할 후보 수")
    ap.add_argument("--links", type=int, default=12, help="종류별 링크 출력 상한")
    ap.add_argument("--width", type=int, default=300, help="프롬프트 출력 길이 상한")
    ap.add_argument("--exclude", default="", help="제외할 세션 id (보통 현재 세션)")
    a = ap.parse_args()
    if a.dump:
        cmd_dump(a)
    elif a.terms:
        cmd_find(a)
    else:
        ap.error("주제어 또는 --dump 가 필요합니다")


if __name__ == "__main__":
    main()
