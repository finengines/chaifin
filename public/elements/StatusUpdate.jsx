export default function StatusUpdate() {
  // Get props with defaults
  const type = props.type || "info";
  const icon = props.icon || "info";
  const title = props.title || "";
  const message = props.message || "";
  const progress = props.progress || null;
  
  // Define class names based on type
  const getTypeClass = () => {
    switch(type) {
      case "email": return "status-email";
      case "calendar": return "status-calendar";
      case "web-search": return "status-web-search";
      case "file-system": return "status-file-system";
      case "database": return "status-database";
      case "api": return "status-api";
      case "progress": return "status-progress";
      case "success": return "status-success";
      case "warning": return "status-warning";
      case "error": return "status-error";
      case "info": 
      default: return "status-info";
    }
  };
  
  // Get icon animation class
  const getIconClass = () => {
    if (type === "progress") return "animate-spin";
    if (type === "warning" || type === "error") return "animate-pulse";
    return "";
  };
  
  // Get badge text
  const getBadgeText = () => {
    switch(type) {
      case "email": return "Email";
      case "calendar": return "Calendar";
      case "web-search": return "Web Search";
      case "file-system": return "File System";
      case "database": return "Database";
      case "api": return "API";
      case "progress": return progress !== null ? `${progress}%` : "Processing";
      case "success": return "Success";
      case "warning": return "Warning";
      case "error": return "Error";
      case "info": 
      default: return "Info";
    }
  };
  
  return (
    <div className={`status-update ${getTypeClass()}`}>
      <div className="status-update-content">
        <div className={`status-update-icon ${type}-icon`}>
          <span className="material-icons">{icon}</span>
        </div>
        <div className="status-update-text">
          <h4 className="status-update-title">{title}</h4>
          <p className="status-update-message">{message}</p>
          {progress !== null && (
            <div className="status-update-progress">
              <div className="status-update-progress-bar" style={{width: `${progress}%`}}></div>
            </div>
          )}
        </div>
        <div className="status-update-badge">
          {getBadgeText()}
        </div>
      </div>
    </div>
  );
} 