import { BackendStatus } from "@/components/BackendStatus";

export default function Home() {
  return (
    <main className="mx-auto flex w-full max-w-2xl flex-1 flex-col justify-center gap-6 px-6 py-16">
      <h1 className="text-4xl font-semibold tracking-tight">Voyage</h1>
      <p className="text-lg text-zinc-600 dark:text-zinc-400">
        AI travel planner. The development environment is ready.
      </p>
      <BackendStatus />
    </main>
  );
}
