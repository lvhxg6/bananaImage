/**
 * 加载动画组件
 */

import React, { useState, useEffect } from 'react';

const tips = [
  '正在分析图片内容...',
  'AI 正在理解艺术风格...',
  '正在融合内容与风格...',
  '生成高质量图像中...',
  '最终优化处理中...',
];

const LoadingSpinner = ({ onCancel }) => {
  const [tipIndex, setTipIndex] = useState(0);
  const [elapsed, setElapsed] = useState(0);

  useEffect(() => {
    // 更新提示文字
    const tipTimer = setInterval(() => {
      setTipIndex((prev) => (prev + 1) % tips.length);
    }, 4000);

    // 更新计时
    const elapsedTimer = setInterval(() => {
      setElapsed((prev) => prev + 1);
    }, 1000);

    return () => {
      clearInterval(tipTimer);
      clearInterval(elapsedTimer);
    };
  }, []);

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg shadow-xl p-8 max-w-md w-full mx-4 text-center">
        {/* 动画 */}
        <div className="mb-6">
          <div className="relative w-20 h-20 mx-auto">
            <div className="absolute inset-0 border-4 border-primary-200 rounded-full"></div>
            <div className="absolute inset-0 border-4 border-primary-500 rounded-full border-t-transparent animate-spin"></div>
            <div className="absolute inset-2 border-4 border-primary-300 rounded-full border-b-transparent animate-spin animation-delay-150"></div>
          </div>
        </div>

        {/* 标题 */}
        <h3 className="text-xl font-semibold text-gray-900 mb-2">
          风格迁移进行中
        </h3>

        {/* 动态提示 */}
        <p className="text-gray-600 mb-4 h-6 transition-opacity duration-300">
          {tips[tipIndex]}
        </p>

        {/* 计时器 */}
        <div className="mb-6">
          <p className="text-sm text-gray-500">
            已用时间: <span className="font-mono">{elapsed}</span> 秒
          </p>
          <p className="text-xs text-gray-400 mt-1">
            预计需要 15-30 秒，请耐心等待
          </p>
        </div>

        {/* 进度条 */}
        <div className="w-full bg-gray-200 rounded-full h-2 mb-6">
          <div
            className="bg-primary-500 h-2 rounded-full transition-all duration-1000 ease-out"
            style={{
              width: `${Math.min((elapsed / 30) * 100, 95)}%`,
            }}
          ></div>
        </div>

        {/* 取消按钮 */}
        {onCancel && (
          <button
            onClick={onCancel}
            className="px-6 py-2 text-gray-600 hover:text-gray-800 transition-colors"
          >
            取消
          </button>
        )}
      </div>
    </div>
  );
};

export default LoadingSpinner;
