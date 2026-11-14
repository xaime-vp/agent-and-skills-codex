/**
 * Bonsai Podman Tools - Quick tools to build Bonsai worker images and safely stop previous workers.
 */

import path from "node:path";
import { Type } from "@earendil-works/pi-ai";
import { defineTool, type ExtensionAPI } from "@earendil-works/pi-coding-agent";

const SAFE_NAME = /^[A-Za-z0-9][A-Za-z0-9_.:/-]*$/;
const SAFE_SUFFIX = /^[A-Za-z0-9._-]+$/;

const buildImageTool = defineTool({
	name: "bonsai_build_image",
	label: "Bonsai Build Image",
	description:
		"Build a Bonsai worker Podman image in podman-machine-default from a local repo checkout (defaults to constant-integration).",
	parameters: Type.Object({
		repoPath: Type.Optional(
			Type.String({
				description: "Path to the constant-integration checkout (default: constant-integration)",
			}),
		),
		tag: Type.Optional(
			Type.String({
				description:
					"Image tag (default: localhost/bonsai-worker:main-<shortsha>)",
			}),
		),
		runCheck: Type.Optional(
			Type.Boolean({
				description: "Run `podman run --rm <tag> check` after building (default: false)",
			}),
		),
	}),

	async execute(_toolCallId, params, signal, _onUpdate, ctx) {
		const repoPath = path.resolve(ctx.cwd, params.repoPath ?? "constant-integration");
		const scriptPath = path.resolve(ctx.cwd, ".agents/skills/bonsai-containers/scripts/podman_wsl.py");
		if (params.tag && !SAFE_NAME.test(params.tag)) {
			throw new Error(`Invalid image tag: ${params.tag}`);
		}
		const args = ["-3", scriptPath, "build", "--repo", repoPath];
		if (params.tag) args.push("--tag", params.tag);
		if (params.runCheck) args.push("--check");

		const res = await piExecPyRef(args, signal);
		const output = [res.stdout, res.stderr].filter(Boolean).join("\n").trim();
		if (res.code !== 0) {
			throw new Error(`bonsai_build_image failed (exit ${res.code}):\n${output}`);
		}
		return {
			content: [{ type: "text", text: output || "Image built." }],
			details: { repoPath, tag: params.tag ?? "auto", runCheck: Boolean(params.runCheck) },
		};
	},
});

const stopWorkerTool = defineTool({
	name: "bonsai_stop_worker",
	label: "Bonsai Stop Worker",
	description:
		"Safely stop a running Bonsai worker container in podman-machine-default (checks for active tasks first, optional backup rename).",
	parameters: Type.Object({
		container: Type.Optional(
			Type.String({
				description: "Container name (default: bonsai-worker)",
			}),
		),
		backupSuffix: Type.Optional(
			Type.String({
				description: "If provided, rename the stopped container to <container>-before-<backupSuffix>",
			}),
		),
		force: Type.Optional(
			Type.Boolean({
				description: "Stop even if active task_process/pi/check.py processes are running (default: false)",
			}),
		),
	}),

	async execute(_toolCallId, params, signal, _onUpdate, ctx) {
		const container = params.container ?? "bonsai-worker";
		if (!SAFE_NAME.test(container)) {
			throw new Error(`Invalid container name: ${container}`);
		}
		if (params.backupSuffix && !SAFE_SUFFIX.test(params.backupSuffix)) {
			throw new Error(`Invalid backupSuffix: ${params.backupSuffix}`);
		}
		const scriptPath = path.resolve(ctx.cwd, ".agents/skills/bonsai-containers/scripts/podman_wsl.py");
		const args = ["-3", scriptPath, "stop", container];
		if (params.backupSuffix) {
			args.push("--backup-suffix", params.backupSuffix);
		}
		if (params.force) {
			args.push("--force");
		}

		const res = await piExecPyRef(args, signal);
		const output = [res.stdout, res.stderr].filter(Boolean).join("\n").trim();
		if (res.code !== 0) {
			throw new Error(`bonsai_stop_worker failed (exit ${res.code}):\n${output}`);
		}
		return {
			content: [{ type: "text", text: output || `Stopped ${container}.` }],
			details: { container, backupSuffix: params.backupSuffix ?? null, force: Boolean(params.force) },
		};
	},
});

const workerEventsTool = defineTool({
	name: "bonsai_worker_events",
	label: "Bonsai Worker Events",
	description:
		"Read or filter recent Bonsai worker events (/var/lib/bonsaiworker/private/events.jsonl) via podman_wsl.py.",
	parameters: Type.Object({
		container: Type.Optional(
			Type.String({
				description: "Container name (default: bonsai-worker)",
			}),
		),
		tail: Type.Optional(
			Type.Number({
				description: "Number of recent events to return (default: 10)",
			}),
		),
		filter: Type.Optional(
			Type.String({
				description: "Optional substring or issue number filter",
			}),
		),
	}),

	async execute(_toolCallId, params, signal, _onUpdate, ctx) {
		const container = params.container ?? "bonsai-worker";
		if (!SAFE_NAME.test(container)) {
			throw new Error(`Invalid container name: ${container}`);
		}
		const tail = params.tail ?? 10;
		if (!Number.isInteger(tail) || tail < 1) {
			throw new Error(`Invalid tail count: ${tail}`);
		}
		const scriptPath = path.resolve(
			ctx.cwd,
			".agents/skills/bonsai-containers/scripts/podman_wsl.py",
		);
		const args = ["-3", scriptPath, "events", "--container", container, "--tail", String(tail)];
		if (params.filter) {
			args.push("--filter", params.filter);
		}

		const res = await piExecPyRef(args, signal);
		const output = [res.stdout, res.stderr].filter(Boolean).join("\n").trim();
		if (res.code !== 0) {
			throw new Error(`bonsai_worker_events failed (exit ${res.code}):\n${output}`);
		}
		return {
			content: [{ type: "text", text: output || "[]" }],
			details: { container, tail, filter: params.filter ?? null },
		};
	},
});

let piExecPyRef: (args: string[], signal?: AbortSignal) => Promise<{ stdout: string; stderr: string; code: number }>;

export default function (pi: ExtensionAPI) {
	piExecPyRef = (args, signal) => pi.exec("py", args, { signal });
	pi.registerTool(buildImageTool);
	pi.registerTool(stopWorkerTool);
	pi.registerTool(workerEventsTool);
}
