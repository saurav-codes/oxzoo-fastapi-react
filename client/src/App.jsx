import { useEffect, useState } from "react";

// One template literal on purpose: the bundler must fold the baked greeting into one contiguous string.
const frontendLine = `frontend: hello world oxzoo-fastapi-react_${import.meta.env.GREETING_TAG}`;

export default function App() {
  const [backend, setBackend] = useState({ status: "loading" });

  useEffect(() => {
    let alive = true;
    fetch("/api/greeting")
      .then((res) => {
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        return res.text();
      })
      .then((text) => {
        if (alive) setBackend({ status: "ok", line: text });
      })
      .catch((err) => {
        if (alive) setBackend({ status: "error", line: String(err) });
      });
    return () => {
      alive = false;
    };
  }, []);

  return (
    <main>
      <h1>oxzoo-fastapi-react</h1>
      <p className="line">{frontendLine}</p>
      <p className={"line" + (backend.status === "error" ? " error" : "")}>
        {backend.status === "loading" && "backend: loading…"}
        {backend.status === "ok" && `backend: ${backend.line}`}
        {backend.status === "error" && `backend: error (${backend.line})`}
      </p>
    </main>
  );
}
