# 安装一次，之后只发照片

由 **佳成的挑战日记** 维护。目标体验：启用撕纸工作流 → 发照片 → 收到四张独立撕纸画。构图、比例、颜色、撕口和生图提示词由技能决定。

以下安装包不含模型、不需要管理员权限，也不会自动配置外部 API。生图能力和额度来自所用平台。安装完成与实际出图是两项检查，验证状态见 [TESTING.md](TESTING.md)。

## Cursor：专用工作室

1. 下载 [photo-studio.zip](https://github.com/zhu135531-hue/photo-to-torn-paper/releases/latest/download/photo-studio.zip)，解压。
2. 用 Cursor 打开里面的 **photo-studio** 文件夹，选择本地 Agent。
3. 新建对话，只上传照片并发送。无需打字、斜杠命令或选择撕口。

工作室内已经放好技能及始终生效的项目规则，不用手工复制隐藏文件。后续照片仍直接发；离开这个项目恢复普通工作。若界面要求输入文字才允许发送，可输入一个“做”作为兼容操作，并向我们反馈客户端版本；这类情况不算严格的零文字验收通过。

本次 Cursor 已用仅含图片的消息自动生成并保存四张真实文件。当前限制：输出 4:3，未完整保持原照片约 3:2；会话逐图预览的呈现仍需复测。可先打开 output/ 下的成品文件查看。详见测试记录。

已有项目也可通过 Cursor 的 Customize → From GitHub Repository 导入本仓库，再安装 **jiacheng-torn-paper** 插件，建议选择项目范围。仓库已提供官方格式的 `.cursor-plugin/marketplace.json` 和插件清单；这不表示已通过官方市场审核。若此入口不在你的版本中，使用工作室包。

## TRAE / TraeWork：上传技能包

1. 下载 [torn-paper-trae.zip](https://github.com/zhu135531-hue/photo-to-torn-paper/releases/latest/download/torn-paper-trae.zip)。
2. 在技能管理中上传 ZIP 并启用。TraeWork 的入口为“插件市场 → 技能 → 上传技能”。
3. 新建任务，只上传照片并发送。不用打字或手动选择撕口。

包内 **SKILL.md 位于 ZIP 根目录**，视觉规范已合并到单文件，避免导入只保留指令而丢失参考文档。也可以用 TRAE 打开上面的 **photo-studio** 文件夹，里面同时包含 `.trae/skills` 和 `.trae/rules`，让新会话也加载照片触发规则。

TraeWork CN 已按上述路径实测：默认本地新任务只发照片，自动调用 torn-paper，生成并保存四张 2400×1600 JPEG；点击文件卡片可预览。部分撕边、色调仍有偏差，四张同时内嵌预览未验证，详见 [TESTING.md](TESTING.md)。这是当前账号与环境的结果；其他 TRAE 版本和账号仍需确认实际开放参考图生图工具。

## WorkBuddy：先启用技能，再验证照片入口

下载 [torn-paper-portable.zip](https://github.com/zhu135531-hue/photo-to-torn-paper/releases/latest/download/torn-paper-portable.zip)，在“专家·技能·连接器 → 技能 → 添加技能 → 上传技能”导入，按客户端安全检测结果处理，再在“已安装技能”中确认 torn-paper 已启用。便携包包含自足的技能正文和 WorkBuddy 展示字段，不依赖脚本、密钥或额外参考文件。

专用专家的配置内容已备好：[workbuddy-expert.txt](integrations/workbuddy-expert.txt)。创建一次“佳成的挑战日记·撕纸”专家并绑定已安装的 torn-paper，之后进入该专家会话只发照片。作者完成客户端实测和分享后，用户才可以进一步简化为“点分享链接 → 发照片”。目前没有可验证的专家分享链接，也没有上架市场，不能通过搜索名称保证安装到本项目。

官方的“对话查找安装”面向市场技能，不能把任意 GitHub URL 当作已支持的安装指令。本机 WorkBuddy v5.8.3 已确认安装并启用 torn-paper；照片自动匹配、真实出图和专家绑定仍待实测，当前不能承诺只发照片就一定出图。

## 豆包：专用会话 / 智能体入口

普通豆包聊天没有在本项目中验证过 GitHub Skill 安装。豆包工作开放平台已提供 Skill / Plugin 接入方向，官方首页目前标注内测；这与普通聊天入口不同。

已准备 [doubao-agent.txt](https://github.com/zhu135531-hue/photo-to-torn-paper/releases/latest/download/doubao-agent.txt)：由创建者一次性放入**支持参考图生图**的专用智能体配置；或由用户在一个专用会话中要求一次性采用。后续在该会话只发照片，规则即表达为开始转撕纸。是否实际生图、是否允许分享，必须在账号中验证。

我们希望最终分享一个“点开就能发照片”的豆包入口。当前尚未创建并验证该智能体，不能宣传成“在普通豆包里说安装就能用”。不需要用户每张照片都复制长提示词；[TRY_IT.md](TRY_IT.md) 仅作为临时手动备用。

## 验收方式

在新会话提交一张照片，不输入“撕纸”、不粘贴提示词：应自动读取规则、引用该照片调用真实生图工具、展示四张独立图片。再发另一张照片，不能混入上一张场景。截图识字、排错或其他明确请求应按该请求处理。

若只输出描述、要求用户去别处粘贴提示词、伪造结果链接，或生成四宫格，都不算跑通。缺失工具、额度或登录要如实报告。

## 官方依据

- [Cursor 插件与安装](https://cursor.com/docs/plugins)、[插件清单和规则格式](https://cursor.com/docs/reference/plugins)、[技能与持续模式](https://cursor.com/docs/skills)
- [TRAE 技能](https://docs.trae.cn/ide_skills)、[TraeWork ZIP 入口与结构](https://docs.trae.cn/work_skills)、[项目规则](https://docs.trae.cn/ide_rules)
- [WorkBuddy 技能包格式](https://open.workbuddy.cn/docs/skill)、[专家配置与分享](https://www.codebuddy.cn/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Expert-Center)
- [豆包工作开放平台](https://open.doubao.com/)

文档核对日期：2026-10-18。平台入口可能随版本和账号变化。
