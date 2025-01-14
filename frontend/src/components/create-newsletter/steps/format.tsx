"use client";

import { Checkbox, CheckboxGroup } from "@nextui-org/react";
import { useNewsletterData } from "../use-newsletter-data";

interface NewsletterFormatProps {}

const NewsletterFormat: React.FC<NewsletterFormatProps> = () => {
  const { format, setFormat } = useNewsletterData();

  const handleChange = (format: string[]) => {
    setFormat(format);
  };

  return (
    <div className="container max-w-7xl flex-grow">
      <CheckboxGroup
        label="Select format"
        value={format}
        onValueChange={handleChange}
      >
        <Checkbox value="hacker-news">Hacker News</Checkbox>
        <Checkbox value="publy">퍼블리</Checkbox>
        <Checkbox value="it-newsletter">요즘 IT 뉴스레터</Checkbox>
        <Checkbox value="robinhood">Robinhood Snacks</Checkbox>
      </CheckboxGroup>
    </div>
  );
};

export default NewsletterFormat;
