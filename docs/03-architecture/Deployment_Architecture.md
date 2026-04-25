# DevSmart 部署架构

本文档详细描述 DevSmart 平台的部署架构设计，包括 Kubernetes 拓扑、服务组件、高可用设计和环境配置。

---

## 1. 部署架构总览图

```mermaid
graph TB
    subgraph Internet["互联网"]
        Users["用户"]
        Developers["开发者"]
    end

    subgraph CDN["CDN 层"]
        CloudFlare["CloudFlare / AWS CloudFront"]
    end

    subgraph LoadBalancer["负载均衡层"]
        ALB["AWS ALB / NLB"]
    end

    subgraph K8s["Kubernetes 集群"]
        subgraph Ingress["入口层"]
            Traefik["Traefik Ingress"]
        end

        subgraph Frontend["前端服��"]
            WebApp["Web App<br/>3 replicas"]
        end

        subgraph Backend["后端服务"]
            API["API Service<br/>3 replicas"]
            WS["WebSocket Service<br/>2 replicas"]
            Worker["Background Worker<br/>2 replicas"]
        end

        subgraph Agent["Agent 服务"]
            Supervisor["Supervisor Agent<br/>2 replicas"]
            PMAgent["PM Agent<br/>2 replicas"]
            CoderAgent["Coder Agent<br/>2 replicas"]
            QAAgent["QA Agent<br/>1 replica"]
        end
    end

    subgraph Data["数据层"]
        PG[(PostgreSQL<br/>Primary + Replica)]
        Redis[(Redis<br/>Cluster)]
        Milvus[(Milvus<br/>向量库)]
        Neo4j[(Neo4j<br/>图数据库)]
        S3[(S3 / MinIO<br/>对象存储)]
    end

    subgraph External["外部服务"]
        OpenAI["OpenAI API"]
        GitHub["GitHub API"]
        Jira["Jira API"]
    end

    Users --> CDN
    Developers --> CDN
    CDN --> ALB
    ALB --> Ingress
    Ingress --> Frontend
    Ingress --> Backend
    Backend --> Agent
    Backend --> Data
    Agent --> Data
    Agent --> External
```

---

## 2. Kubernetes 部署拓扑

### 2.1 命名空间规划

| 命名空间 | 用途 | 资源配额 |
|:---|:---|:---|
| `devsmart-prod` | 生产环境应用 | CPU: 16核, 内存: 32Gi |
| `devsmart-staging` | 测试环境应用 | CPU: 8核, 内存: 16Gi |
| `devsmart-agents` | Agent 服务专用 | CPU: 8核, 内存: 24Gi |
| `devsmart-data` | 数据库服务 | CPU: 8核, 内存: 32Gi |
| `monitoring` | 监控服务 | CPU: 4核, 内存: 8Gi |
| `ingress-system` | 入口控制器 | CPU: 2核, 内存: 4Gi |

### 2.2 命名空间架构图

```mermaid
graph LR
    subgraph Cluster["Kubernetes 集群"]
        subgraph NS1["devsmart-prod"]
            API1["api-deployment"]
            Web1["web-deployment"]
            Worker1["worker-deployment"]
        end

        subgraph NS2["devsmart-agents"]
            Sup["supervisor-deployment"]
            PM["pm-agent-deployment"]
            Coder["coder-agent-deployment"]
            QA["qa-agent-deployment"]
        end

        subgraph NS3["devsmart-data"]
            PG["postgresql-statefulset"]
            Redis["redis-statefulset"]
            Milvus["milvus-statefulset"]
        end

        subgraph NS4["monitoring"]
            Prom["prometheus"]
            Graf["grafana"]
            Loki["loki"]
        end
    end

    NS1 --> NS2
    NS1 --> NS3
    NS2 --> NS3
    NS4 -.-> NS1
    NS4 -.-> NS2
    NS4 -.-> NS3
```

### 2.3 Pod 分布策略

```yaml
# 反亲和性配置示例
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api-deployment
spec:
  replicas: 3
  template:
    spec:
      affinity:
        podAntiAffinity:
          preferredDuringSchedulingIgnoredDuringExecution:
            - weight: 100
              podAffinityTerm:
                labelSelector:
                  matchLabels:
                    app: api
                topologyKey: kubernetes.io/hostname
      topologySpreadConstraints:
        - maxSkew: 1
          topologyKey: topology.kubernetes.io/zone
          whenUnsatisfiable: ScheduleAnyway
          labelSelector:
            matchLabels:
              app: api
```

