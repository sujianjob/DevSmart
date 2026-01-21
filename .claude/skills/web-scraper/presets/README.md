# Web Scraper 预设配置

预设配置是针对特定网站类型优化的配置文件，可以快速启动爬取任务。

---

## 使用方式

### 自动检测

```bash
agent-browser open https://open.oceanengine.com/doc
# -> "检测到预设 'oceanengine'，是否使用？"
```

### 手动指定

```
使用 oceanengine 预设爬取 https://open.oceanengine.com/doc
```

### 保存新预设

```
将当前配置保存为 my-site 预设
```

---

## 可用预设

| 预设名称 | 文件 | 适用网站 |
|---------|------|---------|
| `oceanengine` | oceanengine.yaml | 巨量引擎开放平台 |
| `wechat-open` | wechat-open.yaml | 微信开放平台 |
| `generic-docs` | generic-docs.yaml | 通用文档站点 |

---

## 预设文件格式

```yaml
name: 预设名称
url_pattern: "example.com"  # URL 匹配模式
site_type: spa | static     # 网站类型

navigation:
  type: nested_sidebar | top_nav | tabs
  expand_method: click | hover
  expand_wait: 1000          # 展开等待时间(ms)

content:
  main_selector: ".doc-content"
  title_selector: "h1"
  exclude:                   # 排除的元素
    - ".sidebar"
    - ".header"

timing:
  page_load: 3000           # 页面加载等待(ms)
  menu_expand: 1000         # 菜单展开等待(ms)
  content_render: 2000      # 内容渲染等待(ms)

output:
  structure: mirror_navigation | flat
  filename_from: title | url
```

---

## 自动检测逻辑

1. 获取当前 URL 的域名
2. 遍历所有预设文件
3. 匹配 `url_pattern` 字段
4. 找到匹配则提示使用

```python
# 伪代码
def detect_preset(url):
    domain = extract_domain(url)
    for preset in load_presets():
        if preset.url_pattern in domain:
            return preset
    return None
```

---

## 创建自定义预设

1. 复制 `generic-docs.yaml` 作为模板
2. 修改 `name` 和 `url_pattern`
3. 根据网站特点调整配置
4. 保存到 `presets/` 目录

### 示例：为新网站创建预设

```yaml
# presets/my-docs.yaml
name: 我的文档网站
url_pattern: "docs.mysite.com"
site_type: spa

navigation:
  type: nested_sidebar
  expand_method: click
  expand_wait: 800

content:
  main_selector: ".content-main"
  title_selector: ".page-title"
  exclude:
    - ".nav-sidebar"
    - ".page-footer"

timing:
  page_load: 2000
  menu_expand: 800
  content_render: 1500

output:
  structure: mirror_navigation
  filename_from: title
```
