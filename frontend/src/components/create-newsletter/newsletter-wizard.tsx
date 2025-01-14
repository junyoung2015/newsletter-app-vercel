"use client";

import { useRouter } from "next/navigation";
import React, { useState } from "react";
import {
  createSampleNewsletter,
  saveNewsletter,
} from "@/app/create-newsletter/actions";
import useDebouncedCallback from "@/hooks/use-debounced-callback";
import NewsletterDetail from "./steps/detail";
import NewsletterFormat from "./steps/format";
import NewsletterPreference from "./steps/preference";
import NewsletterSource from "./steps/source";
import NewsletterTopic from "./steps/topic";
import { useNewsletterData } from "./use-newsletter-data";
import WizardStep from "./wizard-step";

export interface NewsletterStep {
  label: string;
  description?: string;
  progress?: number;
  component: React.FC;
  validator?: (data: {
    topics: string[];
    sources: string[];
    format: string[];
    frequency: string;
    exampleContent: string | null;
    name: string;
    description: string;
  }) => boolean;
}

const steps: NewsletterStep[] = [
  {
    label: "Preference",
    description: "First, enter the details of your newsletter.",
    progress: 0,
    component: NewsletterPreference,
    validator: (data) =>
      data.frequency.length > 0 &&
      data.name.length > 0 &&
      data.description.length > 0,
  },
  {
    label: "Topic",
    description: "Select topics you are interested in.",
    progress: 25,
    component: NewsletterTopic,
    validator: (data) => data.topics.length > 0,
  },
  {
    label: "Source",
    description: "Select sources you want to receive news from.",
    progress: 50,
    component: NewsletterSource,
    validator: (data) => data.sources.length > 0,
  },
  {
    label: "Format",
    description: "Select the format / style of the newsletter.",
    progress: 75,
    component: NewsletterFormat,
    validator: (data) => data.format.length > 0,
  },
  {
    label: "Almost Done...",
    // description: "Lastly, enter the details of your newsletter.",
    progress: 100,
    component: NewsletterDetail,
  },
];

const NewsletterWizard: React.FC = () => {
  const [step, setStep] = useState<number>(0);
  const router = useRouter();
  const {
    topics,
    sources,
    format,
    frequency,
    setExampleId,
    setExampleTitle,
    exampleContent,
    setExampleContent,
    name,
    description,
  } = useNewsletterData();

  const currentData = {
    topics,
    sources,
    format,
    frequency,
    exampleContent,
    name,
    description,
  };

  const currentStep = steps[step];

  const canProceed = currentStep.validator
    ? currentStep.validator(currentData)
    : true;

  const debouncedCreateSampleNewsletter = useDebouncedCallback(
    async (topics: string[], sources: string[]) => {
      const id = await createSampleNewsletter(topics, sources);
      if (id) {
        setExampleId(id);
      } else {
        alert("Failed to create sample newsletter");
      }
    },
    2000,
  );

  const goNext = async () => {
    if (step < steps.length - 1) {
      setStep(step + 1);
      if (step === steps.length - 2) {
        setExampleTitle(null);
        setExampleContent(null);
        debouncedCreateSampleNewsletter(topics, sources);
      }
    } else {
      await saveNewsletter(currentData);
      router.push("/");
      alert("Saved successfully!");
    }
  };

  const goPrev = () => {
    if (step > 0) {
      setStep(step - 1);
    }
  };

  const StepComponent = currentStep.component;

  return (
    <WizardStep
      step={step}
      totalSteps={steps.length}
      label={currentStep.label}
      description={currentStep.description}
      progress={currentStep.progress}
      onNext={goNext}
      onPrev={goPrev}
      onNextLabel={step === steps.length - 1 ? "Save" : "Next"}
      canProceed={canProceed}
    >
      <StepComponent />
    </WizardStep>
  );
};

export default NewsletterWizard;