### 2.4 Service 配置

| Service 名称 | 类型 | 端口 | 目标 |
|:---|:---|:---|:---|
| `api-service` | ClusterIP | 8000 | API Pods |
| `web-service` | ClusterIP | 3000 | Web Pods |
| `ws-service` | ClusterIP | 8001 | WebSocket Pods |
| `supervisor-service` | ClusterIP | 8010 | Supervisor Pods |
| `postgresql` | ClusterIP | 5432 | PostgreSQL |
| `redis` | ClusterIP | 6379 | Redis |

### 2.5 Ingress 配置

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: devsmart-ingress
  annotations:
    traefik.ingress.kubernetes.io/router.middlewares:
      devsmart-prod-rate-limit@kubernetescrd,
      devsmart-prod-cors@kubernetescrd
spec:
  ingressClassName: traefik
  tls:
    - hosts:
        - app.devsmart.io
        - api.devsmart.io
      secretName: devsmart-tls
  rules:
    - host: app.devsmart.io
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: web-service
                port:
                  number: 3000
    - host: api.devsmart.io
      http:
        paths:
          - path: /api
            pathType: Prefix
            backend:
              service:
                name: api-service
                port:
                  number: 8000
          - path: /ws
            pathType: Prefix
            backend:
              service:
                name: ws-service
                port:
                  number: 8001
```

---

## 3. 服务组件图

### 3.1 前端服务

```mermaid
graph LR
    subgraph Frontend["前端服务"]
        Nginx["Nginx<br/>静态文件服务"]
        React["React SPA<br/>构建产物"]
    end

    CDN["CDN"] --> Nginx
    Nginx --> React

    subgraph Config["配置"]
        EnvJS["env.js<br/>运行时配置"]
    end

    React --> EnvJS
```

**部署配置**:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-deployment
spec:
  replicas: 3
  template:
    spec:
      containers:
        - name: web
          image: devsmart/web:latest
          ports:
            - containerPort: 3000
          resources:
            requests:
              cpu: 100m
              memory: 128Mi
            limits:
              cpu: 500m
              memory: 512Mi
          livenessProbe:
            httpGet:
              path: /health
              port: 3000
            initialDelaySeconds: 10
            periodSeconds: 10
          readinessProbe:
            httpGet:
              path: /ready
              port: 3000
            initialDelaySeconds: 5
            periodSeconds: 5
```

### 3.2 API 网关

```mermaid
graph TB
    subgraph Gateway["API 网关层"]
        Traefik["Traefik"]

        subgraph Middleware["中间件"]
            RateLimit["速率限制"]
            CORS["CORS"]
            Auth["JWT 验证"]
            Compress["压缩"]
        end
    end

    Request["请求"] --> Traefik
    Traefik --> RateLimit
    RateLimit --> CORS
    CORS --> Auth
    Auth --> Compress
    Compress --> Backend["后端服务"]
```

**中间件配置**:
```yaml
# 速率限制
apiVersion: traefik.io/v1alpha1
kind: Middleware
metadata:
  name: rate-limit
spec:
  rateLimit:
    average: 100
    burst: 200
    period: 1m

# CORS
apiVersion: traefik.io/v1alpha1
kind: Middleware
metadata:
  name: cors
spec:
  headers:
    accessControlAllowMethods:
      - GET
      - POST
      - PUT
      - DELETE
      - OPTIONS
    accessControlAllowOriginList:
      - https://app.devsmart.io
    accessControlAllowHeaders:
      - Authorization
      - Content-Type
    accessControlMaxAge: 86400
```

### 3.3 后端微服务

```mermaid
graph TB
    subgraph Backend["后端服务"]
        API["API Service<br/>业务接口"]
        WS["WebSocket Service<br/>实时通信"]
        Worker["Worker Service<br/>后台任务"]
    end

    subgraph Internal["内部通信"]
        Redis["Redis Pub/Sub"]
        Queue["任务队列"]
    end

    API --> Redis
    WS --> Redis
    Worker --> Queue
    API --> Queue
```

