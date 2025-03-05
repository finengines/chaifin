import { Card, CardContent } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Progress } from "@/components/ui/progress"

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
    if (type === "progress" || type === "running") return "animate-spin";
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
    <Card className={`status-update ${getTypeClass()} my-4 border shadow-sm`}>
      <CardContent className="p-4">
        <div className="status-update-content flex items-start gap-3">
          <div className={`status-update-icon flex-shrink-0 ${getIconClass()}`}>
            <i data-lucide={icon} className="h-5 w-5"></i>
          </div>
          <div className="status-update-text flex-grow">
            <h4 className="status-update-title text-base font-medium">{title}</h4>
            <p className="status-update-message text-sm text-muted-foreground">{message}</p>
            {progress !== null && (
              <div className="mt-3">
                <Progress value={progress} className="h-2" />
                <span className="text-xs text-muted-foreground mt-1 inline-block">{progress}%</span>
              </div>
            )}
          </div>
          <Badge variant="outline" className="status-update-badge flex-shrink-0">
            {getBadgeText()}
          </Badge>
        </div>
      </CardContent>
    </Card>
  );
} 