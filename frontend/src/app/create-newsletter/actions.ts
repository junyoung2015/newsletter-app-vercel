"use server";

import { cookies } from "next/headers";

export interface NewsletterData {
  name: string;
  description: string;
  frequency: string;
  exampleContent: string | null;
  topics: string[];
  sources: string[];
}

export async function saveNewsletter({
  name,
  description,
  frequency,
  exampleContent,
  topics,
  sources,
}: NewsletterData): Promise<void> {
  const cookieStore = await cookies();
  const accessToken = cookieStore.get("access_token")?.value;

  if (!accessToken) {
    return;
  }

  const url = new URL("/api/news/save", "http://localhost:8000");

  try {
    const res = await fetch(url.toString(), {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${accessToken}`,
      },
      body: JSON.stringify({
        name,
        description,
        custom_prmopt: exampleContent,
        send_frequency: frequency,
        is_active: "true",
        topic: topics,
        source: sources,
      }),
      cache: "no-cache",
    });
    if (!res.ok) {
      return;
    }
  } catch {
    return;
  }
}

export async function createSampleNewsletter(
  topics: string[],
  sources: string[],
): Promise<string | null> {
  const cookieStore = await cookies();
  const accessToken = cookieStore.get("access_token")?.value;

  if (!accessToken) {
    return null;
  }

  const url = new URL("/api/news/task", "http://localhost:8000");

  try {
    const res = await fetch(url.toString(), {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${accessToken}`,
      },
      body: JSON.stringify({
        topics,
        sources,
      }),
      cache: "no-cache",
    });
    if (!res.ok) {
      return null;
    }
    const data = await res.json();
    return data.task_id;
  } catch {
    return null;
  }
}

export async function getSampleNewsletter(taskId: string) {
  const cookieStore = await cookies();
  const accessToken = cookieStore.get("access_token")?.value;

  if (!accessToken) {
    return null;
  }

  const url = new URL(`/api/news/example/${taskId}`, "http://localhost:8000");

  try {
    const res = await fetch(url.toString(), {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${accessToken}`,
      },
      cache: "no-cache",
    });
    if (!res.ok) {
      return null;
    }
    const data = await res.json();
    console.log("data", data);
    return data;
  } catch {
    return null;
  }
}
