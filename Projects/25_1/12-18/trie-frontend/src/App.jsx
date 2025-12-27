import { useMemo, useState } from "react";

const API_BASE = "http://192.168.1.213:8080/api";

function colorForCluster(clusterId) {
    const palette = [
        "#ef4444", "#3b82f6", "#22c55e", "#a855f7",
        "#f97316", "#14b8a6", "#f59e0b", "#ec4899",
        "#6366f1", "#10b981",
    ];
    if (clusterId == null || Number.isNaN(clusterId)) return "#9ca3af";
    return palette[Math.abs(clusterId) % palette.length];
}

function normalizeVizResponse(data) {
    if (!data) return { clusters: [], points: [] };
    if (Array.isArray(data)) {
        // legacy: points array
        return { clusters: [], points: data };
    }
    return {
        clusters: Array.isArray(data.clusters) ? data.clusters : [],
        points: Array.isArray(data.points) ? data.points : [],
    };
}

function Scatter2D({ data }) {
    const { clusters, points } = useMemo(() => normalizeVizResponse(data), [data]);

    if (!data) return <div className="placeholder">No visualization yet. Click "Load 2D".</div>;
    if (!points.length) return <div className="placeholder">No points to visualize.</div>;

    const xs = [];
    const ys = [];

    for (const p of points) {
        if (typeof p.x === "number") xs.push(p.x);
        if (typeof p.y === "number") ys.push(p.y);
    }
    for (const c of clusters) {
        if (typeof c.x === "number") xs.push(c.x);
        if (typeof c.y === "number") ys.push(c.y);
    }

    const minX = Math.min(...xs);
    const maxX = Math.max(...xs);
    const minY = Math.min(...ys);
    const maxY = Math.max(...ys);

    const W = 820; // viewBox width
    const H = 420; // viewBox height
    const P = 28;  // padding

    // Map coordinate to SVG space
    const sx = (v) => {
        if (!Number.isFinite(minX) || !Number.isFinite(maxX) || minX === maxX) return W / 2;
        return P + ((v - minX) / (maxX - minX)) * (W - 2 * P);
    };
    const sy = (v) => {
        if (!Number.isFinite(minY) || !Number.isFinite(maxY) || minY === maxY) return H / 2;
        // invert Y for SVG
        return H - (P + ((v - minY) / (maxY - minY)) * (H - 2 * P));
    };

    const clusterIds = Array.from(new Set(points.map((p) => p.cluster))).sort((a, b) => a - b);

    return (
        <div>
            <div className="viz-canvas">
                <svg viewBox={`0 0 ${W} ${H}`} width="100%" height="100%">
                    {/* points */}
                    {points.map((p) => (
                        <circle
                            key={`p-${p.index}`}
                            cx={sx(p.x)}
                            cy={sy(p.y)}
                            r="4"
                            fill={colorForCluster(p.clusterId)}
                            opacity="0.75"
                        >
                            <title>{`#${p.index} | cluster ${p.clusterId}\n(${p.x?.toFixed?.(2)}, ${p.y?.toFixed?.(2)})`}</title>
                        </circle>
                    ))}

                    {/* centroids */}
                    {clusters.map((c) => (
                        <rect
                            key={`c-${c.clusterId}`}
                            x={sx(c.x) - 6}
                            y={sy(c.y) - 6}
                            width="12"
                            height="12"
                            fill={colorForCluster(c.clusterId)}
                            stroke="rgba(255,255,255,0.9)"
                            strokeWidth="1"
                            opacity="0.95"
                        >
                            <title>{`Centroid ${c.clusterId}\n(${c.x?.toFixed?.(2)}, ${c.y?.toFixed?.(2)})`}</title>
                        </rect>
                    ))}
                </svg>
            </div>

            <div className="legend">
                {clusterIds.map((id) => (
                    <div key={id} className="legend-item">
                        <span className="legend-dot" style={{ background: colorForCluster(id) }} />
                        <span>Cluster {id}</span>
                    </div>
                ))}
            </div>
        </div>
    );
}

