# Host execution routes

The installed workflow supplies the defaults. Users send a photo; the agent builds the prompt and executes the image tool. Do not ask them to copy a prompt into a second app.

## Cursor

Use Agent in an opened local project. Read the available image-generation tool's schema and pass the uploaded photo through its actual reference-image field. Cursor documents built-in generation from text or reference images; the tool name can vary by version. Do not guess argument names or replace reference-image generation with a terminal script.

The dedicated studio package contains a project rule that loads this skill for photo-only turns, including a fresh chat. The plugin contains the same rule; prefer project scope when installing. Merely copying the skill without the rule leaves selection to the agent. Ask mode, Quick Chat without a project, cloud agents and custom providers are not assumed equivalent to the tested local Agent route.

For a tool output written to disk, use the path actually returned by the tool. Embed each accepted image in the final conversation using the host's supported image Markdown/attachment mechanism, with an absolute file path when local paths are supported, and provide an individual file link as fallback. A folder path plus four captions does not display four images. Do not claim that the preview is visible unless the host actually renders it. If the account, environment or model does not expose image generation, report the actual missing capability. Do not create an API account, request keys, change providers or install an MCP automatically.

## TRAE / TraeWork

Use the host-provided image-generation capability that accepts an input image. The studio package supplies `.trae/skills` and an always-applied project rule. A local ZIP importer may retain only SKILL.md; the portable package therefore includes the visual instructions in that one file.

If the host requires an official image skill to expose the tool, use it only when already enabled and available to this conversation. Do not assume a Seedream model name implies an executable tool, nor silently configure a billed external API. Local IDE, cloud Agent and TraeWork capabilities must be checked separately.

## WorkBuddy

Load the enabled torn-paper skill when the user submits a photo without text. Use the image-to-image tool actually assigned by WorkBuddy. Tool permissions are supplied by the host, not invented in SKILL.md. Use the current photo as reference, then display all four separate outputs.

Generate serially, one variant at a time. In the Windows v5.8.3 test, concurrent ImageGen calls with the same prompt prefix returned duplicate paths and overwrote two of four images. Use a separate destination directory for each event/attempt if the actual tool schema provides one, for example `output/<run>/01-waterline/attempt-1/`. Start each prompt with a short distinct event identifier as an additional filename safeguard. If no destination field exists, preserve the returned image to a unique event filename before starting the next call. Verify four distinct saved files and their event mapping before the final reply; never count previews or successful calls alone.

WorkBuddy may add an “AI生成” label. Keep this host provenance label. Do not set empty/whitespace watermark parameters, crop, erase, or regenerate merely to remove it. Do not confuse it with an invented caption or promotional logo.

In the Windows v5.8.3 test, the current ImageGen route returned 1024×1024 images for a 1080×719 photo. A separate one-image probe explicitly requested `size: "1536x1024"` but still returned 1024×1024. This is a limitation observed in that account and route, not a guarantee about every version. Read the current schema, use its real supported size field when available, and verify the saved dimensions. If the result remains square, deliver it with a clear ratio limitation; do not promise original-ratio preservation, stretch/crop it, or switch services automatically.

A dedicated expert can bind this workflow persistently; its setup instructions should load this skill before accepting photo-only input. Skill ZIP installation and expert-market publication are different operations. Do not claim market availability or a share link until the host creates it. If photo-only matching is not reliable, bind it to an expert rather than asking for a full prompt every time.

## Doubao

Ordinary Doubao chat and Doubao Work developer skills are separate entry points. Do not claim that a GitHub URL installs a skill in ordinary chat. The standalone agent instructions from this project can configure a dedicated image-capable conversation/agent once, after which subsequent photo-only turns mean conversion. Confirm actual image generation and sharing support in that account before publishing an “open and upload” link. Do not fabricate such a link.

## All hosts

Inspect real outputs, retry specific visual misses within the skill's limit, preserve native sizes, and show the accepted images. A successful install is not a successful run. Never upload user photos to the public repository. Ordinary generation requires no Python dependency installation.
