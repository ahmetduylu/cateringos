import { useState, useEffect } from "react";
import { getPool, assignLead } from "../api/client";

export default function Pool() {
  const [leads, setLeads] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState("");
  const [assigning, setAssigning] = useState(null);

  const fetchLeads = async () => {
    try {
      const data = await getPool(search);
      setLeads(data);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchLeads();
  }, [search]);

  const handleAssign = async (leadId) => {
    setAssigning(leadId);
    try {
      await assignLead(leadId);
      setLeads(leads.filter(l => l.id !== leadId));
    } catch (e) {
      alert(e.response?.data?.detail || "Atama başarısız");
    } finally {
      setAssigning(null);
    }
  };

  return (
    <div className="space-y-4">
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold text-gray-800">Havuz</h1>
        <input type="text" placeholder="Ara..." value={search} onChange={(e) => setSearch(e.target.value)} className="input w-64" />
      </div>

      {loading ? (
        <div className="text-center py-8">Yükleniyor...</div>
      ) : leads.length === 0 ? (
        <div className="text-center py-8 text-gray-500">Havuzda müşteri yok</div>
      ) : (
        <div className="bg-white rounded-xl shadow-sm border overflow-hidden">
          <table className="w-full">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-4 py-3 text-left text-sm font-medium text-gray-600">İşletme</th>
                <th className="px-4 py-3 text-left text-sm font-medium text-gray-600">Telefon</th>
                <th className="px-4 py-3 text-left text-sm font-medium text-gray-600">Adres</th>
                <th className="px-4 py-3 text-right text-sm font-medium text-gray-600">İşlem</th>
              </tr>
            </thead>
            <tbody className="divide-y">
              {leads.map((lead) => (
                <tr key={lead.id} className="hover:bg-gray-50">
                  <td className="px-4 py-3 font-medium">{lead.isletme_adi}</td>
                  <td className="px-4 py-3 text-sm text-gray-600">{lead.telefon || "-"}</td>
                  <td className="px-4 py-3 text-sm text-gray-600">{lead.adres || "-"}</td>
                  <td className="px-4 py-3 text-right">
                    <button onClick={() => handleAssign(lead.id)} disabled={assigning === lead.id} className="btn-success">
                      {assigning === lead.id ? "..." : "Bana Ata"}
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
