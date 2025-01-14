"use client";

import React, { createContext, useContext, useMemo, useState } from "react";

export interface CreateNewsletterData {
  name: string;
  setName: React.Dispatch<React.SetStateAction<string>>;

  description: string;
  setDescription: React.Dispatch<React.SetStateAction<string>>;

  frequency: string;
  setFrequency: React.Dispatch<React.SetStateAction<string>>;

  topics: string[];
  setTopics: React.Dispatch<React.SetStateAction<string[]>>;

  sources: string[];
  setSources: React.Dispatch<React.SetStateAction<string[]>>;

  format: string[];
  setFormat: React.Dispatch<React.SetStateAction<string[]>>;

  exampleId: string | null;
  setExampleId: React.Dispatch<React.SetStateAction<string | null>>;

  exampleTitle: string | null;
  setExampleTitle: React.Dispatch<React.SetStateAction<string | null>>;

  exampleContent: string | null;
  setExampleContent: React.Dispatch<React.SetStateAction<string | null>>;
}

const NewsletterDataContext = createContext<CreateNewsletterData | undefined>(
  undefined,
);

export const NewsletterDataProvider: React.FC<{
  children: React.ReactNode;
}> = ({ children }) => {
  const [name, setName] = useState<string>("");
  const [description, setDescription] = useState<string>("");
  const [frequency, setFrequency] = useState<string>("weekly");
  const [topics, setTopics] = useState<string[]>([]);
  const [sources, setSources] = useState<string[]>([]);
  const [format, setFormat] = useState<string[]>([]);
  const [exampleId, setExampleId] = useState<string | null>(null);
  const [exampleTitle, setExampleTitle] = useState<string | null>(null);
  const [exampleContent, setExampleContent] = useState<string | null>(null);

  const value: CreateNewsletterData = useMemo(
    () => ({
      name,
      setName,
      description,
      setDescription,
      frequency,
      setFrequency,
      topics,
      setTopics,
      sources,
      setSources,
      format,
      setFormat,
      exampleId,
      setExampleId,
      exampleTitle,
      setExampleTitle,
      exampleContent,
      setExampleContent,
    }),
    [
      name,
      description,
      topics,
      sources,
      format,
      frequency,
      exampleId,
      exampleTitle,
      exampleContent,
    ],
  );

  return (
    <NewsletterDataContext.Provider value={value}>
      {children}
    </NewsletterDataContext.Provider>
  );
};

export function useNewsletterData() {
  const context = useContext(NewsletterDataContext);
  if (!context) {
    throw new Error(
      "`useNewsletterData` must be used within a `NewsletterDataProvider`",
    );
  }
  return context;
}
