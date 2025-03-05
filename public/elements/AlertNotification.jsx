import { Alert, AlertTitle, AlertDescription } from "@/components/ui/alert"
import { useEffect, useState } from "react"

export default function AlertNotification() {
  // Get props with defaults
  const type = props.type || "info";
  const title = props.title || "";
  const content = props.content || "";
  const icon = props.icon || getIcon();
  
  // State for animation
  const [isVisible, setIsVisible] = useState(false);
  
  // Animate on mount
  useEffect(() => {
    const timer = setTimeout(() => setIsVisible(true), 50);
    return () => clearTimeout(timer);
  }, []);
  
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
  
  // Get icon animation class
  function getIconClass() {
    switch(type) {
      case "important": return "animate-pulse";
      case "warning": return "animate-pulse-slow";
      case "notification": return "animate-bounce-subtle";
      default: return "";
    }
  }
  
  return (
    <Alert className={`${getClassName()} my-4 alert-notification ${isVisible ? 'alert-visible' : 'alert-hidden'}`}>
      <div className="flex items-start">
        <div className={`flex-shrink-0 mr-3 alert-icon ${getIconClass()}`}>
          <i data-lucide={icon} className="h-5 w-5"></i>
        </div>
        <div className="alert-content">
          <AlertTitle className="text-base font-medium alert-title">{title}</AlertTitle>
          <AlertDescription className="text-sm alert-description">{content}</AlertDescription>
        </div>
      </div>
      <div className="alert-decoration"></div>
    </Alert>
  );
} 