import { useState, useEffect } from 'react';
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";

export default function AnimatedProgress() {
  const [currentStep, setCurrentStep] = useState(0);
  
  // Get props with defaults
  const title = props.title || "Processing";
  const message = props.message || "";
  const steps = props.steps || [];
  const progress = props.progress || 0;
  
  // Update current step based on progress
  useEffect(() => {
    if (steps.length > 0) {
      const stepIndex = Math.min(
        Math.floor((progress / 100) * steps.length),
        steps.length - 1
      );
      setCurrentStep(stepIndex);
    }
  }, [progress, steps]);
  
  return (
    <Card className="animated-progress my-4 border shadow-sm">
      <CardContent className="p-4">
        <div className="flex items-center justify-between mb-2">
          <h4 className="text-base font-medium">{title}</h4>
          <Badge variant="outline" className="text-xs">
            {progress}%
          </Badge>
        </div>
        
        <p className="text-sm text-muted-foreground mb-3">{message}</p>
        
        {/* Progress bar */}
        <div className="h-2 bg-muted rounded-full mb-4 overflow-hidden">
          <div 
            className="h-full bg-primary rounded-full transition-all duration-500 ease-out"
            style={{ width: `${progress}%` }}
          ></div>
        </div>
        
        {/* Steps */}
        {steps.length > 0 && (
          <div className="space-y-2 mt-3">
            {steps.map((step, index) => (
              <div 
                key={index} 
                className={`flex items-center p-2 rounded-md transition-colors ${
                  index < currentStep 
                    ? 'bg-primary/10 text-primary' 
                    : index === currentStep 
                      ? 'bg-primary/5 text-foreground' 
                      : 'text-muted-foreground'
                }`}
              >
                <div className="mr-2 flex-shrink-0">
                  {index < currentStep ? (
                    <i data-lucide="check-circle" className="h-4 w-4"></i>
                  ) : index === currentStep ? (
                    <i data-lucide="loader" className="h-4 w-4 animate-spin"></i>
                  ) : (
                    <i data-lucide="circle" className="h-4 w-4"></i>
                  )}
                </div>
                <span className="text-sm">{step}</span>
              </div>
            ))}
          </div>
        )}
      </CardContent>
    </Card>
  );
} 