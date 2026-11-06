import { Component, ErrorInfo, ReactNode } from 'react';

interface Props {
  children: ReactNode;
  fallback?: ReactNode;
}

interface State {
  hasError: boolean;
  error?: Error;
}

export class ErrorBoundary extends Component<Props, State> {
  public state: State = { hasError: false };

  public static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  public componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error('ErrorBoundary caught error:', error, errorInfo);
  }

  public render() {
    if (this.state.hasError) {
      return (
        this.props.fallback || (
          <div className="p-6 m-4 bg-red-50 border border-red-200 rounded-xl text-red-700">
            <h2 className="text-lg font-bold">Giao diện gặp sự cố tạm thời</h2>
            <p className="text-sm mt-1">{this.state.error?.message || 'Vui lòng tải lại trang hoặc liên hệ hỗ trợ.'}</p>
          </div>
        )
      );
    }
    return this.props.children;
  }
}
