/* ====================================================================
   Prism.js Python syntax highlighting for jQuery Terminal
   ==================================================================== */
if (jQuery.terminal && jQuery.terminal.syntax) {
    jQuery.terminal.syntax("python");
}

/* ====================================================================
   Data URL
   ==================================================================== */
const DATA_BASE = "https://conda-incubator.github.io/condastats-data";
function dataUrl(year, month) {
    return (
        DATA_BASE +
        "/" +
        year +
        "/" +
        year +
        "-" +
        String(month).padStart(2, "0") +
        ".parquet"
    );
}

/* ====================================================================
   State
   ==================================================================== */
let pyodide = null;
let cachedMonthKeys = new Set(); // months already downloaded
let activeMonthSig = null; // signature of currently-active range
let resultChart = null;
let pendingAction = null; // queued example click while Pyodide loads
const CHART_COLORS = [
    "#2563eb",
    "#e11d48",
    "#059669",
    "#7c3aed",
    "#d97706",
    "#0891b2",
    "#dc2626",
    "#6366f1",
    "#ea580c",
    "#0d9488",
    "#be185d",
    "#4d7c0f",
];

/* ====================================================================
   UI helpers
   ==================================================================== */
const $ = (s) => document.querySelector(s);

let _errorTimer = 0;
function setStatus(text, cls) {
    const btn = $("#run-btn");
    clearTimeout(_errorTimer);
    if (cls === "loading") {
        btn.disabled = true;
        btn.innerHTML = '<span class="btn-spinner"></span>' + text;
    } else if (cls === "error") {
        btn.disabled = false;
        btn.textContent = text;
        btn.style.background = "var(--pst-color-danger)";
        _errorTimer = setTimeout(() => {
            btn.style.background = "";
            btn.textContent = "Query";
        }, 4000);
    } else {
        btn.disabled = false;
        btn.style.background = "";
        btn.textContent = "Query";
    }
}

function monthStr(date) {
    return (
        date.getFullYear() + "-" + String(date.getMonth() + 1).padStart(2, "0")
    );
}

function setDefaultRange() {
    const end = new Date();
    end.setMonth(end.getMonth() - 2);
    const start = new Date(end);
    start.setMonth(start.getMonth() - 11);
    $("#month-start").value = monthStr(start);
    $("#month-end").value = monthStr(end);
}

function getMonthList(startVal, endVal) {
    /* Return array of "YYYY-MM" strings from startVal to endVal inclusive. */
    const months = [];
    const [sy, sm] = startVal.split("-").map(Number);
    const [ey, em] = endVal.split("-").map(Number);
    let y = sy,
        m = sm;
    while (y < ey || (y === ey && m <= em)) {
        months.push(y + "-" + String(m).padStart(2, "0"));
        m++;
        if (m > 12) {
            m = 1;
            y++;
        }
    }
    return months;
}

function applyPreset(nMonths) {
    const end = new Date();
    end.setMonth(end.getMonth() - 2);
    const start = new Date(end);
    start.setMonth(start.getMonth() - (nMonths - 1));
    $("#month-start").value = monthStr(start);
    $("#month-end").value = monthStr(end);
}

function hideResults() {
    $("#hero-stat").style.display = "none";
    $("#summary-cards").style.display = "none";
    $("#chart-container").style.display = "none";
    $("#results-content").innerHTML = "";
    if (resultChart) {
        resultChart.destroy();
        resultChart = null;
    }
}

/* ====================================================================
   Chart rendering
   ==================================================================== */
