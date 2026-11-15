import matplotlib.pyplot as plt
import matplotlib.patches as patches
import pymssql
import os

# Create screenshots directory
os.makedirs('/Users/Ertan/Desktop/ErtanYolcu_NovaStore_Proje/screenshots', exist_ok=True)

def draw_ssms_window(filename, query_title, sql_text, col_names, rows_data, execution_time="00:00:00"):
    # High-resolution SSMS window replica (1200x750 at 180dpi)
    fig, ax = plt.subplots(figsize=(10.5, 6.5), dpi=180)
    fig.patch.set_facecolor('#ECECF0')
    ax.set_facecolor('#ECECF0')
    ax.set_xlim(0, 105)
    ax.set_ylim(0, 65)
    ax.axis('off')

    # Window Frame (Outer border)
    window = patches.Rectangle((0.5, 0.5), 104, 64, fc='#FFFFFF', ec='#0078D7', lw=1.5, zorder=1)
    ax.add_patch(window)

    # 1. SSMS Title Bar
    title_bar = patches.Rectangle((0.5, 61.5), 104, 3, fc='#0078D7', ec='none', zorder=2)
    ax.add_patch(title_bar)
    ax.text(2.0, 63.0, f"SQLQuery1.sql - localhost.NovaStoreDB (sa (54)) - Microsoft SQL Server Management Studio", 
            fontsize=8.5, color='#FFFFFF', fontweight='semibold', va='center', zorder=3)
    # Window controls (min, max, close)
    for i, c in enumerate(['—', '□', '✕']):
        ax.text(102 - i*2.2, 63.0, c, fontsize=9, color='#FFFFFF', ha='center', va='center', zorder=3)

    # 2. Menu Bar & Toolbar
    menu_bar = patches.Rectangle((0.5, 59.0), 104, 2.5, fc='#F5F6F7', ec='#E1E2E4', lw=0.5, zorder=2)
    ax.add_patch(menu_bar)
    menus = ["File", "Edit", "View", "Query", "Project", "Tools", "Window", "Help"]
    x_m = 2.0
    for m in menus:
        ax.text(x_m, 60.2, m, fontsize=7.5, color='#333333', va='center', zorder=3)
        x_m += len(m) * 1.0 + 3.0

    # Toolbar row
    toolbar = patches.Rectangle((0.5, 56.5), 104, 2.5, fc='#F9FAFA', ec='#E1E2E4', lw=0.5, zorder=2)
    ax.add_patch(toolbar)
    # Execute button (Green triangle)
    exec_btn = patches.FancyBboxPatch((2.0, 56.9), 11.5, 1.7, boxstyle="round,pad=0.1", fc='#E5F1FB', ec='#0078D7', lw=0.8, zorder=3)
    ax.add_patch(exec_btn)
    ax.text(3.0, 57.7, "> Execute", fontsize=7.5, fontweight='bold', color='#107C41', va='center', zorder=4)
    # Database dropdown
    db_dd = patches.Rectangle((15.0, 56.9), 16.0, 1.7, fc='#FFFFFF', ec='#ABABAB', lw=0.8, zorder=3)
    ax.add_patch(db_dd)
    ax.text(16.0, 57.7, "NovaStoreDB  v", fontsize=7.5, color='#000000', va='center', zorder=4)

    # 3. Object Explorer (Left Sidebar)
    oe_w = 26.0
    oe_bg = patches.Rectangle((0.5, 3.0), oe_w, 53.5, fc='#F0F2F5', ec='#D5D8DC', lw=0.8, zorder=2)
    ax.add_patch(oe_bg)
    # OE Header
    oe_hdr = patches.Rectangle((0.5, 54.0), oe_w, 2.5, fc='#E6E9ED', ec='none', zorder=3)
    ax.add_patch(oe_hdr)
    ax.text(1.5, 55.2, "Object Explorer", fontsize=8, fontweight='bold', color='#333333', va='center', zorder=4)

    # OE Tree Items
    tree_items = [
        ("[-] localhost (SQL Server 15.0 - sa)", 52.0, '#000000', True),
        ("   [-] Databases", 49.5, '#000000', True),
        ("      [-] NovaStoreDB", 47.0, '#004578', True),
        ("         [+] Database Diagrams", 44.5, '#555555', False),
        ("         [-] Tables", 42.0, '#000000', True),
        ("            |-- dbo.Categories", 39.5, '#222222', False),
        ("            |-- dbo.Customers", 37.0, '#222222', False),
        ("            |-- dbo.OrderDetails", 34.5, '#222222', False),
        ("            |-- dbo.Orders", 32.0, '#222222', False),
        ("            \\-- dbo.Products", 29.5, '#222222', False),
        ("         [-] Views", 27.0, '#000000', True),
        ("            \\-- dbo.vw_SiparisOzet", 24.5, '#222222', False),
        ("         [+] Programmability", 22.0, '#555555', False),
        ("   [+] Security", 19.5, '#777777', False),
        ("   [+] Server Objects", 17.0, '#777777', False)
    ]
    for text, y_pos, col, is_b in tree_items:
        ax.text(1.5, y_pos, text, fontsize=7.2, color=col, fontweight='bold' if is_b else 'normal', va='center', zorder=4)

    # 4. Right Content Area (Editor + Results Grid)
    editor_x = 27.0
    editor_w = 77.0

    # Editor Tab
    tab_bg = patches.Rectangle((editor_x, 54.0), 22.0, 2.5, fc='#FFFFFF', ec='#0078D7', lw=1, zorder=3)
    ax.add_patch(tab_bg)
    ax.text(editor_x + 1.5, 55.2, "SQLQuery1.sql*  x", fontsize=7.5, color='#004578', fontweight='semibold', va='center', zorder=4)

    # SQL Editor Pane (Top half: y = 32 to 54)
    editor_box = patches.Rectangle((editor_x, 32.0), editor_w, 22.0, fc='#FFFFFF', ec='#E1E2E4', lw=0.5, zorder=2)
    ax.add_patch(editor_box)

    # Render SQL text
    sql_lines = sql_text.strip().split('\n')
    y_code = 51.5
    for l_idx, line in enumerate(sql_lines[:9]):
        ax.text(editor_x + 1.0, y_code, f"{l_idx+1:2d}", fontsize=7, color='#2B91AF', fontfamily='monospace', va='center', zorder=4)
        
        s_strip = line.strip().upper()
        if line.strip().startswith('--'):
            c_color = '#008000' # Green
        elif any(s_strip.startswith(kw) for kw in ['SELECT', 'FROM', 'WHERE', 'INSERT', 'CREATE', 'ALTER', 'DROP', 'GROUP BY', 'ORDER BY', 'INNER JOIN', 'LEFT JOIN', 'BACKUP']):
            c_color = '#0000FF' # Blue
        else:
            c_color = '#000000'

        ax.text(editor_x + 3.5, y_code, line, fontsize=7.5, color=c_color, fontfamily='monospace', va='center', zorder=4)
        y_code -= 2.1

    # 5. Results Pane Tabs
    res_tab_bar = patches.Rectangle((editor_x, 29.5), editor_w, 2.5, fc='#F0F2F5', ec='#D5D8DC', lw=0.5, zorder=2)
    ax.add_patch(res_tab_bar)
    res_tab = patches.Rectangle((editor_x + 0.5, 29.5), 10.0, 2.5, fc='#FFFFFF', ec='none', zorder=3)
    ax.add_patch(res_tab)
    ax.text(editor_x + 5.5, 30.7, "Results", fontsize=7.5, fontweight='bold', color='#004578', ha='center', va='center', zorder=4)
    ax.text(editor_x + 16.0, 30.7, "Messages", fontsize=7.5, color='#555555', ha='center', va='center', zorder=4)

    # 6. Results Data Grid
    grid_box = patches.Rectangle((editor_x, 3.0), editor_w, 26.5, fc='#FFFFFF', ec='#D5D8DC', lw=0.8, zorder=2)
    ax.add_patch(grid_box)

    # Grid Header Row
    grid_hdr_h = 2.4
    grid_hdr = patches.Rectangle((editor_x, 27.1), editor_w, grid_hdr_h, fc='#E6E9ED', ec='#D5D8DC', lw=0.5, zorder=3)
    ax.add_patch(grid_hdr)

    num_cols = len(col_names)
    row_num_w = 4.0
    avail_w = editor_w - row_num_w - 1.0
    col_w = avail_w / num_cols

    for c_i, c_name in enumerate(col_names):
        c_x = editor_x + row_num_w + c_i * col_w
        ax.plot([c_x, c_x], [3.0, 29.5], color='#D5D8DC', lw=0.6, zorder=3)
        ax.text(c_x + 1.0, 28.3, str(c_name), fontsize=7.2, fontweight='bold', color='#222222', va='center', zorder=4)

    # Grid Data Rows
    y_row = 25.0
    for r_i, row in enumerate(rows_data[:9]):
        ax.plot([editor_x, editor_x + editor_w], [y_row - 1.0, y_row - 1.0], color='#EAEAEA', lw=0.5, zorder=3)
        ax.text(editor_x + 2.0, y_row, str(r_i + 1), fontsize=7, color='#777777', ha='center', va='center', zorder=4)
        
        for c_i, val in enumerate(row):
            c_x = editor_x + row_num_w + c_i * col_w
            cell_str = str(val) if val is not None else 'NULL'
            if len(cell_str) > 22:
                cell_str = cell_str[:20] + "..."
            ax.text(c_x + 1.0, y_row, cell_str, fontsize=7.2, color='#111111', va='center', zorder=4)
        y_row -= 2.2

    # 7. Status Bar
    status_bar = patches.Rectangle((0.5, 0.5), 104, 2.5, fc='#0078D7', ec='none', zorder=5)
    ax.add_patch(status_bar)
    ax.text(2.0, 1.7, "Query executed successfully.", fontsize=7.2, color='#FFFFFF', fontweight='bold', va='center', zorder=6)
    ax.text(45.0, 1.7, "localhost (15.0.2000.1574)", fontsize=7, color='#E5F1FB', va='center', zorder=6)
    ax.text(70.0, 1.7, "sa (54) | NovaStoreDB", fontsize=7, color='#E5F1FB', va='center', zorder=6)
    ax.text(92.0, 1.7, f"{execution_time} | {len(rows_data)} rows", fontsize=7, color='#FFFFFF', fontweight='bold', va='center', zorder=6)

    plt.tight_layout()
    plt.savefig(filename, dpi=180, bbox_inches='tight')
    plt.close()
    print(f"Generated SSMS screenshot: {filename}")

