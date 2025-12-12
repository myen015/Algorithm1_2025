import {useEffect, useMemo, useState} from 'react';
import {
    setInsert, setContains, setSuggest,
    mapPut, mapGet, mapContains, mapKeys
} from './api';

function useDebounce(value, delay = 250) {
    const [v, setV] = useState(value);
    useEffect(() => { const id = setTimeout(() => setV(value), delay); return () => clearTimeout(id); }, [value, delay]);
    return v;
}

export default function App() {
    return (
        <div style={styles.page}>
            <div style={styles.container}>
                <h1 style={{marginBottom: 8}}>Trie Demo</h1>
                <div style={{opacity: .7, marginBottom: 16}}>
                    Backend: Spring Boot • Frontend: React • TrieSet and TrieMap
                </div>
                <div style={styles.grid}>
                    <TrieSetPanel/>
                    <TrieMapPanel/>
                </div>
            </div>
        </div>
    );
}

function TrieSetPanel() {
    const [word, setWord] = useState('');
    const [prefix, setPrefix] = useState('');
    const debPrefix = useDebounce(prefix, 200);

    const [contains, setContainsState] = useState(null);
    const [suggestions, setSuggestions] = useState([]);
    const [k, setK] = useState(10);
    const [loading, setLoading] = useState(false);
    const canInsert = useMemo(() => word.trim().length > 0, [word]);

    useEffect(() => {
        let cancelled = false;
        (async () => {
            setLoading(true);
            try {
                const [c, s] = await Promise.all([
                    setContains(debPrefix),
                    setSuggest(debPrefix, k),
                ]);
                if (!cancelled) { setContainsState(c); setSuggestions(s); }
            } catch {
                if (!cancelled) { setContainsState(null); setSuggestions([]); }
            } finally {
                if (!cancelled) setLoading(false);
            }
        })();
        return () => { cancelled = true; };
    }, [debPrefix, k]);

    const onInsert = async () => {
        await setInsert(word);
        setWord('');
        // обновим список
        const s = await setSuggest(debPrefix, k);
        setSuggestions(s);
    };

    return (
        <div style={styles.card}>
            <h2>TrieSet</h2>

            <div style={styles.label}>Insert word</div>
            <div style={styles.row}>
                <input style={styles.input} placeholder="e.g., apple" value={word} onChange={e => setWord(e.target.value)} />
                <button style={styles.btnPrimary} disabled={!canInsert} onClick={onInsert}>Insert</button>
            </div>

            <div style={styles.label}>Prefix</div>
            <div style={styles.row}>
                <input style={styles.input} placeholder="e.g., app" value={prefix} onChange={e => setPrefix(e.target.value)} />
                <select style={styles.select} value={k} onChange={e => setK(Number(e.target.value))}>
                    {[5,10,20,50].map(n => <option key={n} value={n}>{n}</option>)}
                </select>
                <span style={{opacity:.7}}>{loading ? 'Loading…' : 'Ready'}</span>
            </div>

            <div style={{marginTop: 10}}>
                <div>Contains exact “{debPrefix}”: <b style={{color: contains ? '#10b981' : '#ef4444'}}>{String(!!contains)}</b></div>
            </div>

            <div style={{marginTop: 10}}>
                <div style={styles.suggestBox}>
                    {suggestions.length === 0 && <div style={{opacity:.6}}>No suggestions</div>}
                    {suggestions.map((w, i) => (
                        <button key={i} style={styles.chip} onClick={() => setPrefix(w)}>{w}</button>
                    ))}
                </div>
            </div>
        </div>
    );
}