function renderChart(jsonData) {
    if (resultChart) {
        resultChart.destroy();
        resultChart = null;
    }
    if (!jsonData || !jsonData.labels || jsonData.labels.length === 0) {
        $("#chart-container").style.display = "none";
        return;
    }

    $("#chart-container").style.display = "block";
    const canvasCtx = $("#result-chart").getContext("2d");

    const isDark = window.matchMedia("(prefers-color-scheme: dark)").matches;
    const gridColor = isDark ? "rgba(255,255,255,0.08)" : "rgba(0,0,0,0.06)";
    const textColor = isDark ? "#94a3b8" : "#6b7280";

    // Multiple datasets (comparison) or single
    const datasets = jsonData.datasets.map((ds, i) => ({
        label: ds.label,
        data: ds.data,
        backgroundColor: CHART_COLORS[i % CHART_COLORS.length] + "cc",
        borderColor: CHART_COLORS[i % CHART_COLORS.length],
        borderWidth: 1,
        borderRadius: 3,
    }));

    resultChart = new Chart(canvasCtx, {
        type: "bar",
        data: { labels: jsonData.labels, datasets },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            indexAxis: jsonData.labels.length > 12 ? "y" : "x",
            plugins: {
                legend: {
                    display: datasets.length > 1,
                    labels: { color: textColor, font: { family: "Open Sans" } },
                },
                tooltip: {
                    callbacks: {
                        label: (tip) =>
                            tip.dataset.label +
                            ": " +
                            tip.parsed[
                                jsonData.labels.length > 12 ? "x" : "y"
                            ].toLocaleString(),
                    },
                },
            },
            scales: {
                x: {
                    grid: { color: gridColor },
                    ticks: { color: textColor, font: { size: 11 } },
                },
                y: {
                    grid: { color: gridColor },
                    ticks: { color: textColor, font: { size: 11 } },
                },
            },
        },
    });
}

/* ====================================================================
   Pyodide bootstrap
   ==================================================================== */
