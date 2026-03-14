import { useState } from "react";

/** Mock admin dashboard with login gate. */
export function AdminPage() {
  const [authed, setAuthed] = useState(false);
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  if (!authed) {
    return (
      <div className="min-h-screen bg-[#1A1A18] flex items-center justify-center px-6">
        <div className="w-full max-w-sm">
          <h1 className="font-display text-3xl text-white text-center mb-2">
            CropFolio
          </h1>
          <p className="text-[#A3A29D] text-center text-sm mb-10">
            Admin Dashboard
          </p>

          <div className="space-y-4">
            <input
              type="text"
              placeholder="Username"
              defaultValue="admin"
              className="w-full bg-transparent text-white border-b border-white/20 focus:border-primary pb-3 outline-none text-sm placeholder:text-[#A3A29D] transition-colors"
            />
            <input
              type="password"
              placeholder="Password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full bg-transparent text-white border-b border-white/20 focus:border-primary pb-3 outline-none text-sm placeholder:text-[#A3A29D] transition-colors"
            />
            {error && <p className="text-sm text-[#C43B3B]">{error}</p>}
            <button
              onClick={() => {
                if (password === "12345") {
                  setAuthed(true);
                } else {
                  setError("Invalid credentials");
                }
              }}
              className="w-full py-3 bg-primary text-white rounded-lg text-sm uppercase tracking-wide font-medium hover:bg-primary-dark transition-colors mt-4"
            >
              Sign In
            </button>
          </div>

          <p className="text-[#A3A29D] text-xs text-center mt-8">
            Demo credentials: admin / 12345
          </p>
        </div>
      </div>
    );
  }

  return <AdminDashboard onLogout={() => setAuthed(false)} />;
}

/** Mock dashboard after login. */
function AdminDashboard({ onLogout }: { onLogout: () => void }) {
  const metrics = [
    { label: "Townships", value: "25", change: "+0" },
    { label: "Crops", value: "6", change: "+0" },
    { label: "Optimizations", value: "1,247", change: "+23 today" },
    { label: "Reports Generated", value: "892", change: "+12 today" },
  ];

  const activity = [
    {
      time: "2 min ago",
      user: "Extension Worker (Magway)",
      action: "Ran optimization — Rice + Black Gram + Sesame",
      result: "51.3% risk reduction",
    },
    {
      time: "15 min ago",
      user: "Cooperative (Bago)",
      action: "Downloaded PDF report",
      result: "Monsoon season plan",
    },
    {
      time: "1 hr ago",
      user: "NGO Officer (Sagaing)",
      action: "Monte Carlo simulation — 5,000 runs",
      result: "8.2% catastrophic loss",
    },
    {
      time: "3 hrs ago",
      user: "Extension Worker (Ayeyarwady)",
      action: "Climate risk assessment",
      result: "High flood risk detected",
    },
    {
      time: "5 hrs ago",
      user: "Admin",
      action: "Added Kalaw township",
      result: "25 townships total",
    },
  ];

  return (
    <div className="min-h-screen bg-surface">
      <header className="bg-surface-elevated border-b border-border px-6 py-4 flex items-center justify-between">
        <div>
          <h1 className="font-display text-xl text-text-primary">
            CropFolio Admin
          </h1>
          <p className="text-xs text-text-tertiary">Dashboard</p>
        </div>
        <button
          onClick={onLogout}
          className="text-sm text-text-secondary hover:text-text-primary transition-colors"
        >
          Sign Out
        </button>
      </header>

      <main className="max-w-7xl mx-auto px-6 py-8">
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
          {metrics.map((m) => (
            <div
              key={m.label}
              className="bg-surface-elevated rounded-xl border border-border p-6"
            >
              <p className="text-[11px] uppercase tracking-[0.1em] text-text-tertiary">
                {m.label}
              </p>
              <p className="font-data text-3xl text-text-primary mt-2">
                {m.value}
              </p>
              <p className="text-xs text-primary mt-1">{m.change}</p>
            </div>
          ))}
        </div>

        <div className="bg-surface-elevated rounded-xl border border-border p-6">
          <h2 className="font-display text-lg text-text-primary mb-4">
            Recent Activity
          </h2>
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-border">
                  <th className="text-left py-3 text-[11px] uppercase tracking-wide text-text-tertiary font-medium">
                    Time
                  </th>
                  <th className="text-left py-3 text-[11px] uppercase tracking-wide text-text-tertiary font-medium">
                    User
                  </th>
                  <th className="text-left py-3 text-[11px] uppercase tracking-wide text-text-tertiary font-medium">
                    Action
                  </th>
                  <th className="text-left py-3 text-[11px] uppercase tracking-wide text-text-tertiary font-medium">
                    Result
                  </th>
                </tr>
              </thead>
              <tbody>
                {activity.map((row, i) => (
                  <tr key={i} className="border-b border-border-subtle">
                    <td className="py-3 text-text-tertiary font-data text-xs">
                      {row.time}
                    </td>
                    <td className="py-3 text-text-primary">{row.user}</td>
                    <td className="py-3 text-text-secondary">{row.action}</td>
                    <td className="py-3 text-primary font-data text-xs">
                      {row.result}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </main>
    </div>
  );
}