### 3.4 Agent 服务

```mermaid
graph TB
    subgraph AgentCluster["Agent 服务集群"]
        subgraph Coordinator["协调层"]
            Supervisor["Supervisor Agent<br/>任务路由与编排"]
        end

        subgraph Executors["执行层"]
            PM["PM Agent"]
            Coder["Coder Agent"]
            QA["QA Agent"]
            Designer["Designer Agent"]
        end
    end

    subgraph SharedState["共享状态"]
        Redis["Redis<br/>状态存储"]
        Checkpoint["Checkpoint<br/>检查点存储"]
    end

    Supervisor --> PM
    Supervisor --> Coder
    Supervisor --> QA
    Supervisor --> Designer

    PM --> SharedState
    Coder --> SharedState
    QA --> SharedState
    Designer --> SharedState
```

### 3.5 数据库集群

```mermaid
graph TB
    subgraph PostgreSQL["PostgreSQL 集群"]
        Primary["Primary<br/>读写"]
        Replica1["Replica 1<br/>只读"]
        Replica2["Replica 2<br/>只读"]
    end

    subgraph Redis["Redis 集群"]
        Master1["Master 1"]
        Master2["Master 2"]
        Master3["Master 3"]
        Slave1["Slave 1"]
        Slave2["Slave 2"]
        Slave3["Slave 3"]
    end

    Primary --> Replica1
    Primary --> Replica2

    Master1 --> Slave1
    Master2 --> Slave2
    Master3 --> Slave3
```

---

## 4. 高可用设计

### 4.1 多副本部署

| 服务 | 最小副本数 | 推荐副本数 | 最大副本数 | HPA 触发条件 |
|:---|:---|:---|:---|:---|
| Web | 2 | 3 | 10 | CPU > 70% |
| API | 2 | 3 | 15 | CPU > 60% |
| WebSocket | 2 | 2 | 6 | 连接数 > 1000 |
| Worker | 1 | 2 | 8 | 队列长度 > 100 |
| Supervisor | 2 | 2 | 4 | CPU > 70% |
| PM Agent | 1 | 2 | 6 | 任务队列 > 10 |
| Coder Agent | 1 | 2 | 6 | 任务队列 > 10 |

### 4.2 负载均衡策略

```mermaid
graph TB
    subgraph LB["负载均衡"]
        ALB["AWS ALB"]

        subgraph Strategy["策略"]
            RR["轮询 (Round Robin)"]
            LC["最少连接 (Least Connections)"]
            IP["IP 哈希 (IP Hash)"]
        end
    end

    ALB --> RR
    RR --> API["API 服务"]

    ALB --> LC
    LC --> WS["WebSocket 服务"]

    ALB --> IP
    IP --> Sticky["会话保持服务"]
```

**配置说明**:
- **API 服务**: 使用轮询策略，均匀分配请求
- **WebSocket 服务**: 使用最少连接，优化长连接分配
- **会话敏感服务**: 使用 IP 哈希保持会话亲和性

### 4.3 故障转移机制

```mermaid
sequenceDiagram
    participant Client
    participant LB as 负载均衡
    participant Pod1 as Pod 1
    participant Pod2 as Pod 2
    participant K8s as Kubernetes

    Note over Pod1: Pod 1 故障
    Client->>LB: 请求
    LB->>Pod1: 转发
    Pod1--xLB: 超时/错误
    LB->>Pod2: 重试转发
    Pod2-->>Client: 响应

    K8s->>K8s: 检测 Pod 1 不健康
    K8s->>K8s: 重启 Pod 1
    Note over Pod1: Pod 1 恢复
```

### 4.4 数据备份策略

| 数据类型 | 备份频率 | 保留周期 | 存储位置 | 恢复 RTO |
|:---|:---|:---|:---|:---|
| PostgreSQL 全量 | 每日 | 30 天 | S3 跨区域 | < 4 小时 |
| PostgreSQL WAL | 实时 | 7 天 | S3 | < 15 分钟 |
| Redis RDB | 每小时 | 7 天 | S3 | < 30 分钟 |
| 向量数据库 | 每日 | 14 天 | S3 | < 2 小时 |
| 配置文件 | 每次变更 | 永久 | Git | 即时 |