const PYTHON_HELPERS = `
import pandas as pd
from io import BytesIO
import json

# condastats is installed via micropip (deps=False, since pandas is
# already provided by Pyodide).  Only the pure-pandas query layer is used.
from condastats import query_overall, query_grouped, top_packages as _top_packages

df = None
_pkg_names = []
_month_frames = {}

def load_parquet(raw, month_key):
    """Load a single month's parquet into the cache."""
    mdf = pd.read_parquet(BytesIO(bytes(raw)), engine="fastparquet")
    _month_frames[month_key] = mdf
    return json.dumps({"rows": len(mdf), "month": month_key})

def activate_months(month_keys_json):
    """Concatenate cached months into the active DataFrame."""
    global df, _pkg_names
    keys = json.loads(month_keys_json)
    frames = [_month_frames[k] for k in keys if k in _month_frames]
    if not frames:
        return json.dumps({"error": "No data loaded."})
    df = pd.concat(frames, ignore_index=True)
    _pkg_names = sorted(df["pkg_name"].unique().tolist())
    return json.dumps({"rows": len(df), "packages": len(_pkg_names), "months": len(frames)})

def get_package_names():
    return json.dumps(_pkg_names)

def _summary_stats(filtered):
    """Build summary dict for the UI."""
    total = int(filtered["counts"].sum())
    n_platforms = int(filtered["pkg_platform"].nunique()) if "pkg_platform" in filtered.columns else 0
    n_versions = int(filtered["pkg_version"].nunique()) if "pkg_version" in filtered.columns else 0
    top_platform = str(filtered.groupby("pkg_platform")["counts"].sum().idxmax()) if n_platforms > 0 else ""
    top_source = str(filtered.groupby("data_source")["counts"].sum().idxmax()) if "data_source" in filtered.columns else ""
    return {
        "total": total,
        "platforms": n_platforms,
        "versions": n_versions,
        "top_platform": top_platform,
        "top_source": top_source,
    }

def _fmt(x):
    return f"{x:,}"

def query(packages_str, query_type="overall"):
    """Return JSON with table HTML, chart data, and summary stats.

    Uses condastats.query_overall / query_grouped under the hood.
    """
    if df is None:
        return json.dumps({"error": "No data loaded."})

    pkgs = [p.strip().lower() for p in packages_str.split(",") if p.strip()]
    if not pkgs:
        return json.dumps({"error": "Please enter at least one package name."})

    filtered = df[df["pkg_name"].isin(pkgs)]
    if len(filtered) == 0:
        matches = sorted([n for n in _pkg_names if any(p in n for p in pkgs)])[:15]
        suggestions = ", ".join(matches) if matches else "none"
        return json.dumps({"error": f"No data found. Similar: {suggestions}"})

    result = {"summary": _summary_stats(filtered)}

    if query_type == "overall":
        grp = query_overall(df, package=pkgs)           # Series: pkg_name -> count
        grp = grp.sort_values(ascending=False)

        if len(pkgs) == 1:
            total = int(grp.iloc[0]) if len(grp) > 0 else 0
            result["hero"] = {"value": total, "label": f"total downloads for {pkgs[0]}"}
            result["table"] = ""
            result["chart"] = None
        else:
            result["chart"] = {
                "labels": grp.index.tolist(),
                "datasets": [{"label": "Downloads", "data": grp.values.tolist()}],
            }
            out = grp.reset_index()
            out.columns = ["Package", "Downloads"]
            out["Downloads"] = out["Downloads"].apply(_fmt)
            result["table"] = out.to_html(index=False, border=0)
    else:
        grp = query_grouped(df, query_type, package=pkgs)  # MultiIndex Series

        if len(pkgs) == 1:
            # Drop the pkg_name level – leaves just the dimension
            grp = grp.droplevel("pkg_name").sort_values(ascending=False)
            result["chart"] = {
                "labels": [str(x) for x in grp.index.tolist()],
                "datasets": [{"label": pkgs[0], "data": grp.values.tolist()}],
            }
            out = grp.reset_index()
            out.columns = [query_type.replace("_", " ").title(), "Downloads"]
            out["Downloads"] = out["Downloads"].apply(_fmt)
            result["table"] = out.to_html(index=False, border=0)
        else:
            pivot = grp.unstack(fill_value=0)
            all_dims = pivot.columns.tolist()
            datasets = []
            for pkg in pkgs:
                if pkg in pivot.index:
                    datasets.append({"label": pkg, "data": [int(pivot.loc[pkg, d]) for d in all_dims]})
            result["chart"] = {
                "labels": [str(d) for d in all_dims],
                "datasets": datasets,
            }
            flat = grp.reset_index()
            flat.columns = ["Package", query_type.replace("_", " ").title(), "Downloads"]
            flat = flat.sort_values("Downloads", ascending=False)
            flat["Downloads"] = flat["Downloads"].apply(_fmt)
            result["table"] = flat.to_html(index=False, border=0)

    return json.dumps(result)

def top_packages(n=20):
    if df is None:
        return json.dumps({"error": "No data loaded."})
    grp = _top_packages(df, n=n)                     # Series from condastats
    chart = {
        "labels": grp.index.tolist(),
        "datasets": [{"label": "Downloads", "data": grp.values.tolist()}],
    }
    out = grp.reset_index()
    out.columns = ["Package", "Downloads"]
    out["Downloads"] = out["Downloads"].apply(_fmt)
    summary = {"total": int(grp.sum()), "packages": len(grp)}
    return json.dumps({"chart": chart, "table": out.to_html(index=False, border=0), "summary": summary})
`;

async function initPyodide() {
    setStatus("Downloading Pyodide runtime\u2026", "loading");
    const script = document.createElement("script");
    script.src = "https://cdn.jsdelivr.net/pyodide/v0.29.3/full/pyodide.js";
    document.head.appendChild(script);
    await new Promise((res, rej) => {
        script.onload = res;
        script.onerror = () => rej(new Error("Failed to load Pyodide"));
    });

    setStatus("Initializing Python\u2026", "loading");
    pyodide = await loadPyodide();

    setStatus("Installing pandas + fastparquet\u2026", "loading");
    await pyodide.loadPackage(["pandas", "fastparquet", "micropip"]);

    setStatus("Installing condastats\u2026", "loading");
    await pyodide.runPythonAsync(`
import micropip
await micropip.install("condastats", deps=False)
`);

    await pyodide.runPythonAsync(PYTHON_HELPERS);

    // If the user clicked an example while loading, or URL has query params, auto-run
    if (pendingAction) {
        const action = pendingAction;
        pendingAction = null;
        $("#package").value = action.pkg;
        $("#query-type").value = action.queryType;
        updatePkgField();
        runQuery();
    } else if (hasUrlQuery) {
        runQuery();
    } else {
        setStatus("Ready", "ready");
    }
}

