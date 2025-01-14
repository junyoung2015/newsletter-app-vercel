"use client";

import { Checkbox, CheckboxGroup, Chip, Input } from "@nextui-org/react";
import { useState } from "react";
import { useNewsletterData } from "../use-newsletter-data";

interface NewsletterSourceProps {}

const NewsletterSource: React.FC<NewsletterSourceProps> = () => {
  const [inputValue, setInputValue] = useState("");
  const { sources, setSources } = useNewsletterData();

  const handleChange = (source: string[]) => {
    setSources(source);
  };

  const handleClose = (source: string) => {
    setSources(sources.filter((s) => s !== source));
  };

  // function to validate the URL
  function isValidURL(url: string) {
    try {
      new URL(url);
      return true;
    } catch (e) {
      return false;
    }
  }

  return (
    <div className="container flex max-w-7xl flex-grow flex-col gap-4">
      <div className="mb-2 flex gap-2">
        {sources.map((source, index) => (
          <Chip key={index} variant="flat" onClose={() => handleClose(source)}>
            {source}
          </Chip>
        ))}
      </div>
      <CheckboxGroup
        // label="Select sources"
        value={sources}
        onValueChange={handleChange}
      >
        <Checkbox value="https://www.bbc.com/news">BBC News</Checkbox>
        {/* TODO: Fix the LinkedIn News URL */}
        <Checkbox value="https://www.linkedin.com/showcase/linkedin-news/">
          LinkedIn News
        </Checkbox>
        <Checkbox value="https://abcnews.go.com/">ABC News</Checkbox>
        <Checkbox value="https://edition.cnn.com/">CNN</Checkbox>
        <Checkbox value="https://www.bloomberg.com">Bloomberg</Checkbox>
      </CheckboxGroup>
      <Input
        className="max-w-xs"
        label="Custom source"
        placeholder="https://example.com"
        value={inputValue}
        onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
          setInputValue(e.currentTarget.value)
        }
        onKeyDown={(e: React.KeyboardEvent<HTMLInputElement>) => {
          if (e.key === "Enter") {
            if (!isValidURL(e.currentTarget.value)) {
              alert("Please enter a valid URL");
              return;
            }
            setSources([...sources, e.currentTarget.value]);
            setInputValue("");
            e.currentTarget.value = "";
          }
        }}
      />
    </div>
  );
};

export default NewsletterSource;
