import React, { useState, useEffect } from "react";
import "./App.css";
import { PropagateLoader } from "react-spinners";

type Response = {
  answer: string;
  relevant_documents: {
    name: string;
    relevance: string;
    rid: string;
  }[];
};

const App = () => {
  // const [file, setFile] = useState<File | null>(null);
  // const [appText, setAppText] = useState<string | null>(null);
  const [placeholder, setPlaceholder] = useState('');
  const [query, setQuery] = useState<string>("");
  const [isFocused, setIsFocused] = useState(false);

   useEffect(() => {
     const phrases = [
       'How is 387 Market zoned?',
       'Where can I build the tallest building?',
       'How can I lose my minigolf permit?'
     ];
     let currentPhraseIndex = 0;
     let charIndex = -1;
     let direction = 'forward';
     let interval: ReturnType<typeof setInterval>;

     const startTypingAnimation = () => {
      interval = setInterval(() => {
       if (direction === 'forward') {
         if (charIndex < phrases[currentPhraseIndex].length - 1) {
           charIndex++;
           setPlaceholder(prev => prev + phrases[currentPhraseIndex][charIndex]);
         } else {
            setTimeout(() => {
            direction = 'backward';
            charIndex--;
             }, 100); // Pause at the end of a phrase
           }
       } else {
         if (charIndex > 0) {
           setPlaceholder(prev => prev.slice(0, -1));
           charIndex--;
         } else {
           setPlaceholder(''); // Clear the placeholder before starting new phrase
           direction = 'forward';
           currentPhraseIndex = (currentPhraseIndex + 1) % phrases.length;
           charIndex = -1;
         }
       }
     }, 50); // Speed of typing animation
    };

     if (!isFocused) {
       startTypingAnimation();
     }

     return () => clearInterval(interval);
   }, [isFocused]);

  const [response, setResponse] = useState<Response | null>(null);
  // const [answer, setAnswer] = useState<string | null>(null);
  const [responseLoading, setResponseLoading] = useState<boolean>(false);

  // const onUpload = (f: File | null) => {
  //   setFile(f);

  //   const data: any = new FormData();
  //   data.append("file", f);

  //   fetch("/api/parse_pdf", {
  //     method: "POST",
  //     body: data,
  //   }).then(async (r) => {
  //     const body = await r.json();
  //     setAppText(body["text"]);
  //   });
  // };

  const onSubmit = () => {
    setResponseLoading(true);
    fetch("/api/query", {
      method: "POST",
      body: JSON.stringify({
        query,
      }),
      headers: {
        "Content-Type": "application/json",
      },
    }).then(async (r) => {
      const body = await r.json();
      setResponse(body["answer"]);
      setResponseLoading(false);
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
        <h1>PlanningGPT</h1>
        <div>
          Interact with the SF Planning Code. A project by Alex Shadley, Jacob
          Marshall, and Salim Damerdji. If you have feedback email me at
          shadleyalex@gmail.com
        </div>
        <div className="query-box">
          <textarea
            placeholder={placeholder}
            className="textarea-hide"
            value={query}
            onChange={(e) => setQuery(e.currentTarget.value)}
            onFocus={() => {setIsFocused(true); setPlaceholder('');}}
            onBlur={() => setIsFocused(false)}
          />
          <div className="submit-button" onClick={onSubmit}>
            Submit
          </div>
        </div>
        {/* {answer && <div className="shit-response">{answer}</div>} */}
        {response && (
          <>
            <div className="shit-response">{response["answer"]}</div>

            {response["relevant_documents"].map((d) => (
              <div className="shit-response">
                {
                  <>
                    <a
                      target="_blank"
                      href={`https://codelibrary.amlegal.com/codes/san_francisco/latest/sf_planning/${d.rid}`}
                      rel="noreferrer"
                    >
                      {d["name"]}:
                    </a>
                    {d["relevance"]}
                  </>
                }
              </div>
            ))}
          </>
        )}
        {responseLoading && <Spinner />}
      </div>
    </div>
  );
};

// const UploadBox = ({
//   onUploadFile,
// }: {
//   onUploadFile: (file: File | null) => void;
// }) => {
//   const inputRef = useRef<null | HTMLInputElement>(null);
//   const [fileName, setFileName] = useState<null | string>(null);

//   return (
//     <div className="file-input-box">
//       {fileName ? (
//         <div
//           style={{
//             display: "flex",
//             width: "100%",
//             justifyContent: "space-between",
//           }}
//         >
//           <div>{fileName}</div>
//           <img src={check} width="25px" className="filter-green" />
//         </div>
//       ) : (
//         <div
//           className="file-input-button"
//           onClick={() => inputRef.current?.click()}
//         >
//           Upload application
//         </div>
//       )}
//       <input
//         ref={inputRef}
//         style={{ display: "none" }}
//         type="file"
//         onChange={(e) => {
//           onUploadFile(e.currentTarget.files?.[0] ?? null);
//           setFileName(e.currentTarget.files?.[0].name ?? null);
//         }}
//       />
//     </div>
//   );
// };

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
