# DevSmart 分角色详解流程图

为展示更深度的业务逻辑，以下将核心流程拆解为三个独立的泳道：**需求分析**、**原型设计**、**测试生成**。

## 1. 需求分析流 (The PM Workflow)
**目标**：将"一句话需求"转化为"无歧义的结构化 PRD"。

```mermaid
flowchart TD
    %% 角色样式
    classDef user fill:#e1f5fe,stroke:#01579b,stroke-width:2px;
    classDef agent fill:#f3e5f5,stroke:#4a148c,stroke-width:2px;
    classDef doc fill:#fff9c4,stroke:#fbc02d,stroke-dasharray:5,5;
    classDef white fill:#ffffff,stroke:#757575,stroke-width:1px;
    
    User(["👤 用户/业务方"]):::user
    PMAgent("📝 PM Agent"):::agent
    
    User -- "1. 输入模糊需求<br/>(如：要做个积分商城)" --> PMAgent
    
    subgraph Analysis_Loop [澄清闭环]
        direction TB
        PMAgent -->|分析缺失信息| Question["❓ 生成追问清单<br/>(规则/边界/权限)"]:::white
        Question --> User
        User -->|回答| Answer["✅ 补充信息"]:::white
        Answer --> PMAgent
    end
    
    PMAgent -->|信息完备?| Check{"是否足够?"}
    Check --"No (继续追问)"--> Question
    
    Check --"Yes"--> Draft["📄 生成 PRD 初稿<br/>(User Stories + AC)"]:::doc
    Draft --> Review{"👤 人工评审"}:::user
    
    Review --"修改意见"--> PMAgent
    Review --"批准"--> FinalPRD["✅ 锁定 PRD"]:::doc
```

---

## 2. 原型设计流 (The Prototype Workflow)
**目标**：将文字 PRD 转化为可视化原型，消除"想象力偏差"。

```mermaid
flowchart TD
    classDef agent fill:#e0f2f1,stroke:#00695c,stroke-width:2px;
    classDef asset fill:#ffe0b2,stroke:#e65100,stroke-dasharray:5,5;
    
    InputPRD["📄 锁定 PRD"] --> UXAgent("🎨 Prototype Agent"):::agent
    
    subgraph Gen_Process [生成流水线]
        UXAgent -->|1. 提取页面结构| PageTree["页面层级树"]:::white
        UXAgent -->|2. 识别组件需求| CompLib[("📚 组件库匹配")]:::white
        
        PageTree & CompLib --> Layout["📐 布局生成"]
        Layout --> Render["🖼️ 渲染低保真原型"]
    end
    
    Render --> Preview["📱 在线预览链接"]:::asset
    Preview --> UserFeedback{"👤 用户试用反馈"}
    
    UserFeedback --"布局不合理"--> UXAgent
    UserFeedback --"确认"--> FinalDesign["✅ UI 规格说明书<br/>(Figma/HTML)"]:::asset
```

---

## 3. 测试设计流 (The QA Workflow)
**目标**：在写代码之前，先把"怎么测"定好 (TDD 思想)。

```mermaid
flowchart TD
    classDef agent fill:#fce4ec,stroke:#880e4f,stroke-width:2px;
    classDef case fill:#e8eaf6,stroke:#1a237e,stroke-dasharray:5,5;
    
    PRD["📄 锁定 PRD"] & Proto["✅ UI 规格"] --> QAAgent("🧪 QA Agent"):::agent
    
    subgraph Design_Logic [用例设计逻辑]
        QAAgent -->|分析| HappyPath["🟢 快乐路径 (Main Flow)"]
        QAAgent -->|分析| EdgeCase["🔴 异常边界 (Edge Cases)"]
        QAAgent -->|分析| Security["🛡️ 安全场景 (权限/注入)"]
    end
    
    HappyPath & EdgeCase & Security --> Gherkin["提取 Gherkin 剧本<br/>(Given/When/Then)"]
    
    Gherkin --> CaseGen["📊 生成测试矩阵 (Excel/XMind)"]:::case
    
    CaseGen --> CaseReview{"👤 测试评审"}
    CaseReview --"补充场景"--> QAAgent
    CaseReview --"批准"--> FinalTest["✅ 标准验收用例集"]:::case
```
