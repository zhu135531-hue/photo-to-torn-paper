# Photo to Torn Paper — Open-source AI Agent Skill for Paper Art

**One photo. Four ways to tear the paper.**

Created and maintained by **佳成的挑战日记 — Jiacheng's Challenge Diary**.

**Photo to Torn Paper** is an open-source Agent Skill named `torn-paper`. It guides a reference-image-capable agent to turn photographs into layered torn-paper illustrations, normally producing four separate variants. Photo-only generation after setup has been tested in Cursor local Agent, TraeWork CN and WorkBuddy; exact fidelity and aspect-ratio limitations are recorded for each host.

[中文](README.md) · [Setup](INSTALL.md) · [FAQ](docs/FAQ.en.md) · [Latest release](https://github.com/zhu135531-hue/photo-to-torn-paper/releases/latest) · [Security](SECURITY.md)

![Jiacheng's Challenge Diary — Photo to Torn Paper](assets/cover.png)

Turn a photograph into a full-bleed illustration built from textured paper, torn fibers and shallow overlapping shadows. Keep the original composition, subject scale and palette. Each variant changes the dominant tear, rather than merely recoloring the scene.

This repository shares instructions, a prompt skeleton and nine tear events. **It does not include model weights, an API client or guaranteed image-generation access.** Use an image-capable host that can accept a reference photograph.

## Quick start

Ask your agent to handle setup; copy this once:

```text
Help me install and enable the Photo to Torn Paper skill by Jiacheng's Challenge Diary:
https://github.com/zhu135531-hue/photo-to-torn-paper

Read INSTALL.md, follow the supported route for this host, and check that a real reference-image generation tool is available. After setup, treat my photo-only messages as requests for four separate torn-paper images. Ask only for necessary installation or permission confirmations, and report any unsupported step honestly.
```

This agent-assisted, from-scratch installation route has not yet passed a complete test. The verified runs start after installation using the routes below. A GitHub URL alone does not establish installation support in ordinary Doubao chat. The skill does not provide a model, credentials or image-generation access; generation availability, fees and photo handling depend on the host.

For the photo-only workflow, download [photo-studio.zip](https://github.com/zhu135531-hue/photo-to-torn-paper/releases/latest/download/photo-studio.zip), extract it, and open **photo-studio** in Cursor or TRAE. Start a local Agent chat and send a photograph. The bundled project rule supplies the request; no per-photo prompt or slash command is intended. See [platform setup and verification status](INSTALL.md).

Portable ZIP packages support skill import, including a root-level SKILL.md for TraeWork. WorkBuddy was tested in a new default office task after skill installation; a dedicated expert is optional and its setup/share flow remains unverified. Ordinary Doubao chat has no verified GitHub skill-installation route in this project; its dedicated image-capable agent must be configured and tested first. Packaging alone does not establish end-to-end compatibility.

### Manual fallback

Upload your own photo in a reference-image editing tool and try:

```text
Rebuild this photo as one full-bleed layered torn-paper illustration.
Keep its aspect ratio, composition, subject scale, identifying features and palette.
Make every surface paper, including water, bark, clothing and skin.
Use one dominant physically plausible tear along an existing object boundary;
keep other edges clean-cut, without uniform white sticker outlines.
Keep people intact. Preserve bridge openings, connected branches and aligned reflections.
No invented words, promotional watermarks, people or landmarks.
Preserve host-applied AI/provenance labels. Produce one image, not a grid.
```

For the full agent workflow, download and extract the `torn-paper` skill folder. Copy it into your host's supported skill directory. Codex uses `.agents/skills/torn-paper` for a project; Cursor uses `.cursor/skills/torn-paper`. See the [installation guide](skills/torn-paper/README.md). Then explicitly invoke the skill with a reference photo and request four separate images.

## What has been tested

In a Codex session with the built-in image-generation tool, we explicitly loaded this skill and tested two photos: a magnolia courtyard and a canal with a stone bridge. Eight final images were retained after two targeted corrections. See [testing notes](TESTING.md).

In Cursor local IDE Agent, a fresh studio chat received only a canal photograph, with no text. It loaded the workflow, generated four real images, retried two, and saved four JPEGs. The output was 1152×864 (4:3), rather than the source's approximately 3:2; some tear placement and color details also drifted. This verifies the photo-only execution path, not full visual fidelity or compatibility across accounts.

In TraeWork CN, we imported the published root-level ZIP, enabled torn-paper, and sent only the canal photograph in a new default local task. It automatically invoked the skill and delivered four separate JPEGs, each saved at 2400×1600. Files decoded successfully and opened in the side-panel preview. Some tears, reflections and colors still drifted; platform AI labels remained. Four simultaneous inline previews and the generation tool's native versus saved dimensions were not independently verified.

WorkBuddy v5.8.3 also passed a fresh default-task, photo-only run: automatic skill selection, real generation and four distinct PNG files with previews. All four were 1024×1024 for a 1080×719 source; a separate explicit `size: "1536x1024"` probe still returned a square image. Original-ratio preservation and strict visual acceptance did not pass. The update prevents observed concurrent filename collisions and preserves host AI labels. Installation and a scanner's safe result are not a comprehensive security certification. Doubao's dedicated entry and fresh-session automatic discovery in Codex remain unverified. Output varies by host and model; an enlarged export is not described as native 4K.

## Privacy and security

Generation sends your selected photo and prompt to your chosen image service. The optional local collection helper makes no network calls and does not execute shell commands, but it decodes images and copies approved files. Its path roots must be supplied explicitly, outputs stay inside the authorized workspace, and prompts are excluded from logs by default. See [security boundaries](SECURITY.md) and the [self-review](docs/SECURITY_REVIEW.md).

## Share what works

Reproduction reports, improvements and honest failures are welcome. Use [Issues](https://github.com/zhu135531-hue/photo-to-torn-paper/issues) to tell us your host, model, prompt adjustments and outcome; upload images only if you have permission and want them to be public. Starring or sharing the project is optional.

Suggested optional credit: “Workflow by 佳成的挑战日记 / Jiacheng's Challenge Diary.” No brand watermark is added to ordinary output.

Skill instructions, prompts and documentation: [MIT](LICENSE). Showcase images in `examples/` and brand artwork in `assets/` are excluded from the MIT grant; contact the creator before reusing those images. Your own photos and generated images remain subject to their applicable rights and platform terms.
