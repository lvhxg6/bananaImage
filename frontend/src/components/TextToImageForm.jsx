/**
 * 文生图表单组件
 * 用户输入文字描述生成图片
 */

import React, { useState } from 'react';

function TextToImageForm({ config, onSubmit, loading }) {
  const [prompt, setPrompt] = useState('');
  const [params, setParams] = useState({
    resolution: '2K',
    aspectRatio: '1:1',
    outputFormat: 'JPEG',
  });

  const handleSubmit = () => {
    if (!prompt.trim()) {
      return;
    }
    onSubmit(prompt, params);
  };

  const handleParamChange = (key, value) => {
    setParams(prev => ({ ...prev, [key]: value }));
  };

  return (
    <div className="space-y-6">
      {/* 提示词输入 */}
      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-lg font-medium text-gray-900 mb-4">
          图片描述
        </h2>
        <textarea
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          placeholder="请描述你想要生成的图片内容...&#10;&#10;例如：一只橙色的猫咪坐在窗台上，背景是夕阳西下的城市天际线，画面风格是油画"
          className="w-full h-40 px-4 py-3 border border-gray-300 rounded-lg
            focus:ring-2 focus:ring-primary-500 focus:border-primary-500
            resize-none placeholder-gray-400"
        />
        <p className="mt-2 text-sm text-gray-500">
          提示：描述越详细，生成效果越好。可以包含主体、场景、风格、色调等信息。
        </p>
      </div>

      {/* 参数设置 */}
      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-lg font-medium text-gray-900 mb-4">
          生成参数
        </h2>

        <div className="space-y-4">
          {/* 分辨率 */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              分辨率
            </label>
            <div className="flex gap-2">
              {(config?.resolutions || ['1K', '2K', '4K']).map((res) => (
                <button
                  key={res}
                  onClick={() => handleParamChange('resolution', res)}
                  className={`px-4 py-2 rounded-lg text-sm font-medium transition-all
                    ${params.resolution === res
                      ? 'bg-primary-500 text-white'
                      : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                    }`}
                >
                  {res}
                </button>
              ))}
            </div>
          </div>

          {/* 宽高比 */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              宽高比
            </label>
            <div className="flex flex-wrap gap-2">
              {(config?.aspect_ratios || ['1:1', '16:9', '9:16', '4:3', '3:4']).map((ratio) => (
                <button
                  key={ratio}
                  onClick={() => handleParamChange('aspectRatio', ratio)}
                  className={`px-3 py-1.5 rounded-lg text-sm font-medium transition-all
                    ${params.aspectRatio === ratio
                      ? 'bg-primary-500 text-white'
                      : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                    }`}
                >
                  {ratio}
                </button>
              ))}
            </div>
          </div>

          {/* 输出格式 */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              输出格式
            </label>
            <div className="flex gap-2">
              {(config?.output_formats || ['JPEG', 'PNG']).map((format) => (
                <button
                  key={format}
                  onClick={() => handleParamChange('outputFormat', format)}
                  className={`px-4 py-2 rounded-lg text-sm font-medium transition-all
                    ${params.outputFormat === format
                      ? 'bg-primary-500 text-white'
                      : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                    }`}
                >
                  {format}
                </button>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* 提交按钮 */}
      <button
        onClick={handleSubmit}
        disabled={!prompt.trim() || loading}
        className={`w-full py-3 px-6 rounded-lg font-medium text-white
          transition-all duration-200 ${
            prompt.trim() && !loading
              ? 'bg-primary-500 hover:bg-primary-600 cursor-pointer'
              : 'bg-gray-300 cursor-not-allowed'
          }`}
      >
        {loading ? '生成中...' : '生成图片'}
      </button>

      {/* 使用说明 */}
      <div className="bg-blue-50 rounded-lg p-4">
        <h4 className="font-medium text-blue-900 mb-2">使用说明</h4>
        <ul className="text-sm text-blue-700 space-y-1">
          <li>1. 在文本框中输入图片描述</li>
          <li>2. 选择输出参数（分辨率、宽高比等）</li>
          <li>3. 点击"生成图片"按钮</li>
          <li>4. 等待 15-30 秒获取结果</li>
        </ul>
      </div>
    </div>
  );
}

export default TextToImageForm;
