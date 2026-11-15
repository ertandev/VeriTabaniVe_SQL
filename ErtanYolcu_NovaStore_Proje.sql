/*
================================================================================
    PROJE ADI: NovaStore E-Ticaret Veri Yönetim Sistemi
    GELİŞTİRİCİ: Ertan Yolcu
    VERİ TABANI: Microsoft SQL Server (T-SQL)
    AÇIKLAMA: Bu betik, NovaStore e-ticaret sistemi için ilişkisel veri tabanı
              tasarımını, örnek veri girişini, analitik DQL sorgularını,
              görünüm (View) ve yedekleme (Backup) komutlarını içerir.
================================================================================
*/

-- =============================================================================
-- BÖLÜM 1: Veri Tabanı Tasarımı (Logical Design ve DDL)
-- =============================================================================

-- 1. Veri Tabanı Oluşturma
IF NOT EXISTS (SELECT name FROM sys.databases WHERE name = N'NovaStoreDB')
BEGIN
    CREATE DATABASE NovaStoreDB;
END;
GO

USE NovaStoreDB;
GO

-- Bağımlılık sırasına göre eski tablolar varsa temizleme (Drop in reverse dependency order)
IF OBJECT_ID('dbo.OrderDetails', 'U') IS NOT NULL DROP TABLE dbo.OrderDetails;
IF OBJECT_ID('dbo.Orders', 'U') IS NOT NULL DROP TABLE dbo.Orders;
IF OBJECT_ID('dbo.Products', 'U') IS NOT NULL DROP TABLE dbo.Products;
IF OBJECT_ID('dbo.Customers', 'U') IS NOT NULL DROP TABLE dbo.Customers;
IF OBJECT_ID('dbo.Categories', 'U') IS NOT NULL DROP TABLE dbo.Categories;
GO

-- A. Tablo: Categories (Kategoriler)
-- CategoryID: Birincil anahtar (Primary Key), otomatik artan (Identity 1,1)
-- CategoryName: Kategori adı, boş geçilemez (Not Null)
CREATE TABLE dbo.Categories (
    CategoryID INT IDENTITY(1,1) NOT NULL,
    CategoryName VARCHAR(50) NOT NULL,
    CONSTRAINT PK_Categories PRIMARY KEY (CategoryID)
);
GO

-- C. Tablo: Customers (Müşteriler)
-- Not: Bağımlılık zincirinde Orders tablosundan önce oluşturulmalıdır.
-- CustomerID: Birincil anahtar, otomatik artan
-- FullName: Müşteri adı soyadı
-- City: Şehir bilgisi
-- Email: Benzersiz e-posta adresi (Unique)
CREATE TABLE dbo.Customers (
    CustomerID INT IDENTITY(1,1) NOT NULL,
    FullName VARCHAR(50) NOT NULL,
    City VARCHAR(20) NOT NULL,
    Email VARCHAR(100) NOT NULL,
    CONSTRAINT PK_Customers PRIMARY KEY (CustomerID),
    CONSTRAINT UQ_Customers_Email UNIQUE (Email)
);
GO

-- B. Tablo: Products (Ürünler)
-- ProductID: Birincil anahtar, otomatik artan
-- ProductName: Ürün adı, boş geçilemez
-- Price: Ürün satış fiyatı
-- Stock: Stok adedi (Varsayılan değer: 0)
-- CategoryID: Categories tablosuna bağlanan Yabancı Anahtar (Foreign Key)
CREATE TABLE dbo.Products (
    ProductID INT IDENTITY(1,1) NOT NULL,
    ProductName VARCHAR(100) NOT NULL,
    Price DECIMAL(10,2) NOT NULL,
    Stock INT NOT NULL CONSTRAINT DF_Products_Stock DEFAULT (0),
    CategoryID INT NOT NULL,
    CONSTRAINT PK_Products PRIMARY KEY (ProductID),
    CONSTRAINT FK_Products_Categories FOREIGN KEY (CategoryID) 
        REFERENCES dbo.Categories(CategoryID)
);
GO

