import { Link } from 'react-router-dom';

const navItems = [
  { to: '/tasks/create', label: '任务创建 POC' },
  { to: '/prd/approval', label: 'PRD 审批 POC' },
  { to: '/tasks/split', label: '任务拆分 POC' },
  { to: '/workflow/replay', label: '工作流回放 POC' },
];

export function HomePage() {
  return (
    <main>
      <h1>DevSmart 前端 POC 导航</h1>
      <ul>
        {navItems.map((item) => (
          <li key={item.to}>
            <Link to={item.to}>{item.label}</Link>
          </li>
        ))}
      </ul>
    </main>
  );
}
