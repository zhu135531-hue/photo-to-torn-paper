---
name: torn-paper
description: "从一张照片做出撕纸分层海报：整张都是剪纸，不留照片像素，主体保持原来的大小和比例，颜色跟照片走，奶油色只出现在撕口。默认一次给四张，四张只换撕口的位置。人像的撕口不经过身体，只把人和后面的景物分开。Use when the user asks for 撕纸, 四种撕纸, 撕纸分层, 撕纸风格, 撕纸照片, torn paper, torn-paper, or cut-paper layers. Do not use for a photo collage that keeps the photograph, a 3:5 blank-paper poster, or a captioned zine."
---

# 撕纸

The user gives one photograph. Rebuild it as layered cut paper. Return four posters unless the user asks for a single one.

This skill is standalone. Do not borrow a blank-paper poster layout, a single accent color, a 3:5 canvas, or a caption from another paper skill. If the user explicitly asks to keep the photograph itself, or to make a sparse editorial poster, stop and use that other skill instead.

## Read before generating

Read these files beside this skill, once per conversation, before the first image:

- `references/visual-system.md`
- `references/tear-events.md`
- `references/prompt.md`

## What comes back

1. Four finished images, in the same reply. A revision of one image returns that one image.
2. For each image, in Chinese: 设计灵感, 设计语言, 设计思路.
3. No generation prompt in the reply.

The reply is unfinished if only some of the images are shown.

## Decision order

When two rules conflict, use the earlier one:

1. The place or the person must stay recognizable at the photograph's own scale.
2. No photographic pixels remain.
3. Colors stay close to the photograph. Cream is only the torn fiber.
4. The tear separates real sheets. It does not cross a person's body.
5. The four posters share one material and differ by the tear event.
6. No added words.

## Read the photograph

Write this down before choosing events. Do not show it to the user.

- Hero: the one thing the photograph is about.
- Two relationships that survive in every poster, such as "person in front of the flowering tree" or "wheel behind the roof".
- Three to five sheets already in the picture: sky, foliage, building, water, person, boat.
- Five to eight colors, named from the photograph, not from a palette.
- Aspect: the photograph's own orientation after EXIF. Use the nearest of `16:9`, `9:16`, `4:3`, `3:4`, `1:1`. Do not convert a landscape into a tall poster.
- Lettering: only words that are large and certainly readable. Otherwise none.
- People: if a person is the hero, mark the portrait rule on all four.

## Choose the four tears

Pick four events from `references/tear-events.md` that this photograph can support. Write one physical sentence for each: which sheet tears, what it separates, what it must not cross.

Reject a set where two posters tear the same sheet in the same place. Reject a set that changes the palette or the scale instead of the tear.

For a person, the only allowed events are whole sheet, window, stop, and sides.

## Generate

Pass the photograph as a semantic reference. Build each prompt from `references/prompt.md`. One prompt, one tear event.

Generate all four before judging them. Then look at each image.

Regenerate an image before showing it if any of these are true:

- photographic texture or a pasted face remains
- the hero has shrunk into an icon, a sticker, or a black logo
- the scene has been repainted beige, brown, or a single accent
- a tear crosses a face, neck, hair, hat, glasses, shirt, arm, hand, or strap
- a background tear only frames the person and the tree together, with no gap between them
- invented text, an extra person, or a watermark appears
- the tear is a smooth oval, a repeating zigzag, or a white sticker outline

Replace only the failed image. Keep the ones that pass. Do not stop at two.

If a generation fails, say which of the four failed and show the ones that exist.

## Save

When the conversation is inside a project that keeps outputs, scale each accepted image so the long side is 3840 pixels, keep the aspect ratio, and write:

`output/<scene>-tear-<event>-4k.jpg`

Use a short scene name and the event name: `whole`, `window`, `stop`, `sides`, `stack`, `waterline`, `through`, `sky`, `frame`.

Do not save or commit the user's source photograph unless they ask.

## Tell the user

Show every finished image. Under each one:

- 设计灵感: the physical idea, one sentence
- 设计语言: which sheet tears
- 设计思路: what stayed intact, and what the tear separates

Name the hero and the two relationships that stayed. Do not describe a poster that was rejected.

## Single image

If the user asks to redo one poster, change only the tear they named. Keep the same scale, colors, and hero. Return that one image with the same three lines.
