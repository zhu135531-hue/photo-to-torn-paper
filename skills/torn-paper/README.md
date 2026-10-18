# 撕纸 Torn Paper

一张照片，做成四张撕纸分层海报。

整张画面都是剪纸。不留照片像素，不把地方缩成小图标，不改成一张大空白纸。颜色跟着照片走，奶油色只出现在撕口。四张共用这一套纸，只换撕口的位置。人在正中时，撕口不经过身体，只把人和后面的景物分开。

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

Claude Code 把同一文件夹拷到 `~/.claude/skills/torn-paper`。Codex 拷到 `~/.codex/skills/torn-paper`。

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

技能会按原图比例出图。横图保持横图。需要存文件时，长边做成 3840 像素，放在 `output/`。

## 技能里有什么

| 文件 | 作用 |
| --- | --- |
| `SKILL.md` | 代理要遵守的步骤 |
| `references/visual-system.md` | 纸、颜色、大小、撕口 |
| `references/tear-events.md` | 九种撕口，每次从里面选四种 |
| `references/prompt.md` | 给图像模型的提示骨架 |

## 许可

本技能使用 MIT 许可，见 `LICENSE`。
