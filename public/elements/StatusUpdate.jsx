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
    if (type === "progress") return "animate-spin";
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
    <Card className={`status-update ${getTypeClass()} border-0 my-4`}>
      <CardContent className="p-4 flex items-start">
        <div className="status-update-icon mr-4 mt-1">
          <i data-lucide={icon} className={getIconClass()}></i>
        </div>
        <div className="flex-1">
          <div className="flex items-center justify-between">
            <h4 className="text-base font-semibold mb-1">{title}</h4>
            <Badge variant="outline" className="ml-2 capitalize">
              {getBadgeText()}
            </Badge>
          </div>
          <p className="text-sm opacity-90">{message}</p>
          {progress !== null && (
            <div className="mt-3">
              <Progress value={progress} className="h-2" />
            </div>
          )}
        </div>
      </CardContent>
    </Card>
  );
} 