"use server";

import { cookies } from "next/headers";
import { redirect } from "next/navigation";
import { MyNewsDto } from "@/components/profile/profile-info";

export async function fetchUserProfile(): Promise<MyNewsDto[]> {
  const cookieStore = await cookies();
  const accessToken = cookieStore.get("access_token")?.value;

  if (!accessToken) {
    return [];
  }

  const url = new URL("/api/user/news", "http://localhost:8000");

  try {
    const res = await fetch(url.toString(), {
      method: "GET",
      headers: {
        Authorization: `Bearer ${accessToken}`,
      },
      cache: "no-store", // `cache: 'no-store'` to ensure we always refetch or handle caching as needed
    });
    if (!res.ok) {
      return [];
    }
    const data = await res.json();
    return data.news ?? [];
  } catch {
    return [];
  }
}

export async function logout() {
  (await cookies()).delete("access_token");
  redirect("/login");
}
