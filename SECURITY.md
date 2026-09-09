# Güvenlik politikası

VeriYaşam eğitim amaçlı bir demonstrasyondur. Gerçek kişisel veya özel nitelikli veriyle kullanılmamalıdır.

## Desteklenen sürüm

Yalnızca en güncel main dalı güvenlik düzeltmeleri alır.

## Bildirim

Bir güvenlik sorunu bulursanız herkese açık issue içinde gerçek veri, anahtar veya istismar ayrıntısı paylaşmayın. GitHub Security Advisory üzerinden özel bildirim oluşturun.

## Tehdit sınırları

- X-Demo-Role yalnızca rol matrisini göstermek içindir; kimlik doğrulama değildir.
- SQLite dosyasına işletim sistemi düzeyinde erişebilen bir kullanıcı kayıtları değiştirebilir.
- Hash zinciri kazara veya tekil olay tahrifini tespit eder; harici imza veya değiştirilemez depolama sağlamaz.
- Demo silme işlemi kanıtı korumak için kaydı maskeler. Gerçek sistemde fiziksel silme, yedekler ve yasal saklama istisnaları ayrıca tasarlanmalıdır.