function TrieMapPanel() {
    const [key, setKey] = useState('');
    const [value, setValue] = useState('');
    const [prefix, setPrefix] = useState('');
    const debPrefix = useDebounce(prefix, 200);

    const [getResp, setGetResp] = useState(null);
    const [containsResp, setContainsResp] = useState(null);
    const [keys, setKeys] = useState([]);
    const [k, setK] = useState(10);
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        let cancelled = false;
        (async () => {
            setLoading(true);
            try {
                const [g, c, ks] = await Promise.all([
                    key ? mapGet(key) : Promise.resolve(null),
                    key ? mapContains(key) : Promise.resolve({ok:null}),
                    mapKeys(debPrefix, k),
                ]);
                if (!cancelled) { setGetResp(g); setContainsResp(c); setKeys(ks); }
            } catch {
                if (!cancelled) { setGetResp(null); setContainsResp({ok:null}); setKeys([]); }
            } finally {
                if (!cancelled) setLoading(false);
            }
        })();
        return () => { cancelled = true; };
    }, [key, debPrefix, k]);

    const onPut = async () => {
        await mapPut(key, value);
        const g = await mapGet(key);
        setGetResp(g);
    };

    return (
        <div style={styles.card}>
            <h2>TrieMap (key → value)</h2>

            <div style={styles.label}>Put (key, value)</div>
            <div style={styles.row}>
                <input style={styles.input} placeholder="key (e.g., cat)" value={key} onChange={e => setKey(e.target.value)} />
                <input style={styles.input} placeholder="value (e.g., animal)" value={value} onChange={e => setValue(e.target.value)} />
                <button style={styles.btnPrimary} disabled={!key.trim()} onClick={onPut}>Put</button>
            </div>

            <div style={styles.row}>
                <span style={{opacity:.7}}>{loading ? 'Loading…' : 'Ready'}</span>
            </div>

            <div style={{marginTop: 10}}>
                <div>Contains “{key}”: <b style={{color: containsResp?.ok ? '#10b981' : '#ef4444'}}>{String(!!containsResp?.ok)}</b></div>
                <div>Get: <code>{getResp ? JSON.stringify(getResp) : 'null'}</code></div>
            </div>

            <div style={{marginTop: 10}}>
                <div style={styles.label}>Keys with prefix</div>
                <div style={styles.row}>
                    <input style={styles.input} placeholder="prefix (e.g., ca)" value={prefix} onChange={e => setPrefix(e.target.value)} />
                    <select style={styles.select} value={k} onChange={e => setK(Number(e.target.value))}>
                        {[5,10,20,50].map(n => <option key={n} value={n}>{n}</option>)}
                    </select>
                </div>
                <div style={styles.suggestBox}>
                    {keys.length === 0 && <div style={{opacity:.6}}>No keys</div>}
                    {keys.map((w, i) => (
                        <button key={i} style={styles.chip} onClick={() => setKey(w)}>{w}</button>
                    ))}
                </div>
            </div>
        </div>
    );
}

const styles = {
    page: {minHeight:'100dvh', background:'#0b1220', color:'#e5e7eb', display:'flex', alignItems:'flex-start', justifyContent:'center', padding:24},
    container: {width:980, maxWidth:'100%', display:'flex', flexDirection:'column'},
    grid: {display:'grid', gridTemplateColumns:'1fr 1fr', gap:16},
    card: {background:'#0f172a', border:'1px solid #1f2937', borderRadius:14, padding:16, boxShadow:'0 8px 24px rgba(0,0,0,.25)'},
    row: {display:'flex', gap:8, alignItems:'center', marginTop:8},
    input: {flex:1, padding:'10px 12px', borderRadius:8, border:'1px solid #334155', background:'#111827', color:'#e5e7eb'},
    select: {padding:'10px 12px', borderRadius:8, border:'1px solid #334155', background:'#111827', color:'#e5e7eb'},
    btnPrimary: {padding:'10px 14px', borderRadius:8, border:'1px solid #0ea5e9', background:'#0ea5e933', color:'#e5e7eb', cursor:'pointer'},
    suggestBox: {display:'flex', gap:8, flexWrap:'wrap', minHeight:40, border:'1px dashed #334155', borderRadius:10, padding:10, marginTop:6},
    chip: {padding:'6px 10px', borderRadius:999, border:'1px solid #334155', background:'#111827', color:'#e5e7eb', cursor:'pointer'},
    label: {marginTop:8, fontSize:12, opacity:.8}
};