/* ====================================================================
   Data loading
   ==================================================================== */
async function ensureData(startVal, endVal) {
    const months = getMonthList(startVal, endVal);
    const sig = months.join(",");
    if (sig === activeMonthSig) return;

    // Download months we don't have yet
    const needed = months.filter((m) => !cachedMonthKeys.has(m));
    if (needed.length > 0) {
        setStatus(
            "Downloading " + needed.length + " month(s)\u2026",
            "loading",
        );
        // Fetch in parallel (batches of 4), then parse sequentially via Pyodide
        const fetched = []; // [{mKey, buf}, ...]
        for (let i = 0; i < needed.length; i += 4) {
            const batch = needed.slice(i, i + 4);
            const results = await Promise.all(
                batch.map(async (mKey) => {
                    const [y, m] = mKey.split("-").map(Number);
                    const resp = await fetch(dataUrl(y, m));
                    if (!resp.ok)
                        throw new Error(
                            "Data not available for " +
                                mKey +
                                " (HTTP " +
                                resp.status +
                                ")",
                        );
                    return { mKey, buf: await resp.arrayBuffer() };
                }),
            );
            fetched.push(...results);
            setStatus(
                "Downloaded " +
                    fetched.length +
                    " / " +
                    needed.length +
                    " months\u2026",
                "loading",
            );
        }
        // Parse parquet files sequentially (Pyodide is single-threaded)
        for (let i = 0; i < fetched.length; i++) {
            const { mKey, buf } = fetched[i];
            setStatus(
                "Loading " + (i + 1) + " / " + fetched.length + " months\u2026",
                "loading",
            );
            pyodide.globals.set(
                "_parquet_bytes",
                pyodide.toPy(new Uint8Array(buf)),
            );
            await pyodide.runPythonAsync(
                "load_parquet(_parquet_bytes, " + JSON.stringify(mKey) + ")",
            );
            pyodide.globals.delete("_parquet_bytes");
            cachedMonthKeys.add(mKey);
        }
    }

    // Activate (concatenate) the requested months
    setStatus("Preparing " + months.length + " month(s)\u2026", "loading");
    await pyodide.runPythonAsync(
        "activate_months(" + JSON.stringify(JSON.stringify(months)) + ")",
    );
    activeMonthSig = sig;

    // Populate autocomplete
    const names = JSON.parse(
        await pyodide.runPythonAsync("get_package_names()"),
    );
    const dl = $("#pkg-suggestions");
    dl.innerHTML = "";
    names.slice(0, 500).forEach((n) => {
        const opt = document.createElement("option");
        opt.value = n;
        dl.appendChild(opt);
    });

    setStatus(
        "Loaded " + months.length + " month(s), running query\u2026",
        "loading",
    );
}

/* ====================================================================
   Render results
   ==================================================================== */
