import { useCallback, useEffect, useRef, useState } from 'react'
import './App.css'
import { api, API_BASE } from './services/api'

const ATTACKS = {
  traffic: { name: 'Traffic Signal Manipulation', short: 'TRAFFIC SIGNALS', target: 'SUMO junction', icon: '🚦', description: 'Observe signal phase and queue manipulation in the city traffic simulator.' },
  cctv: { name: 'CCTV Session Compromise', short: 'CCTV SECURITY', target: 'CAM-01 / CAM-02 / CAM-03', icon: '▣', description: 'Demonstrate unauthorized camera authentication and session containment.' },
  scada: { name: 'SCADA Control Manipulation', short: 'SCADA CONTROL', target: 'OpenPLC / Modbus TCP', icon: '⌁', description: 'Inspect unauthorized PLC writes and the resulting defensive response.' },
  network: { name: 'Rogue Access Point Simulation', short: 'PUBLIC NETWORK', target: 'SMARTCITY_PUBLIC', icon: '⌁', description: 'Compare authorized and observed network identity in the local simulator.' },
  api: { name: 'Unauthorized Admin API Access', short: 'ADMIN API', target: 'OWASP Juice Shop', icon: '◈', description: 'Review the local administrative API exposure and detector evidence.' },
}
const CAMERA_IDS = ['CAM-01', 'CAM-02', 'CAM-03']

function pathFor(type, id) { return `/${type}/${id}` }
function readRoute() {
  const path = window.location.pathname.replace(/\/+$/, '') || '/'
  if (path === '/cctv') return { view: 'cctv' }
  const match = path.match(/^\/(attack|soc)\/(traffic|cctv|scada|network|api)$/)
  return match ? { view: match[1], id: match[2] } : { view: 'dashboard' }
}
function navigate(path) {
  window.history.pushState({}, '', path)
  window.dispatchEvent(new PopStateEvent('popstate'))
}
function Status({ value, tone }) {
  const text = value == null ? 'UNKNOWN' : String(value).replaceAll('_', ' ')
  return <span className={`status ${tone || (/online|ready|completed|contained|normal/i.test(text) ? 'good' : /fail|error|offline|high|critical/i.test(text) ? 'bad' : 'warn')}`}>{text}</span>
}
function compactValue(value) {
  if (value == null || value === '') return ''
  if (typeof value !== 'object') return String(value).replaceAll('_', ' ')
  return Object.entries(value).map(([key, item]) => `${key.replaceAll('_', ' ')}: ${compactValue(item)}`).join(' · ')
}
function DataBlock({ title, value }) {
  if (value == null || value === '') return null
  return <div className="data-block"><label>{title}</label><pre>{typeof value === 'object' ? JSON.stringify(value, null, 2) : String(value)}</pre></div>
}

