# Mimari

## Bileşenler

- Web arayüzü: Envanter ve karar akışını görünür kılan yalın HTML, CSS ve JavaScript.
- FastAPI: Şema doğrulama, rol kontrolü ve HTTP uç noktaları.
- Kural motoru: Saklama bitişi ile review_due ve overdue durumlarını saf fonksiyonlarla hesaplar.
- SQLite: Envanter, insan kararları ve denetim olaylarını transaction içinde saklar.
- Denetim zinciri: Her olayın kanonik JSON yükünü ve önceki olay özetini yeni SHA-256 özetine bağlar.

## Veri akışı

    Kayıt isteği
        |
    Pydantic doğrulama
        |
    Rol kontrolü
        |
    SQLite transaction
       / \
    Varlık  Denetim olayı

Karar uç noktası varlığı ve karar kaydını aynı transaction içinde günceller. Böylece iş durumu değişip denetim olayının yazılmaması veya tersinin gerçekleşmesi engellenir.

## Güven sınırı

Tarayıcıdaki rol başlığına güvenilmez; bu yalnızca portföy demosudur. Üretim tasarımında kimlik, güvenilir bir OpenID Connect sağlayıcısından gelir ve rol kontrolü sunucuda imzalı taleple yapılır.

## Ölçekleme yolu

SQLite yerine PostgreSQL, tek süreç yerine yatay FastAPI örnekleri, dosya temelli log yerine harici imzalı olay deposu ve migration aracı eklenebilir. Bu değişiklikler demo kapsamını gereksiz büyütmemek için ilk sürüme alınmamıştır.
