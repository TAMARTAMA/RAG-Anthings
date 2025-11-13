// import React, { useEffect, useMemo, useState } from "react";
// import { addIndex, getIndexes, removeIndex } from "../services/api";

// type Props = {
//   open: boolean;
//   onClose: () => void;
//   token: string | null;
//   userId: string | null;
// };

// export default function IndexesDrawer({ open, onClose, token, userId }: Props) {
//   const [items, setItems] = useState<string[]>([]);
//   const [loading, setLoading] = useState(false);
//   const [err, setErr] = useState<string | null>(null);
//   const [newName, setNewName] = useState("");
//   const [creating, setCreating] = useState(false);
//   const [deleting, setDeleting] = useState<string | null>(null);

//   const canCall = useMemo(() => !!token && !!userId, [token, userId]);

//   async function load() {
//     if (!canCall) { setItems([]); return; }
//     setLoading(true);
//     setErr(null);
//     try {
//       const list = await getIndexes(token!);        // GET /auth/indexes -> { indexs: [...] }
//       setItems(Array.isArray(list) ? list : []);
//     } catch (e: any) {
//       setErr(e?.message || "Failed to fetch indexes");
//     } finally {
//       setLoading(false);
//     }
//   }

//   async function add() {
//     if (!canCall || !newName.trim()) return;
//     setCreating(true);
//     setErr(null);
//     try {
//       const resp = await addIndex(token!, userId!, newName.trim()); // POST /api/message/add_index (FormData)
//       const ix = resp?.user?.indexs ?? [];
//       setItems(ix);
//       setNewName("");
//     } catch (e: any) {
//       setErr(e?.message || "Failed to create index");
//     } finally {
//       setCreating(false);
//     }
//   }

//   async function remove(name: string) {
//     if (!canCall) return;
//     setDeleting(name);
//     setErr(null);
//     try {
//       const resp = await removeIndex(token!, name, userId!);        // POST /api/message/remove_index
//       const ix = resp?.user?.indexs ?? [];
//       setItems(ix);
//     } catch (e: any) {
//       setErr(e?.message || "Failed to delete index");
//     } finally {
//       setDeleting((x) => (x === name ? null : x));
//     }
//   }

//   useEffect(() => { if (open) load(); }, [open, canCall]);

//   return (
//     <div className={`fixed inset-0 z-40 ${open ? "" : "pointer-events-none"}`} aria-hidden={!open}>
//       <div
//         className={`absolute inset-0 bg-black/40 transition-opacity ${open ? "opacity-100" : "opacity-0"}`}
//         onClick={onClose}
//       />
//       <aside
//         className={`absolute right-0 top-0 h-full w-full max-w-lg bg-white shadow-2xl transition-transform ${open ? "translate-x-0" : "translate-x-full"
//           }`}
//       >
//         <div className="p-4 border-b flex items-center justify-between">
//           <h3 className="text-lg font-bold">Index Management</h3>
//           <button onClick={onClose} className="text-sm hover:underline">Close</button>
//         </div>

//         <div className="p-4 space-y-4">
//           {!canCall && <div className="text-sm text-gray-600">Login required to manage indexes.</div>}

//           <div className="flex gap-2">
//             <input
//               className="flex-1 border rounded-xl px-3 py-2"
//               placeholder="New index name"
//               value={newName}
//               onChange={(e) => setNewName(e.target.value)}
//               disabled={!canCall}
//             />
//             <button
//               onClick={add}
//               disabled={!canCall || creating || !newName.trim()}
//               className="px-3 py-2 rounded-xl bg-blue-600 text-white hover:bg-blue-700 disabled:opacity-60"
//             >
//               {creating ? "Adding..." : "Add"}
//             </button>
//           </div>

//           {err && <div className="text-sm text-red-600">{err}</div>}

//           <div className="border rounded-xl overflow-hidden">
//             <table className="w-full text-left text-sm">
//               <thead className="bg-gray-100">
//                 <tr>
//                   <th className="px-3 py-2">Index</th>
//                   <th className="px-3 py-2 w-28">Actions</th>
//                 </tr>
//               </thead>
//               <tbody>
//                 {loading ? (
//                   <tr><td className="px-3 py-3" colSpan={2}>Loading...</td></tr>
//                 ) : items.length === 0 ? (
//                   <tr><td className="px-3 py-3" colSpan={2}>No indexes</td></tr>
//                 ) : (
//                   items.map((name) => (
//                     <tr key={name} className="border-t">
//                       <td className="px-3 py-2">{name}</td>
//                       <td className="px-3 py-2">
//                         <button
//                           onClick={() => remove(name)}
//                           disabled={deleting === name || name === "wikipedia"}
//                           className="px-2 py-1 rounded-lg border hover:bg-gray-50 disabled:opacity-60"
//                         >
//                           {deleting === name
//                             ? "Deleting..."
//                             : name === "wikipedia"
//                               ? "Protected"
//                               : "Delete"}
//                         </button>
//                       </td>
//                     </tr>
//                   ))

