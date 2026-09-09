# Gereksinimler ve kabul kriterleri

## Problem

Bir veri kaydının yalnızca hangi tabloda bulunduğunu bilmek yeterli değildir. Neden tutulduğu, kimden sorulduğu ve ne zaman gözden geçirileceği çalışan sistemde görünür olmalıdır.

## İşlevsel gereksinimler

1. Kullanıcı kayıt adı, kategori, amaç, dayanak, konum, sorumlu rol, sentetik kişi referansı, toplama tarihi ve saklama süresi girebilmelidir.
2. Sistem bitiş tarihini toplama tarihi artı saklama günü olarak hesaplamalıdır.
3. Süresi geçmiş ve yedi gün içinde dolacak kayıtlar ayrı listelenmelidir.
4. Kayıt hakkında keep, anonymize veya delete kararı yalnızca data steward ve admin rolüyle verilebilmelidir.
5. Her kararda insan kimliği ve açıklanabilir gerekçe zorunlu olmalıdır.
6. Tüm değişiklikler birbirine bağlı denetim olayları üretmelidir.
7. Admin zincirin bütünlüğünü doğrulayabilmelidir.

## İşlevsel olmayan gereksinimler

- Gerçek kişisel veri içermeyen sentetik demo
- Klavye ile kullanılabilen, mobil ekrana uyumlu arayüz
- Temel iş kuralları için otomatik test
- Tek komutla yerel veya Docker çalıştırma
- Hata durumunda veri işlemini transaction ile geri alma

## Kapsam dışı

- Hukuki uygunluk kararı
- Gerçek kimlik doğrulama
- Bildirim gönderme
- Yedekleme ve felaket kurtarma
- Dağıtık ve değiştirilemez kayıt altyapısı
