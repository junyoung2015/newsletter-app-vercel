"use client";

import { Checkbox, CheckboxGroup, Chip, Input } from "@nextui-org/react";
import { useState } from "react";
import { useNewsletterData } from "../use-newsletter-data";

interface NewsletterTopicProps {}

const NewsletterTopic: React.FC<NewsletterTopicProps> = () => {
  const [inputValue, setInputValue] = useState("");
  const { topics, setTopics } = useNewsletterData();

  const handleChange = (topic: string[]) => {
    setTopics(topic);
  };

  const handleClose = (topic: string) => {
    setTopics(topics.filter((t) => t !== topic));
  };

  return (
    <div className="container mx-auto flex max-w-7xl flex-grow flex-col gap-4">
      <div className="mb-2 flex gap-2">
        {topics.map((topic, index) => (
          <Chip key={index} variant="flat" onClose={() => handleClose(topic)}>
            {topic}
          </Chip>
        ))}
      </div>
      <CheckboxGroup
        // label="Select topics"
        value={topics}
        onValueChange={handleChange}
      >
        <Checkbox value="economy">💰 Economy</Checkbox>
        <Checkbox value="science">🔬 Science</Checkbox>
        <Checkbox value="health">🏥 Health</Checkbox>
        <Checkbox value="environment">🌍 Environment</Checkbox>
        <Checkbox value="celebrity">📺 Celebrity</Checkbox>
      </CheckboxGroup>
      <Input
        className="max-w-xs"
        label="Custom topic"
        placeholder="Add custom topic"
        value={inputValue}
        onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
          setInputValue(e.currentTarget.value)
        }
        onKeyDown={(e: React.KeyboardEvent<HTMLInputElement>) => {
          if (e.key === "Enter") {
            setTopics([...topics, e.currentTarget.value]);
            setInputValue("");
            e.currentTarget.value = "";
          }
        }}
      />
    </div>
  );
};

export default NewsletterTopic;