//                 )}
//               </tbody>
//             </table>
//           </div>
//         </div>
//       </aside>
//     </div>
//   );
// }
import React, { useEffect, useMemo, useRef, useState } from "react";
import { addIndex, getIndexes, removeIndex } from "../services/api";

type Props = {
  open: boolean;
  onClose: () => void;
  token: string | null;
  userId: string | null;
  onIndexesChanged?: () => void; // notify parent (App) so IndexSelect can refresh immediately
};

const PROTECTED_INDEX = "wikipedia";
const ALLOWED_EXTS = [".txt", ".pdf", ".docx"];

function isAllowed(file: File) {
  const name = file.name.toLowerCase();
  return ALLOWED_EXTS.some(ext => name.endsWith(ext));
}

export default function IndexesDrawer({
  open,
  onClose,
  token,
  userId,
  onIndexesChanged, // <--- include in props destructuring
}: Props) {
  const [items, setItems] = useState<string[]>([]);
  const [loading, setLoading] = useState(false);
  const [err, setErr] = useState<string | null>(null);
  const [info, setInfo] = useState<string | null>(null);

  // New index: name + staged files + expand toggle
  const [newName, setNewName] = useState("");
  const [stagedNewFiles, setStagedNewFiles] = useState<File[]>([]);
  const [newExpanded, setNewExpanded] = useState(false);
  const [creating, setCreating] = useState(false);

  // Existing indexes: staged files per index + expand toggles + uploading state
  const [stagedPerIndex, setStagedPerIndex] = useState<Record<string, File[]>>({});
  const [expandedRows, setExpandedRows] = useState<Record<string, boolean>>({});
  const [uploadingIndex, setUploadingIndex] = useState<string | null>(null);

  // Delete state
  const [deleting, setDeleting] = useState<string | null>(null);

  const canCall = useMemo(() => !!token && !!userId, [token, userId]);

  // hidden inputs for per-row file pickers
  const addNewInputRef = useRef<HTMLInputElement | null>(null);
  const addRowInputs = useRef<Record<string, HTMLInputElement | null>>({});

  function resetStatus() {
    setErr(null);
    setInfo(null);
  }

  // Helper: signal parent that indexes changed (so IndexSelect can re-fetch)
  function signalChanged() {
    if (onIndexesChanged) onIndexesChanged();
  }

  async function load() {
    if (!canCall) { setItems([]); return; }
    resetStatus();
    setLoading(true);
    try {
      const list = await getIndexes(token!); // GET /auth/indexes -> string[]
      setItems(Array.isArray(list) ? list : []);
    } catch (e: any) {
      setErr(e?.message || "Failed to fetch indexes");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => { if (open) load(); }, [open, canCall]);

  // ------------- New index handlers -------------
  function handlePickNewFiles(e: React.ChangeEvent<HTMLInputElement>) {
    resetStatus();
    const files = e.target.files ? Array.from(e.target.files) : [];
    if (!files.length) return;

    const allowed = files.filter(isAllowed);
    const rejected = files.filter(f => !isAllowed(f));
    if (rejected.length) {
      setErr(`Some files were rejected (allowed: .txt, .pdf, .docx): ${rejected.map(f => f.name).join(", ")}`);
    }
    if (allowed.length) {
      setStagedNewFiles(prev => [...prev, ...allowed]);
      setNewExpanded(true);
    }
    // reset the input so the same file can be selected again
    if (addNewInputRef.current) addNewInputRef.current.value = "";
  }

  function removeNewStaged(idx: number) {
    setStagedNewFiles(prev => prev.filter((_, i) => i !== idx));
  }

  async function createNewIndex() {
    if (!canCall || !newName.trim()) return;
    resetStatus();
    setCreating(true);
    try {
      const resp = await addIndex(token!, userId!, newName.trim(), stagedNewFiles.length ? stagedNewFiles : undefined);
      const ix = resp?.user?.indexs ?? [];
      setItems(ix);
      setInfo(`Index "${newName.trim()}" created${stagedNewFiles.length ? " and files uploaded" : ""}.`);

      // notify parent so the header selector refreshes immediately
      signalChanged();

      setNewName("");
      setStagedNewFiles([]);
      setNewExpanded(false);
    } catch (e: any) {
      setErr(e?.message || "Failed to create index");
    } finally {
      setCreating(false);
    }
  }

  // ------------- Existing index handlers -------------
  function handlePickRowFiles(name: string, e: React.ChangeEvent<HTMLInputElement>) {
    resetStatus();
    const files = e.target.files ? Array.from(e.target.files) : [];
    if (!files.length) return;

    const allowed = files.filter(isAllowed);
    const rejected = files.filter(f => !isAllowed(f));
    if (rejected.length) {
      setErr(`Some files were rejected (allowed: .txt, .pdf, .docx): ${rejected.map(f => f.name).join(", ")}`);
    }
    if (allowed.length) {
      setStagedPerIndex(prev => ({
        ...prev,
        [name]: (prev[name] || []).concat(allowed),
      }));
      setExpandedRows(prev => ({ ...prev, [name]: true }));
    }
    const input = addRowInputs.current[name];
    if (input) input.value = "";
  }

  function removeRowStaged(name: string, idx: number) {
    setStagedPerIndex(prev => {
      const list = (prev[name] || []).filter((_, i) => i !== idx);
      return { ...prev, [name]: list };
    });
  }

  async function uploadRow(name: string) {
    if (!canCall) return;
    const files = stagedPerIndex[name] || [];
    if (!files.length) return;
    if (name.toLowerCase() === PROTECTED_INDEX) return; // protected

    resetStatus();
    setUploadingIndex(name);
    try {
      const resp = await addIndex(token!, userId!, name, files); // append to existing index
      const ix = resp?.user?.indexs ?? [];
      setItems(ix);
      setInfo(`${files.length} file(s) uploaded to "${name}".`);

      // notify parent so the header selector refreshes immediately
      signalChanged();

      setStagedPerIndex(prev => ({ ...prev, [name]: [] }));
      setExpandedRows(prev => ({ ...prev, [name]: false }));
    } catch (e: any) {
      setErr(e?.message || "Failed to upload files");
    } finally {
      setUploadingIndex(null);
    }
  }

  async function removeIndexRow(name: string) {
    if (!canCall) return;
    if (name.toLowerCase() === PROTECTED_INDEX) return; // protected

    resetStatus();
    setDeleting(name);
    try {
      const resp = await removeIndex(token!, name, userId!);
      const ix = resp?.user?.indexs ?? [];
      setItems(ix);
      setInfo(`Index "${name}" deleted.`);

      // notify parent so the header selector refreshes immediately
      signalChanged();

      // cleanup staged state
      setStagedPerIndex(prev => {
        const copy = { ...prev };
        delete copy[name];
        return copy;
      });
      setExpandedRows(prev => {
        const copy = { ...prev };
        delete copy[name];
        return copy;
      });
    } catch (e: any) {
      setErr(e?.message || "Failed to delete index");
    } finally {
      setDeleting((x) => (x === name ? null : x));
    }
  }

  return (
    <div className={`fixed inset-0 z-40 ${open ? "" : "pointer-events-none"}`} aria-hidden={!open}>
      <div
        className={`absolute inset-0 bg-black/40 transition-opacity ${open ? "opacity-100" : "opacity-0"}`}
        onClick={onClose}
      />
      <aside
        className={`absolute right-0 top-0 h-full w-full max-w-lg bg-white shadow-2xl transition-transform ${
          open ? "translate-x-0" : "translate-x-full"
        }`}
      >
        <div className="p-4 border-b flex items-center justify-between">
          <h3 className="text-lg font-bold">Index Management</h3>
          <button onClick={onClose} className="text-sm hover:underline">Close</button>
        </div>

        <div className="p-4 space-y-6">
          {!canCall && <div className="text-sm text-gray-600">Login required to manage indexes.</div>}
          {err && <div className="text-sm text-red-600">{err}</div>}
          {info && <div className="text-sm text-green-700">{info}</div>}

          {/* New index section */}
          <section className="space-y-3">
            <div className="font-semibold">Create new index</div>
            <div className="flex gap-2">
              <input
                className="flex-1 border rounded-xl px-3 py-2"
                placeholder="New index name"
                value={newName}
                onChange={(e) => setNewName(e.target.value)}
                disabled={!canCall}
              />
              <button
                className="px-3 py-2 rounded-xl border hover:bg-gray-50"
                onClick={() => addNewInputRef.current?.click()}
                disabled={!canCall}
              >
                + Add files
              </button>
              <input
                ref={addNewInputRef}
                type="file"
                multiple
                accept=".txt,.pdf,.docx,application/pdf,application/vnd.openxmlformats-officedocument.wordprocessingml.document,text/plain"
                className="hidden"
                onChange={handlePickNewFiles}
              />
              <button
                onClick={createNewIndex}
                disabled={!canCall || creating || !newName.trim()}
                className="px-3 py-2 rounded-xl bg-blue-600 text-white hover:bg-blue-700 disabled:opacity-60"
              >
                {creating ? "Creating..." : "Create"}
              </button>
            </div>

            {stagedNewFiles.length > 0 && (
              <div>
                <button
                  className="text-sm text-gray-600 hover:underline"
                  onClick={() => setNewExpanded(v => !v)}
                >
                  {newExpanded ? "▾ Hide files" : "▸ Show files"} ({stagedNewFiles.length})
                </button>
                {newExpanded && (
                  <ul className="mt-2 text-sm bg-gray-50 border rounded-xl p-2 max-h-40 overflow-auto">
                    {stagedNewFiles.map((f, i) => (
                      <li key={i} className="flex items-center justify-between gap-2 py-1">
                        <span className="truncate">{f.name}</span>
                        <button
                          onClick={() => removeNewStaged(i)}
                          className="px-2 py-0.5 rounded border hover:bg-gray-100"
                        >
                          ×
                        </button>
                      </li>
                    ))}
                  </ul>
                )}
              </div>
            )}
          </section>

          {/* Existing indexes */}
          <section className="border rounded-xl overflow-hidden">
            <table className="w-full text-left text-sm">
              <thead className="bg-gray-100">
                <tr>
                  <th className="px-3 py-2">Index</th>
                  <th className="px-3 py-2 w-60">Files</th>
                  <th className="px-3 py-2 w-40">Actions</th>
                </tr>
              </thead>
              <tbody>
                {loading ? (
                  <tr><td className="px-3 py-3" colSpan={3}>Loading...</td></tr>
                ) : items.length === 0 ? (
                  <tr><td className="px-3 py-3" colSpan={3}>No indexes</td></tr>
                ) : (
                  items.map((name) => {
                    const protectedIndex = name.toLowerCase() === PROTECTED_INDEX;
                    const staged = stagedPerIndex[name] || [];
                    const expanded = !!expandedRows[name];

                    return (
                      <tr key={name} className="border-t align-top">
                        <td className="px-3 py-2">{name}</td>

                        <td className="px-3 py-2">
                          <div className="flex items-center gap-2">
                            <button
                              className="px-3 py-1 rounded-lg border hover:bg-gray-50 disabled:opacity-60"
                              onClick={() => !protectedIndex && addRowInputs.current[name]?.click()}
                              disabled={protectedIndex || uploadingIndex === name}
                              title={protectedIndex ? "Wikipedia is protected" : "Choose files to stage"}
                            >
                              + Add files
                            </button>
                            <input
                              ref={(el) => { addRowInputs.current[name] = el; }}
                              type="file"
                              multiple
                              accept=".txt,.pdf,.docx,application/pdf,application/vnd.openxmlformats-officedocument.wordprocessingml.document,text/plain"
                              className="hidden"
                              onChange={(e) => handlePickRowFiles(name, e)}
                            />
                            {staged.length > 0 && (
                              <button
                                className="text-xs text-gray-600 hover:underline"
                                onClick={() => setExpandedRows(prev => ({ ...prev, [name]: !expanded }))}
                              >
                                {expanded ? "▾ Hide files" : `▸ Show files (${staged.length})`}
                              </button>
                            )}
                          </div>
                          {expanded && staged.length > 0 && (
                            <ul className="mt-2 text-sm bg-gray-50 border rounded-xl p-2 max-h-32 overflow-auto">
                              {staged.map((f, i) => (
                                <li key={`${name}-${i}`} className="flex items-center justify-between gap-2 py-1">
                                  <span className="truncate">{f.name}</span>
                                  <button
                                    onClick={() => removeRowStaged(name, i)}
                                    className="px-2 py-0.5 rounded border hover:bg-gray-100"
                                  >
                                    ×
                                  </button>
                                </li>
                              ))}
                            </ul>
                          )}
                        </td>

                        <td className="px-3 py-2">
                          <div className="flex items-center gap-2">
                            <button
                              onClick={() => uploadRow(name)}
                              disabled={protectedIndex || uploadingIndex === name || (stagedPerIndex[name]?.length ?? 0) === 0}
                              className="px-2 py-1 rounded-lg border hover:bg-gray-50 disabled:opacity-60"
                              title={protectedIndex ? "Wikipedia is protected" : "Upload all staged files"}
                            >
                              {uploadingIndex === name ? "Uploading..." : "Upload all"}
                            </button>
                            <button
                              onClick={() => removeIndexRow(name)}
                              disabled={protectedIndex || deleting === name}
                              className="px-2 py-1 rounded-lg border hover:bg-gray-50 disabled:opacity-60"
                              title={protectedIndex ? "Wikipedia is protected" : "Delete index"}
                            >
                              {deleting === name ? "Deleting..." : "Delete"}
                            </button>
                          </div>
                        </td>
                      </tr>
                    );
                  })
                )}
              </tbody>
            </table>
          </section>
        </div>
      </aside>
    </div>
  );
}