function showResults(data, title) {
    hideResults();
    $("#results").style.display = "block";
    $("#results-title").textContent = title;

    if (data.error) {
        const p = document.createElement("p");
        p.className = "error-msg";
        p.textContent = data.error;
        $("#results-content").appendChild(p);
        return;
    }

    // Hero number
    if (data.hero) {
        $("#hero-stat").style.display = "block";
        $("#hero-number").textContent = data.hero.value.toLocaleString();
        $("#hero-label").textContent = data.hero.label;
    }

    // Summary cards
    if (data.summary) {
        const s = data.summary;
        let html = "";
        html +=
            '<div class="summary-card"><div class="value">' +
            s.total.toLocaleString() +
            '</div><div class="label">Total downloads</div></div>';
        if (s.platforms)
            html +=
                '<div class="summary-card"><div class="value">' +
                s.platforms +
                '</div><div class="label">Platforms</div></div>';
        if (s.top_platform)
            html +=
                '<div class="summary-card"><div class="value">' +
                s.top_platform +
                '</div><div class="label">Top platform</div></div>';
        if (s.top_source)
            html +=
                '<div class="summary-card"><div class="value">' +
                s.top_source +
                '</div><div class="label">Top source</div></div>';
        if (s.versions)
            html +=
                '<div class="summary-card"><div class="value">' +
                s.versions +
                '</div><div class="label">Versions</div></div>';
        $("#summary-cards").innerHTML = html;
        $("#summary-cards").style.display = "grid";
    }

    // Chart
    if (data.chart) renderChart(data.chart);

    // Table
    if (data.table) $("#results-content").innerHTML = data.table;
}

/* ====================================================================
   Shareable URLs
   ==================================================================== */
function queryParams() {
    const params = new URLSearchParams();
    const qtype = $("#query-type").value;
    params.set("type", qtype);
    if (qtype !== "top") {
        const pkg = $("#package").value.trim();
        if (pkg) params.set("pkg", pkg);
    }
    params.set("start", $("#month-start").value);
    params.set("end", $("#month-end").value);
    return params;
}

function buildQueryUrl() {
    return location.origin + location.pathname + "?" + queryParams().toString();
}

function updateUrlFromForm() {
    history.replaceState(null, "", "?" + queryParams().toString());
}

const VALID_QUERY_TYPES = new Set([
    "overall",
    "pkg_platform",
    "data_source",
    "pkg_version",
    "pkg_python",
    "top",
]);

function loadFormFromUrl() {
    const params = new URLSearchParams(location.search);
    if (!params.has("type")) return false;
    const qtype = params.get("type");
    if (!VALID_QUERY_TYPES.has(qtype)) return false;
    $("#query-type").value = qtype;
    if (params.has("pkg")) $("#package").value = params.get("pkg");
    if (params.has("start")) $("#month-start").value = params.get("start");
    if (params.has("end")) $("#month-end").value = params.get("end");
    updatePkgField();
    return true;
}

/* ====================================================================
   Query execution
   ==================================================================== */
function rangeLabel() {
    const s = $("#month-start").value,
        e = $("#month-end").value;
    return s === e ? s : s + " to " + e;
}

function updatePkgField() {
    const isTop = $("#query-type").value === "top";
    const pkg = $("#package");
    pkg.style.opacity = isTop ? "0.45" : "";
    if (isTop) pkg.placeholder = "(not needed for Top packages)";
    else pkg.placeholder = "e.g. pandas, numpy";
}

async function runQuery() {
    const qtype = $("#query-type").value;
    const pkg = $("#package").value.trim();
    if (qtype !== "top" && !pkg) {
        alert("Enter a package name.");
        return;
    }
    const startVal = $("#month-start").value;
    const endVal = $("#month-end").value;
    if (!startVal || !endVal) {
        alert("Select a date range.");
        return;
    }
    if (startVal > endVal) {
        alert("Start month must be before end month.");
        return;
    }

    updateUrlFromForm();

    const labels = {
        overall: "Overall downloads",
        pkg_platform: "Downloads by platform",
        data_source: "Downloads by data source",
        pkg_version: "Downloads by version",
        pkg_python: "Downloads by Python version",
        top: "Top 20 most downloaded packages",
    };

    try {
        await ensureData(startVal, endVal);
        setStatus("Running query\u2026", "loading");
        let raw;
        if (qtype === "top") {
            raw = await pyodide.runPythonAsync("top_packages(20)");
        } else {
            raw = await pyodide.runPythonAsync(
                "query(" +
                    JSON.stringify(pkg) +
                    ", " +
                    JSON.stringify(qtype) +
                    ")",
            );
        }
        const data = JSON.parse(raw);
        showResults(data, labels[qtype] + " (" + rangeLabel() + ")");
        setStatus("Done.", "ready");
    } catch (err) {
        setStatus("Error: " + err.message, "error");
        showResults({ error: err.message }, "Error");
    } finally {
        activateCard(null);
    }
}

