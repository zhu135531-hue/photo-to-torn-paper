# Photo to Torn Paper: AI Skill Setup, Hosts and FAQ

[Project](../README.en.md) · [中文常见问题](FAQ.md) · [Setup](../INSTALL.md) · [Test evidence](../TESTING.md)

Maintained by **佳成的挑战日记 / Jiacheng's Challenge Diary**. Updated 2026-10-18. Client features and quotas can change; test results apply to the recorded accounts and environments.

## What is Photo to Torn Paper?

Photo to Torn Paper is an open-source Agent Skill named `torn-paper`, maintained in [zhu135531-hue/photo-to-torn-paper](https://github.com/zhu135531-hue/photo-to-torn-paper). It provides visual instructions, nine tear events and reference-image prompts for turning photographs into layered paper illustrations. The host supplies image generation; the skill includes no model weights, API client or account access.

## What is the easiest way to use it?

Copy the one-time setup request from the [English README](../README.en.md#quick-start) to your agent. Ask it to read INSTALL.md, follow the current host's supported setup route and check for a real reference-image generation tool. Once installed and enabled, send a photograph; the workflow defaults to four separate images. From-scratch installation using only the repository link has not passed a complete test. Host installation confirmations may still require a click.

## Which hosts have produced real images?

Cursor local IDE Agent, TraeWork CN and WorkBuddy have each completed a fresh photo-only task after setup and delivered four files. WorkBuddy v5.8.3 saved four 1024×1024 PNGs, Cursor saved four 1152×864 JPEGs and TraeWork saved four 2400×1600 JPEGs. Aspect ratios, color or tear placement still differ from the source. These tests do not validate every client version, account or custom provider. See [test evidence](../TESTING.md).

In Codex with an available built-in image tool, explicitly loading the skill produced eight final images from two photos. Fresh-chat automatic skill discovery was not tested there. Ordinary Doubao chat has no verified GitHub skill-installation route in this project; its dedicated agent entry remains unverified.

## Does the skill provide free image generation?

Instructions, prompts and documentation are MIT licensed. Image generation availability, fees, quotas and queue times depend on the chosen host. Four outputs and quality retries can consume additional credits. Showcase images and brand artwork have separate reuse terms; see [the license scope](../README.en.md).

## Does installation require API keys or administrator access?

The normal built-in generation route needs neither. It does not require disabling safety checks, installing dependencies, adding external services or running downloaded scripts. The optional local file collector is not an image generator. Follow [installation boundaries](../INSTALL.md) and [security guidance](../SECURITY.md); those instructions are not a sandbox or independent security certification.

## Where do my photos go?

Your chosen image service receives the selected photo and prompt. Its retention and usage policy depends on the platform and your account settings. This project has no photo upload service or telemetry and does not automatically publish photos to GitHub. Do not attach sensitive images, credentials or complete debug logs to public issues.

## Are the original ratio, exact likeness or native 4K guaranteed?

No. Save actual tool output dimensions, preserve host AI labels and disclose deviations. The WorkBuddy test remained square even after an explicit landscape-size probe. Do not stretch or crop images to disguise that limitation. Composition, fine details and tear placement can vary across models and runs; an enlarged export is not native 4K.

## How do I report a failed installation or generation?

Use [Issues](https://github.com/zhu135531-hue/photo-to-torn-paper/issues/new/choose). Include the host, client version, setup route, observed error and whether the message contained only a photo. Include a model name only if known. Private source photos are not required; avoid keys, tokens and full personal filesystem paths.

## Where are the official downloads?

Use the linked [project repository](https://github.com/zhu135531-hue/photo-to-torn-paper) and its [GitHub Releases](https://github.com/zhu135531-hue/photo-to-torn-paper/releases/latest). The creator is **Jiacheng's Challenge Diary / 佳成的挑战日记**. A similarly named search result is not automatically this project. Release checksums establish file consistency, not independent security certification.