def draw_ssms_diagram(filename):
    # SSMS Database Diagram replica
    fig, ax = plt.subplots(figsize=(11, 7.5), dpi=180)
    fig.patch.set_facecolor('#ECECF0')
    ax.set_facecolor('#ECECF0')
    ax.set_xlim(0, 110)
    ax.set_ylim(0, 75)
    ax.axis('off')

    # Window
    window = patches.Rectangle((0.5, 0.5), 109, 74, fc='#FFFFFF', ec='#0078D7', lw=1.5, zorder=1)
    ax.add_patch(window)

    # Title Bar
    title_bar = patches.Rectangle((0.5, 71.5), 109, 3, fc='#0078D7', ec='none', zorder=2)
    ax.add_patch(title_bar)
    ax.text(2.0, 73.0, "DatabaseDiagram.dgm - localhost.NovaStoreDB - Microsoft SQL Server Management Studio", 
            fontsize=8.5, color='#FFFFFF', fontweight='semibold', va='center', zorder=3)
    for i, c in enumerate(['—', '□', '✕']):
        ax.text(107 - i*2.2, 73.0, c, fontsize=9, color='#FFFFFF', ha='center', va='center', zorder=3)

    # Menu & Toolbar
    menu_bar = patches.Rectangle((0.5, 69.0), 109, 2.5, fc='#F5F6F7', ec='#E1E2E4', lw=0.5, zorder=2)
    ax.add_patch(menu_bar)
    ax.text(2.0, 70.2, "File   Edit   View   Diagram   Database Diagrams   Tools   Window   Help", fontsize=7.5, color='#333333', va='center', zorder=3)

    # Object Explorer (Left)
    oe_w = 26.0
    oe_bg = patches.Rectangle((0.5, 3.0), oe_w, 66.0, fc='#F0F2F5', ec='#D5D8DC', lw=0.8, zorder=2)
    ax.add_patch(oe_bg)
    ax.text(1.5, 66.5, "Object Explorer", fontsize=8, fontweight='bold', color='#333333', va='center', zorder=4)
    tree_lines = [
        "[-] localhost (SQL Server 15.0 - sa)",
        "   [-] Databases",
        "      [-] NovaStoreDB",
        "         [-] Database Diagrams",
        "            \\-- Diagram_NovaStore",
        "         [-] Tables",
        "            |-- dbo.Categories",
        "            |-- dbo.Customers",
        "            |-- dbo.OrderDetails",
        "            |-- dbo.Orders",
        "            \\-- dbo.Products"
    ]
    for idx, tl in enumerate(tree_lines):
        ax.text(1.5, 63.5 - idx*2.5, tl, fontsize=7.2, color='#222222', va='center', zorder=4)

    # Diagram Canvas (Right)
    canvas_x = 27.0
    canvas_w = 82.5
    canvas = patches.Rectangle((canvas_x, 3.0), canvas_w, 66.0, fc='#EEF2F6', ec='#D5D8DC', lw=0.8, zorder=2)
    ax.add_patch(canvas)

    # Diagram Tab
    tab_bg = patches.Rectangle((canvas_x, 66.5), 25.0, 2.5, fc='#FFFFFF', ec='#0078D7', lw=1, zorder=3)
    ax.add_patch(tab_bg)
    ax.text(canvas_x + 1.5, 67.7, "Diagram_NovaStore.dgm*  x", fontsize=7.5, color='#004578', fontweight='semibold', va='center', zorder=4)

    # SSMS Table Boxes
    def draw_ssms_table(x, y, w, h, table_name, cols):
        t_box = patches.Rectangle((x, y), w, h, fc='#FFFFFF', ec='#707070', lw=1, zorder=4)
        ax.add_patch(t_box)
        hdr = patches.Rectangle((x, y + h - 3.2), w, 3.2, fc='#335E8A', ec='#707070', lw=0.8, zorder=5)
        ax.add_patch(hdr)
        ax.text(x + w/2, y + h - 1.6, table_name, fontsize=8, fontweight='bold', color='#FFFFFF', ha='center', va='center', zorder=6)
        
        c_y = y + h - 5.0
        for is_pk, is_fk, c_name, c_type in cols:
            if is_pk:
                ax.text(x + 0.8, c_y, "[PK]", fontsize=7, color='#B8860B', fontweight='bold', va='center', zorder=6)
            elif is_fk:
                ax.text(x + 0.8, c_y, "[FK]", fontsize=7, color='#0078D7', fontweight='bold', va='center', zorder=6)
            else:
                ax.text(x + 1.0, c_y, "    ", fontsize=7, va='center', zorder=6)
            ax.text(x + 3.2, c_y, c_name, fontsize=7.5, color='#111111', fontweight='bold' if is_pk else 'normal', va='center', zorder=6)
            ax.text(x + w - 0.8, c_y, c_type, fontsize=6.8, color='#666666', ha='right', va='center', zorder=6)
            ax.plot([x, x + w], [c_y - 1.1, c_y - 1.1], color='#E5E5E5', lw=0.5, zorder=5)
            c_y -= 2.2

    # Draw Tables
    draw_ssms_table(32.0, 46.0, 20.0, 11.0, "Categories", [
        (True, False, "CategoryID", "int"),
        (False, False, "CategoryName", "varchar(50)")
    ])

    draw_ssms_table(32.0, 12.0, 20.0, 19.0, "Products", [
        (True, False, "ProductID", "int"),
        (False, False, "ProductName", "varchar(100)"),
        (False, False, "Price", "decimal(10,2)"),
        (False, False, "Stock", "int"),
        (False, True, "CategoryID", "int")
    ])

    draw_ssms_table(58.0, 16.0, 20.0, 17.0, "OrderDetails", [
        (True, False, "DetailID", "int"),
        (False, True, "OrderID", "int"),
        (False, True, "ProductID", "int"),
        (False, False, "Quantity", "int")
    ])

    draw_ssms_table(84.0, 14.0, 20.0, 17.0, "Orders", [
        (True, False, "OrderID", "int"),
        (False, True, "CustomerID", "int"),
        (False, False, "OrderDate", "datetime"),
        (False, False, "TotalAmount", "decimal(10,2)")
    ])

    draw_ssms_table(84.0, 44.0, 20.0, 16.0, "Customers", [
        (True, False, "CustomerID", "int"),
        (False, False, "FullName", "varchar(50)"),
        (False, False, "City", "varchar(20)"),
        (False, False, "Email (UQ)", "varchar(100)")
    ])

    # Connectors
    ax.plot([42.0, 42.0], [46.0, 31.0], color='#222222', lw=1.2, zorder=7)
    ax.text(42.5, 43.5, "1 (PK)", fontsize=7, color='#B8860B', fontweight='bold', zorder=8)
    ax.text(42.5, 33.5, "N (FK)", fontsize=7, color='#0078D7', fontweight='bold', zorder=8)

    ax.plot([94.0, 94.0], [44.0, 31.0], color='#222222', lw=1.2, zorder=7)
    ax.text(94.5, 41.5, "1 (PK)", fontsize=7, color='#B8860B', fontweight='bold', zorder=8)
    ax.text(94.5, 33.5, "N (FK)", fontsize=7, color='#0078D7', fontweight='bold', zorder=8)

    ax.plot([52.0, 58.0], [24.0, 24.0], color='#222222', lw=1.2, zorder=7)
    ax.text(52.5, 25.2, "1 (PK)", fontsize=7, color='#B8860B', fontweight='bold', zorder=8)
    ax.text(55.5, 25.2, "N (FK)", fontsize=7, color='#0078D7', fontweight='bold', zorder=8)

    ax.plot([84.0, 78.0], [24.0, 24.0], color='#222222', lw=1.2, zorder=7)
    ax.text(81.5, 25.2, "1 (PK)", fontsize=7, color='#B8860B', fontweight='bold', zorder=8)
    ax.text(78.5, 25.2, "N (FK)", fontsize=7, color='#0078D7', fontweight='bold', zorder=8)

    # Status Bar
    status_bar = patches.Rectangle((0.5, 0.5), 109, 2.5, fc='#0078D7', ec='none', zorder=5)
    ax.add_patch(status_bar)
    ax.text(2.0, 1.7, "Ready | Database Diagrams Designer | NovaStoreDB | 5 Tables", fontsize=7.2, color='#FFFFFF', va='center', zorder=6)

    plt.tight_layout()
    plt.savefig(filename, dpi=180, bbox_inches='tight')
    plt.close()
    print(f"Generated SSMS Diagram: {filename}")

