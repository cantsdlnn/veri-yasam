# ADR-0001: Saklama işlemlerini insan onayına bağlamak

Durum: Kabul edildi

## Bağlam

Bir saklama süresinin dolması her zaman kaydın derhal silinebileceği anlamına gelmez. Hukuki istisna, devam eden uyuşmazlık veya operasyonel hata bulunabilir. Tam otomatik silme geri dönüşü zor sonuç doğurur.

## Karar

Kural motoru yalnızca review_due veya overdue durumu ve önerilen eylemleri üretir. Kesin keep, anonymize veya delete işlemi için yetkili insan, kimliğini ve gerekçesini yazar. Karar ayrı tabloda ve denetim zincirinde tutulur.

## Sonuçlar

- İnsan sorumluluğu görünür kalır.
- Kararın dayanağı daha sonra incelenebilir.
- İş yükü artar ve otomasyon hızı azalır.
- Gerçek sistemde yetkilendirme ve ayrık görev ilkesi gerekir.
