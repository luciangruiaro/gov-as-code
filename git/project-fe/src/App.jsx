import { useCallback, useEffect, useState } from 'react'

const API = import.meta.env.VITE_API_URL ?? 'http://localhost:47102'

// ADR-007 law 3: one page, three states. FR-006 is the message, FR-007 the error.
export default function App() {
  const [state, setState] = useState({ status: 'loading' })

  const load = useCallback(async () => {
    setState({ status: 'loading' })
    try {
      const response = await fetch(`${API}/api/hello`)
      const body = await response.json()
      if (!response.ok) throw new Error(body.error ?? `HTTP ${response.status}`)
      setState({ status: 'ready', message: body.message })
    } catch {
      setState({ status: 'error' })
    }
  }, [])

  useEffect(() => { load() }, [load])

  return (
    <main className="page">
      <section className="card" aria-busy={state.status === 'loading'}>
        <p className="eyebrow">Release 0 · Hello World</p>
        {state.status === 'loading' && <p className="muted" role="status">Loading the greeting…</p>}
        {state.status === 'ready' && <h1 className="greeting">{state.message}</h1>}
        {state.status === 'error' && (
          <div role="alert">
            <h1 className="title">We couldn't load the greeting.</h1>
            <p className="muted">The API or its database isn't answering right now.</p>
            <button className="button" onClick={load}>Try again</button>
          </div>
        )}
        <p className="footnote">Database → API → this page. Styled by the Prodigy Design System.</p>
      </section>
      <ThemeToggle />
    </main>
  )
}

// Light and dark come from the tokens (data-theme on <html>), never from the app's own palette.
function ThemeToggle() {
  const [theme, setTheme] = useState(() =>
    window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light')
  useEffect(() => { document.documentElement.dataset.theme = theme }, [theme])
  const next = theme === 'dark' ? 'light' : 'dark'
  return (
    <button className="toggle" onClick={() => setTheme(next)} aria-label={`Switch to the ${next} theme`}>
      {next === 'dark' ? 'Dark theme' : 'Light theme'}
    </button>
  )
}
