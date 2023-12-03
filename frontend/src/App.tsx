import React, { useRef, useState } from "react";
import "./App.css";
import check from "./check-circle-svgrepo-com.svg";
import { CircleLoader, PropagateLoader } from "react-spinners";

type Resposne = {
  summary: string;
  relevant_documents: {
    name: string;
    relevance: string;
  };
};

const App = () => {
  const [file, setFile] = useState<File | null>(null);
  const [appText, setAppText] = useState<string | null>(null);

  const [query, setQuery] = useState<string>("");

  const [response, setResponse] = useState<string | null>(null);
  const [responseLoading, setResponseLoading] = useState<boolean>(false);

  const onUpload = (f: File | null) => {
    setFile(f);

    const data: any = new FormData();
    data.append("file", f);

    fetch("http://localhost:8000/parse_pdf", {
      method: "POST",
      body: data,
    }).then(async (r) => {
      const body = await r.json();
      setAppText(body["text"]);
    });
  };

  const onSubmit = () => {
    fetch("http://localhost:8000/query", {
      method: "POST",
      body: JSON.stringify({
        query,
        application: appText ?? "",
      }),
      headers: {
        "Content-Type": "application/json",
      },
    }).then(async (r) => {
      const body = await r.json();
      setResponse(body["response"]);
    });
  };

  return (
    <div
      style={{
        display: "flex",
        justifyContent: "center",
        height: "100vh",
        width: "100vw",
      }}
    >
      <div
        style={{
          display: "flex",
          flexDirection: "column",
          gap: "10px",
          flexBasis: "600px",
        }}
      >
        <UploadBox onUploadFile={onUpload} />
        {appText && (
          <div className="query-box">
            <textarea
              placeholder="Ask PlanningGPT about this application..."
              className="textarea-hide"
              value={query}
              onChange={(e) => setQuery(e.currentTarget.value)}
            />
            <div className="submit-button" onClick={onSubmit}>
              Submit
            </div>
          </div>
        )}
        {response && <div className="shit-response">{response}</div>}
        {responseLoading && <Spinner />}
      </div>
    </div>
  );
};

const UploadBox = ({
  onUploadFile,
}: {
  onUploadFile: (file: File | null) => void;
}) => {
  const inputRef = useRef<null | HTMLInputElement>(null);
  const [fileName, setFileName] = useState<null | string>(null);

  return (
    <div className="file-input-box">
      {fileName ? (
        <div
          style={{
            display: "flex",
            width: "100%",
            justifyContent: "space-between",
          }}
        >
          <div>{fileName}</div>
          <img src={check} width="25px" className="filter-green" />
        </div>
      ) : (
        <div
          className="file-input-button"
          onClick={() => inputRef.current?.click()}
        >
          Upload application
        </div>
      )}
      <input
        ref={inputRef}
        style={{ display: "none" }}
        type="file"
        onChange={(e) => {
          onUploadFile(e.currentTarget.files?.[0] ?? null);
          setFileName(e.currentTarget.files?.[0].name ?? null);
        }}
      />
    </div>
  );
};

const Spinner = ({ text }: { text?: string }) => {
  return (
    <div
      style={{ display: "flex", justifyContent: "center", paddingTop: "50px" }}
    >
      <PropagateLoader color="#069108" size={15} />
      {text && <div>{text}</div>}
    </div>
  );
};

export default App;
