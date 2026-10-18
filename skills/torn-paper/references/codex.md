# Running in Codex

## Tool boundary

Use Codex's available built-in image-generation tool. If an installed image-generation skill supplies host instructions, follow it for tool parameters and output handling. No API key is needed for the built-in path. This skill does not supply a model and does not make a text-only environment able to render images.

If image generation is unavailable or fails with quota/access errors, report that concrete limitation. Do not silently switch to an API, ask for a key, generate a Python/SVG imitation, or present written prompts as completed images. API execution requires the user's explicit choice of that route.

## Reference handling

1. Inspect every source photo and its EXIF-oriented dimensions. A local path must be accessible to the image tool, not merely mentioned in a prompt.
2. Use the tool's documented image-reference mechanism. If it accepts local reference paths, pass only the current scene's path. If it only accepts recent conversation images, select the relevant source explicitly and identify it in the prompt.
3. Use one call per standalone variant. Do not combine the two scenes or request a four-panel image in place of four files.
4. For a correction, include the original source again to reduce composition drift. Also include the candidate only if the tool supports it and the correction needs it.

## Review and persistence

Inspect the returned image itself. File existence and correct dimensions do not prove visual fidelity. Check composition, material, main tear location, differences between variants, and scene-specific structures such as connected branches, bridge openings and aligned reflections.

The built-in tool may save under a host-managed generated-images directory. Use only the paths actually returned by the tool. Copy accepted files into the workspace; keep native PNG files and native dimensions by default. Do not claim a model name or seed if the tool does not disclose it. Do not commit the source photograph or generated tests unless publication is authorized.

For repeatable checks and non-destructive copying, run the bundled helper:

```text
python scripts/collect_outputs.py /absolute/path/to/manifest.json --output-dir /absolute/path/to/output/new-run
```

The script uses Pillow for decoding and EXIF-aware dimension checks; it never generates, edits or resizes images. Each manifest entry needs `id`, `scene`, `event`, `source_path`, `generated_path`, `prompt`, and a human visual `review` containing `status` (`accepted` or `rejected`) and `notes`. Optional fields may record previous attempts.

```json
{
  "execution": {"route": "Codex built-in image generation", "model": "not disclosed"},
  "images": [
    {
      "id": "scene-waterline",
      "scene": "scene",
      "event": "waterline",
      "source_path": "/absolute/path/source.jpg",
      "generated_path": "/actual/tool/returned/path.png",
      "prompt": "Actual prompt supplied to the tool",
      "review": {"status": "accepted", "notes": "Describe what was visually checked"}
    }
  ]
}
```

The saved `run.json` contains the prompts, original and generated dimensions, hashes, copied paths and review notes. It deliberately omits local source paths. It is a local test record, not a claim of compatibility with other hosts, automatic skill discovery, or pixel-identical reproduction.

## Invoking the repository copy

For a direct test without installing globally, explicitly ask Codex to read `skills/torn-paper/SKILL.md` in the current project and follow it. That verifies the loaded instructions and image execution, not automatic discovery in a fresh chat. For installation, follow the current official Codex skill-folder instructions rather than assuming another agent's `.cursor/skills` path applies.
