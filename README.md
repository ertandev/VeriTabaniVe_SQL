# NovaStore E-Ticaret Veri Yönetim Sistemi

Bu proje, 5 günlük SQL eğitimi bitirme projesi kapsamında NovaStore e-ticaret platformu için tasarlanmış ilişkisel veri tabanı yönetim ve analiz sistemidir.

## Proje İçeriği
- **BÖLÜM 1: Veri Tabanı Tasarımı (DDL)**: `NovaStoreDB` veri tabanı, tablolar, birincil anahtarlar (PK), yabancı anahtarlar (FK), kısıtlayıcılar (Constraints) ve veri tipleri.
- **BÖLÜM 2: Veri Girişi (DML)**: Test ve analiz için tutarlı örnek veri (dummy data) seti.
- **BÖLÜM 3: Sorgulama ve Analiz (DQL)**: Yönetim kurulunun ihtiyaç duyduğu stok, müşteri, sipariş, ciro ve zaman analizleri (Join, Group By, Subquery, Aggregate).
- **BÖLÜM 4: İleri Seviye Veri Tabanı Nesneleri**: Sipariş özet görünümü (`VIEW`) ve tam veritabanı yedeği (`BACKUP DATABASE`) betiği.
- **BÖLÜM 5: Teslim Dosyaları**:
  - `ErtanYolcu_NovaStore_Proje.sql` : Tüm T-SQL komutlarını içeren ana betik dosyası.
  - `ErtanYolcu_NovaStore_Proje.docx`: Kod blokları, çıktı tabloları ve açıklamaları içeren Word raporu.
  - `ErtanYolcu_NovaStore_Proje.png` : İlişkisel veri tabanı şema (ER) diyagramı.

## Mac Ortamında Microsoft SQL Server Çalıştırma (Docker)
Microsoft SQL Server yerel bir macOS uygulaması olarak sunulmadığından, Mac ortamında (özellikle Apple Silicon M1/M2/M3/M4) SQL Server çalıştırmak için en standart ve kararlı yöntem **Docker** kullanmaktır.

```bash
# Docker üzerinde Azure SQL Edge (veya MSSQL 2022) başlatmak için:
docker run --cap-add SYS_PTRACE -e 'ACCEPT_EULA=1' -e 'MSSQL_SA_PASSWORD=YourStrong@Passw0rd' -p 1433:1433 --name novastore_sql -d mcr.microsoft.com/azure-sql-edge:latest
```
Görsel yönetim aracı olarak Mac için Microsoft'un resmi aracı **Azure Data Studio** veya **DBeaver** kullanılabilir.
