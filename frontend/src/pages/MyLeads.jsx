import { useState, useEffect } from "react";
import { getMyLeads, updateStatus, getLeadDetail } from "../api/client";
import LeadModal from "../components/LeadModal";

const STATUSES = ["havuzda", "aranmadi_ulasma", "gorusuldu_olumlu", "teklif_iletildi", "kazanildi", "ilgilenmiyor"];
const STATUS_LABELS = { havuzda: "Havuzda", aranmadi_ulasma: "Arandı - Ulaşılamadı", gorusuldu_olumlu: "Görüşüldü - Olumlu", teklif_iletildi: "Teklif İletildi", kazanildi: "Kazanıldı", ilgilenmiyor: "İlgilenmiyor" };

export default function MyLeads() {
  const [leads, setLeads] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState("");
  const [selectedLead, setSelectedLead] = useState(null);

  const fetchLeads = async () => {
    try {
      const data = await getMyLeads(filter);
      setLeads(data);
    } catch (e) { console.error(e); }
    finally { setLoading(false); }
  };

  useEffect(() => { fetchLeads(); }, [filter]);

  const handleStatusChange = async (id, newStatus) => {
    try {
      await updateStatus(id, newStatus);
      fetchLeads();
    } catch (e) { alert("Durum güncellenemedi"); }
  };

  return (
    <div className="space-y-4">
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold text-gray-800">Portföyüm</h1>
        <select value={filter} onChange={(e) => setFilter(e.target.value)} className="input w-64">
          <option value="">Tümü</option>
          {STATUSES.map(s => <option key={s} value={s}>{STATUS_LABELS[s]}</option>)}
        </select>
      </div>

      {loading ? <div className="text-center py-8">Yükleniyor...</div> : leads.length === 0 ? (
        <div className="text-center py-8 text-gray-500">Portföyünüzde müşteri yok</div>
      ) : (
        <div className="bg-white rounded-xl shadow-sm border overflow-hidden">
          <table className="w-full">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-4 py-3 text-left text-sm font-medium text-gray-600">İşletme</th>
                <th className="px-4 py-3 text-left text-sm font-medium text-gray-600">Telefon</th>
                <th className="px-4 py-3 text-left text-sm font-medium text-gray-600">Durum</th>
                <th className="px-4 py-3 text-right text-sm font-medium text-gray-600">İşlem</th>
              </tr>
            </thead>
            <tbody className="divide-y">
              {leads.map((lead) => (
                <tr key={lead.id} className="hover:bg-gray-50">
                  <td className="px-4 py-3 font-medium">{lead.isletme_adi}</td>
                  <td className="px-4 py-3 text-sm">{lead.telefon || "-"}</td>
                  <td className="px-4 py-3">
                    <select value={lead.status} onChange={(e) => handleStatusChange(lead.id, e.target.value)} className="text-sm border rounded px-2 py-1">
                      {STATUSES.map(s => <option key={s} value={s}>{STATUS_LABELS[s]}</option>)}
                    </select>
                  </td>
                  <td className="px-4 py-3 text-right">
                    <button onClick={() => setSelectedLead(lead)} className="text-blue-600 hover:underline text-sm">Detay / Not</button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {selectedLead && <LeadModal lead={selectedLead} onClose={() => setSelectedLead(null)} onUpdated={fetchLeads} />}
    </div>
  );
}
