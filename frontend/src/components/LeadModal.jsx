import { useState, useEffect } from "react";
import { getLeadDetail, addNote } from "../api/client";

export default function LeadModal({ lead, onClose, onUpdated }) {
  const [detail, setDetail] = useState(null);
  const [note, setNote] = useState("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getLeadDetail(lead.id).then(setDetail).finally(() => setLoading(false));
  }, [lead.id]);

  const handleAddNote = async () => {
    if (!note.trim()) return;
    try {
      await addNote(lead.id, note);
      setNote("");
      const updated = await getLeadDetail(lead.id);
      setDetail(updated);
      onUpdated?.();
    } catch (e) {
      alert("Not eklenemedi");
    }
  };

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
      <div className="bg-white rounded-xl w-full max-w-2xl max-h-[80vh] overflow-hidden">
        <div className="p-4 border-b flex justify-between items-center">
          <h2 className="text-lg font-bold">{lead.isletme_adi}</h2>
          <button onClick={onClose} className="text-gray-500 hover:text-gray-700 text-2xl">&times;</button>
        </div>
        <div className="p-4 overflow-y-auto max-h-[60vh]">
          {loading ? <div className="text-center py-4">Yükleniyor...</div> : (
            <div className="space-y-4">
              <div className="grid grid-cols-2 gap-4 text-sm">
                <div><span className="text-gray-500">Telefon:</span> {detail?.telefon || "-"}</div>
                <div><span className="text-gray-500">Adres:</span> {detail?.adres || "-"}</div>
                <div><span className="text-gray-500">Durum:</span> {detail?.status}</div>
                <div><span className="text-gray-500">Eklenme:</span> {new Date(detail?.eklenme_tarihi).toLocaleDateString("tr-TR")}</div>
              </div>
              
              <div>
                <h3 className="font-medium mb-2">İşlem Geçmişi</h3>
                <div className="space-y-2">
                  {detail?.logs?.map((log) => (
                    <div key={log.id} className="bg-gray-50 p-3 rounded-lg text-sm">
                      <div className="flex justify-between text-xs text-gray-500">
                        <span>{log.user_ad}</span>
                        <span>{new Date(log.tarih).toLocaleString("tr-TR")}</span>
                      </div>
                      <div className="mt-1">{log.aciklama}</div>
                    </div>
                  ))}
                </div>
              </div>

              <div>
                <textarea value={note} onChange={(e) => setNote(e.target.value)} placeholder="Yeni not ekle..." className="input h-24" />
                <button onClick={handleAddNote} className="btn-primary mt-2">Not Ekle</button>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
