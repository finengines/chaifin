import { Progress } from "@/components/ui/progress"
import { Card, CardContent } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { useEffect, useState } from "react"

export default function AnimatedProgress() {
  const [currentStep, setCurrentStep] = useState(0);
  const title = props.title || "Processing";
  const message = props.message || "";
  const steps = props.steps || [];
  const progress = props.progress || 0;
  
  useEffect(() => {
    // Update the current step when progress changes
    if (steps.length > 0) {
      const stepIndex = Math.min(
        Math.floor((progress / 100) * steps.length),
        steps.length - 1
      );
      setCurrentStep(stepIndex);
    }
  }, [progress, steps]);
  
  return (
    <Card className="status-update status-progress border-0 my-4">
      <CardContent className="p-4 flex items-start">
        <div className="status-update-icon mr-4 mt-1">
          <i data-lucide="loader-2" className="animate-spin"></i>
        </div>
        <div className="flex-1">
          <div className="flex items-center justify-between">
            <h4 className="text-base font-semibold mb-1">{title}</h4>
            <Badge variant="outline" className="ml-2">
              {Math.round(progress)}%
            </Badge>
          </div>
          <p className="text-sm opacity-90">
            {steps.length > 0 ? steps[currentStep] : message}
          </p>
          <div className="mt-3">
            <Progress value={progress} className="h-2" />
          </div>
        </div>
      </CardContent>
    </Card>
  );
} 