import Image from "next/image";

export default function Home() {
  return (
    <div className="grid grid-rows-[20px_1fr_20px] items-center justify-items-center min-h-screen p-8 pb-20 gap-16 sm:p-20 font-[family-name:var(--font-geist-sans)]">
      <main className="min-h-screen flex flex-col items-center justify-center gap-6 px-4 text-center">
      <h1 className="text-4xl sm:text-5xl font-bold">
        Canada-First Net-Worth Tracker
      </h1>
      <p className="max-w-xl">
        Instantly see your real TFSA, RRSP & FHSA room — no spreadsheets, no
        guesswork.
      </p>

      {/* wait-list form */}
      <form
        action="https://tally.so/r/abc123"   /* ← paste your ID */
        method="POST"
        className="flex flex-col sm:flex-row gap-3 w-full max-w-md"
      >
        <input
          name="email"
          type="email"
          required
          placeholder="Email address"
          className="flex-1 border px-3 py-2 rounded"
        />
        <button className="bg-black text-white px-4 py-2 rounded">
          Join wait-list
        </button>
      </form>
    </main>
    </div>
  );
}
