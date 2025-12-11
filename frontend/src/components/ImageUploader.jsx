/**
 * 图片上传组件
 * 支持拖拽上传和点击选择
 */

import React, { useCallback } from 'react';
import { useDropzone } from 'react-dropzone';

const ImageUploader = ({
  label,
  description,
  image,
  onImageSelect,
  accept = { 'image/*': ['.jpeg', '.jpg', '.png', '.webp'] }
}) => {
  const onDrop = useCallback((acceptedFiles) => {
    if (acceptedFiles.length > 0) {
      const file = acceptedFiles[0];
      const preview = URL.createObjectURL(file);
      onImageSelect({ file, preview });
    }
  }, [onImageSelect]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept,
    maxFiles: 1,
    maxSize: 10 * 1024 * 1024, // 10MB
  });

  const handleRemove = (e) => {
    e.stopPropagation();
    if (image?.preview) {
      URL.revokeObjectURL(image.preview);
    }
    onImageSelect(null);
  };

  return (
    <div className="flex flex-col">
      <label className="block text-sm font-medium text-gray-700 mb-2">
        {label}
      </label>

      <div
        {...getRootProps()}
        className={`
          relative border-2 border-dashed rounded-lg p-4 text-center cursor-pointer
          transition-colors duration-200 min-h-[200px] flex items-center justify-center
          ${isDragActive
            ? 'border-primary-500 bg-primary-50'
            : 'border-gray-300 hover:border-primary-400 bg-white'
          }
          ${image ? 'border-solid border-primary-500' : ''}
        `}
      >
        <input {...getInputProps()} />

        {image ? (
          <div className="relative w-full h-full">
            <img
              src={image.preview}
              alt="预览"
              className="max-h-[180px] mx-auto object-contain rounded"
            />
            <button
              onClick={handleRemove}
              className="absolute top-0 right-0 bg-red-500 text-white rounded-full w-6 h-6
                         flex items-center justify-center text-sm hover:bg-red-600
                         transform translate-x-1/2 -translate-y-1/2"
            >
              ×
            </button>
            <p className="text-xs text-gray-500 mt-2 truncate">
              {image.file.name}
            </p>
          </div>
        ) : (
          <div className="text-gray-500">
            <svg
              className="mx-auto h-12 w-12 text-gray-400"
              stroke="currentColor"
              fill="none"
              viewBox="0 0 48 48"
            >
              <path
                d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28m0 0l4 4m4-24h8m-4-4v8m-12 4h.02"
                strokeWidth={2}
                strokeLinecap="round"
                strokeLinejoin="round"
              />
            </svg>
            <p className="mt-2 text-sm">
              {isDragActive ? '释放以上传图片' : '拖拽图片到此处，或点击选择'}
            </p>
            <p className="mt-1 text-xs text-gray-400">
              {description || '支持 JPG、PNG、WebP，最大 10MB'}
            </p>
          </div>
        )}
      </div>
    </div>
  );
};

export default ImageUploader;
