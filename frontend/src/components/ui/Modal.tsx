import { X } from 'lucide-react';
import { cn } from '../../lib/utils';

interface ModalProps {
  title: string;
  onClose: () => void;
  children: React.ReactNode;
  className?: string;
  showClose?: boolean;
  titleExtra?: React.ReactNode;
}

export default function Modal({
  title,
  onClose,
  children,
  className,
  showClose = true,
  titleExtra
}: ModalProps) {
  // Close modal when clicking outside
  const handleBackdropClick = (e: React.MouseEvent<HTMLDivElement>) => {
    if (e.target === e.currentTarget) {
      onClose();
    }
  };

  return (
    <div 
      className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50 backdrop-blur-sm"
      onClick={handleBackdropClick}
    >
      <div 
        className={cn(
          "bg-white rounded-lg shadow-xl w-full max-h-[90vh] overflow-y-auto",
          className
        )}
      >
        <div className="sticky top-0 z-10 bg-white px-6 py-4 border-b flex justify-between items-center">
          <div className="flex flex-col">
            <h2 className="text-xl font-semibold">{title}</h2>
            {titleExtra}
          </div>
          {showClose && (
            <button
              onClick={onClose}
              className="text-gray-500 hover:text-gray-700 transition-colors"
            >
              <X className="h-6 w-6" />
            </button>
          )}
        </div>

        <div className="p-6">
          {children}
        </div>
      </div>
    </div>
  );
}