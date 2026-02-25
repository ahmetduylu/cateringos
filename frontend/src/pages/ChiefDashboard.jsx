import { useState, useEffect } from "react";
import { getDashboard, getTeamReport, getPoolStats } from "../api/client";

export default function ChiefDashboard() {
  const [stats, setStats] = useState(null);
  const [team, setTeam] = useState([]);
  const [pool, setPool] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetch = async () => {
      try {
        const [dash, teamData, poolData] = await Promise.all([getDashboard(), getTeamReport(), getPoolStats()]);
        setStats(dash);
        setTeam(teamData.personeller || teamData);
        setPool(poolData);
      } catch (e) { console.error(e); }
      finally { setLoading(false); }
    };
    fetch();
  }, []);

  if (loading) return <div className="p-8 text-center">Yükleniyor...</div>;

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-gray-800">Yönetim Paneli</h1>
      
      {/* Özet Kartları */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="card text-center">
          <div className="text-3xl font-bold text-blue-600">{stats?.toplam_musteri || 0}</div>
          <div className="text-sm text-gray-500 mt-1">Toplam Müşteri</div>
        </div>
        <div className="card text-center">
          <div className="text-3xl font-bold text-orange-500">{pool?.havuzdaki || 0}</div>
          <div className="text-sm text-gray-500 mt-1">Havuzda</div>
        </div>
        <div className="card text-center">
          <div className="text-3xl font-bold text-green-600">{stats?.kazanilan || 0}</div>
          <div className="text-sm text-gray-500 mt-1">Kazanılan</div>
        </div>
        <div className="card text-center">
          <div className="text-3xl font-bold text-purple-600">{stats?.personel_sayisi || 0}</div>
          <div className="text-sm text-gray-500 mt-1">Personel</div>
        </div>
      </div>

      {/* Personel Performans */}
      <div className="card">
        <h2 className="text-lg font-semibold mb-4">Personel Performansı</h2>
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-4 py-2 text-left">Personel</th>
                <th className="px-4 py-2 text-right">Toplam</th>
                <th className="px-4 py-2 text-right">Kazanılan</th>
                <th className="px-4 py-2 text-right">Aktif</th>
                <th className="px-4 py-2 text-right">İlgilenmiyor</th>
                <th className="px-4 py-2 text-right">Dönüşüm</th>
              </tr>
            </thead>
            <tbody className="divide-y">
              {team.map((p) => (
                <tr key={p.user_id} className="hover:bg-gray-50">
                  <td className="px-4 py-2 font-medium">{p.ad}</td>
                  <td className="px-4 py-2 text-right">{p.toplam}</td>
                  <td className="px-4 py-2 text-right text-green-600">{p.kazanildi}</td>
                  <td className="px-4 py-2 text-right text-blue-600">{p.aktif}</td>
                  <td className="px-4 py-2 text-right text-red-500">{p.ilgilenmiyor}</td>
                  <td className="px-4 py-2 text-right font-medium">{p.donusum_orani}%</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
