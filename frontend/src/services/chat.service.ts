export async function sendMessage(
  message: string,
  sessionId: string
) {
  console.log("🟡 sendMessage CALLED:", {
    message,
    sessionId,
  });

  const res = await fetch(
    "http://localhost:8000/chat",
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        message,
        session_id: sessionId,
      }),
    }
  );

  console.log("🟢 FETCH DONE:", res);

  const data = await res.json();

  console.log(
    "🔥 RAW BACKEND RESPONSE:",
    data
  );

  return data;
}