---

## 5. 环境配置

### 5.1 开发环境 (Dev)

```mermaid
graph TB
    subgraph DevEnv["开发环境"]
        subgraph Local["本地"]
            Docker["Docker Compose"]
            VSCode["VS Code"]
        end

        subgraph Services["本地服务"]
            PG["PostgreSQL"]
            Redis["Redis"]
            Chroma["Chroma"]
        end

        subgraph Mock["Mock 服务"]
            MockLLM["Mock LLM"]
            MockGitHub["Mock GitHub"]
        end
    end

    Docker --> Services
    Docker --> Mock
```

**Docker Compose 配置**:
```yaml
# docker-compose.dev.yml
version: '3.8'
services:
  postgres:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: devsmart_dev
      POSTGRES_USER: dev
      POSTGRES_PASSWORD: dev
    ports:
      - "5432:5432"
    volumes:
      - pg_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

  chroma:
    image: chromadb/chroma:latest
    ports:
      - "8000:8000"
    volumes:
      - chroma_data:/chroma/chroma

  api:
    build:
      context: ./backend
      dockerfile: Dockerfile.dev
    volumes:
      - ./backend:/app
    environment:
      - DATABASE_URL=postgresql://dev:dev@postgres:5432/devsmart_dev
      - REDIS_URL=redis://redis:6379
    ports:
      - "8080:8000"
    depends_on:
      - postgres
      - redis

volumes:
  pg_data:
  chroma_data:
```

### 5.2 测试环境 (Staging)

```mermaid
graph TB
    subgraph Staging["Staging 环境"]
        subgraph K8s["Kubernetes"]
            API["API x1"]
            Web["Web x1"]
            Agent["Agents x1"]
        end

        subgraph Data["数据"]
            PG["PostgreSQL<br/>单实例"]
            Redis["Redis<br/>单实例"]
        end

        subgraph External["外部"]
            LLM["LLM API<br/>真实"]
            GitHub["GitHub<br/>测试 Org"]
        end
    end

    K8s --> Data
    K8s --> External
```

**环境变量配置**:
```yaml
# staging 环境
apiVersion: v1
kind: ConfigMap
metadata:
  name: devsmart-config
  namespace: devsmart-staging
data:
  APP_ENV: staging
  LOG_LEVEL: debug
  DATABASE_POOL_SIZE: "5"
  REDIS_POOL_SIZE: "5"
  LLM_MODEL_ROUTE: low_cost  # 通过模型路由选择低成本模型
  RATE_LIMIT_REQUESTS: "1000"
  RATE_LIMIT_PERIOD: "1m"
```

### 5.3 生产环境 (Production)

```mermaid
graph TB
    subgraph Production["生产环境"]
        subgraph K8s["Kubernetes 集群"]
            subgraph Zone1["可用区 A"]
                API1["API x2"]
                Agent1["Agents x1"]
            end
            subgraph Zone2["可用区 B"]
                API2["API x2"]
                Agent2["Agents x1"]
            end
        end

        subgraph Data["数据层"]
            PG["PostgreSQL<br/>Primary + 2 Replica"]
            Redis["Redis<br/>6 节点集群"]
            Milvus["Milvus<br/>分布式"]
        end

        subgraph Monitoring["监控"]
            Prom["Prometheus"]
            Graf["Grafana"]
            Alert["AlertManager"]
        end
    end

    K8s --> Data
    Monitoring -.-> K8s
    Monitoring -.-> Data
```

**生产环境特性**:
- 多可用区部署
- 自动扩缩容
- 完整监控告警
- 数据加密
- 审计日志

---

## 6. 网络架构

### 6.1 VPC 设计

