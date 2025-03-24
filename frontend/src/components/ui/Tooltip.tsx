import { cn } from '../../lib/utils';

interface TooltipProps {
  tip: string;
  children: React.ReactNode;
  className?: string;
}

export default function Tooltip({ tip, children, className }: TooltipProps) {
  return (
    <div className={cn('tooltip', className)} data-tip={tip}>
      {children}
    </div>
  );
}