/**
 * 参数配置面板
 */

import React from 'react';

const ParameterPanel = ({ params, onChange, config }) => {
  const handleChange = (key, value) => {
    onChange({ ...params, [key]: value });
  };

  return (
    <div className="bg-white rounded-lg shadow p-4 space-y-4">
      <h3 className="text-lg font-medium text-gray-900">参数设置</h3>

      {/* 提示词 */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">
          提示词（可选）
        </label>
        <textarea
          value={params.prompt || ''}
          onChange={(e) => handleChange('prompt', e.target.value)}
          placeholder="描述你想要的风格迁移效果..."
          rows={2}
          className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm
                     focus:ring-primary-500 focus:border-primary-500 text-sm"
        />
      </div>

      {/* 分辨率 */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">
          分辨率
        </label>
        <div className="flex gap-2">
          {(config?.resolutions || ['1K', '2K', '4K']).map((res) => (
            <button
              key={res}
              onClick={() => handleChange('resolution', res)}
              className={`px-4 py-2 rounded-md text-sm font-medium transition-colors
                ${params.resolution === res
                  ? 'bg-primary-500 text-white'
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }`}
            >
              {res}
            </button>
          ))}
        </div>
      </div>

      {/* 宽高比 */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">
          宽高比
        </label>
        <select
          value={params.aspectRatio}
          onChange={(e) => handleChange('aspectRatio', e.target.value)}
          className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm
                     focus:ring-primary-500 focus:border-primary-500 text-sm"
        >
          {(config?.aspect_ratios || ['1:1', '16:9', '9:16', '4:3', '3:4']).map((ratio) => (
            <option key={ratio} value={ratio}>
              {ratio}
            </option>
          ))}
        </select>
      </div>

      {/* 输出格式 */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">
          输出格式
        </label>
        <div className="flex gap-2">
          {(config?.output_formats || ['JPEG', 'PNG']).map((fmt) => (
            <button
              key={fmt}
              onClick={() => handleChange('outputFormat', fmt)}
              className={`px-4 py-2 rounded-md text-sm font-medium transition-colors
                ${params.outputFormat === fmt
                  ? 'bg-primary-500 text-white'
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }`}
            >
              {fmt}
            </button>
          ))}
        </div>
      </div>
    </div>
  );
};

export default ParameterPanel;