```mermaid
graph TB
    subgraph VPC["VPC: 10.0.0.0/16"]
        subgraph Public["公有子网"]
            subgraph PubA["10.0.1.0/24 (AZ-A)"]
                NAT1["NAT Gateway"]
                ALB1["ALB"]
            end
            subgraph PubB["10.0.2.0/24 (AZ-B)"]
                NAT2["NAT Gateway"]
                ALB2["ALB"]
            end
        end

        subgraph Private["私有子网 - 应用"]
            subgraph AppA["10.0.10.0/24 (AZ-A)"]
                K8sA["K8s Workers"]
            end
            subgraph AppB["10.0.11.0/24 (AZ-B)"]
                K8sB["K8s Workers"]
            end
        end

        subgraph Data["私有子网 - 数据"]
            subgraph DataA["10.0.20.0/24 (AZ-A)"]
                RDS1["RDS Primary"]
                Redis1["Redis"]
            end
            subgraph DataB["10.0.21.0/24 (AZ-B)"]
                RDS2["RDS Replica"]
                Redis2["Redis"]
            end
        end
    end

    Internet["Internet"] --> ALB1
    Internet --> ALB2
    ALB1 --> K8sA
    ALB2 --> K8sB
    K8sA --> NAT1
    K8sB --> NAT2
    K8sA --> DataA
    K8sB --> DataB
```

### 6.2 安全组规则

| 安全组 | 入站规则 | 出站规则 |
|:---|:---|:---|
| `sg-alb` | 80/443 from 0.0.0.0/0 | All to sg-k8s |
| `sg-k8s` | All from sg-alb | All to sg-data, NAT |
| `sg-data` | 5432/6379 from sg-k8s | None |
| `sg-monitoring` | 9090/3000 from VPN | All to sg-k8s |

### 6.3 内外网隔离架构

```mermaid
graph LR
    subgraph External["外部网络"]
        Users["用户"]
        Attackers["潜在攻击"]
    end

    subgraph Edge["边缘层"]
        WAF["WAF"]
        CDN["CDN"]
        DDoS["DDoS 防护"]
    end

    subgraph DMZ["DMZ"]
        ALB["负载均衡"]
    end

    subgraph Internal["内部网络"]
        K8s["K8s 集群"]
        Data["数据库"]
    end

    Users --> Edge
    Attackers --> Edge
    Edge --> DMZ
    DMZ --> Internal

    style Attackers fill:#f66
    style WAF fill:#6f6
    style DDoS fill:#6f6
```

---

## 7. 资源配置建议

### 7.1 CPU/内存配额

| 服务 | CPU Request | CPU Limit | Memory Request | Memory Limit |
|:---|:---|:---|:---|:---|
| Web | 100m | 500m | 128Mi | 512Mi |
| API | 250m | 1000m | 512Mi | 2Gi |
| WebSocket | 100m | 500m | 256Mi | 1Gi |
| Worker | 200m | 1000m | 512Mi | 2Gi |
| Supervisor | 500m | 2000m | 1Gi | 4Gi |
| PM Agent | 250m | 1000m | 512Mi | 2Gi |
| Coder Agent | 500m | 2000m | 1Gi | 4Gi |

### 7.2 存储规划

| 存储类型 | 初始大小 | 扩展上限 | 存储类 | IOPS |
|:---|:---|:---|:---|:---|
| PostgreSQL | 100Gi | 1Ti | gp3 | 3000 |
| Redis | 20Gi | 100Gi | gp3 | 3000 |
| Milvus | 200Gi | 2Ti | gp3 | 6000 |
| Neo4j | 50Gi | 500Gi | gp3 | 3000 |
| Logs (Loki) | 100Gi | 1Ti | gp2 | - |
| Metrics (Prometheus) | 50Gi | 500Gi | gp2 | - |

### 7.3 扩缩容策略

```yaml
# HPA 配置示例
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: api-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: api-deployment
  minReplicas: 2
  maxReplicas: 15
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 60
    - type: Resource
      resource:
        name: memory
        target:
          type: Utilization
          averageUtilization: 70
  behavior:
    scaleUp:
      stabilizationWindowSeconds: 60
      policies:
        - type: Pods
          value: 2
          periodSeconds: 60
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
        - type: Pods
          value: 1
          periodSeconds: 120
```

### 7.4 成本估算 (AWS 参考)

| 资源 | 规格 | 数量 | 月成本 (USD) |
|:---|:---|:---|:---|
| EKS 集群 | - | 1 | $73 |
| EC2 (Worker) | m5.xlarge | 4 | $560 |
| RDS PostgreSQL | db.r5.large | 2 | $340 |
| ElastiCache Redis | cache.r5.large | 3 | $450 |
| ALB | - | 2 | $50 |
| S3 (备份) | 500GB | - | $12 |
| CloudWatch | - | - | $50 |
| **合计** | | | **~$1,535** |

