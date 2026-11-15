const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

export async function apiRequest<T>(path: string, init: RequestInit = {}): Promise<T> {
  const response = await fetch(`${API_URL}${path}`, {
    ...init,
    headers: { "Content-Type": "application/json", ...init.headers }
  });
  if (!response.ok) {
    const detail = await response.text();
    throw new Error(detail || `API request failed (${response.status})`);
  }
  return response.json() as Promise<T>;
}
