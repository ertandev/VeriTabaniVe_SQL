import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn
import pymssql
import os

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def add_code_block(doc, code_text):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    
    cell = tbl.cell(0, 0)
    cell.width = Inches(6.5)
    set_cell_background(cell, "1E293B")  # Dark slate background
    set_cell_margins(cell, top=140, bottom=140, left=200, right=200)

    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.line_spacing = 1.15

    for line in code_text.strip().split('\n'):
        run = p.add_run(line + '\n')
        run.font.name = 'Courier New'
        run.font.size = Pt(8.5)
        # Simple syntax tinting
        s_line = line.strip().upper()
        if line.strip().startswith('--') or line.strip().startswith('/*'):
            run.font.color.rgb = RGBColor(148, 163, 184) # Comment gray
        elif any(s_line.startswith(kw) for kw in ['SELECT', 'FROM', 'WHERE', 'INSERT', 'CREATE', 'ALTER', 'DROP', 'GROUP BY', 'ORDER BY', 'INNER JOIN', 'LEFT JOIN', 'BACKUP']):
            run.font.color.rgb = RGBColor(56, 189, 248) # Cyan/blue
        else:
            run.font.color.rgb = RGBColor(241, 245, 249) # White/light slate

    # Space after code block
    sp_p = doc.add_paragraph()
    sp_p.paragraph_format.space_after = Pt(4)

def format_result_table(table, col_names, rows_data):
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    
    # Header row
    hdr_cells = table.rows[0].cells
    for i, name in enumerate(col_names):
        hdr_cells[i].text = name
        set_cell_background(hdr_cells[i], "0F766E") # Teal header
        set_cell_margins(hdr_cells[i], top=100, bottom=100, left=120, right=120)
        p = hdr_cells[i].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for run in p.runs:
            run.font.bold = True
            run.font.name = 'Calibri'
            run.font.size = Pt(9)
            run.font.color.rgb = RGBColor(255, 255, 255)

    # Data rows
    for r_idx, row_data in enumerate(rows_data):
        row_cells = table.rows[r_idx + 1].cells
        bg_color = "F8FAFC" if r_idx % 2 == 0 else "FFFFFF"
        for c_idx, val in enumerate(row_data):
            row_cells[c_idx].text = str(val) if val is not None else 'NULL'
            set_cell_background(row_cells[c_idx], bg_color)
            set_cell_margins(row_cells[c_idx], top=80, bottom=80, left=120, right=120)
            p = row_cells[c_idx].paragraphs[0]
            # align numbers right, text left
            if str(val).replace('.', '', 1).isdigit() and len(str(val)) < 8:
                p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            for run in p.runs:
                run.font.name = 'Calibri'
                run.font.size = Pt(8.5)
                run.font.color.rgb = RGBColor(30, 41, 59)

