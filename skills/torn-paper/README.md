# 撕纸 Torn Paper

一张照片，做成四张撕纸分层海报。

整张画面都是剪纸。不留照片像素，不把地方缩成小图标，不改成一张大空白纸。颜色跟着照片走，新增暖白纤维只出现在窄撕口，原图本来浅色的物体保留原色。四张共用构图和材质，主要改变撕口位置。人在正中时，撕口不经过身体，只把人和后面的景物分开。多张照片分别处理，默认两张照片给八张独立成品。

This folder is a standalone skill. It does not include, modify, or relicense any other paper-poster skill.

## 安装

Cursor，当前项目：

```bash
mkdir -p .cursor/skills
cp -R skills/torn-paper .cursor/skills/torn-paper
```

Cursor，所有项目：

```bash
mkdir -p ~/.cursor/skills
cp -R path/to/torn-paper ~/.cursor/skills/torn-paper
```

Claude Code 把同一文件夹拷到 `~/.claude/skills/torn-paper`。

Codex 当前官方的项目级目录是 `.agents/skills/torn-paper`，用户级目录是 `~/.agents/skills/torn-paper`，详见[官方技能文档](https://learn.chatgpt.com/docs/build-skills)。把完整文件夹复制过去，包括 `references/` 和 `scripts/`，不要只复制 `SKILL.md`。本次实测是显式读取仓库内的技能，并未验证新会话中的自动发现。

也可以在 Codex 中直接测试仓库副本，不必全局安装：

```text
请读取当前项目 skills/torn-paper/SKILL.md 及其引用文档，
使用可用的内置图片生成工具，把附件照片做成四种独立撕纸图片，
检查成品并保存到当前项目 output/ 的新运行目录。
```

前提是所用 Codex 环境实际提供图片生成工具。本技能不包含模型、API 客户端或 API 密钥，不会使纯文本环境自动具备生图能力。执行和失败恢复见 [Codex 运行说明](references/codex.md)。

装好后新开一轮对话，让技能描述被读到。

## 怎么用

上传一张照片，说：

```text
做成四种撕纸
```

也可以指定一张：

```text
只做一张，撕口沿着天际线，倒影留在下面那张纸上
```

人像可以说：

```text
撕口不要经过身体，把人和后面的树分开
```

技能按原图比例出图，包括横向 3:2 和竖向 3:4。默认保留工具返回的原生尺寸和格式，存入 `output/<run-id>/`，不覆盖先前版本。需要 4K 等尺寸时请明确提出，并区分原生生成尺寸与后期导出尺寸。

## 技能里有什么

- `SKILL.md`：代理要遵守的步骤。
- `references/visual-system.md`：纸、颜色、大小、撕口。
- `references/tear-events.md`：九种撕口，每次选四种。
- `references/prompt.md`：给图像模型的提示骨架。
- `references/codex.md`：Codex 执行、检查、重试和保存。
- `scripts/collect_outputs.py`：可选文件检查和复制工具，依赖 Pillow；不负责生图，不修改像素。

## 许可

本技能使用 MIT 许可，见 `LICENSE`。
