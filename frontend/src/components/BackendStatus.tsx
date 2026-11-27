"use client";

import { useEffect, useState } from "react";

import { API_BASE_URL } from "@/lib/api";

type Status = "checking" | "online" | "offline";

/** Small dev helper: shows whether the FastAPI backend answers /health. */
export function BackendStatus() {
  const [status, setStatus] = useState<Status>("checking");

  useEffect(() => {
    fetch(`${API_BASE_URL}/health`)
      .then((res) => setStatus(res.ok ? "online" : "offline"))
      .catch(() => setStatus("offline"));
  }, []);

  const label = {
    checking: "Checking backend…",
    online: "Backend is online",
    offline: "Backend is offline – start it with: uvicorn app.main:app --reload",
  }[status];

  return (
    <p
      role="status"
      className="rounded-md border border-zinc-300 px-4 py-3 text-sm dark:border-zinc-700"
    >
      {label}
    </p>
  );
}
