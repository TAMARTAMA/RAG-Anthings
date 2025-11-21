import React, { useEffect, useMemo, useState } from "react";
import { getIndexes } from "../services/api";

type Props = {
  token: string | null;
  value: string | null;
  onChange: (index: string) => void;
  reloadKey?: number; // NEW: increase to trigger re-fetch
};

const PROTECTED_INDEX = "wikipedia";

export default function IndexSelect({ token, value, onChange ,reloadKey}: Props) {
  const [list, setList] = useState<string[]>([]);
  const [loading, setLoading] = useState(false);

  const canCall = useMemo(() => !!token, [token]);

  useEffect(() => {
    let mounted = true;
    async function load() {
        if (!canCall) { setList([]); return; }
        setLoading(true);
        try {
        const indexes = await getIndexes(token!);
        const s = new Set([PROTECTED_INDEX, ...(indexes || [])]);
        const final = Array.from(s);
        if (mounted) {
            setList(final);
            if (!value || !final.includes(value)) onChange(PROTECTED_INDEX);
        }
        } finally {
        if (mounted) setLoading(false);
        }
    }
    load();
}, [canCall, reloadKey]);  

  return (
    <div className="flex items-center gap-2">
      <span className="text-sm text-gray-600">Active index:</span>
      <select
        className="border rounded-lg px-2 py-1 text-sm"
        disabled={!canCall || loading}
        value={value ?? PROTECTED_INDEX}
        onChange={(e) => onChange(e.target.value)}
      >
        {(list.length ? list : [PROTECTED_INDEX]).map((name) => (
          <option key={name} value={name}>
            {name}
          </option>
        ))}
      </select>
    </div>
  );
}