-- D. Tablo: Orders (Siparişler)
-- OrderID: Birincil anahtar, otomatik artan
-- CustomerID: Customers tablosuna bağlanan Yabancı Anahtar
-- OrderDate: Sipariş tarihi (Varsayılan değer: GETDATE())
-- TotalAmount: Toplam sipariş tutarı
CREATE TABLE dbo.Orders (
    OrderID INT IDENTITY(1,1) NOT NULL,
    CustomerID INT NOT NULL,
    OrderDate DATETIME NOT NULL CONSTRAINT DF_Orders_OrderDate DEFAULT (GETDATE()),
    TotalAmount DECIMAL(10,2) NOT NULL,
    CONSTRAINT PK_Orders PRIMARY KEY (OrderID),
    CONSTRAINT FK_Orders_Customers FOREIGN KEY (CustomerID) 
        REFERENCES dbo.Customers(CustomerID)
);
GO

-- E. Tablo: OrderDetails (Sipariş Detayları - Ara Tablo)
-- DetailID: Birincil anahtar, otomatik artan
-- OrderID: Orders tablosuna bağlanan Yabancı Anahtar
-- ProductID: Products tablosuna bağlanan Yabancı Anahtar
-- Quantity: Kaç adet alındığı bilgisi
CREATE TABLE dbo.OrderDetails (
    DetailID INT IDENTITY(1,1) NOT NULL,
    OrderID INT NOT NULL,
    ProductID INT NOT NULL,
    Quantity INT NOT NULL,
    CONSTRAINT PK_OrderDetails PRIMARY KEY (DetailID),
    CONSTRAINT FK_OrderDetails_Orders FOREIGN KEY (OrderID) 
        REFERENCES dbo.Orders(OrderID),
    CONSTRAINT FK_OrderDetails_Products FOREIGN KEY (ProductID) 
        REFERENCES dbo.Products(ProductID)
);
GO

-- =============================================================================
-- BÖLÜM 2: Veri Girişi (DML - Insert)
-- =============================================================================

-- Görev 1: 5 Adet Kategori Ekleme
INSERT INTO dbo.Categories (CategoryName) VALUES
('Elektronik'),
('Giyim'),
('Kitap'),
('Kozmetik'),
('Ev ve Yaşam');
GO

-- Görev 2: Her kategoriye ait olacak şekilde toplam 13 adet Ürün Ekleme
-- (Farklı fiyat ve stok seviyeleri, analiz senaryoları için stok < 20 olanlar dahil)
INSERT INTO dbo.Products (ProductName, Price, Stock, CategoryID) VALUES
('Kablosuz Kulaklık ANC', 1450.00, 12, 1),        -- Kategori: Elektronik (Stok < 20)
('Akıllı Saat Pro', 3200.00, 8, 1),              -- Kategori: Elektronik (Stok < 20)
('Bluetooth Hoparlör', 950.00, 25, 1),           -- Kategori: Elektronik
('Deri Ceket', 2850.00, 5, 2),                    -- Kategori: Giyim (Stok < 20)
('Pamuklu Kapüşonlu Sweatshirt', 650.00, 35, 2), -- Kategori: Giyim
('Slim Fit Jean Pantolon', 850.00, 18, 2),        -- Kategori: Giyim (Stok < 20)
('Veri Tabanı Yönetim Sistemleri', 220.00, 50, 3),-- Kategori: Kitap
('Yazılım Mimarisi ve Clean Code', 280.00, 14, 3), -- Kategori: Kitap (Stok < 20)
('Özel Tasarım Dolma Kalem', 450.00, 30, 3),      -- Kategori: Kitap
('Nemlendirici Yüz Bakım Kremi', 380.00, 40, 4), -- Kategori: Kozmetik
('Doğal Esanslı Parfüm 100ml', 1950.00, 7, 4),   -- Kategori: Kozmetik (Stok < 20)
('Otomatik Filtre Kahve Makinesi', 2400.00, 15, 5),-- Kategori: Ev ve Yaşam (Stok < 20)
('Paslanmaz Çelik Termos 1L', 550.00, 60, 5);     -- Kategori: Ev ve Yaşam
GO

