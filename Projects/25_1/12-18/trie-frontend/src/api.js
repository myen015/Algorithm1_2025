const BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8080/api';

// ----- TrieSet -----
export async function setInsert(word) {
    const res = await fetch(`${BASE}/trie-set/insert`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ word })
    });
    if (!res.ok && res.status !== 204) throw new Error('insert failed');
}

export async function setContains(q) {
    const url = new URL(`${BASE}/trie-set/contains`);
    url.searchParams.set('q', q ?? '');
    const res = await fetch(url);
    if (!res.ok) throw new Error('contains failed');
    return res.json(); // boolean
}

export async function setSuggest(q, k = 10) {
    const url = new URL(`${BASE}/trie-set/suggest`);
    url.searchParams.set('q', q ?? '');
    url.searchParams.set('k', String(k));
    const res = await fetch(url);
    if (!res.ok) throw new Error('suggest failed');
    return res.json(); // string[]
}

// ----- TrieMap -----
export async function mapPut(key, value) {
    const res = await fetch(`${BASE}/trie-map/put`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ key, value })
    });
    if (!res.ok && res.status !== 204) throw new Error('put failed');
}

export async function mapGet(key) {
    const url = new URL(`${BASE}/trie-map/get`);
    url.searchParams.set('key', key ?? '');
    const res = await fetch(url);
    if (!res.ok) throw new Error('get failed');
    return res.json(); // { key, value }
}

export async function mapContains(key) {
    const url = new URL(`${BASE}/trie-map/contains`);
    url.searchParams.set('key', key ?? '');
    const res = await fetch(url);
    if (!res.ok) throw new Error('contains failed');
    return res.json(); // { ok: boolean }
}

export async function mapKeys(q, k = 10) {
    const url = new URL(`${BASE}/trie-map/keys`);
    url.searchParams.set('q', q ?? '');
    url.searchParams.set('k', String(k));
    const res = await fetch(url);
    if (!res.ok) throw new Error('keys failed');
    return res.json(); // string[]
}
