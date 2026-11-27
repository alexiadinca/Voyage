import { render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";

import { BackendStatus } from "./BackendStatus";

describe("BackendStatus", () => {
  afterEach(() => vi.unstubAllGlobals());

  it("shows online when /health responds OK", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue({ ok: true }));
    render(<BackendStatus />);
    expect(await screen.findByText("Backend is online")).toBeInTheDocument();
  });

  it("shows offline when the request fails", async () => {
    vi.stubGlobal("fetch", vi.fn().mockRejectedValue(new Error("network")));
    render(<BackendStatus />);
    expect(await screen.findByText(/Backend is offline/)).toBeInTheDocument();
  });
});