function Header({ route }) {
  return <header className="topbar">
    <button className="brand" onClick={() => navigate('/')}><span className="brand-mark">✦</span><span><b>SMARTCITY-X</b><small>CYBER OPERATIONS CENTER</small></span></button>
    <nav><button className={route.view === 'dashboard' ? 'active' : ''} onClick={() => navigate('/')}>Dashboard</button>{route.view === 'cctv' && <><span>/</span><button className="active" onClick={() => navigate('/cctv')}>CCTV monitor</button></>}{route.id && <><span>/</span><button className={route.view === 'attack' ? 'active' : ''} onClick={() => navigate(pathFor('attack', route.id))}>Attack</button><span>/</span><button className={route.view === 'soc' ? 'active' : ''} onClick={() => navigate(pathFor('soc', route.id))}>SOC response</button></>}</nav>
    <div className="connection"><i /> API {API_BASE.replace(/^https?:\/\//, '')}</div>
  </header>
}

function Health() {
  const [state, setState] = useState({ loading: true, data: null, error: '' })
  useEffect(() => {
    let live = true
    api.health().then((data) => live && setState({ loading: false, data, error: '' })).catch((error) => live && setState({ loading: false, data: null, error: error.message }))
    return () => { live = false }
  }, [])
  const serviceStatus = state.data?.status
  return <section className="health panel"><div className="section-title"><span>SYSTEM STATUS</span><span className="muted">{state.loading ? 'CHECKING…' : state.error ? 'BACKEND OFFLINE' : 'LIVE'}</span></div>{state.error ? <div className="offline">● BACKEND OFFLINE <small>{state.error}</small></div> : state.data && <div className="health-grid"><div className="health-item"><i className={/online|ready|ok/i.test(String(serviceStatus)) ? 'up' : 'down'} />{state.data.service || 'Backend'} <Status value={serviceStatus} /></div><div className="health-item"><span className="muted">LAST CHECK</span> {state.data.timestamp}</div></div>}</section>
}

function AttackCard({ id, config, saveResult }) {
  const [busy, setBusy] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState('')
  async function launch() {
    setBusy(true); setError('')
    try { const data = await api.attack(id); setResult(data); saveResult(id, data) } catch (launchError) { setError(launchError.message) } finally { setBusy(false) }
  }
  const status = result?.final_state?.status || result?.execution_status || result?.attack?.result?.status || 'NORMAL'
  const incident = result?.soc?.incident
  return <article className="attack-card panel"><div className="card-head"><span className="attack-icon">{config.icon}</span><span className="eyebrow">{config.short}</span><Status value={status} /></div><h2>{config.name}</h2><p className="target">TARGET <b>{config.target}</b></p><p>{config.description}</p>{error && <div className="error">{error}</div>}{result && <div className="result-summary" aria-label="Actual attack result"><div><span>EXECUTION</span><b>{compactValue(result.execution_status || result.attack?.result?.status)}</b></div>{result.final_state != null && <div><span>FINAL STATE</span><b>{compactValue(result.final_state)}</b></div>}{incident != null && <div><span>INCIDENT</span><b>{compactValue(incident)}</b></div>}</div>}<div className="card-actions"><button className="primary" disabled={busy} onClick={launch}>{busy ? 'ATTACK IN PROGRESS…' : 'LAUNCH ATTACK'}</button><button onClick={() => navigate(pathFor('soc', id))}>VIEW SOC</button></div>{result && <button className="result-link" onClick={() => navigate(pathFor('attack', id))}>VIEW EXECUTION RESULT →</button>}</article>
}

function Dashboard({ saveResult }) {
  return <><div className="hero"><div><p className="eyebrow">SMART CITY / THREAT SIMULATION</p><h1>Operational <em>visibility</em><br />for a connected city.</h1><p className="lede">Run isolated attack scenarios, inspect real telemetry, and follow the evidence through detection to containment.</p></div><div className="hero-readout"><span>ACTIVE SURFACES</span><strong>05</strong><small>LOCAL SIMULATION ENVIRONMENT</small></div></div><Health /><div className="section-title surface-title"><span>ATTACK SURFACES</span><span className="muted">SELECT A SCENARIO TO BEGIN</span></div><div className="cards">{Object.entries(ATTACKS).map(([id, config]) => <AttackCard id={id} config={config} saveResult={saveResult} key={id} />)}</div></>
}

function Result({ id, mode, cachedResult, saveResult }) {
  const config = ATTACKS[id]
  const [state, setState] = useState({ loading: false, data: cachedResult || null, error: '' })
  const shouldUseCacheOnly = id === 'cctv'
  const run = useCallback(() => {
    if (shouldUseCacheOnly) return
    setState((current) => ({ ...current, loading: true, error: '' }))
    api.attack(id).then((data) => { saveResult(id, data); setState({ loading: false, data, error: '' }) }).catch((error) => setState({ loading: false, data: null, error: error.message }))
  }, [id, saveResult, shouldUseCacheOnly])
  useEffect(() => {
    if (cachedResult || shouldUseCacheOnly) return
    let live = true
    api.attack(id).then((data) => {
      if (live) {
        saveResult(id, data)
        setState({ loading: false, data, error: '' })
      }
    }).catch((error) => live && setState({ loading: false, data: null, error: error.message }))
    return () => { live = false }
  }, [cachedResult, id, saveResult, shouldUseCacheOnly])
  const data = state.data
  if (state.loading) return <div className="loading panel"><span className="spinner" /> CONTACTING FLASK ORCHESTRATOR…</div>
  if (state.error) return <div className="error-panel panel"><h2>BACKEND OFFLINE</h2><p>{state.error}</p><button onClick={run}>RETRY</button></div>
  if (!data) return <div className="error-panel panel"><h2>NO COMPLETED CCTV ATTACK</h2><p>Launch the CCTV attack from the dashboard or CCTV monitor before opening SOC response.</p><button onClick={() => navigate(id === 'cctv' ? '/cctv' : '/')}>RETURN</button></div>
  const attack = data.attack || {}; const result = attack.result || {}; const detection = data.detection || {}; const soc = data.soc || {}
  return <div className="result-page"><div className="page-heading"><div><p className="eyebrow">{mode === 'soc' ? 'SOC / INCIDENT REVIEW' : 'ATTACK / EXECUTION TRACE'}</p><h1>{config.name}</h1><p className="target">TARGET <b>{config.target}</b></p></div><Status value={soc.status || data.execution_status} /></div><div className="flow"><span>NORMAL STATE</span><b>→</b><span className="highlight">ATTACK IMPACT</span><b>→</b><span>SOC DETECTION</span><b>→</b><span>SOC RESPONSE</span></div><div className="result-grid"><section className="panel result-section"><div className="section-title">ATTACK EXECUTION</div><DataBlock title="Status" value={result.status} /><DataBlock title="Execution evidence" value={result.stdout || result.stderr} /><DataBlock title="Telemetry" value={result.telemetry} /></section><section className="panel result-section"><div className="section-title">DETECTION</div><DataBlock title="Detector status" value={detection.status} /><DataBlock title="Detection evidence" value={detection.stdout || detection.telemetry} /></section><section className="panel result-section"><div className="section-title">SOC RESPONSE</div><DataBlock title="SOC status" value={soc.status} /><DataBlock title="Response evidence" value={soc.stdout || soc.stderr} /><DataBlock title="Incident" value={soc.incident} /></section><section className="panel result-section"><div className="section-title">FINAL STATE</div><DataBlock title="Backend final state" value={data.final_state} /></section></div>{mode === 'attack' && <button className="primary result-next" onClick={() => navigate(pathFor('soc', id))}>OPEN SOC RESPONSE →</button>}</div>
}

function CameraPanel({ camera, videoRef }) {
  const interrupted = camera?.stream === 'INTERRUPTED'
  return <article className={`camera-panel panel ${interrupted ? 'camera-panel-interrupted' : ''}`}><div className="camera-heading"><div><p className="eyebrow">SURVEILLANCE NODE</p><h2>{camera?.id}</h2><p className="camera-location">{camera?.location || 'Location unavailable'}</p></div><Status value={camera?.status} /></div><div className="video-frame"><video ref={videoRef} src={`${API_BASE}/api/cctv/${camera?.id}/video`} autoPlay muted loop playsInline aria-label={`${camera?.id} live CCTV feed`} />{interrupted && <div className="stream-overlay">STREAM INTERRUPTED</div>}</div><dl className="camera-state"><div><dt>AUTHENTICATION</dt><dd><Status value={camera?.authentication} /></dd></div><div><dt>SESSION</dt><dd><Status value={camera?.session} /></dd></div><div><dt>STREAM</dt><dd><Status value={camera?.stream} /></dd></div></dl></article>
}

function CctvMonitor({ saveResult, cachedResult }) {
  const [cameras, setCameras] = useState({})
  const [loading, setLoading] = useState(true)
  const [attackInProgress, setAttackInProgress] = useState(false)
  const [error, setError] = useState('')
  const [attackResult, setAttackResult] = useState(cachedResult || null)
  const videoRefs = useRef({})
  const fetchCameraStates = useCallback(async () => Object.fromEntries(await Promise.all(CAMERA_IDS.map(async (id) => [id, await api.camera(id)]))), [])
  useEffect(() => { let live = true; fetchCameraStates().then((states) => live && setCameras(states)).catch((loadError) => live && setError(loadError.message)).finally(() => live && setLoading(false)); return () => { live = false } }, [fetchCameraStates])
  useEffect(() => { if (cameras['CAM-01']?.stream === 'INTERRUPTED') videoRefs.current['CAM-01']?.pause() }, [cameras])
  async function launchAttack() {
    setAttackInProgress(true); setError('')
    try { const result = await api.attack('cctv'); setAttackResult(result); saveResult('cctv', result); setCameras(await fetchCameraStates()) } catch (attackError) { setError(attackError.message) } finally { setAttackInProgress(false) }
  }
  async function resetCamera() {
    setError('')
    try { await api.resetCamera('CAM-01'); setCameras(await fetchCameraStates()); setAttackResult(null); saveResult('cctv', null) } catch (resetError) { setError(resetError.message) }
  }
  return <div className="cctv-page"><section className="monitor-header"><div><p className="eyebrow">PHASE 3E / AUTHENTICATED VIDEO SURVEILLANCE</p><h1>CCTV monitor</h1><p className="monitor-copy">Live camera state is read from the orchestration backend. The attack control operates only on the local simulator.</p></div><div className="monitor-actions"><button className="attack-button" type="button" onClick={launchAttack} disabled={attackInProgress || loading}>{attackInProgress ? 'ATTACK IN PROGRESS...' : 'LAUNCH CCTV ATTACK'}</button><button className="reset-button" type="button" onClick={resetCamera} disabled={attackInProgress}>RESET CAM-01</button></div></section>{error && <div className="error-banner" role="alert">BACKEND OFFLINE / {error}</div>}{loading ? <div className="loading-state">LOADING CCTV STATE...</div> : <section className="camera-grid">{CAMERA_IDS.map((id) => <CameraPanel key={id} camera={cameras[id]} videoRef={(element) => { videoRefs.current[id] = element }} />)}</section>}{attackResult && <Result id="cctv" mode="attack" cachedResult={attackResult} saveResult={saveResult} />}</div>
}

export default function App() {
  const [route, setRoute] = useState(readRoute())
  const [results, setResults] = useState({})
  const saveResult = useCallback((id, result) => setResults((current) => ({ ...current, [id]: result })), [])
  useEffect(() => { const handler = () => setRoute(readRoute()); window.addEventListener('popstate', handler); return () => window.removeEventListener('popstate', handler) }, [])
  return <div className="app"><Header route={route} /><main>{route.view === 'dashboard' && <Dashboard saveResult={saveResult} />}{route.view === 'cctv' && <CctvMonitor saveResult={saveResult} cachedResult={results.cctv} />}{route.id && <Result id={route.id} mode={route.view} cachedResult={results[route.id]} saveResult={saveResult} />}</main><footer>SMARTCITY-X // EDUCATIONAL CYBER ATTACK &amp; THREAT DETECTION SIMULATOR <span>FLASK API • LOCAL ONLY</span></footer></div>
}
