# Doğrulama raporu

Tarih: 9 Eylül 2026
Ortam: Windows, Python 3.11.9

## Otomatik test

Komut: python -m pytest

Sonuç: 8 test geçti, 0 test başarısız oldu.

- `ruff check .`: başarılı
- `ruff format --check .`: 20 dosya biçimli
- `pip-audit --local`: bilinen bağımlılık açığı bulunmadı

Kapsanan davranışlar:

- artık yıl tarih sınırı,
- sıfır ve negatif saklama süresinin reddi,
- yedi günlük gözden geçirme sınırı,
- süresi geçmiş kayıt tespiti,
- viewer rolünün yazma işleminin engellenmesi,
- kayıt oluşturma ve insan onaylı anonimleştirme akışı,
- admin denetim zinciri doğrulaması,
- geçmiş audit payload değiştiğinde tahrif tespiti.

Bağımlılık katmanından iki deprecation uyarısı raporlandı; uygulama testlerinde başarısızlık veya proje kaynaklı warning bulunmadı. Uyarılar FastAPI TestClient ile Starlette sürüm geçişine ilişkindir ve sonraki bağımlılık güncellemesinde yeniden değerlendirilecektir.

## Sözdizimi ve başlangıç testi

- python -m compileall -q app: başarılı
- GET /health: HTTP 200 ve status=ok
- GET /: HTTP 200

## Henüz doğrulanmayanlar

- Uzun süreli yük ve eşzamanlı yazma testi
- Gerçek kimlik sağlayıcısı entegrasyonu
- PostgreSQL geçişi
- Tarayıcı/ekran okuyucu ile manuel WCAG incelemesi

Bu sınırlar README içinde üretime hazır olmama notuyla birlikte açıkça belirtilmiştir.
