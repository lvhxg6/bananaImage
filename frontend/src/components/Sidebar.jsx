/**
 * 侧边栏导航组件
 * 用于切换文生图和图生图模式
 */

import React from 'react';

const menuItems = [
  {
    id: 'text-to-image',
    label: '文生图',
    description: '文字描述生成图片',
    icon: (
      <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
          d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
      </svg>
    ),
  },
  {
    id: 'style-transfer',
    label: '图生图',
    description: '风格迁移',
    icon: (
      <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
          d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
      </svg>
    ),
  },
];

function Sidebar({ activeMode, onModeChange }) {
  return (
    <aside className="w-56 bg-white shadow-sm rounded-lg p-4">
      <h3 className="text-sm font-medium text-gray-500 mb-3">功能选择</h3>
      <nav className="space-y-2">
        {menuItems.map((item) => (
          <button
            key={item.id}
            onClick={() => onModeChange(item.id)}
            className={`w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-left transition-all duration-200
              ${activeMode === item.id
                ? 'bg-primary-50 text-primary-700 border border-primary-200'
                : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900 border border-transparent'
              }`}
          >
            <span className={`${activeMode === item.id ? 'text-primary-600' : 'text-gray-400'}`}>
              {item.icon}
            </span>
            <div>
              <div className="font-medium text-sm">{item.label}</div>
              <div className="text-xs text-gray-400">{item.description}</div>
            </div>
          </button>
        ))}
      </nav>
    </aside>
  );
}

export default Sidebar;
