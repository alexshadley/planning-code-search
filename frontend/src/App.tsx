import React, { useState } from "react";
import logo from "./logo.svg";
import "./App.css";

function App() {
  const [file, setFile] = useState<File | null>(null);
  const [appText, setAppText] = useState<string | null>(null);
  console.log(appText);

  const onUpload = () => {
    const data: any = new FormData();
    data.append("file", file);

    fetch("http://localhost:8000/parse_pdf", {
      method: "POST",
      body: data,
    }).then(async (r) => {
      const body = await r.json();
      setAppText(body["text"]);
    });
  };

  return (
    <div className="App">
      <input
        type="file"
        onChange={(e) => setFile(e.currentTarget.files?.[0] ?? null)}
      />
      <button onClick={onUpload}>Upload</button>
    </div>
  );
}

export default App;
