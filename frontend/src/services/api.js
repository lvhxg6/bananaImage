/**
 * API 调用服务
 */

import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

// 创建 axios 实例
const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 120000, // 2分钟超时（图片生成需要较长时间）
});

/**
 * 执行风格迁移
 */
export const styleTransfer = async (contentImage, styleImage, params = {}) => {
  const formData = new FormData();
  formData.append('content_image', contentImage);
  formData.append('style_image', styleImage);

  if (params.prompt) {
    formData.append('prompt', params.prompt);
  }
  formData.append('aspect_ratio', params.aspectRatio || '1:1');
  formData.append('resolution', params.resolution || '2K');
  formData.append('output_format', params.outputFormat || 'JPEG');

  const response = await api.post('/api/style-transfer', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });

  return response.data;
};

/**
 * 文生图：根据文字描述生成图片
 */
export const textToImage = async (prompt, params = {}) => {
  const formData = new FormData();
  formData.append('prompt', prompt);
  formData.append('aspect_ratio', params.aspectRatio || '1:1');
  formData.append('resolution', params.resolution || '2K');
  formData.append('output_format', params.outputFormat || 'JPEG');

  const response = await api.post('/api/text-to-image', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });

  return response.data;
};

/**
 * 获取配置选项
 */
export const getConfig = async () => {
  const response = await api.get('/api/config');
  return response.data;
};

/**
 * 健康检查
 */
export const healthCheck = async () => {
  const response = await api.get('/api/health');
  return response.data;
};

/**
 * 获取图片完整 URL
 */
export const getImageUrl = (path) => {
  if (path.startsWith('http')) {
    return path;
  }
  return `${API_BASE_URL}${path}`;
};

export default api;
