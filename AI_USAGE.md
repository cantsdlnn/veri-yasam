# Yapay zekâ kullanım beyanı

Bu projeyi Codex ile eşli programlama yöntemiyle geliştirdim. Üretken yapay zekâdan şu alanlarda yararlandım:

- gereksinimleri küçük ve test edilebilir parçalara ayırma,
- alternatif veri modeli ve API sınırlarını karşılaştırma,
- sınır durumu ve kötüye kullanım senaryoları önerme,
- başlangıç kodu ve dokümantasyon taslağı oluşturma,
- test sonuçlarından sonra kodu yeniden gözden geçirme.

Çalışma zamanında herhangi bir yapay zekâ modeli kullanılmaz. Saklama tarihi deterministik bir tarih kuralıyla hesaplanır; sistem bir karar önerse bile kayıt üzerinde kesin işlem yapmaz. Saklama, anonimleştirme veya silme kararı yetkili bir insanın açık gerekçesiyle tamamlanır.

AI tarafından üretilen önerileri doğrulanmış gerçek gibi kabul etmedim. Yayımlanan sürümün otomatik testleri çalıştırıldı; mimari kararlar ADR dosyalarında, bilinen sınırlar README ve SECURITY belgelerinde görünür tutuldu. Kodun nihai sorumluluğu bana aittir.

Bu beyan, yapay zekâ desteğini gizlememek ve runtime karar desteğiyle geliştirme aracını birbirinden ayırmak için repoda tutulur.
