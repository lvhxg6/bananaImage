/**
 * Gemini 风格迁移应用主组件
 */

import React, { useState, useEffect } from 'react';
import ImageUploader from './components/ImageUploader';
import ParameterPanel from './components/ParameterPanel';
import ResultDisplay from './components/ResultDisplay';
import LoadingSpinner from './components/LoadingSpinner';
import { styleTransfer, getConfig, healthCheck } from './services/api';

function App() {
  // 状态
  const [contentImage, setContentImage] = useState(null);
  const [styleImage, setStyleImage] = useState(null);
  const [params, setParams] = useState({
    prompt: '',
    resolution: '2K',
    aspectRatio: '1:1',
    outputFormat: 'JPEG',
  });
  const [config, setConfig] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [serverStatus, setServerStatus] = useState(null);

  // 加载配置
  useEffect(() => {
    const loadConfig = async () => {
      try {
        const [configData, health] = await Promise.all([
          getConfig(),
          healthCheck(),
        ]);
        setConfig(configData);
        setServerStatus(health);
      } catch (err) {
        console.error('加载配置失败:', err);
        setError('无法连接到服务器，请确保后端服务已启动');
      }
    };
    loadConfig();
  }, []);

  // 执行风格迁移
  const handleSubmit = async () => {
    if (!contentImage || !styleImage) {
      setError('请上传内容图片和风格图片');
      return;
    }

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await styleTransfer(
        contentImage.file,
        styleImage.file,
        params
      );

      if (response.success) {
        setResult(response);
      } else {
        setError(response.error || '风格迁移失败');
      }
    } catch (err) {
      console.error('风格迁移失败:', err);
      const message = err.response?.data?.detail || err.message || '请求失败';
      setError(message);
    } finally {
      setLoading(false);
    }
  };

  // 重置
  const handleReset = () => {
    setResult(null);
    setError(null);
  };

  // 完全重置
  const handleFullReset = () => {
    setContentImage(null);
    setStyleImage(null);
    setResult(null);
    setError(null);
    setParams({
      prompt: '',
      resolution: '2K',
      aspectRatio: '1:1',
      outputFormat: 'JPEG',
    });
  };

  return (
    <div className="min-h-screen bg-gray-100">
      {/* 加载动画 */}
      {loading && <LoadingSpinner />}

      {/* 头部 */}
      <header className="bg-white shadow-sm">
        <div className="max-w-6xl mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold text-gray-900">
                Gemini 风格迁移
              </h1>
              <p className="text-sm text-gray-500">
                基于 Gemini 3 Pro Image 的 AI 图片风格迁移工具
              </p>
            </div>
            {serverStatus && (
              <div className="flex items-center gap-2">
                <span
                  className={`w-2 h-2 rounded-full ${
                    serverStatus.api_key_configured
                      ? 'bg-green-500'
                      : 'bg-yellow-500'
                  }`}
                ></span>
                <span className="text-sm text-gray-500">
                  {serverStatus.api_key_configured ? '服务正常' : 'API Key 未配置'}
                </span>
              </div>
            )}
          </div>
        </div>
      </header>

      {/* 主内容 */}
      <main className="max-w-6xl mx-auto px-4 py-8">
        {/* 错误提示 */}
        {error && (
          <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg">
            <div className="flex items-center">
              <svg
                className="w-5 h-5 text-red-500 mr-2"
                fill="currentColor"
                viewBox="0 0 20 20"
              >
                <path
                  fillRule="evenodd"
                  d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"
                  clipRule="evenodd"
                />
              </svg>
              <span className="text-red-700">{error}</span>
            </div>
          </div>
        )}

        {/* 结果展示 */}
        {result ? (
          <div className="space-y-6">
            <ResultDisplay
              result={result}
              contentImage={contentImage}
              styleImage={styleImage}
              onReset={handleReset}
            />
            <div className="text-center">
              <button
                onClick={handleFullReset}
                className="text-primary-600 hover:text-primary-700 text-sm"
              >
                开始新的风格迁移
              </button>
            </div>
          </div>
        ) : (
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* 左侧：图片上传 */}
            <div className="lg:col-span-2 space-y-6">
              <div className="bg-white rounded-lg shadow p-6">
                <h2 className="text-lg font-medium text-gray-900 mb-4">
                  上传图片
                </h2>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <ImageUploader
                    label="内容图片"
                    description="提供图像内容结构"
                    image={contentImage}
                    onImageSelect={setContentImage}
                  />
                  <ImageUploader
                    label="风格图片"
                    description="提供艺术风格"
                    image={styleImage}
                    onImageSelect={setStyleImage}
                  />
                </div>
              </div>

              {/* 提交按钮 */}
              <button
                onClick={handleSubmit}
                disabled={!contentImage || !styleImage || loading}
                className={`w-full py-3 px-6 rounded-lg font-medium text-white
                  transition-all duration-200 ${
                    contentImage && styleImage && !loading
                      ? 'bg-primary-500 hover:bg-primary-600 cursor-pointer'
                      : 'bg-gray-300 cursor-not-allowed'
                  }`}
              >
                {loading ? '处理中...' : '开始风格迁移'}
              </button>
            </div>

            {/* 右侧：参数设置 */}
            <div>
              <ParameterPanel
                params={params}
                onChange={setParams}
                config={config}
              />

              {/* 使用说明 */}
              <div className="mt-6 bg-blue-50 rounded-lg p-4">
                <h4 className="font-medium text-blue-900 mb-2">使用说明</h4>
                <ul className="text-sm text-blue-700 space-y-1">
                  <li>• 上传一张内容图片（保留其结构）</li>
                  <li>• 上传一张风格图片（应用其风格）</li>
                  <li>• 选择输出参数</li>
                  <li>• 点击"开始风格迁移"</li>
                  <li>• 等待 15-30 秒获取结果</li>
                </ul>
              </div>
            </div>
          </div>
        )}
      </main>

      {/* 页脚 */}
      <footer className="mt-auto py-6 text-center text-gray-500 text-sm">
        <p>
          Powered by{' '}
          <a
            href="https://ai.google.dev/gemini-api"
            target="_blank"
            rel="noopener noreferrer"
            className="text-primary-600 hover:underline"
          >
            Google Gemini
          </a>
        </p>
      </footer>
    </div>
  );
}

export default App;