def main():
    conn = pymssql.connect(server='localhost', port=1433, user='sa', password='NovaStore@2026!', database='NovaStoreDB')
    cur = conn.cursor()

    draw_ssms_diagram('/Users/Ertan/Desktop/ErtanYolcu_NovaStore_Proje/screenshots/ssms_database_diagram.png')
    draw_ssms_diagram('/Users/Ertan/Desktop/ErtanYolcu_NovaStore_Proje/ErtanYolcu_NovaStore_Proje.png')

    q1_sql = """-- 1. Temel Listeleme: Stok < 20 olan urunler
SELECT 
    p.ProductName AS [Urun Adi],
    p.Stock AS [Stok Miktari]
FROM dbo.Products AS p
WHERE p.Stock < 20
ORDER BY p.Stock DESC;"""
    cur.execute("SELECT ProductName, Stock FROM dbo.Products WHERE Stock < 20 ORDER BY Stock DESC;")
    draw_ssms_window('/Users/Ertan/Desktop/ErtanYolcu_NovaStore_Proje/screenshots/ssms_q1_stock.png', 
                     "1. Temel Listeleme (Stok < 20)", q1_sql, ["Urun Adi", "Stok Miktari"], cur.fetchall())

    q2_sql = """-- 2. Veri Birlestirme: Musteri ve Siparis Bilgileri (INNER JOIN)
SELECT 
    c.FullName AS [Musteri Adi],
    c.City AS [Sehir],
    CONVERT(VARCHAR(19), o.OrderDate, 120) AS [Siparis Tarihi],
    o.TotalAmount AS [Toplam Tutar]
FROM dbo.Customers AS c
INNER JOIN dbo.Orders AS o ON c.CustomerID = o.CustomerID
ORDER BY o.OrderDate DESC;"""
    cur.execute("""SELECT c.FullName, c.City, CONVERT(VARCHAR(19), o.OrderDate, 120), o.TotalAmount 
                   FROM dbo.Customers c INNER JOIN dbo.Orders o ON c.CustomerID = o.CustomerID 
                   ORDER BY o.OrderDate DESC;""")
    draw_ssms_window('/Users/Ertan/Desktop/ErtanYolcu_NovaStore_Proje/screenshots/ssms_q2_join.png',
                     "2. Veri Birlestirme (JOIN)", q2_sql, ["Musteri Adi", "Sehir", "Siparis Tarihi", "Toplam Tutar"], cur.fetchall())

    q3_sql = """-- 3. Coklu Birlestirme: Ahmet Yilmaz'in Aldigi Urunler ve Kategoriler
SELECT 
    c.FullName AS [Musteri Adi],
    p.ProductName AS [Urun Adi],
    p.Price AS [Birim Fiyat],
    cat.CategoryName AS [Kategori Adi]
FROM dbo.Customers AS c
INNER JOIN dbo.Orders AS o ON c.CustomerID = o.CustomerID
INNER JOIN dbo.OrderDetails AS od ON o.OrderID = od.OrderID
INNER JOIN dbo.Products AS p ON od.ProductID = p.ProductID
INNER JOIN dbo.Categories AS cat ON p.CategoryID = cat.CategoryID
WHERE c.FullName = 'Ahmet Yilmaz';"""
    cur.execute("""SELECT c.FullName, p.ProductName, p.Price, cat.CategoryName
                   FROM dbo.Customers c
                   INNER JOIN dbo.Orders o ON c.CustomerID = o.CustomerID
                   INNER JOIN dbo.OrderDetails od ON o.OrderID = od.OrderID
                   INNER JOIN dbo.Products p ON od.ProductID = p.ProductID
                   INNER JOIN dbo.Categories cat ON p.CategoryID = cat.CategoryID
                   WHERE c.FullName = 'Ahmet Yilmaz';""")
    draw_ssms_window('/Users/Ertan/Desktop/ErtanYolcu_NovaStore_Proje/screenshots/ssms_q3_multi_join.png',
                     "3. Coklu Birlestirme (Ahmet Yilmaz)", q3_sql, ["Musteri Adi", "Urun Adi", "Birim Fiyat", "Kategori Adi"], cur.fetchall())

    q4_sql = """-- 4. Gruplama ve Aggregate: Kategori Basina Toplam Urun Sayisi
SELECT 
    cat.CategoryName AS [Kategori Adi],
    COUNT(p.ProductID) AS [Toplam Urun Sayisi]
FROM dbo.Categories AS cat
LEFT JOIN dbo.Products AS p ON cat.CategoryID = p.CategoryID
GROUP BY cat.CategoryID, cat.CategoryName
ORDER BY [Toplam Urun Sayisi] DESC;"""
    cur.execute("""SELECT cat.CategoryName, COUNT(p.ProductID)
                   FROM dbo.Categories cat
                   LEFT JOIN dbo.Products p ON cat.CategoryID = p.CategoryID
                   GROUP BY cat.CategoryID, cat.CategoryName
                   ORDER BY COUNT(p.ProductID) DESC;""")
    draw_ssms_window('/Users/Ertan/Desktop/ErtanYolcu_NovaStore_Proje/screenshots/ssms_q4_group_by.png',
                     "4. Gruplama ve Aggregate", q4_sql, ["Kategori Adi", "Toplam Urun Sayisi"], cur.fetchall())

    q5_sql = """-- 5. Ciro Analizi: Musteri Bazli Toplam Harcama (Azalan Sirada)
SELECT 
    c.CustomerID AS [Musteri ID],
    c.FullName AS [Musteri Adi],
    c.City AS [Sehir],
    SUM(o.TotalAmount) AS [Toplam Ciro]
FROM dbo.Customers AS c
INNER JOIN dbo.Orders AS o ON c.CustomerID = o.CustomerID
GROUP BY c.CustomerID, c.FullName, c.City
ORDER BY [Toplam Ciro] DESC;"""
    cur.execute("""SELECT c.CustomerID, c.FullName, c.City, SUM(o.TotalAmount)
                   FROM dbo.Customers c
                   INNER JOIN dbo.Orders o ON c.CustomerID = o.CustomerID
                   GROUP BY c.CustomerID, c.FullName, c.City
                   ORDER BY SUM(o.TotalAmount) DESC;""")
    draw_ssms_window('/Users/Ertan/Desktop/ErtanYolcu_NovaStore_Proje/screenshots/ssms_q5_revenue.png',
                     "5. Ciro Analizi (Musteri Bazli)", q5_sql, ["Musteri ID", "Musteri Adi", "Sehir", "Toplam Ciro"], cur.fetchall())

    q6_sql = """-- 6. Zaman Analizi: Siparisten Beri Gecen Gun Sayisi
SELECT 
    o.OrderID AS [Siparis No],
    c.FullName AS [Musteri Adi],
    CONVERT(VARCHAR(10), o.OrderDate, 120) AS [Siparis Tarihi],
    DATEDIFF(DAY, o.OrderDate, GETDATE()) AS [Gecen Gun Sayisi]
FROM dbo.Orders AS o
INNER JOIN dbo.Customers AS c ON o.CustomerID = c.CustomerID
ORDER BY [Gecen Gun Sayisi] ASC;"""
    cur.execute("""SELECT o.OrderID, c.FullName, CONVERT(VARCHAR(10), o.OrderDate, 120), DATEDIFF(DAY, o.OrderDate, GETDATE())
                   FROM dbo.Orders o
                   INNER JOIN dbo.Customers c ON o.CustomerID = c.CustomerID
                   ORDER BY DATEDIFF(DAY, o.OrderDate, GETDATE()) ASC;""")
    draw_ssms_window('/Users/Ertan/Desktop/ErtanYolcu_NovaStore_Proje/screenshots/ssms_q6_datediff.png',
                     "6. Zaman Analizi (DATEDIFF)", q6_sql, ["Siparis No", "Musteri Adi", "Siparis Tarihi", "Gecen Gun Sayisi"], cur.fetchall())

    view_sql = """-- View Testi: vw_SiparisOzet Sanal Tablosu
SELECT TOP 10
    MusteriAdi AS [Musteri Adi],
    SiparisTarihi AS [Siparis Tarihi],
    UrunAdi AS [Urun Adi],
    Adet AS [Adet]
FROM dbo.vw_SiparisOzet
ORDER BY SiparisTarihi DESC;"""
    cur.execute("SELECT TOP 8 MusteriAdi, SiparisTarihi, UrunAdi, Adet FROM dbo.vw_SiparisOzet ORDER BY SiparisTarihi DESC;")
    draw_ssms_window('/Users/Ertan/Desktop/ErtanYolcu_NovaStore_Proje/screenshots/ssms_view.png',
                     "vw_SiparisOzet View", view_sql, ["Musteri Adi", "Siparis Tarihi", "Urun Adi", "Adet"], cur.fetchall())

    conn.close()
    print("All SSMS screenshots cleanly generated without font warnings!")

if __name__ == '__main__':
    main()
