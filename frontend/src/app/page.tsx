"use client";

import { Textarea } from "@nextui-org/react";
import { SearchLinearIcon } from "@/icons";
import { subtitle, title } from "@/styles/primitives";

export default function Home() {
  return (
    <main className="container mx-auto max-w-7xl flex-grow px-6">
      <section className="flex flex-col items-center justify-center">
        <section className="relative flex h-[calc(100vh_-_64px)] w-full flex-nowrap items-center justify-between overflow-hidden lg:overflow-visible 2xl:h-[calc(84vh_-_64px)]">
          <div className="relative z-20 flex w-full flex-col gap-4 xl:mt-10">
            <div className="text-left leading-8 md:leading-10">
              <h1 className={title()}>Your News, Your Style.</h1>
            </div>
            <h2
              className={subtitle({
                fullWidth: true,
                class: "text-center md:text-left",
              })}
            >
              Create your own newsletter with just a few clicks.
            </h2>
            <div className="flex flex-col items-start justify-center">
              <Textarea
                placeholder="Enter what you want to read about..."
                classNames={{
                  base: "max-w-[600px] w-full",
                  inputWrapper: "shadow-lg",
                }}
                radius="full"
                type="text"
                minRows={1}
                maxRows={8}
                endContent={<SearchLinearIcon />}
              />
            </div>
          </div>
        </section>
      </section>
    </main>
  );
}
