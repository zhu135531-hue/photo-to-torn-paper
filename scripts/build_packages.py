"""Build offline distributions from one maintained skill; no downloads or installation."""
import argparse
import hashlib
import json
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parent.parent
VERSION = '0.2.0'
SKILL = ROOT / 'skills/torn-paper'
REPO = 'https://github.com/zhu135531-hue/photo-to-torn-paper'


def skill_files():
    names = ['SKILL.md', 'README.md', 'LICENSE', 'agents/openai.yaml',
             'scripts/collect_outputs.py', 'scripts/requirements.txt']
    names += ['references/'+name for name in ('visual-system.md', 'tear-events.md',
              'prompt.md', 'hosts.md', 'codex.md')]
    result = {}
    for name in names:
        path = SKILL/name
        if path.is_symlink() or not path.resolve().is_relative_to(SKILL.resolve()):
            raise ValueError('Skill files must stay inside the source skill')
        result[name] = path.read_bytes()
    return result


def standalone():
    """Inline style references for hosts whose import UI retains only SKILL.md."""
    text = (SKILL / 'SKILL.md').read_text(encoding='utf-8')
    text = text.replace('Read `references/hosts.md` to select the current host\'s execution route.',
                        'Use the host execution routes included below.')
    start = text.index('## Read before generating')
    end = text.index('## What comes back', start)
    text = text[:start] + '## Execution\n\nThe visual and execution references are included below; no extra files or dependency installation are needed. Use the current host\'s real reference-image generation tool.\n\n' + text[end:]
    text = text.replace('from `references/tear-events.md`', 'from the Tear events section below')
    text = text.replace('from `references/prompt.md`', 'from the Prompt section below')
    text = text.replace('Read `references/codex.md` for the optional verification/copy helper.',
                        'The optional local collector is omitted from this portable package.')
    for filename, title in [('visual-system.md', 'Visual system'), ('tear-events.md', 'Tear events'),
                            ('prompt.md', 'Prompt'), ('hosts.md', 'Host execution routes')]:
        text += '\n\n# ' + title + '\n\n' + (SKILL/'references'/filename).read_text(encoding='utf-8')
    return text


def write_zip(destination, entries):
    with zipfile.ZipFile(destination, 'x', zipfile.ZIP_DEFLATED) as archive:
        for name, data in sorted(entries.items()):
            path = Path(name)
            if path.is_absolute() or '..' in path.parts or '\\' in name:
                raise ValueError('Unsafe archive entry')
            info = zipfile.ZipInfo(name, (2026, 10, 18, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, data)
    with zipfile.ZipFile(destination) as archive:
        if archive.testzip() is not None:
            raise RuntimeError('Archive failed CRC verification')


def build(destination):
    destination = Path(destination)
    destination.mkdir(parents=True, exist_ok=True)
    names = ['torn-paper.zip', 'torn-paper-portable.zip', 'torn-paper-trae.zip', 'photo-studio.zip',
             'cursor-plugin.zip', 'doubao-agent.txt', 'SHA256SUMS.txt']
    if any((destination/n).exists() for n in names):
        raise FileExistsError('Use a new output directory; existing releases are never overwritten')
    files = skill_files()
    source = ('Photo to Torn Paper v' + VERSION + '\n佳成的挑战日记\n' + REPO +
              '\nSkill and instructions: MIT. Requires a host image tool. No keys or model weights.\n').encode()
    files['SOURCE.txt'] = source
    write_zip(destination/'torn-paper.zip', {'torn-paper/'+n: b for n,b in files.items()})
    portable = standalone()
    # WorkBuddy market metadata is added only to its portable distribution, keeping the
    # canonical Agent Skills frontmatter compatible with stricter hosts.
    portable = portable.replace('metadata:\n',
        'version: "0.2.0"\nauthor: "佳成的挑战日记"\ndescription_zh: "只发照片，自动做成四种独立撕纸画"\ndescription_en: "Convert photo-only uploads into four separate torn-paper artworks."\nmetadata:\n', 1)
    write_zip(destination/'torn-paper-portable.zip', {
        'torn-paper/SKILL.md': portable.encode(), 'torn-paper/LICENSE': files['LICENSE'],
        'torn-paper/SOURCE.txt': source})
    # TraeWork explicitly requires SKILL.md at the archive root.
    write_zip(destination/'torn-paper-trae.zip', {
        'SKILL.md': standalone().encode(), 'LICENSE': files['LICENSE'], 'SOURCE.txt': source})
    rule = (ROOT/'rules/photo-only.mdc').read_text(encoding='utf-8')
    studio = {'photo-studio/START_HERE.md': (
        '# 佳成的挑战日记 · 撕纸工作室\n\n用 Cursor 或 TRAE 打开此文件夹。'
        '选择本地 Agent，新建对话，只上传照片并发送。默认生成四张独立撕纸画。'
        '无需输入提示词。所用环境必须提供参考图生图工具。\n\n'
        '规则仅作用于此工作室；离开该项目恢复普通使用。照片和成品不要提交到公开仓库。\n\n'
        'TRAE 和 WorkBuddy 尚需客户端实测；不是所有环境都具备生图能力。\n' + REPO + '\n').encode(),
        'photo-studio/.gitignore': b'output/\ninput/\n*.jpg\n*.jpeg\n*.png\n*.webp\n.env*\n',
        'photo-studio/.cursor/rules/photo-only.mdc': rule.replace('skills/torn-paper/SKILL.md', '.cursor/skills/torn-paper/SKILL.md').encode(),
        'photo-studio/.trae/rules/photo-only.md': rule.replace('skills/torn-paper/SKILL.md', '.trae/skills/torn-paper/SKILL.md').encode()}
    for host in ('.cursor', '.trae'):
        studio.update({'photo-studio/'+host+'/skills/torn-paper/'+n:b for n,b in files.items()})
    write_zip(destination/'photo-studio.zip', studio)
    plugin = {n:(ROOT/n).read_bytes() for n in ('.cursor-plugin/plugin.json', '.cursor-plugin/marketplace.json', 'rules/photo-only.mdc', 'LICENSE')}
    plugin.update({'skills/torn-paper/'+n:b for n,b in files.items()})
    write_zip(destination/'cursor-plugin.zip', {'jiacheng-torn-paper/'+n:b for n,b in plugin.items()})
    doubao = ('佳成的挑战日记 · 照片转撕纸：专用智能体配置\n\n'
        '将下列内容作为支持参考图生图的专用智能体指令；或由用户在专用对话中主动要求一次性采用。'
        '此文件不是豆包普通聊天的自动安装程序，不包含分享链接。\n\n'
        '用户只发照片时立即使用该照片生成四张独立成品。自行补齐提示词，不追问想做什么。'
        '无照片时只说“发一张照片，我来做成四种撕纸画。”若当前智能体不具备真实生图能力，明确说明。\n\n' + standalone())
    (destination/'doubao-agent.txt').write_text(doubao, encoding='utf-8')
    sums = [hashlib.sha256((destination/n).read_bytes()).hexdigest()+'  '+n for n in names[:-1]]
    (destination/'SHA256SUMS.txt').write_text('\n'.join(sums)+'\n', encoding='utf-8')
    return {n: (destination/n).stat().st_size for n in names}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=ROOT/'dist'/('v'+VERSION))
    print(json.dumps(build(parser.parse_args().output), ensure_ascii=False))