-- Görev 3: 6 Adet Müşteri Kaydı Oluşturma
INSERT INTO dbo.Customers (FullName, City, Email) VALUES
('Ahmet Yılmaz', 'İstanbul', 'ahmet.yilmaz@email.com'),
('Ayşe Kaya', 'Ankara', 'ayse.kaya@email.com'),
('Mehmet Demir', 'İzmir', 'mehmet.demir@email.com'),
('Fatma Şahin', 'Bursa', 'fatma.sahin@email.com'),
('Can Yıldız', 'Antalya', 'can.yildiz@email.com'),
('Zeynep Çelik', 'Eskişehir', 'zeynep.celik@email.com');
GO

-- Görev 4: Farklı tarihlerde yapılmış 10 Adet Sipariş ve Sipariş Detayları Ekleme
-- Siparişler (Farklı tarih aralıkları DATEDIFF analizi için DATEADD ile girilmiştir)
INSERT INTO dbo.Orders (CustomerID, OrderDate, TotalAmount) VALUES
(1, DATEADD(DAY, -45, GETDATE()), 4650.00), -- Sipariş 1: Ahmet Yılmaz (45 gün önce)
(2, DATEADD(DAY, -38, GETDATE()), 1300.00), -- Sipariş 2: Ayşe Kaya (38 gün önce)
(3, DATEADD(DAY, -30, GETDATE()), 2400.00), -- Sipariş 3: Mehmet Demir (30 gün önce)
(1, DATEADD(DAY, -22, GETDATE()), 1450.00), -- Sipariş 4: Ahmet Yılmaz (22 gün önce)
(4, DATEADD(DAY, -18, GETDATE()), 3800.00), -- Sipariş 5: Fatma Şahin (18 gün önce)
(5, DATEADD(DAY, -12, GETDATE()), 950.00),  -- Sipariş 6: Can Yıldız (12 gün önce)
(2, DATEADD(DAY, -8, GETDATE()), 1950.00),  -- Sipariş 7: Ayşe Kaya (8 gün önce)
(6, DATEADD(DAY, -5, GETDATE()), 1400.00),  -- Sipariş 8: Zeynep Çelik (5 gün önce)
(1, DATEADD(DAY, -2, GETDATE()), 850.00),   -- Sipariş 9: Ahmet Yılmaz (2 gün önce)
(3, GETDATE(), 500.00);                    -- Sipariş 10: Mehmet Demir (Bugün)
GO

-- Sipariş Detayları (OrderDetails)
INSERT INTO dbo.OrderDetails (OrderID, ProductID, Quantity) VALUES
-- Sipariş 1 Detayları (Ahmet Yılmaz)
(1, 2, 1), -- Akıllı Saat Pro (1 Adet)
(1, 1, 1), -- Kablosuz Kulaklık ANC (1 Adet)

-- Sipariş 2 Detayları (Ayşe Kaya)
(2, 5, 2), -- Pamuklu Sweatshirt (2 Adet)

-- Sipariş 3 Detayları (Mehmet Demir)
(3, 12, 1), -- Otomatik Filtre Kahve Makinesi (1 Adet)

-- Sipariş 4 Detayları (Ahmet Yılmaz)
(4, 1, 1), -- Kablosuz Kulaklık ANC (1 Adet)

-- Sipariş 5 Detayları (Fatma Şahin)
(5, 4, 1), -- Deri Ceket (1 Adet)
(5, 3, 1), -- Bluetooth Hoparlör (1 Adet)

-- Sipariş 6 Detayları (Can Yıldız)
(6, 3, 1), -- Bluetooth Hoparlör (1 Adet)

-- Sipariş 7 Detayları (Ayşe Kaya)
(7, 11, 1), -- Doğal Esanslı Parfüm 100ml (1 Adet)

-- Sipariş 8 Detayları (Zeynep Çelik)
(8, 6, 1), -- Slim Fit Jean Pantolon (1 Adet)
(8, 13, 1), -- Paslanmaz Çelik Termos 1L (1 Adet)

-- Sipariş 9 Detayları (Ahmet Yılmaz)
(9, 6, 1), -- Slim Fit Jean Pantolon (1 Adet)

-- Sipariş 10 Detayları (Mehmet Demir)
(10, 8, 1), -- Yazılım Mimarisi ve Clean Code (1 Adet)
(10, 7, 1); -- Veri Tabanı Yönetim Sistemleri (1 Adet)
GO