---

## 8. 部署流程

### 8.1 人工部署与 CI 状态读取

根据仓库约束，DevSmart 不设计自动化 CI/CD 触发流程。构建、测试、发布必须由人工操作；系统可读取外部 CI 状态、测试结果和安全扫描摘要，用于生成质量建议和审计记录。

```mermaid
graph LR
    subgraph Manual["人工操作"]
        Build["人工构建镜像"]
        Test["人工运行测试"]
        Scan["人工执行安全扫描"]
        Push2["人工推送镜像"]
    end

    subgraph Observe["DevSmart 只读观察"]
        ReadCI["读取 CI 状态"]
        Summarize["生成质量摘要"]
        Audit["写入审计事件"]
    end

    subgraph DeployFlow["人工部署"]
        Deploy["人工触发滚动部署"]
        Verify["健康检查"]
    end

    Build --> Test
    Test --> Scan
    Scan --> Push2
    Push2 --> Deploy
    Deploy --> Verify
    ReadCI --> Summarize
    Summarize --> Audit
```

### 8.2 滚动更新策略

```yaml
apiVersion: apps/v1
kind: Deployment
spec:
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 25%
      maxUnavailable: 0
```

### 8.3 回滚流程

```mermaid
sequenceDiagram
    participant Dev as 开发者
    participant Ops as 运维负责人
    participant K8s as Kubernetes
    participant Mon as 监控

    Dev->>Ops: 提交回滚申请
    Ops->>K8s: 人工触发滚动更新
    K8s->>Mon: 上报指标
    Mon-->>Dev: 错误告警
    Dev->>Ops: 确认回滚
    Ops->>K8s: 恢复上一版本
    K8s-->>Dev: 回滚完成
```

---

## 9. 灾难恢复

### 9.1 RPO/RTO 目标

| 场景 | RPO | RTO | 恢复策略 |
|:---|:---|:---|:---|
| 单 Pod 故障 | 0 | < 1分钟 | K8s 自动重启 |
| 单节点故障 | 0 | < 5分钟 | Pod 重新调度 |
| 可用区故障 | 0 | < 15分钟 | 跨 AZ 故障转移 |
| 数据库故障 | < 1分钟 | < 30分钟 | 主从切换 |
| 区域级灾难 | < 15分钟 | < 4小时 | 跨区域恢复 |

### 9.2 灾难恢复流程

```mermaid
graph TB
    subgraph Detection["检测"]
        Monitor["监控系统"]
        Alert["告警触发"]
    end

    subgraph Assessment["评估"]
        Triage["问题定位"]
        Decision["决策: 恢复/切换"]
    end

    subgraph Recovery["恢复"]
        Failover["故障转移"]
        Restore["数据恢复"]
        Verify["验证服务"]
    end

    subgraph PostIncident["事后"]
        RCA["根因分析"]
        Improve["改进措施"]
    end

    Monitor --> Alert
    Alert --> Triage
    Triage --> Decision
    Decision --> Failover
    Decision --> Restore
    Failover --> Verify
    Restore --> Verify
    Verify --> RCA
    RCA --> Improve
```

---

## 附录

### A. 部署检查清单

- [ ] Kubernetes 集群就绪
- [ ] 命名空间创建完成
- [ ] Secrets 配置完成
- [ ] ConfigMaps 配置完成
- [ ] PVC 创建完成
- [ ] 网络策略配置
- [ ] Ingress 配置
- [ ] HPA 配置
- [ ] 监控集成
- [ ] 日志收集
- [ ] 备份策略验证
- [ ] 安全扫描通过

### B. 常用命令

```bash
# 查看 Pod 状态
kubectl get pods -n devsmart-prod

# 查看服务日志
kubectl logs -f deployment/api-deployment -n devsmart-prod

# 手动扩缩容
kubectl scale deployment api-deployment --replicas=5 -n devsmart-prod

# 执行滚动重启
kubectl rollout restart deployment/api-deployment -n devsmart-prod

# 回滚到上一版本
kubectl rollout undo deployment/api-deployment -n devsmart-prod

# 查看资源使用
kubectl top pods -n devsmart-prod
```