function Table3D({ data }) {
    const { points } = useMemo(() => normalizeVizResponse(data), [data]);

    if (!data) return <div className="placeholder">No visualization yet. Click "Load 3D".</div>;
    if (!points.length) return <div className="placeholder">No points to visualize.</div>;

    return (
        <div className="table3d-wrapper">
            <table className="table3d">
                <thead>
                <tr>
                    <th>#</th>
                    <th>x</th>
                    <th>y</th>
                    <th>z</th>
                    <th>cluster</th>
                </tr>
                </thead>
                <tbody>
                {points.slice(0, 120).map((p) => (
                    <tr key={p.index}>
                        <td>{p.index}</td>
                        <td>{Number(p.x).toFixed(2)}</td>
                        <td>{Number(p.y).toFixed(2)}</td>
                        <td>{Number(p.z).toFixed(2)}</td>
                        <td>
                <span className="cluster-pill" style={{ background: colorForCluster(p.clusterId) }}>
                  {p.clusterId}
                </span>
                        </td>
                    </tr>
                ))}
                </tbody>
            </table>

            {points.length > 120 && (
                <div className="placeholder" style={{ marginTop: 8 }}>
                    Showing first 120 points of {points.length}.
                </div>
            )}
        </div>
    );
}

export default function App() {
    const [isInited, setIsInited] = useState(false);
    const [initInfo, setInitInfo] = useState(null);
    const [loadingInit, setLoadingInit] = useState(false);

    const [semanticQuery, setSemanticQuery] = useState("");
    const [semanticTopK, setSemanticTopK] = useState(10);
    const [semanticResults, setSemanticResults] = useState([]);
    const [searchLoading, setSearchLoading] = useState(false);

    const [clusters, setClusters] = useState([]);
    const [selectedCluster, setSelectedCluster] = useState(null);
    const [clusterItems, setClusterItems] = useState([]);
    const [clusterLoading, setClusterLoading] = useState(false);

    const [vizMode, setVizMode] = useState("2d");
    const [viz2D, setViz2D] = useState(null);
    const [viz3D, setViz3D] = useState(null);
    const [vizLoading, setVizLoading] = useState(false);

    const [error, setError] = useState(null);

    async function loadClusters() {
        const res = await fetch(`${API_BASE}/clusters`);
        if (!res.ok) throw new Error("Failed to load clusters");
        const data = await res.json();

        // Accept either: [0,1,2] or { clusters: [0,1,2] }
        if (Array.isArray(data)) return data;
        if (data && Array.isArray(data.clusters)) return data.clusters;

        console.warn("Unexpected /clusters response:", data);
        return [];
    }


    async function handleInit() {
        setError(null);
        setLoadingInit(true);
        setSelectedCluster(null);
        setClusterItems([]);
        setSemanticResults([]);
        setViz2D(null);
        setViz3D(null);

        try {
            const res = await fetch(`${API_BASE}/load-from-resources`, { method: "POST" });
            if (!res.ok) throw new Error("Failed to init data");
            const info = await res.json();

            const cls = await loadClusters();

            setInitInfo(info);
            setClusters(cls);
            setIsInited(true);
        } catch (e) {
            console.error(e);
            setError(e.message || "Init error");
        } finally {
            setLoadingInit(false);
        }
    }

    async function handleSearchSubmit(e) {
        e.preventDefault();
        if (!semanticQuery.trim()) {
            setSemanticResults([]);
            return;
        }

        setError(null);
        setSearchLoading(true);

        try {
            const params = new URLSearchParams({
                q: semanticQuery,
                k: String(semanticTopK),
            });

            const res = await fetch(`${API_BASE}/search/semantic?${params}`);
            if (!res.ok) throw new Error("Search failed");
            const data = await res.json();

            setSemanticResults(Array.isArray(data) ? data : []);
        } catch (e) {
            console.error(e);
            setError(e.message || "Search error");
        } finally {
            setSearchLoading(false);
        }
    }

    async function handleClusterClick(clusterId) {
        setSelectedCluster(clusterId);
        setClusterItems([]);
        setClusterLoading(true);
        setError(null);

        try {
            const params = new URLSearchParams({
                id: String(clusterId),
                k: "30",
            });

            const res = await fetch(`${API_BASE}/search/by-cluster?${params}`);
            if (!res.ok) throw new Error("Failed to load cluster items");
            const data = await res.json();

            setClusterItems(Array.isArray(data) ? data : []);
        } catch (e) {
            console.error(e);
            setError(e.message || "Cluster items error");
        } finally {
            setClusterLoading(false);
        }
    }

    async function handleLoadViz(mode) {
        setError(null);
        setVizLoading(true);

        try {
            const endpoint = mode === "3d" ? "/visualize/3d" : "/visualize/2d";
            const res = await fetch(`${API_BASE}${endpoint}`);
            if (!res.ok) throw new Error("Failed to load visualization");
            const data = await res.json();

            if (mode === "3d") {
                setViz3D(data);
                setVizMode("3d");
            } else {
                setViz2D(data);
                setVizMode("2d");
            }
        } catch (e) {
            console.error(e);
            setError(e.message || "Visualization error");
        } finally {
            setVizLoading(false);
        }
    }

    return (
        <div className="app">
            <div className="app-header">
                <h1>Triemap Demo</h1>

                <button className="init-button" onClick={handleInit} disabled={loadingInit}>
                    {loadingInit ? "Loading..." : isInited ? "Re-load" : "Load data"}
                </button>

                {initInfo && (
                    <div className="init-info">
                        Items: <b>{initInfo.items}</b> · Clusters: <b>{initInfo.kClusters}</b>
                    </div>
                )}
            </div>

            {error && <div className="error-box">{error}</div>}

            <div className="main-grid">
                {/* LEFT COLUMN */}
                <div className="column">
                    <h2 style={{ marginTop: 0 }}>Semantic search</h2>

                    <form className="search-form" onSubmit={handleSearchSubmit}>
                        <input
                            className="search-input"
                            placeholder="Type a query..."
                            value={semanticQuery}
                            onChange={(e) => setSemanticQuery(e.target.value)}
                        />

                        <input
                            className="search-input"
                            style={{ width: 90 }}
                            type="number"
                            min={1}
                            max={100}
                            value={semanticTopK}
                            onChange={(e) => setSemanticTopK(Number(e.target.value) || 1)}
                        />

                        <button className="primary-button" type="submit" disabled={!isInited || searchLoading}>
                            {searchLoading ? "Searching..." : "Search"}
                        </button>
                    </form>

                    <div className="results-box">
                        {!isInited && <div className="placeholder">Initialize data first.</div>}
                        {isInited && semanticResults.length === 0 && !searchLoading && (
                            <div className="placeholder">No results yet.</div>
                        )}

                        {semanticResults.map((r, idx) => (
                            <div className="result-item" key={r.id ?? idx}>
                                <div className="result-text">{r.text}</div>
                                <div className="result-meta">
                                    <span>cluster: {r.clusterId}</span>
                                    {"similarity" in r ? <span>sim: {Number(r.similarity).toFixed(3)}</span> : <span />}
                                </div>
                            </div>
                        ))}
                    </div>
                </div>

                {/* RIGHT COLUMN */}
                <div className="column">
                    <div className="cluster-header">
                        <h2 className="cluster-title">Clusters</h2>
                        <button
                            className="small-button"
                            onClick={() => handleLoadViz("2d")}
                            disabled={!isInited || vizLoading}
                            title="Load 2D visualization"
                        >
                            {vizLoading && vizMode === "2d" ? "Loading..." : "Load 2D"}
                        </button>
                        <button
                            className="small-button"
                            onClick={() => handleLoadViz("3d")}
                            disabled={!isInited || vizLoading}
                            title="Load 3D visualization"
                        >
                            {vizLoading && vizMode === "3d" ? "Loading..." : "Load 3D"}
                        </button>
                    </div>

                    <div className="cluster-list">
                        {Array.isArray(clusters) && clusters.map((cid) => (
                            <button
                                key={cid}
                                className={"cluster-button" + (selectedCluster === cid ? " active" : "")}
                                onClick={() => handleClusterClick(cid)}
                                disabled={!isInited}
                            >
                                Cluster {cid}
                            </button>
                        ))}
                    </div>

                    {/* Visualization block */}
                    <div style={{ marginBottom: 12 }}>
                        <div className="viz-tabs">
                            <button
                                className={"viz-tab" + (vizMode === "2d" ? " active" : "")}
                                onClick={() => setVizMode("2d")}
                            >
                                2D
                            </button>
                            <button
                                className={"viz-tab" + (vizMode === "3d" ? " active" : "")}
                                onClick={() => setVizMode("3d")}
                            >
                                3D
                            </button>
                        </div>

                        {vizMode === "2d" ? <Scatter2D data={viz2D} /> : <Table3D data={viz3D} />}
                    </div>

                    <div className="results-box">
                        {!selectedCluster && <div className="placeholder">Select a cluster to view items.</div>}
                        {clusterLoading && <div className="placeholder">Loading cluster items...</div>}

                        {!clusterLoading &&
                            selectedCluster != null &&
                            clusterItems.map((it, idx) => (
                                <div className="result-item" key={it.id ?? idx}>
                                    <div className="result-text">{it.text}</div>
                                    <div className="result-meta">
                                        <span>cluster: {it.clusterId}</span>
                                        <span />
                                    </div>
                                </div>
                            ))}
                    </div>
                </div>
            </div>
        </div>
    );
}
