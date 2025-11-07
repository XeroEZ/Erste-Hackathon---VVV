const BASE_URL = process.env.EXPO_PUBLIC_API_URL;

async function postJson(path: string, body: any, token?: string) {
  const res = await fetch(`${BASE_URL}${path}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
      Accept: "application/json",
    },
    body: JSON.stringify(body),
  });
  if (!res.ok) {
    let msg = `HTTP ${res.status}`;
    try {
      const j = await res.json();
      msg = typeof j?.detail === "string" ? j.detail : JSON.stringify(j);
    } catch {}
    throw new Error(msg);
  }

  try {
    return await res.json();
  } catch {
    return null;
  }
}

// Zmena hesla – uprav path podľa backendu (napr. /api/auth/password/change/)
export async function changePassword(payload: {
  current_password: string;
  new_password: string;
  new_password_confirm: string;
}, token?: string) {
  // token môžeš doplniť z tvojho auth storage a preposlať sem
  return postJson("/api/auth/password/change/", payload, token);
}
