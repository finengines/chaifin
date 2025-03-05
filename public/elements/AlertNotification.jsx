export default function AlertNotification() {
  // Get props with defaults
  const type = props.type || "notification";
  const title = props.title || "";
  const message = props.message || "";
  
  // Get icon based on type
  const getIcon = () => {
    switch(type) {
      case "important": return "alert-circle";
      case "warning": return "alert-triangle";
      case "notification": return "bell";
      case "system":
      default: return "info";
    }
  };
  
  // Get class name based on type
  const getClassName = () => {
    switch(type) {
      case "important": return "alert-important";
      case "warning": return "alert-warning";
      case "notification": return "alert-notification-type";
      case "system":
      default: return "alert-system";
    }
  };
  
  return (
    <div className={`alert-notification ${getClassName()} my-4`}>
      <div className="flex items-start p-4">
        <div className="alert-icon">
          <i data-lucide={getIcon()}></i>
        </div>
        <div className="alert-content">
          <div className="alert-title">{title}</div>
          <div className="alert-message">{message}</div>
        </div>
      </div>
    </div>
  );
} 