"use client";

import { Button, Progress } from "@nextui-org/react";
import React from "react";
import { subtitle, title } from "@/styles/primitives";

/**
 * @description 뉴스레터 생성에 필요한 단계 (스탭) 를 위한 인터페이스
 * @interface WizardStepProps
 * @property {number} step - 현재 단계 인덱스 (e.g., 0..n-1)
 * @property {number} totalSteps - 전체 단계 수
 * @property {string} label - 매 단계를 나타내는 레이블 (제목)
 * @property {string} description - 해당 단계에 대한 설명
 * @property {number} progress - 진행률 값 (0..100)
 * @property {() => void} onPrev - "이전" 버튼을 위한 콜백
 * @property {() => void} onNext - "다음" 버튼을 위한 콜백
 * @property {string} onNextLabel - 다음 버튼에 대한 텍스트 ("다음" / "저장")
 * @property {boolean} canProceed - 다음 단계로 진행 가능 여부
 * @property {React.ReactNode} children - 해당 단계에 대한 콘텐츠
 */
interface WizardStepProps {
  step: number;
  totalSteps: number;
  label: string;
  description?: string;
  progress?: number;
  onPrev: () => void;
  onNext: () => void;
  onNextLabel?: string;
  canProceed?: boolean;
  children: React.ReactNode;
}

const WizardStep: React.FC<WizardStepProps> = ({
  step,
  totalSteps,
  label,
  description,
  progress,
  onPrev,
  onNext,
  onNextLabel = "Next",
  canProceed = true,
  children,
}) => {
  const progressValue = progress ?? (step / totalSteps) * 100;

  return (
    <div className="flex h-full w-full flex-col justify-between space-y-6 rounded-lg p-6">
      <div className="flex h-full w-full flex-col gap-4">
        <div className="flex flex-col gap-2">
          <h1
            className={title({
              size: "sm",
            })}
          >
            {label}
          </h1>
          <Progress
            aria-label="Progress bar"
            classNames={{
              base: "max-w-[300px]",
            }}
            value={progressValue}
            showValueLabel={true}
          />
          {description && <p className={subtitle()}>{description}</p>}
        </div>

        <div className="flex h-full flex-col">{children}</div>
      </div>
      <div className="flex w-full items-center justify-between">
        {step > 0 ? <Button onPress={onPrev}>Prev</Button> : <div />}
        <Button
          onPress={onNext}
          color="primary"
          variant="solid"
          isDisabled={!canProceed}
        >
          {onNextLabel}
        </Button>
      </div>
    </div>
  );
};

export default WizardStep;
