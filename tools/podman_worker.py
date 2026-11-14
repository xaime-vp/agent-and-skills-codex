"""Manage and relaunch Bonsai worker containers on Podman (Windows WSL or Linux)."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile


DEFAULT_WSL_DISTRO = "podman-machine-default"
DEFAULT_CONTAINERS = ("bonsai-worker", "bonsai-ui-worker")
ACTIVE_STATUSES = ("preparing", "running", "dispatched", "publishing", "unknown")


def _to_wsl_path(path: Path) -> str:
    resolved = path.resolve()
    text = str(resolved)
    if os.name == "nt":
        match = re.match(r"^([A-Za-z]):[\\/](.*)$", text)
        if match:
            drive = match.group(1).lower()
            rest = match.group(2).replace("\\", "/")
            return f"/mnt/{drive}/{rest}"
    return text.replace("\\", "/")


def _podman_cmd(args: list[str], *, wsl_distro: str | None) -> list[str]:
    if os.name == "nt":
        distro = wsl_distro or DEFAULT_WSL_DISTRO
        return ["wsl", "-d", distro, "--", "podman", *args]
    return ["podman", *args]


def _run_podman(
    args: list[str],
    *,
    wsl_distro: str | None,
    check: bool = True,
    capture: bool = True,
) -> subprocess.CompletedProcess[str]:
    env = dict(os.environ)
    env["MSYS_NO_PATHCONV"] = "1"
    env.setdefault("PODMAN_IGNORE_CGROUPSV1_WARNING", "1")
    cmd = _podman_cmd(args, wsl_distro=wsl_distro)
    return subprocess.run(
        cmd,
        env=env,
        text=True,
        capture_output=capture,
        check=check,
    )


def _git_output(repo: Path, args: list[str]) -> str:
    res = subprocess.run(
        ["git", "-C", str(repo), *args],
        text=True,
        capture_output=True,
        check=True,
    )
    return res.stdout.strip()


def _container_exists(name: str, *, wsl_distro: str | None) -> bool:
    res = _run_podman(["container", "exists", name], wsl_distro=wsl_distro, check=False)
    return res.returncode == 0


def _inspect_container(name: str, *, wsl_distro: str | None) -> dict:
    res = _run_podman(["inspect", name], wsl_distro=wsl_distro)
    data = json.loads(res.stdout)
    if not data:
        raise RuntimeError(f"Container not found: {name}")
    return data[0]


def _detect_volume(inspect_data: dict) -> str:
    for mount in inspect_data.get("Mounts") or []:
        if mount.get("Destination") == "/var/lib/bonsaiworker":
            name = mount.get("Name") or mount.get("Source")
            if name:
                return str(name)
    raise RuntimeError("Could not detect /var/lib/bonsaiworker volume mount from container inspect.")


def _env_map(inspect_data: dict) -> dict[str, str]:
    out: dict[str, str] = {}
    for entry in (inspect_data.get("Config") or {}).get("Env") or []:
        if "=" in entry:
            k, v = entry.split("=", 1)
            out[k] = v
    return out


def _read_worker_runtime_info(container: str, *, wsl_distro: str | None) -> dict:
    script = (
        "import json, sqlite3, os, pathlib; "
        "cfg_path = pathlib.Path('/var/lib/bonsaiworker/config.json'); "
        "cfg = json.loads(cfg_path.read_text()) if cfg_path.is_file() else {}; "
        "db_path = pathlib.Path('/var/lib/bonsaiworker/private/state.db'); "
        "active = []; recent = []; "
        "conn = sqlite3.connect(str(db_path)) if db_path.is_file() else None; "
        "active = [list(r) for r in conn.execute(\"SELECT key, issue, status, updated_at FROM tasks WHERE status IN ('preparing','running','dispatched','publishing','unknown') ORDER BY updated_at DESC\")] if conn else []; "
        "recent = [list(r) for r in conn.execute('SELECT key, issue, status, updated_at FROM tasks ORDER BY updated_at DESC LIMIT 4')] if conn else []; "
        "procs = [p for p in os.listdir('/proc') if p.isdigit()]; "
        "cmds = [pathlib.Path(f'/proc/{p}/cmdline').read_bytes().replace(b'\\x00', b' ').decode('utf-8','replace') for p in procs]; "
        "busy = [c for c in cmds if any(k in c for k in ('task_process', 'pi', 'check.py')) and 'import json, sqlite3' not in c]; "
        "print(json.dumps({'config': {k: cfg.get(k) for k in ('target_repository','max_concurrent_tasks','automatic_pr_reviews','process_containment','model','release_root')}, 'active_tasks': active, 'recent_tasks': recent, 'active_procs': busy}))"
    )
    res = _run_podman(["exec", container, "python3", "-c", script], wsl_distro=wsl_distro)
    return json.loads(res.stdout)


def cmd_status(args: argparse.Namespace) -> int:
    containers = args.container or list(DEFAULT_CONTAINERS)
    rows = []
    for name in containers:
        if not _container_exists(name, wsl_distro=args.wsl_distro):
            rows.append({"container": name, "exists": False})
            continue
        insp = _inspect_container(name, wsl_distro=args.wsl_distro)
        state = insp.get("State") or {}
        running = bool(state.get("Running"))
        info: dict = {
            "container": name,
            "exists": True,
            "running": running,
            "status": state.get("Status"),
            "image": insp.get("ImageName"),
        }
        if running:
            info.update(_read_worker_runtime_info(name, wsl_distro=args.wsl_distro))
        rows.append(info)

    if args.json:
        print(json.dumps(rows, indent=2))
        return 0

    for item in rows:
        if not item["exists"]:
            print(f"{item['container']}: not found")
            continue
        cfg = item.get("config") or {}
        print(f"=== {item['container']} ({item.get('status')}, {item.get('image')}) ===")
        if item["running"]:
            print(
                f"  repo={cfg.get('target_repository')} slots={cfg.get('max_concurrent_tasks')} "
                f"reviewer={cfg.get('automatic_pr_reviews')} containment={cfg.get('process_containment')} "
                f"model={cfg.get('model')}"
            )
            active = item.get("active_tasks") or []
            if active:
                for key, issue, status, updated in active:
                    print(f"  ACTIVE: #{issue} {key} [{status}] ({updated})")
            else:
                print("  ACTIVE: none")
            for key, issue, status, updated in item.get("recent_tasks") or []:
                print(f"  recent: #{issue} {key} [{status}] ({updated})")
    return 0


def build_image_from_ref(
    *,
    repo_path: Path,
    ref: str,
    tag: str | None,
    wsl_distro: str | None,
) -> tuple[str, str]:
    _git_output(repo_path, ["fetch", "origin"])
    short_sha = _git_output(repo_path, ["rev-parse", "--short", ref])
    resolved_tag = tag or f"localhost/bonsai-worker:main-{short_sha}"
    worktree_dir = Path(tempfile.mkdtemp(prefix=f"bonsai-build-{short_sha}-"))
    try:
        subprocess.run(
            ["git", "-C", str(repo_path), "worktree", "add", "--detach", str(worktree_dir), ref],
            check=True,
        )
        wsl_wt = _to_wsl_path(worktree_dir)
        print(f"Building {resolved_tag} from {ref} ({short_sha})...")
        _run_podman(
            [
                "build",
                "-f",
                f"{wsl_wt}/workers/bonsai/Dockerfile",
                "--build-arg",
                f"BONSAI_SOURCE_REVISION={short_sha}",
                "--tag",
                resolved_tag,
                wsl_wt,
            ],
            wsl_distro=wsl_distro,
            capture=False,
        )
    finally:
        subprocess.run(
            ["git", "-C", str(repo_path), "worktree", "remove", "--force", str(worktree_dir)],
            check=False,
            capture_output=True,
        )
    return resolved_tag, short_sha


def cmd_build(args: argparse.Namespace) -> int:
    tag, sha = build_image_from_ref(
        repo_path=Path(args.repo_path),
        ref=args.ref,
        tag=args.tag,
        wsl_distro=args.wsl_distro,
    )
    print(f"Built {tag} (revision {sha})")
    return 0


def cmd_relaunch(args: argparse.Namespace) -> int:
    name = args.container
    insp = _inspect_container(name, wsl_distro=args.wsl_distro)
    volume = _detect_volume(insp)
    running = bool((insp.get("State") or {}).get("Running"))
    env_vars = _env_map(insp)

    runtime_cfg: dict = {}
    if running:
        info = _read_worker_runtime_info(name, wsl_distro=args.wsl_distro)
        runtime_cfg = info.get("config") or {}
        if not args.force and (info.get("active_tasks") or info.get("active_procs")):
            print("Refusing to relaunch while active tasks or role processes exist (use --force to override):", file=sys.stderr)
            print(json.dumps({"active_tasks": info.get("active_tasks"), "active_procs": info.get("active_procs")}, indent=2), file=sys.stderr)
            return 2

    target_repo = args.target_repository or runtime_cfg.get("target_repository") or env_vars.get("BONSAI_TARGET_REPOSITORY")
    if not target_repo:
        raise RuntimeError("Could not determine target_repository; pass --target-repository.")
    slots = args.max_concurrent_tasks if args.max_concurrent_tasks is not None else (runtime_cfg.get("max_concurrent_tasks") or int(env_vars.get("BONSAI_MAX_CONCURRENT_TASKS", "10")))
    if args.automatic_pr_reviews is not None:
        reviewer = args.automatic_pr_reviews
    else:
        reviewer = bool(runtime_cfg.get("automatic_pr_reviews", False))
    containment = args.process_containment or runtime_cfg.get("process_containment") or env_vars.get("BONSAI_PROCESS_CONTAINMENT") or "session"
    model = args.model or runtime_cfg.get("model") or env_vars.get("BONSAI_MODEL") or ""

    if args.image:
        image = args.image
        short_sha = image.rsplit("-", 1)[-1] if "-" in image else dt.datetime.now().strftime("%Y%m%d%H%M%S")
    else:
        image, short_sha = build_image_from_ref(
            repo_path=Path(args.repo_path),
            ref=args.ref,
            tag=args.tag,
            wsl_distro=args.wsl_distro,
        )

    backup_name = f"{name}-before-{short_sha}"
    if _container_exists(backup_name, wsl_distro=args.wsl_distro):
        backup_name = f"{backup_name}-{dt.datetime.now().strftime('%Y%m%d%H%M%S')}"

    if args.dry_run:
        print(json.dumps({
            "container": name,
            "backup_name": backup_name,
            "volume": volume,
            "image": image,
            "target_repository": target_repo,
            "max_concurrent_tasks": slots,
            "automatic_pr_reviews": reviewer,
            "process_containment": containment,
            "model": model,
        }, indent=2))
        return 0

    if running:
        print(f"Stopping {name}...")
        _run_podman(["stop", name], wsl_distro=args.wsl_distro, capture=False)
    print(f"Renaming {name} -> {backup_name}...")
    _run_podman(["rename", name, backup_name], wsl_distro=args.wsl_distro, capture=False)

    configure_args = [
        "configure",
        "--target-repository", target_repo,
        "--worker-python", "/usr/local/bin/python",
        "--worker-uid", "10001",
        "--worker-gid", "10001",
        "--max-concurrent-tasks", str(slots),
        "--automatic-pr-reviews" if reviewer else "--no-automatic-pr-reviews",
        "--secrets-file", "/var/lib/bonsaiworker/private/secrets.env",
        "--policy-file", "/var/lib/bonsaiworker/intake-policy.json",
        "--checks-file", "/var/lib/bonsaiworker/checks.json",
        "--install-root", "/var/lib/bonsaiworker",
        "--process-containment", containment,
    ]
    if model:
        configure_args.extend(["--model", model])

    configure_py = (
        "import sys; sys.path.insert(0, '/opt/bonsai'); "
        f"sys.argv = {json.dumps(configure_args)}; "
        "from workers.bonsai.configure import main; main()"
    )
    print(f"Preparing release on volume {volume}...")
    _run_podman(
        ["run", "--rm", "--entrypoint", "python3", "-v", f"{volume}:/var/lib/bonsaiworker", image, "-I", "-B", "-c", configure_py],
        wsl_distro=args.wsl_distro,
        capture=False,
    )
    print(f"Installing release on volume {volume}...")
    _run_podman(
        ["run", "--rm", "-v", f"{volume}:/var/lib/bonsaiworker", image, "install"],
        wsl_distro=args.wsl_distro,
        capture=False,
    )

    run_args = [
        "run", "-d",
        "--name", name,
        "--restart", "unless-stopped",
        "-v", f"{volume}:/var/lib/bonsaiworker",
        "-e", f"BONSAI_TARGET_REPOSITORY={target_repo}",
        "-e", f"BONSAI_MAX_CONCURRENT_TASKS={slots}",
        "-e", f"BONSAI_AUTOMATIC_PR_REVIEWS={'true' if reviewer else 'false'}",
        "-e", f"BONSAI_PROCESS_CONTAINMENT={containment}",
    ]
    if model:
        run_args.extend(["-e", f"BONSAI_MODEL={model}"])
    run_args.extend([image, "run"])

    print(f"Starting {name} with {image}...")
    _run_podman(run_args, wsl_distro=args.wsl_distro, capture=False)
    info = _read_worker_runtime_info(name, wsl_distro=args.wsl_distro)
    print("Relaunch complete:", json.dumps(info["config"], indent=2))
    return 0


def cmd_reconcile(args: argparse.Namespace) -> int:
    name = args.container
    insp = _inspect_container(name, wsl_distro=args.wsl_distro)
    volume = _detect_volume(insp)
    image = insp.get("ImageName")
    running = bool((insp.get("State") or {}).get("Running"))

    if running:
        info = _read_worker_runtime_info(name, wsl_distro=args.wsl_distro)
        if info.get("active_procs") and not args.force:
            print("Refusing to reconcile while role processes are running:", info["active_procs"], file=sys.stderr)
            return 2
        _run_podman(["stop", name], wsl_distro=args.wsl_distro, capture=False)

    if args.process_containment:
        update_py = (
            "import sys, json; from pathlib import Path; sys.path.insert(0, '/opt/bonsai'); "
            "from workers.bonsai.state import atomic_json\n"
            "for p in (Path('/var/lib/bonsaiworker/config.json'), Path('/var/lib/bonsaiworker/private/prepared-config.json')):\n"
            "    if p.is_file():\n"
            "        d = json.loads(p.read_text(encoding='utf-8'))\n"
            f"        d['process_containment'] = {json.dumps(args.process_containment)}\n"
            "        atomic_json(p, d)\n"
        )
        _run_podman(
            ["run", "--rm", "--entrypoint", "python3", "-v", f"{volume}:/var/lib/bonsaiworker", image, "-I", "-B", "-c", update_py],
            wsl_distro=args.wsl_distro,
            capture=False,
        )

    evidence = args.evidence or f"Confirmed no task_process/pi/check.py processes running in {name} via /proc; container stopped cleanly before reconciliation."
    reconcile_py = (
        "import sys; sys.path.insert(0, '/opt/bonsai'); "
        f"sys.argv = ['controller', '--config', '/var/lib/bonsaiworker/config.json', '--reconcile-task', {json.dumps(args.task_key)}, '--confirmed-stopped', '--evidence', {json.dumps(evidence)}]; "
        "from workers.bonsai.controller import main; main()"
    )
    _run_podman(
        ["run", "--rm", "--entrypoint", "python3", "-v", f"{volume}:/var/lib/bonsaiworker", image, "-I", "-B", "-c", reconcile_py],
        wsl_distro=args.wsl_distro,
        capture=False,
    )
    _run_podman(["start", name], wsl_distro=args.wsl_distro, capture=False)
    print(f"Reconciled {args.task_key} and restarted {name}.")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--wsl-distro", default=DEFAULT_WSL_DISTRO, help="WSL distro hosting Podman on Windows")
    sub = parser.add_subparsers(dest="command", required=True)

    p_status = sub.add_parser("status", help="Show container, config, and active task slot status")
    p_status.add_argument("--container", action="append", help="Container name (repeatable; defaults to bonsai-worker and bonsai-ui-worker)")
    p_status.add_argument("--json", action="store_true", help="Print JSON output")
    p_status.set_defaults(func=cmd_status)

    p_build = sub.add_parser("build", help="Build a Bonsai worker image from a git ref using a clean detached worktree")
    p_build.add_argument("--repo-path", default="constant-integration", help="Local constant-integration git checkout")
    p_build.add_argument("--ref", default="origin/main", help="Git ref/commit to build (default: origin/main)")
    p_build.add_argument("--tag", help="Image tag (default: localhost/bonsai-worker:main-<shortsha>)")
    p_build.set_defaults(func=cmd_build)

    p_relaunch = sub.add_parser("relaunch", help="Safely stop, upgrade/reconfigure, and relaunch an existing Bonsai worker")
    p_relaunch.add_argument("--container", required=True, help="Existing container name (e.g. bonsai-worker)")
    p_relaunch.add_argument("--repo-path", default="constant-integration", help="Local constant-integration git checkout")
    p_relaunch.add_argument("--ref", default="origin/main", help="Git ref/commit to build when --image is omitted")
    p_relaunch.add_argument("--image", help="Use an existing image tag instead of building")
    p_relaunch.add_argument("--tag", help="Custom tag when building from --ref")
    p_relaunch.add_argument("--target-repository", help="Override target repository (owner/name)")
    p_relaunch.add_argument("--max-concurrent-tasks", type=int, help="Override concurrent task slots (1..10)")
    p_relaunch.add_argument("--automatic-pr-reviews", action=argparse.BooleanOptionalAction, default=None, help="Enable or disable automatic PR reviews")
    p_relaunch.add_argument("--process-containment", choices=("cgroup", "session"), help="Override process containment mode")
    p_relaunch.add_argument("--model", help="Override OpenRouter model ID")
    p_relaunch.add_argument("--force", action="store_true", help="Proceed even if active tasks/processes are detected")
    p_relaunch.add_argument("--dry-run", action="store_true", help="Print resolved relaunch plan without mutating")
    p_relaunch.set_defaults(func=cmd_relaunch)

    p_reconcile = sub.add_parser("reconcile", help="Safely stop, reconcile an unknown task, optionally update containment, and restart")
    p_reconcile.add_argument("--container", required=True, help="Container name")
    p_reconcile.add_argument("--task-key", required=True, help="Unknown task key to reconcile")
    p_reconcile.add_argument("--evidence", help="Operator stop-confirmation evidence")
    p_reconcile.add_argument("--process-containment", choices=("cgroup", "session"), help="Also update process_containment in config.json and prepared-config.json")
    p_reconcile.add_argument("--force", action="store_true", help="Proceed even if role processes are detected")
    p_reconcile.set_defaults(func=cmd_reconcile)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
