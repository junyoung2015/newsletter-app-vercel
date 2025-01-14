"use server";

import { cookies } from "next/headers";

export async function fetchUserEmail(): Promise<string | null> {
  const cookieStore = await cookies();
  const accessToken = cookieStore.get("access_token")?.value;

  if (!accessToken) {
    return null;
  }

  const url = new URL("/api/user/me", "http://localhost:8000");

  try {
    const res = await fetch(url, {
      method: "GET",
      headers: {
        Authorization: `Bearer ${accessToken}`,
      },
      cache: "no-store", // `cache: 'no-store'` to ensure we always refetch or handle caching as needed
    });
    if (!res.ok) {
      return null;
    }
    const data = await res.json(); // e.g. { "id": "...", "email": "..." }
    return data.email ?? null;
  } catch {
    return null;
  }
}
