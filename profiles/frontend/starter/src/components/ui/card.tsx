import React from 'react';

export interface CardProps extends React.HTMLAttributes<HTMLDivElement> {
  title?: string;
  description?: string;
}

export const Card: React.FC<CardProps> = ({
  title,
  description,
  children,
  className = '',
  ...props
}) => {
  return (
    <div className={`bg-white border border-slate-200 rounded-xl shadow-sm p-6 ${className}`} {...props}>
      {title && <h3 className="text-lg font-semibold text-slate-900 mb-1">{title}</h3>}
      {description && <p className="text-sm text-slate-500 mb-4">{description}</p>}
      {children}
    </div>
  );
};