/* ====================================================================
   Quick-start cards
   ==================================================================== */
function activateCard(card) {
    document
        .querySelectorAll(".example-card.active")
        .forEach((c) => c.classList.remove("active"));
    if (card) card.classList.add("active");
}

document.querySelectorAll(".example-card").forEach((card) => {
    card.addEventListener("click", () => {
        activateCard(card);

        // Fill in the form from the card's data attributes
        $("#package").value = card.dataset.pkg || "";
        $("#query-type").value = card.dataset.type;
        updatePkgField();

        // If Pyodide is still loading, queue to run once ready
        if ($("#run-btn").disabled) {
            pendingAction = {
                pkg: card.dataset.pkg || "",
                queryType: card.dataset.type,
            };
            return;
        }
        runQuery();
    });
});

/* ====================================================================
   REPL (jQuery Terminal + pyodide.console.PyodideConsole)
   ==================================================================== */
let replTerminal = null;

const REPL_BANNER = [
    "Python (Pyodide) on WebAssembly/Emscripten",
    "condastats interactive shell \u2014 df auto-loads from the date range above",
    "",
    '  >>> query_overall(df, package="numpy")',
    '  >>> query_overall(df, package=["pandas", "polars"])',
    '  >>> query_grouped(df, "pkg_platform", package="scipy")',
    "  >>> top_packages(df, n=10)",
    "  >>> df.head()",
    "  >>> df.columns.tolist()",
    "  >>> help(query_overall)",
].join("\n");

function initReplConsole() {
    if (replTerminal) return;
    if (!pyodide) return;

    // Create PyodideConsole sharing __main__'s namespace (where df, query_overall, etc. live)
    pyodide.runPython(`
from pyodide.console import PyodideConsole, repr_shorten
from pyodide.ffi import to_js
import __main__, builtins

pyconsole = PyodideConsole(__main__.__dict__)

async def _await_fut(fut):
    res = await fut
    if res is not None:
        builtins._ = res
    return to_js([res], depth=1)

def _clear_console():
    pyconsole.buffer = []
`);

    const pyconsole = pyodide.globals.get("pyconsole");
    const repr_shorten = pyodide.globals.get("repr_shorten");
    const await_fut = pyodide.globals.get("_await_fut");
    const clear_console = pyodide.globals.get("_clear_console");

    const ps1 = ">>> ";
    const ps2 = "... ";

    async function lock() {
        let resolve;
        const ready = replTerminal.ready;
        replTerminal.ready = new Promise((res) => (resolve = res));
        await ready;
        return resolve;
    }

    async function interpreter(command) {
        const unlock = await lock();
        replTerminal.pause();
        for (const c of command.split("\n")) {
            const fut = pyconsole.push(c);
            replTerminal.set_prompt(
                fut.syntax_check === "incomplete" ? ps2 : ps1,
            );
            switch (fut.syntax_check) {
                case "syntax-error":
                    replTerminal.error(fut.formatted_error.trimEnd());
                    continue;
                case "incomplete":
                    continue;
                case "complete":
                    break;
                default:
                    throw new Error(
                        "Unexpected syntax_check: " + fut.syntax_check,
                    );
            }
            const wrapped = await_fut(fut);
            try {
                const [value] = await wrapped;
                if (value !== undefined) {
                    replTerminal.echo(
                        repr_shorten.callKwargs(value, {
                            separator: "\n<long output truncated>\n",
                        }),
                    );
                }
                if (value instanceof pyodide.ffi.PyProxy) {
                    value.destroy();
                }
            } catch (e) {
                if (e.constructor.name === "PythonError") {
                    const message = fut.formatted_error || e.message;
                    replTerminal.error(message.trimEnd());
                } else {
                    throw e;
                }
            } finally {
                fut.destroy();
                wrapped.destroy();
            }
        }
        replTerminal.resume();
        await new Promise((r) => setTimeout(r, 10));
        unlock();
    }

    replTerminal = jQuery("#repl-terminal").terminal(interpreter, {
        greetings: REPL_BANNER,
        prompt: ps1,
        completionEscape: false,
        completion: function (command, callback) {
            callback(pyconsole.complete(command).toJs()[0]);
        },
        keymap: {
            "CTRL+C": async function (event, original) {
                clear_console();
                replTerminal.echo(
                    replTerminal.get_prompt() + replTerminal.get_command(),
                );
                replTerminal.echo("KeyboardInterrupt");
                replTerminal.set_command("");
                replTerminal.set_prompt(ps1);
            },
            TAB: (event, original) => {
                const command = replTerminal.before_cursor();
                if (command.trim() === "") {
                    replTerminal.insert("\t");
                    return false;
                }
                return original(event);
            },
        },
    });

    pyconsole.stdout_callback = (s) => replTerminal.echo(s, { newline: false });
    pyconsole.stderr_callback = (s) => replTerminal.error(s.trimEnd());
    replTerminal.ready = Promise.resolve();
}

