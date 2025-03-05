import { useState, useEffect } from 'react';
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";

export default function AnimatedProgress() {
  const [currentStep, setCurrentStep] = useState(0);
  const [isVisible, setIsVisible] = useState(false);
  
  // Get props with defaults
  const title = props.title || "Processing";
  const message = props.message || "";
  const steps = props.steps || [];
  const progress = props.progress || 0;
  
  // Animate on mount
  useEffect(() => {
    const timer = setTimeout(() => setIsVisible(true), 50);
    return () => clearTimeout(timer);
  }, []);
  
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
  
  // Generate a unique gradient based on progress
  const getProgressGradient = () => {
    const hue1 = 200; // Blue-ish
    const hue2 = 170; // Teal-ish
    const saturation = 80;
    const lightness = 60;
    
    return {
      background: `linear-gradient(135deg, 
        hsl(${hue1}, ${saturation}%, ${lightness}%) 0%, 
        hsl(${hue2}, ${saturation}%, ${lightness}%) 100%)`
    };
  };
  
  return (
    <Card 
      className={`animated-progress my-4 border shadow-sm ${isVisible ? 'progress-visible' : 'progress-hidden'}`}
      style={getProgressGradient()}
    >
      <CardContent className="p-4">
        <div className="flex items-center justify-between mb-2">
          <div className="flex items-center">
            <div className="animated-progress-icon mr-2">
              <i data-lucide="activity" className="h-5 w-5 text-white animate-pulse-slow"></i>
            </div>
            <h4 className="text-base font-medium text-white animated-progress-title">{title}</h4>
          </div>
          <Badge variant="progress" className="text-xs animated-progress-badge">
            {progress}%
          </Badge>
        </div>
        
        <p className="text-sm text-white/80 mb-3 animated-progress-message">{message}</p>
        
        {/* Progress bar with animated gradient */}
        <div className="h-2 bg-white/30 rounded-full mb-4 overflow-hidden animated-progress-bar">
          <div 
            className="h-full bg-white/90 rounded-full transition-all duration-500 ease-out animated-progress-bar-fill"
            style={{ width: `${progress}%` }}
          >
            <div className="progress-glow"></div>
          </div>
        </div>
        
        {/* Steps with enhanced styling */}
        {steps.length > 0 && (
          <div className="space-y-2 mt-3 animated-progress-steps">
            {steps.map((step, index) => (
              <div 
                key={index} 
                className={`flex items-center p-2 rounded-md transition-colors animated-progress-step ${
                  index < currentStep 
                    ? 'step-completed' 
                    : index === currentStep 
                      ? 'step-current' 
                      : 'step-pending'
                }`}
              >
                <div className="mr-2 flex-shrink-0 step-icon">
                  {index < currentStep ? (
                    <i data-lucide="check-circle" className="h-4 w-4 text-white"></i>
                  ) : index === currentStep ? (
                    <i data-lucide="loader" className="h-4 w-4 text-white animate-spin"></i>
                  ) : (
                    <i data-lucide="circle" className="h-4 w-4 text-white/60"></i>
                  )}
                </div>
                <span className="text-sm step-text">{step}</span>
              </div>
            ))}
          </div>
        )}
      </CardContent>
    </Card>
  );
} 