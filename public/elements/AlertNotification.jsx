import { Alert, AlertTitle, AlertDescription } from "@/components/ui/alert"

export default function AlertNotification() {
  // Get props with defaults
  const type = props.type || "info";
  const title = props.title || "";
  const content = props.content || "";
  const icon = props.icon || getIcon();
  
  // Get icon based on type
  function getIcon() {
    switch(type) {
      case "important": return "alert-circle";
      case "warning": return "alert-triangle";
      case "notification": return "bell";
      case "system": 
      default: return "info";
    }
  }
  
  // Get class name based on type
  function getClassName() {
    switch(type) {
      case "important": return "alert-important";
      case "warning": return "alert-warning";
      case "notification": return "alert-notification";
      case "system": 
      default: return "alert-system";
    }
  }
  
  return (
    <Alert className={`${getClassName()} my-4`}>
      <div className="flex items-start">
        <div className="flex-shrink-0 mr-3">
          <i data-lucide={icon} className="h-5 w-5"></i>
        </div>
        <div>
          <AlertTitle className="text-base font-medium">{title}</AlertTitle>
          <AlertDescription className="text-sm">{content}</AlertDescription>
        </div>
      </div>
    </Alert>
  );
} 