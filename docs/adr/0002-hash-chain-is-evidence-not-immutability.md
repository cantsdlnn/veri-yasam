# ADR-0002: Hash zincirini değişmezlik değil tahrif sinyali olarak kullanmak

Durum: Kabul edildi

## Bağlam

Portföy demonstrasyonu, bir olay değiştirildiğinde bunu fark edebilmelidir. Dağıtık defter veya harici WORM depolama ilk sürüm için gereksiz karmaşıktır.

## Karar

Her olay; zaman, aktör, eylem, kaynak, kanonik payload ve önceki olay hash değerinden SHA-256 özeti üretir. Doğrulayıcı zinciri baştan hesaplar.

## Sonuçlar

- Tekil tahrif ve sıra değişikliği tespit edilir.
- Tasarım küçük ve test edilebilirdir.
- Veritabanının tamamına sahip saldırgan zinciri yeniden yazabilir.
- Üretimde imzalı checkpoint ve ayrı güven alanındaki olay deposu gerekir.
