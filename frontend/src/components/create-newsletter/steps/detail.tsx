"use client";

import {
  Card,
  CardBody,
  CardHeader,
  Divider,
  ScrollShadow,
  Spinner,
  Tab,
  Table,
  TableBody,
  TableCell,
  TableColumn,
  TableHeader,
  TableRow,
  Tabs,
} from "@nextui-org/react";
import { useEffect } from "react";
import { getSampleNewsletter } from "@/app/create-newsletter/actions";
import { subtitle, title } from "@/styles/primitives";
import { useNewsletterData } from "../use-newsletter-data";

interface NewsletterDetailProps {}

const NewsletterDetail: React.FC<NewsletterDetailProps> = () => {
  const {
    name,
    description,
    topics,
    sources,
    frequency,
    exampleId,
    exampleTitle,
    setExampleTitle,
    exampleContent,
    setExampleContent,
  } = useNewsletterData();

  useEffect(() => {
    if (!exampleId) return;
    let isCancelled = false;

    async function pollExample() {
      if (!exampleId) return;
      const data = await getSampleNewsletter(exampleId);
      if (!data) return;

      if (data?.status === "pending") {
        if (!isCancelled) {
          setTimeout(pollExample, 3000);
        }
      } else if (!isCancelled && data.content) {
        setExampleTitle(data.title);
        setExampleContent(data.content);
      }
    }

    pollExample();

    return () => {
      isCancelled = true;
    };
  }, [exampleId, setExampleTitle, setExampleContent]);

  return (
    <div className="container mx-auto mt-4 flex max-w-7xl flex-col">
      <Tabs aria-label="Newsletter Detail">
        <Tab key="Newsletter-detail" title="Detail">
          <h1 className={title({ size: "xs", fullWidth: true })}>
            News Detail
          </h1>

          <div className="mt-4 flex justify-center">
            <Table aria-label="News detail Table" isStriped>
              <TableHeader>
                <TableColumn className="w-1/4 text-lg">Item</TableColumn>
                <TableColumn className="text-lg">Detail</TableColumn>
              </TableHeader>
              <TableBody>
                <TableRow key="name">
                  <TableCell>Newsletter Name</TableCell>
                  <TableCell>{name}</TableCell>
                </TableRow>
                <TableRow key="description">
                  <TableCell>Description</TableCell>
                  <TableCell>{description}</TableCell>
                </TableRow>
                <TableRow key="topics">
                  <TableCell>Topics</TableCell>
                  <TableCell>{topics.join(", ")}</TableCell>
                </TableRow>
                <TableRow key="sources">
                  <TableCell>Sources</TableCell>
                  <TableCell>{sources.join(", ")}</TableCell>
                </TableRow>
                <TableRow key="frequency">
                  <TableCell>Frequency</TableCell>
                  <TableCell>{frequency}</TableCell>
                </TableRow>
              </TableBody>
            </Table>
          </div>
        </Tab>
        <Tab key="Newsletter-example" title="Example">
          <h1 className={title({ size: "xs", fullWidth: true })}>
            Example Newsletter
          </h1>
          <div className="mt-4 flex justify-center">
            {exampleTitle ? (
              <Card classNames={{ base: "w-full" }}>
                <CardHeader>
                  <h2 className={subtitle()}>{exampleTitle}</h2>
                </CardHeader>
                <Divider />
                <CardBody className="max-h-[400px] overflow-y-auto">
                  <div className="whitespace-pre-wrap">{exampleContent}</div>
                </CardBody>
              </Card>
            ) : (
              <Spinner color="primary" label="Generating news sample..." />
            )}
          </div>
        </Tab>
      </Tabs>
    </div>
  );
};

export default NewsletterDetail;
