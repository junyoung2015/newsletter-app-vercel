"use client";

import { Input, Select, SelectItem, SharedSelection } from "@nextui-org/react";
import { useNewsletterData } from "../use-newsletter-data";

interface NewsletterPreferenceProps {}

interface NewsletterPreference {
  key: string;
  label: string;
}

const frequencies: NewsletterPreference[] = [
  {
    key: "daily",
    label: "Daily",
  },
  {
    key: "weekly",
    label: "Weekly",
  },
  {
    key: "bi-weekly",
    label: "Bi-weekly",
  },
  {
    key: "monthly",
    label: "Monthly",
  },
];

const NewsletterPreference: React.FC<NewsletterPreferenceProps> = () => {
  const {
    frequency,
    setFrequency,
    name,
    setName,
    description,
    setDescription,
  } = useNewsletterData();

  const handleChange = (keys: SharedSelection) => {
    const frequency = Array.from(keys)[0] as string;
    setFrequency(frequency);
  };
  return (
    <div className="mx-auto flex max-w-7xl flex-grow flex-col gap-4">
      <Input
        className="max-w-xs"
        label="Name"
        placeholder="Name"
        type="text"
        value={name}
        onChange={(e) => setName(e.target.value)}
      />
      <Input
        className="max-w-xs"
        label="Description"
        placeholder="Description"
        type="text"
        value={description}
        onChange={(e) => setDescription(e.target.value)}
      />
      <Select
        className="max-w-xs"
        label="Frequency"
        placeholder="Select frequency"
        defaultSelectedKeys={[frequency]}
        onSelectionChange={handleChange}
      >
        {frequencies.map((frequency) => (
          <SelectItem key={frequency.key}>{frequency.label}</SelectItem>
        ))}
      </Select>
    </div>
  );
};

export default NewsletterPreference;
