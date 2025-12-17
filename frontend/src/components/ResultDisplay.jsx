/**
 * 结果展示组件
 * 支持文生图（单图展示）和图生图（三图对比）两种模式
 */

import React from 'react';
import { getImageUrl } from '../services/api';

const ResultDisplay = ({ result, contentImage, styleImage, onReset, mode = 'style-transfer' }) => {
  if (!result) return null;

  const isTextToImage = mode === 'text-to-image';

  const handleDownload = () => {
    const link = document.createElement('a');
    link.href = getImageUrl(result.image_url);
    const prefix = isTextToImage ? 'text_to_image' : 'style_transfer';
    link.download = `${prefix}_${Date.now()}.jpg`;
    link.click();
  };

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <h3 className="text-lg font-medium text-gray-900 mb-4">
        {isTextToImage ? '生成结果' : '风格迁移结果'}
      </h3>

      {/* 图片展示 */}
      {isTextToImage ? (
        // 文生图：单图展示
        <div className="mb-6">
          <div className="bg-gray-100 rounded-lg p-4 flex items-center justify-center">
            <img
              src={getImageUrl(result.image_url)}
              alt="生成结果"
              className="max-w-full max-h-[500px] object-contain rounded-lg shadow-sm"
            />
          </div>
        </div>
      ) : (
        // 图生图：三图对比
        <div className="grid grid-cols-3 gap-4 mb-6">
          {/* 内容图 */}
          <div className="text-center">
            <p className="text-sm text-gray-500 mb-2">内容图</p>
            <div className="bg-gray-100 rounded-lg p-2 aspect-square flex items-center justify-center">
              {contentImage && (
                <img
                  src={contentImage.preview}
                  alt="内容图"
                  className="max-h-full max-w-full object-contain rounded"
                />
              )}
            </div>
          </div>

          {/* 风格图 */}
          <div className="text-center">
            <p className="text-sm text-gray-500 mb-2">风格图</p>
            <div className="bg-gray-100 rounded-lg p-2 aspect-square flex items-center justify-center">
              {styleImage && (
                <img
                  src={styleImage.preview}
                  alt="风格图"
                  className="max-h-full max-w-full object-contain rounded"
                />
              )}
            </div>
          </div>

          {/* 结果图 */}
          <div className="text-center">
            <p className="text-sm text-gray-500 mb-2">生成结果</p>
            <div className="bg-gray-100 rounded-lg p-2 aspect-square flex items-center justify-center">
              <img
                src={getImageUrl(result.image_url)}
                alt="生成结果"
                className="max-h-full max-w-full object-contain rounded"
              />
            </div>
          </div>
        </div>
      )}

      {/* 描述信息 */}
      {result.description && (
        <div className="mb-4 p-3 bg-gray-50 rounded-lg">
          <p className="text-sm text-gray-600">
            <span className="font-medium">AI 描述：</span>
            {result.description}
          </p>
        </div>
      )}

      {/* 元数据 */}
      {result.metadata && (
        <div className="mb-4 flex flex-wrap gap-2 text-xs text-gray-500">
          <span className="px-2 py-1 bg-gray-100 rounded">
            分辨率: {result.metadata.resolution}
          </span>
          <span className="px-2 py-1 bg-gray-100 rounded">
            宽高比: {result.metadata.aspect_ratio}
          </span>
          <span className="px-2 py-1 bg-gray-100 rounded">
            格式: {result.metadata.output_format}
          </span>
          <span className="px-2 py-1 bg-gray-100 rounded">
            耗时: {result.metadata.processing_time}秒
          </span>
          {result.metadata.width && result.metadata.height && (
            <span className="px-2 py-1 bg-gray-100 rounded">
              尺寸: {result.metadata.width}x{result.metadata.height}
            </span>
          )}
        </div>
      )}

      {/* 操作按钮 */}
      <div className="flex gap-3">
        <button
          onClick={handleDownload}
          className="flex-1 px-4 py-2 bg-primary-500 text-white rounded-lg
                     hover:bg-primary-600 transition-colors font-medium"
        >
          下载图片
        </button>
        <button
          onClick={onReset}
          className="flex-1 px-4 py-2 bg-gray-100 text-gray-700 rounded-lg
                     hover:bg-gray-200 transition-colors font-medium"
        >
          重新生成
        </button>
      </div>
    </div>
  );
};

export default ResultDisplay;
