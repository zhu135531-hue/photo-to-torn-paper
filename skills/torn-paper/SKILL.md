---
name: torn-paper
description: "把实拍照片转为满幅撕纸分层插画，保留主体大小、构图和原图颜色，默认每张照片输出四种撕口。人像保持完整，撕口避开身体。Use for 撕纸风格、四种撕纸、照片转撕纸、torn-paper or cut-paper layers. Not for layouts that retain photographic pixels or add editorial captions."
---

# 撕纸

Rebuild each supplied photograph as layered cut paper. Return four separate posters per photograph unless the user specifies another count. Two photos therefore mean eight deliverables; never mix the scenes or replace separate files with a contact sheet.

This skill is standalone. Do not borrow a blank-paper poster layout, a single accent color, a 3:5 canvas, or a caption from another paper skill. If the user explicitly asks to keep the photograph itself, or to make a sparse editorial poster, stop and use that other skill instead.

## Read before generating

Read these files beside this skill, once per conversation, before the first image:

- `references/visual-system.md`
- `references/tear-events.md`
- `references/prompt.md`

In Codex, also read `references/codex.md` for tool execution and saving. The skill supplies visual instructions, not a model or API client. Check that image generation is actually available before promising finished images.

## What comes back

1. Four finished images, in the same reply. A revision of one image returns that one image.
2. For each image, in Chinese: 设计灵感, 设计语言, 设计思路.
3. Keep the ordinary reply focused on the images. For a test/debug request, save the actual prompts, output dimensions, and review notes to a local run record and link it; follow the host image tool's reporting requirements.

The reply is unfinished if only some of the images are shown.

## Decision order

When two rules conflict, use the earlier one:

1. The place or the person must stay recognizable at the photograph's own scale.
2. No photographic pixels remain.
3. Colors stay close to the photograph. Warm exposed fibers stay narrow; naturally pale or cream objects in the source may keep their color.
4. The tear separates real sheets. It does not cross a person's body.
5. The four posters share one material and differ by the tear event.
6. No added words.

## Read the photograph

Write this down before choosing events. Do not show it to the user.

- Hero: the one thing the photograph is about.
- Two relationships that survive in every poster, such as "person in front of the flowering tree" or "wheel behind the roof".
- Three to five sheets already in the picture: sky, foliage, building, water, person, boat.
- Five to eight colors, named from the photograph, not from a palette.
- Aspect: inspect actual dimensions after EXIF orientation. Preserve their ratio, including `3:2` and `2:3`; prefer the exact ratio when supported. Do not force a landscape into a portrait or crop to a preset. If the tool only supports approximate ratios, use the closest and disclose a material deviation; never stretch the image.
- Lettering: only words that are large and certainly readable. Otherwise none.
- People: if a person is the hero, mark the portrait rule on all four.

## Choose the four tears

Pick four events from `references/tear-events.md` that this photograph can support. Write one physical sentence for each: which sheet tears, what it separates, what it must not cross.

Reject a set where two posters tear the same sheet in the same place. Reject a set that changes the palette or the scale instead of the tear. Name the dominant torn sheet and location in each prompt; specify which other edges remain clean cut paper so the model does not outline every object in white.

For a person, the only allowed events are whole sheet, window, stop, and sides.

## Generate

Pass the photograph as a semantic reference. Build each prompt from `references/prompt.md`. One prompt, one tear event.

Generate one independent image per planned variant. Inspect each result and track which source and event it belongs to. Finish the requested set, retaining accepted images when retrying others.

Regenerate an image before showing it if any of these are true:

- photographic texture or a pasted face remains
- the hero has shrunk into an icon, a sticker, or a black logo
- the scene has been repainted beige, brown, or a single accent
- a tear crosses a face, neck, hair, hat, glasses, shirt, arm, hand, or strap
- a background tear only frames the person and the tree together, with no gap between them
- invented text, an extra person, or a watermark appears
- the tear is a smooth oval, a repeating zigzag, or a white sticker outline
- variants differ only in texture or color, with the same dominant torn sheet and location
- a main branch is severed, the bridge opening is filled, or reflections detach from their buildings

Replace only the failed image. Keep the ones that pass. Do not stop at two.

For a quality miss, retry that image with a specific correction and the original photo as reference. Avoid an unbounded retry loop: ordinarily allow two correction attempts per variant, then disclose the remaining limitation. For tool/authentication/quota errors, follow the host tool's recovery rules; do not switch to a paid API or claim success without actual images. Say which variants failed and show the ones that exist.

## Save

When the conversation is inside a project that keeps outputs, copy each accepted generated file into a new run directory at its actual native dimensions, without overwriting earlier work:

`output/<run-id>/<scene>-tear-<event>.png`

Use a short scene name and the event name: `whole`, `window`, `stop`, `sides`, `stack`, `waterline`, `through`, `sky`, `frame`.

Use the actual image extension. Do not label an image `4k` merely because it was enlarged. If the user asks for a specific export size, preserve the aspect ratio, follow the host image tool's supported workflow, and report native versus exported dimensions. Read `references/codex.md` for the optional verification/copy helper.

Do not save or commit the user's source photograph unless they ask.

## Tell the user

Show every finished image. Under each one:

- 设计灵感: the physical idea, one sentence
- 设计语言: which sheet tears
- 设计思路: what stayed intact, and what the tear separates

Name the hero and the two relationships that stayed. Do not describe a poster that was rejected.

## Single image

If the user asks to redo one poster, change only the tear they named. Keep the same scale, colors, and hero. Return that one image with the same three lines.