def main():
    doc = Document()

    # Page Margins: 1 inch (72pt)
    for section in doc.sections:
        section.top_margin = Inches(0.8)
        section.bottom_margin = Inches(0.8)
        section.left_margin = Inches(0.8)
        section.right_margin = Inches(0.8)

    # Database connection
    conn = pymssql.connect(server='localhost', port=1433, user='sa', password='NovaStore@2026!', database='NovaStoreDB')
    cur = conn.cursor()

    # ================= COVER / HEADER =================
    title_p = doc.add_paragraph()
    title_p.paragraph_format.space_before = Pt(12)
    title_p.paragraph_format.space_after = Pt(2)
    r_title = title_p.add_run("NovaStore E-Ticaret Veri Yönetim Sistemi")
    r_title.font.name = 'Arial'
    r_title.font.size = Pt(22)
    r_title.font.bold = True
    r_title.font.color.rgb = RGBColor(15, 23, 42)

    sub_p = doc.add_paragraph()
    sub_p.paragraph_format.space_after = Pt(14)
    r_sub = sub_p.add_run("SQL Eğitimi Bitirme Projesi & DBA Teknik Yönetim Raporu")
    r_sub.font.name = 'Arial'
    r_sub.font.size = Pt(13)
    r_sub.font.color.rgb = RGBColor(14, 116, 144)

    # Metadata Box
    meta_tbl = doc.add_table(rows=2, cols=2)
    meta_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta_info = [
        ("Geliştirici / DBA:", "Ertan Yolcu", "Veritabanı Motoru:", "Microsoft SQL Server 2022 / Azure SQL"),
        ("Tarih:", "15 Kasım 2026", "Teslim Formatı:", "T-SQL Script (.sql), Rapor (.docx), Şema (.png)")
    ]
    for row_idx, (k1, v1, k2, v2) in enumerate(meta_info):
        cells = meta_tbl.rows[row_idx].cells
        set_cell_background(cells[0], "F1F5F9")
        set_cell_background(cells[1], "F1F5F9")
        set_cell_margins(cells[0], top=60, bottom=60, left=100, right=100)
        set_cell_margins(cells[1], top=60, bottom=60, left=100, right=100)
        p0 = cells[0].paragraphs[0]
        r0 = p0.add_run(f"{k1} ")
        r0.font.bold = True
        r0.font.size = Pt(9)
        r0_val = p0.add_run(v1)
        r0_val.font.size = Pt(9)
        
        p1 = cells[1].paragraphs[0]
        r1 = p1.add_run(f"{k2} ")
        r1.font.bold = True
        r1.font.size = Pt(9)
        r1_val = p1.add_run(v2)
        r1_val.font.size = Pt(9)

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # ================= GİRİŞ VE SENARYO =================
    h1 = doc.add_heading("Projenin Amacı ve Senaryo", level=1)
    h1.paragraph_format.space_before = Pt(12)
    h1.paragraph_format.space_after = Pt(4)
    for r in h1.runs:
        r.font.color.rgb = RGBColor(15, 23, 42)

    p_intro = doc.add_paragraph(
        "Bu proje, NovaStore adlı yeni kurulan e-ticaret şirketinin veri tabanı yöneticisi (DBA) olarak, "
        "şirketin ilişkisel veri modelinin sıfırdan tasarlanması, ilişkisel bütünlüğün (Primary Key, Foreign Key, "
        "Unique, Default constraints) kurulması, test verilerinin oluşturulması ve yönetim kurulunun ihtiyaç duyduğu "
        "kritik analiz raporlarının (stok, ciro, zaman, müşteri davranışları) T-SQL sorguları ile hazırlanmasını kapsar."
    )
    p_intro.paragraph_format.line_spacing = 1.15
    p_intro.paragraph_format.space_after = Pt(12)

    # ================= BÖLÜM 1: DDL =================
    h2 = doc.add_heading("BÖLÜM 1: Veri Tabanı Tasarımı (Logical Design ve DDL)", level=1)
    h2.paragraph_format.space_before = Pt(12)
    for r in h2.runs:
        r.font.color.rgb = RGBColor(15, 23, 42)

    doc.add_paragraph(
        "Veri tabanı bağımlılık prensiplerine göre öncelikle ana (ebeveyn) tablolar olan Categories ve Customers, "
        "ardından bu tablolara yabancı anahtar (FK) ile bağlı olan Products ve Orders, son olarak da çoka-çok ilişkiyi "
        "çözen OrderDetails ara tablosu oluşturulmuştur."
    )

    ddl_code = """-- NovaStoreDB Veri Tabanı ve Tablo Şemaları (DDL)
CREATE DATABASE NovaStoreDB;
GO
USE NovaStoreDB;
GO

-- 1. Categories Tablosu
CREATE TABLE dbo.Categories (
    CategoryID INT IDENTITY(1,1) NOT NULL,
    CategoryName VARCHAR(50) NOT NULL,
    CONSTRAINT PK_Categories PRIMARY KEY (CategoryID)
);

-- 2. Customers Tablosu
CREATE TABLE dbo.Customers (
    CustomerID INT IDENTITY(1,1) NOT NULL,
    FullName VARCHAR(50) NOT NULL,
    City VARCHAR(20) NOT NULL,
    Email VARCHAR(100) NOT NULL,
    CONSTRAINT PK_Customers PRIMARY KEY (CustomerID),
    CONSTRAINT UQ_Customers_Email UNIQUE (Email)
);

-- 3. Products Tablosu
CREATE TABLE dbo.Products (
    ProductID INT IDENTITY(1,1) NOT NULL,
    ProductName VARCHAR(100) NOT NULL,
    Price DECIMAL(10,2) NOT NULL,
    Stock INT NOT NULL CONSTRAINT DF_Products_Stock DEFAULT (0),
    CategoryID INT NOT NULL,
    CONSTRAINT PK_Products PRIMARY KEY (ProductID),
    CONSTRAINT FK_Products_Categories FOREIGN KEY (CategoryID) REFERENCES dbo.Categories(CategoryID)
);

-- 4. Orders Tablosu
CREATE TABLE dbo.Orders (
    OrderID INT IDENTITY(1,1) NOT NULL,
    CustomerID INT NOT NULL,
    OrderDate DATETIME NOT NULL CONSTRAINT DF_Orders_OrderDate DEFAULT (GETDATE()),
    TotalAmount DECIMAL(10,2) NOT NULL,
    CONSTRAINT PK_Orders PRIMARY KEY (OrderID),
    CONSTRAINT FK_Orders_Customers FOREIGN KEY (CustomerID) REFERENCES dbo.Customers(CustomerID)
);

-- 5. OrderDetails Tablosu (Ara Tablo)
CREATE TABLE dbo.OrderDetails (
    DetailID INT IDENTITY(1,1) NOT NULL,
    OrderID INT NOT NULL,
    ProductID INT NOT NULL,
    Quantity INT NOT NULL,
    CONSTRAINT PK_OrderDetails PRIMARY KEY (DetailID),
    CONSTRAINT FK_OrderDetails_Orders FOREIGN KEY (OrderID) REFERENCES dbo.Orders(OrderID),
    CONSTRAINT FK_OrderDetails_Products FOREIGN KEY (ProductID) REFERENCES dbo.Products(ProductID)
);"""
    add_code_block(doc, ddl_code)

    # ================= ŞEMA GÖRSELİ =================
    h2_img = doc.add_heading("İlişkisel Veri Tabanı Şeması (ER Diyagramı)", level=2)
    for r in h2_img.runs:
        r.font.color.rgb = RGBColor(15, 23, 42)

    doc.add_paragraph("Aşağıda NovaStoreDB veri tabanının tablolar arası 1:N ve M:N ilişkilerini, Primary Key (PK) ve Foreign Key (FK) bağımlılıklarını gösteren ilişkisel şeması yer almaktadır:")
    
    img_path = "/Users/Ertan/Desktop/ErtanYolcu_NovaStore_Proje/ErtanYolcu_NovaStore_Proje.png"
    if os.path.exists(img_path):
        doc.add_picture(img_path, width=Inches(6.5))
        cap = doc.add_paragraph("Şekil 1: NovaStoreDB İlişkisel Veri Tabanı Mimarisi (Entity-Relationship Diyagramı)")
        cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        cap.paragraph_format.space_after = Pt(12)
        for r in cap.runs:
            r.font.size = Pt(8.5)
            r.font.italic = True
            r.font.color.rgb = RGBColor(100, 116, 139)

    # ================= BÖLÜM 2: DML =================
    h2_dml = doc.add_heading("BÖLÜM 2: Veri Girişi (DML - Insert)", level=1)
    for r in h2_dml.runs:
        r.font.color.rgb = RGBColor(15, 23, 42)

    doc.add_paragraph(
        "Sistemin analiz senaryolarını test edebilmek amacıyla 5 kategori, 13 ürün, 6 müşteri, "
        "farklı tarihlerde gerçekleşen 10 sipariş ve bunlara ait 14 sipariş detayı ilişkisel bütünlük kurallarına uygun olarak eklenmiştir."
    )

    dml_code = """-- BÖLÜM 2: Örnek Veri Girişi (DML)
-- Kategoriler (5 Adet)
INSERT INTO dbo.Categories (CategoryName) VALUES
('Elektronik'), ('Giyim'), ('Kitap'), ('Kozmetik'), ('Ev ve Yaşam');

-- Müşteriler (6 Adet)
INSERT INTO dbo.Customers (FullName, City, Email) VALUES
('Ahmet Yılmaz', 'İstanbul', 'ahmet.yilmaz@email.com'),
('Ayşe Kaya', 'Ankara', 'ayse.kaya@email.com'),
('Mehmet Demir', 'İzmir', 'mehmet.demir@email.com'),
('Fatma Şahin', 'Bursa', 'fatma.sahin@email.com'),
('Can Yıldız', 'Antalya', 'can.yildiz@email.com'),
('Zeynep Çelik', 'Eskişehir', 'zeynep.celik@email.com');

-- Ürünler (13 Adet - Çeşitli Stok ve Fiyatlar)
INSERT INTO dbo.Products (ProductName, Price, Stock, CategoryID) VALUES
('Kablosuz Kulaklık ANC', 1450.00, 12, 1),
('Akıllı Saat Pro', 3200.00, 8, 1),
('Bluetooth Hoparlör', 950.00, 25, 1),
('Deri Ceket', 2850.00, 5, 2),
('Pamuklu Kapüşonlu Sweatshirt', 650.00, 35, 2),
('Slim Fit Jean Pantolon', 850.00, 18, 2),
('Veri Tabanı Yönetim Sistemleri', 220.00, 50, 3),
('Yazılım Mimarisi ve Clean Code', 280.00, 14, 3),
('Özel Tasarım Dolma Kalem', 450.00, 30, 3),
('Nemlendirici Yüz Bakım Kremi', 380.00, 40, 4),
('Doğal Esanslı Parfüm 100ml', 1950.00, 7, 4),
('Otomatik Filtre Kahve Makinesi', 2400.00, 15, 5),
('Paslanmaz Çelik Termos 1L', 550.00, 60, 5);

-- Siparişler (Farklı gün aralıklarında 10 Sipariş)
INSERT INTO dbo.Orders (CustomerID, OrderDate, TotalAmount) VALUES
(1, DATEADD(DAY, -45, GETDATE()), 4650.00),
(2, DATEADD(DAY, -38, GETDATE()), 1300.00),
(3, DATEADD(DAY, -30, GETDATE()), 2400.00),
(1, DATEADD(DAY, -22, GETDATE()), 1450.00),
(4, DATEADD(DAY, -18, GETDATE()), 3800.00),
(5, DATEADD(DAY, -12, GETDATE()), 950.00),
(2, DATEADD(DAY, -8, GETDATE()), 1950.00),
(6, DATEADD(DAY, -5, GETDATE()), 1400.00),
(1, DATEADD(DAY, -2, GETDATE()), 850.00),
(3, GETDATE(), 500.00);"""
    add_code_block(doc, dml_code)

    # ================= BÖLÜM 3: DQL SORGULARI =================
    h2_dql = doc.add_heading("BÖLÜM 3: Sorgulama ve Analiz (DQL - Select ve Joins)", level=1)
    for r in h2_dql.runs:
        r.font.color.rgb = RGBColor(15, 23, 42)

    doc.add_paragraph(
        "Yönetim kurulunun karar destek süreçlerinde kullanacağı 6 adet analitik rapor sorgusu hazırlanmış "
        "ve SQL Server üzerinde çalıştırılarak gerçek sonuçlar elde edilmiştir."
    )

    # 3.1
    doc.add_heading("1. Temel Listeleme (Kritik Stok Raporu)", level=2)
    doc.add_paragraph(
        "Soru: Stok miktarı 20'den az olan ürünlerin adını ve stok miktarını, stok miktarına göre AZALAN sırada listeleyin.\n"
        "Kullanılan Teknikler: SELECT, WHERE (filtreleme), ORDER BY ... DESC (azalan sıralama)."
    )
    q1_sql = """SELECT 
    p.ProductName AS [Ürün Adı],
    p.Stock AS [Stok Miktarı]
FROM dbo.Products AS p
WHERE p.Stock < 20
ORDER BY p.Stock DESC;"""
    add_code_block(doc, q1_sql)

    cur.execute("SELECT ProductName, Stock FROM dbo.Products WHERE Stock < 20 ORDER BY Stock DESC;")
    q1_rows = cur.fetchall()
    t1 = doc.add_table(rows=len(q1_rows)+1, cols=2)
    format_result_table(t1, ["Ürün Adı", "Stok Miktarı"], q1_rows)
    p_desc1 = doc.add_paragraph("Analiz Açıklaması: Tedarik zinciri yöneticisi bu rapor sayesinde kritik stok seviyesinde (20 altı) bulunan 7 ürünü tespit edebilir ve acil sipariş planlaması yapabilir.")
    p_desc1.paragraph_format.space_before = Pt(4)
    p_desc1.paragraph_format.space_after = Pt(12)

    # 3.2
    doc.add_heading("2. Veri Birleştirme (Müşteri ve Sipariş Raporu)", level=2)
    doc.add_paragraph(
        "Soru: Hangi müşteri, hangi tarihte sipariş vermiş? Müşteri Adı, Şehir, Sipariş Tarihi ve Toplam Tutar listelensin.\n"
        "Kullanılan Teknikler: INNER JOIN (Customers ve Orders tablolarının CustomerID üzerinden bağlanması)."
    )
    q2_sql = """SELECT 
    c.FullName AS [Müşteri Adı],
    c.City AS [Şehir],
    CONVERT(VARCHAR(19), o.OrderDate, 120) AS [Sipariş Tarihi],
    o.TotalAmount AS [Toplam Tutar]
FROM dbo.Customers AS c
INNER JOIN dbo.Orders AS o 
    ON c.CustomerID = o.CustomerID
ORDER BY o.OrderDate DESC;"""
    add_code_block(doc, q2_sql)

    cur.execute("""SELECT c.FullName, c.City, CONVERT(VARCHAR(19), o.OrderDate, 120), o.TotalAmount 
                   FROM dbo.Customers c INNER JOIN dbo.Orders o ON c.CustomerID = o.CustomerID 
                   ORDER BY o.OrderDate DESC;""")
    q2_rows = cur.fetchall()
    t2 = doc.add_table(rows=len(q2_rows)+1, cols=4)
    format_result_table(t2, ["Müşteri Adı", "Şehir", "Sipariş Tarihi", "Toplam Tutar (TL)"], q2_rows)
    p_desc2 = doc.add_paragraph("Analiz Açıklaması: Tüm müşterilerin sipariş hareketleri kronolojik sırada listelenmiş; coğrafi dağılım ve işlem tutarları net bir şekilde ortaya konmuştur.")
    p_desc2.paragraph_format.space_before = Pt(4)
    p_desc2.paragraph_format.space_after = Pt(12)

    # 3.3
    doc.add_heading("3. Çoklu Birleştirme ve Detay Raporu (Müşteri Sepet Detayı)", level=2)
    doc.add_paragraph(
        "Soru: 'Ahmet Yılmaz' isimli müşterinin aldığı ürünlerin isimlerini, fiyatlarını ve kategorilerini listeleyin.\n"
        "Kullanılan Teknikler: 5 tablonun zincirleme INNER JOIN ile bağlanması (Customers -> Orders -> OrderDetails -> Products -> Categories)."
    )
    q3_sql = """SELECT 
    c.FullName AS [Müşteri Adı],
    p.ProductName AS [Ürün Adı],
    p.Price AS [Birim Fiyat],
    cat.CategoryName AS [Kategori Adı]
FROM dbo.Customers AS c
INNER JOIN dbo.Orders AS o 
    ON c.CustomerID = o.CustomerID
INNER JOIN dbo.OrderDetails AS od 
    ON o.OrderID = od.OrderID
INNER JOIN dbo.Products AS p 
    ON od.ProductID = p.ProductID
INNER JOIN dbo.Categories AS cat 
    ON p.CategoryID = cat.CategoryID
WHERE c.FullName = 'Ahmet Yılmaz';"""
    add_code_block(doc, q3_sql)

    cur.execute("""SELECT c.FullName, p.ProductName, p.Price, cat.CategoryName
                   FROM dbo.Customers c
                   INNER JOIN dbo.Orders o ON c.CustomerID = o.CustomerID
                   INNER JOIN dbo.OrderDetails od ON o.OrderID = od.OrderID
                   INNER JOIN dbo.Products p ON od.ProductID = p.ProductID
                   INNER JOIN dbo.Categories cat ON p.CategoryID = cat.CategoryID
                   WHERE c.FullName = 'Ahmet Yılmaz';""")
    q3_rows = cur.fetchall()
    t3 = doc.add_table(rows=len(q3_rows)+1, cols=4)
    format_result_table(t3, ["Müşteri Adı", "Ürün Adı", "Birim Fiyat (TL)", "Kategori Adı"], q3_rows)
    p_desc3 = doc.add_paragraph("Analiz Açıklaması: Ahmet Yılmaz isimli müşterinin hem Elektronik hem de Giyim kategorilerinden alışveriş yaptığı, sepet derinliğinin ve ürün tercihlerinin analizi sağlanmıştır.")
    p_desc3.paragraph_format.space_before = Pt(4)
    p_desc3.paragraph_format.space_after = Pt(12)

    # 3.4
    doc.add_heading("4. Gruplama ve Aggregate Fonksiyonlar (Kategori Envanter Raporu)", level=2)
    doc.add_paragraph(
        "Soru: Hangi kategoride toplam kaç adet ürünümüz var? (Örn: Elektronik - 5 ürün).\n"
        "Kullanılan Teknikler: GROUP BY, COUNT(p.ProductID), LEFT JOIN (ürün atanmamış kategori olsa dahi 0 sayısını gösterebilmek için)."
    )
    q4_sql = """SELECT 
    cat.CategoryName AS [Kategori Adı],
    COUNT(p.ProductID) AS [Toplam Ürün Sayısı]
FROM dbo.Categories AS cat
LEFT JOIN dbo.Products AS p 
    ON cat.CategoryID = p.CategoryID
GROUP BY cat.CategoryID, cat.CategoryName
ORDER BY [Toplam Ürün Sayısı] DESC;"""
    add_code_block(doc, q4_sql)

    cur.execute("""SELECT cat.CategoryName, COUNT(p.ProductID)
                   FROM dbo.Categories cat
                   LEFT JOIN dbo.Products p ON cat.CategoryID = p.CategoryID
                   GROUP BY cat.CategoryID, cat.CategoryName
                   ORDER BY COUNT(p.ProductID) DESC;""")
    q4_rows = cur.fetchall()
    t4 = doc.add_table(rows=len(q4_rows)+1, cols=2)
    format_result_table(t4, ["Kategori Adı", "Toplam Ürün Çeşidi Sayısı"], q4_rows)
    p_desc4 = doc.add_paragraph("Analiz Açıklaması: Şirketin ürün portföyünün dengeli olduğu; Elektronik, Giyim ve Kitap kategorilerinde 3'er, Kozmetik ve Ev & Yaşam'da 2'şer çeşit ürün bulunduğu görülmektedir.")
    p_desc4.paragraph_format.space_before = Pt(4)
    p_desc4.paragraph_format.space_after = Pt(12)

    # 3.5
    doc.add_heading("5. Ciro Analizi (En Değerli Müşteriler - VIP Analizi)", level=2)
    doc.add_paragraph(
        "Soru: Her müşterinin şirkete kazandırdığı toplam ciro nedir? En çok harcama yapan müşteriden en aza doğru sıralayın.\n"
        "Kullanılan Teknikler: SUM(TotalAmount), GROUP BY, ORDER BY DESC."
    )
    q5_sql = """SELECT 
    c.CustomerID AS [Müşteri ID],
    c.FullName AS [Müşteri Adı],
    c.City AS [Şehir],
    SUM(o.TotalAmount) AS [Toplam Ciro]
FROM dbo.Customers AS c
INNER JOIN dbo.Orders AS o 
    ON c.CustomerID = o.CustomerID
GROUP BY c.CustomerID, c.FullName, c.City
ORDER BY [Toplam Ciro] DESC;"""
    add_code_block(doc, q5_sql)

    cur.execute("""SELECT c.CustomerID, c.FullName, c.City, SUM(o.TotalAmount)
                   FROM dbo.Customers c
                   INNER JOIN dbo.Orders o ON c.CustomerID = o.CustomerID
                   GROUP BY c.CustomerID, c.FullName, c.City
                   ORDER BY SUM(o.TotalAmount) DESC;""")
    q5_rows = cur.fetchall()
    t5 = doc.add_table(rows=len(q5_rows)+1, cols=4)
    format_result_table(t5, ["Müşteri ID", "Müşteri Adı", "Şehir", "Toplam Ciro (TL)"], q5_rows)
    p_desc5 = doc.add_paragraph("Analiz Açıklaması: Ahmet Yılmaz (6.950 TL) ve Fatma Şahin (3.800 TL) şirketimizin en yüksek ciro getiren ilk 2 müşterisidir. Pazarlama departmanı bu müşterilere özel sadakat kampanyaları düzenleyebilir.")
    p_desc5.paragraph_format.space_before = Pt(4)
    p_desc5.paragraph_format.space_after = Pt(12)

    # 3.6
    doc.add_heading("6. Zaman Analizi (Siparişten Beri Geçen Gün Sayısı)", level=2)
    doc.add_paragraph(
        "Soru: Bugünün tarihine göre, siparişlerin üzerinden kaç gün geçtiğini hesaplayan bir sorgu yazın.\n"
        "Kullanılan Teknikler: DATEDIFF(DAY, o.OrderDate, GETDATE()), GETDATE()."
    )
    q6_sql = """SELECT 
    o.OrderID AS [Sipariş No],
    c.FullName AS [Müşteri Adı],
    CONVERT(VARCHAR(10), o.OrderDate, 120) AS [Sipariş Tarihi],
    DATEDIFF(DAY, o.OrderDate, GETDATE()) AS [Geçen Gün Sayısı]
FROM dbo.Orders AS o
INNER JOIN dbo.Customers AS c 
    ON o.CustomerID = c.CustomerID
ORDER BY [Geçen Gün Sayısı] ASC;"""
    add_code_block(doc, q6_sql)

    cur.execute("""SELECT o.OrderID, c.FullName, CONVERT(VARCHAR(10), o.OrderDate, 120), DATEDIFF(DAY, o.OrderDate, GETDATE())
                   FROM dbo.Orders o
                   INNER JOIN dbo.Customers c ON o.CustomerID = c.CustomerID
                   ORDER BY DATEDIFF(DAY, o.OrderDate, GETDATE()) ASC;""")
    q6_rows = cur.fetchall()
    t6 = doc.add_table(rows=len(q6_rows)+1, cols=4)
    format_result_table(t6, ["Sipariş No", "Müşteri Adı", "Sipariş Tarihi", "Geçen Gün Sayısı"], q6_rows)
    p_desc6 = doc.add_paragraph("Analiz Açıklaması: Dinamik DATEDIFF fonksiyonu ile siparişlerin teslimat, iade hakları ve müşteri memnuniyeti anket zamanlamaları için gereken gün farkı hesaplanmıştır.")
    p_desc6.paragraph_format.space_before = Pt(4)
    p_desc6.paragraph_format.space_after = Pt(12)

    # ================= BÖLÜM 4: VIEW VE BACKUP =================
    h2_adv = doc.add_heading("BÖLÜM 4: İleri Seviye Veri Tabanı Nesneleri", level=1)
    for r in h2_adv.runs:
        r.font.color.rgb = RGBColor(15, 23, 42)

    doc.add_heading("1. Görünüm (View) Oluşturma: vw_SiparisOzet", level=2)
    doc.add_paragraph(
        "Yazılım geliştiricilerin ve raporlama uzmanlarının her seferinde 4 tabloyu birbirine bağlayan "
        "karmaşık JOIN ifadeleri yazmalarını engellemek, veri güvenliği sağlamak ve performansı artırmak "
        "amacıyla 'vw_SiparisOzet' sanal tablosu (View) oluşturulmuştur."
    )
    view_sql = """CREATE VIEW dbo.vw_SiparisOzet
AS
SELECT 
    c.FullName AS [Müşteri Adı],
    CONVERT(VARCHAR(19), o.OrderDate, 120) AS [Sipariş Tarihi],
    p.ProductName AS [Ürün Adı],
    od.Quantity AS [Adet]
FROM dbo.Customers AS c
INNER JOIN dbo.Orders AS o 
    ON c.CustomerID = o.CustomerID
INNER JOIN dbo.OrderDetails AS od 
    ON o.OrderID = od.OrderID
INNER JOIN dbo.Products AS p 
    ON od.ProductID = p.ProductID;
GO

-- Kullanımı:
SELECT * FROM dbo.vw_SiparisOzet;"""
    add_code_block(doc, view_sql)

    cur.execute("SELECT TOP 8 * FROM dbo.vw_SiparisOzet ORDER BY SiparisTarihi DESC;")
    v_rows = cur.fetchall()
    tv = doc.add_table(rows=len(v_rows)+1, cols=4)
    format_result_table(tv, ["Müşteri Adı", "Sipariş Tarihi", "Ürün Adı", "Adet"], v_rows)
    p_descv = doc.add_paragraph("Analiz Açıklaması: View sayesinde tek satırlık bir 'SELECT * FROM vw_SiparisOzet' komutu ile sipariş detaylarına doğrudan erişim sağlanmaktadır.")
    p_descv.paragraph_format.space_before = Pt(4)
    p_descv.paragraph_format.space_after = Pt(12)

    doc.add_heading("2. Veri Tabanı Yedekleme (Full Database Backup)", level=2)
    doc.add_paragraph(
        "Felaket kurtarma senaryolarına hazırlık ve veri güvenliğini garanti altına almak amacıyla "
        "NovaStoreDB veritabanının tam yedeğini 'C:\\Yedek\\' dizinine alan T-SQL komutu aşağıdadır:"
    )
    backup_sql = """-- NovaStoreDB Tam Yedeğini Alma (Full Backup)
BACKUP DATABASE NovaStoreDB
TO DISK = 'C:\\Yedek\\NovaStoreDB.bak'
WITH 
    FORMAT,
    MEDIANAME = 'NovaStoreDBBackup',
    NAME = 'Full Backup of NovaStoreDB';
GO"""
    add_code_block(doc, backup_sql)
    p_descbk = doc.add_paragraph("Yedekleme Açıklaması: WITH FORMAT parametresi mevcut yedekleme başlıklarını yeniden başlatır, MEDIANAME ve NAME parametreleri ise yedekleme arşivinin izlenebilirliğini ve yönetimini sağlar.")
    p_descbk.paragraph_format.space_after = Pt(12)

    # ================= EK BÖLÜM: MAC'TE SQL SERVER =================
    h2_mac = doc.add_heading("Teknik Not: Mac Ortamında Microsoft SQL Server Mimarisi", level=1)
    for r in h2_mac.runs:
        r.font.color.rgb = RGBColor(15, 23, 42)

    doc.add_paragraph(
        "Microsoft, SQL Server'ın doğrudan macOS (.dmg/.pkg) versiyonunu sunmadığı için Mac geliştirme ortamlarında "
        "endüstri standardı yöntem Docker konteyneri kullanmaktır. Bu projede Docker üzerinde çalışan Microsoft Azure SQL "
        "motoru kullanılmış; veritabanı port 1433 üzerinden ayağa kaldırılarak tüm T-SQL komutları test edilmiştir. "
        "Görsel yönetim aracı olarak Azure Data Studio veya DBeaver ile tam uyumlu çalışmaktadır."
    )

    doc_out = "/Users/Ertan/Desktop/ErtanYolcu_NovaStore_Proje/ErtanYolcu_NovaStore_Proje.docx"
    doc.save(doc_out)
    print(f"Document created successfully: {doc_out}")
    conn.close()

if __name__ == '__main__':
    main()