$("#repl-toggle").addEventListener("click", async () => {
    $("#repl-toggle").classList.toggle("open");
    $("#repl-body").classList.toggle("open");
    if ($("#repl-body").classList.contains("open")) {
        if (!replTerminal && pyodide) {
            // Auto-load data if not loaded yet
            const hasData = pyodide.runPython("df is not None");
            if (!hasData) {
                const startVal = $("#month-start").value;
                const endVal = $("#month-end").value;
                if (startVal && endVal) {
                    try {
                        await ensureData(startVal, endVal);
                    } catch (err) {
                        console.error("Failed to auto-load data:", err);
                    }
                }
            }
            initReplConsole();
        }
        if (replTerminal) {
            replTerminal.focus();
        }
    }
});

/* ====================================================================
   Init
   ==================================================================== */
setDefaultRange();
const hasUrlQuery = loadFormFromUrl(); // override defaults if URL has params
$("#run-btn").addEventListener("click", runQuery);
$("#package").addEventListener("keydown", (e) => {
    if (e.key === "Enter" && !$("#run-btn").disabled) runQuery();
});
$("#query-type").addEventListener("change", updatePkgField);
$("#package").addEventListener("focus", () => {
    if ($("#query-type").value === "top") {
        $("#query-type").value = "overall";
        updatePkgField();
    }
});

// Share button
$("#share-btn").addEventListener("click", () => {
    const url = buildQueryUrl();
    navigator.clipboard
        .writeText(url)
        .then(() => {
            const btn = $("#share-btn");
            const orig = btn.innerHTML;
            btn.innerHTML = "&#10003; Copied!";
            setTimeout(() => {
                btn.innerHTML = orig;
            }, 2000);
        })
        .catch(() => {
            // Fallback: show URL in a prompt
            prompt("Copy this link:", buildQueryUrl());
        });
});

// Preset range buttons
document.querySelectorAll(".preset-btn").forEach((btn) => {
    btn.addEventListener("click", () => {
        document
            .querySelectorAll(".preset-btn")
            .forEach((b) => b.classList.remove("active"));
        btn.classList.add("active");
        applyPreset(parseInt(btn.dataset.range, 10));
    });
});

// Clear preset highlight when user manually edits dates
["month-start", "month-end"].forEach((id) => {
    document.getElementById(id).addEventListener("input", () => {
        document
            .querySelectorAll(".preset-btn")
            .forEach((b) => b.classList.remove("active"));
    });
});

function startDemo() {
    $("#consent-overlay").style.display = "none";
    $("#app-content").style.display = "block";
    initPyodide().catch((err) => {
        setStatus("Failed to initialize: " + err.message, "error");
        console.error(err);
    });
}

$("#consent-btn").addEventListener("click", startDemo);

// In standalone mode (not embedded), skip consent and start immediately
if (!document.body.classList.contains("embed-mode")) {
    startDemo();
}
