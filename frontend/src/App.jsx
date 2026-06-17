import { useState } from "react";

function App() {

  const [showConfirm, setShowConfirm] =
    useState(false);

  const [pendingSQL, setPendingSQL] =
    useState("");

  const [question, setQuestion] =
    useState("");

  const [loading, setLoading] =
    useState(false);

  const [response, setResponse] =
    useState(null);

  const askQuestion = async () => {

    if (!question.trim()) return;

    setLoading(true);

    try {

      const res = await fetch(
        "http://127.0.0.1:8000/chat",
        {
          method: "POST",

          headers: {
            "Content-Type":
              "application/json"
          },

          body: JSON.stringify({
            question
          })
        }
      );

      const data =
        await res.json();

      setResponse(data);

      if (
        data.summary &&
        data.summary.includes(
          "Confirmation required"
        )
      ) {

        setPendingSQL(
          data.sql
        );

        setShowConfirm(
          true
        );
      }

    } catch (err) {

      console.error(err);

    } finally {

      setLoading(false);
    }
  };

  const confirmOperation =
    async () => {

      try {

        const res =
          await fetch(
            "http://127.0.0.1:8000/confirm",
            {

              method: "POST",

              headers: {
                "Content-Type":
                  "application/json"
              },

              body: JSON.stringify({

                sql:
                  pendingSQL
              })
            }
          );

        const data =
          await res.json();

        alert(
          "Operation executed successfully"
        );

        console.log(data);

        setShowConfirm(false);

      } catch (err) {

        console.error(err);

        alert(
          "Failed to execute operation"
        );
      }
    };

  return (

    <div className="container">

      <div className="hero">

        <h1>
          Database Copilot
        </h1>

        <p>
          Natural Language SQL Assistant
        </p>

      </div>

      <div className="input-card">

        <textarea
          placeholder={`
Show all employees

Add employee Alex in Marketing with salary 70000

Update Alex salary to 85000

Delete employee Alex

Delete employees table
`}
          value={question}
          onChange={(e) =>
            setQuestion(
              e.target.value
            )
          }
        />

        <button
          onClick={
            askQuestion
          }
        >
          Generate
        </button>

      </div>

      {loading && (

        <div className="loading">

          Thinking...

        </div>

      )}

      {response && (

        <>

          <div className="card">

            <div className="card-header">

              <h2>
                Generated SQL
              </h2>

              <button
                className="copy-btn"
                onClick={() =>
                  navigator
                    .clipboard
                    .writeText(
                      response.sql
                    )
                }
              >
                Copy
              </button>

            </div>

            <pre>
              {response.sql}
            </pre>

          </div>

          <div className="card">

            <h2>
              Summary
            </h2>

            <div className="summary">

              {response.summary}

            </div>

          </div>

          {response.rows &&
            response.rows.length > 0 && (

              <div className="card">

                <h2>
                  Query Results
                </h2>

                <table>

                  <thead>

                    <tr>

                      {response.columns.map(
                        (column) => (

                          <th
                            key={column}
                          >
                            {column}
                          </th>

                        )
                      )}

                    </tr>

                  </thead>

                  <tbody>

                    {response.rows.map(
                      (
                        row,
                        index
                      ) => (

                        <tr
                          key={index}
                        >

                          {row.map(
                            (
                              cell,
                              i
                            ) => (

                              <td key={i}>
                                {cell}
                              </td>

                            )
                          )}

                        </tr>

                      )
                    )}

                  </tbody>

                </table>

              </div>

            )}

        </>

      )}

      {showConfirm && (

        <div className="modal">

          <div className="modal-content">

            <h2>
              ⚠ Confirm Operation
            </h2>

            <p>

              This action will permanently
              modify your database.

            </p>

            <pre>
              {pendingSQL}
            </pre>

            <div className="modal-buttons">

              <button
                className="confirm-btn"
                onClick={
                  confirmOperation
                }
              >
                Confirm
              </button>

              <button
                className="cancel-btn"
                onClick={() =>
                  setShowConfirm(
                    false
                  )
                }
              >
                Cancel
              </button>

            </div>

          </div>

        </div>

      )}

    </div>
  );
}

export default App;