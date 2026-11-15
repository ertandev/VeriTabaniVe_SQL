import matplotlib.pyplot as plt
import matplotlib.patches as patches

def draw_er_diagram():
    fig, ax = plt.subplots(figsize=(15, 9), dpi=300)
    fig.patch.set_facecolor('#F1F5F9')
    ax.set_facecolor('#F1F5F9')

    # Grid limits
    ax.set_xlim(0, 15)
    ax.set_ylim(0, 9)
    ax.axis('off')

    # Title & Subtitle
    plt.text(7.5, 8.5, "NovaStoreDB - İlişkisel Veri Tabanı Şeması (ER Diyagramı)", 
             fontsize=18, fontweight='bold', ha='center', va='center', color='#0F172A', fontfamily='sans-serif')
    plt.text(7.5, 8.15, "Tasarım: Ertan Yolcu | Microsoft SQL Server (T-SQL)", 
             fontsize=11, fontstyle='italic', ha='center', va='center', color='#475569', fontfamily='sans-serif')

    # Table specifications: (x, y, width, height, title, columns)
    # y is bottom-left
    tables = {
        'Categories': {
            'x': 1.2, 'y': 5.2, 'w': 3.4, 'h': 2.0,
            'title': 'Categories', 'header_bg': '#1E293B',
            'cols': [
                ('PK', 'CategoryID', 'INT (Identity)'),
                ('  ', 'CategoryName', 'VARCHAR(50)')
            ]
        },
        'Products': {
            'x': 1.2, 'y': 1.2, 'w': 3.4, 'h': 2.8,
            'title': 'Products', 'header_bg': '#0284C7',
            'cols': [
                ('PK', 'ProductID', 'INT (Identity)'),
                ('  ', 'ProductName', 'VARCHAR(100)'),
                ('  ', 'Price', 'DECIMAL(10,2)'),
                ('  ', 'Stock', 'INT (DEFAULT 0)'),
                ('FK', 'CategoryID', 'INT')
            ]
        },
        'Customers': {
            'x': 10.4, 'y': 5.2, 'w': 3.4, 'h': 2.4,
            'title': 'Customers', 'header_bg': '#0D9488',
            'cols': [
                ('PK', 'CustomerID', 'INT (Identity)'),
                ('  ', 'FullName', 'VARCHAR(50)'),
                ('  ', 'City', 'VARCHAR(20)'),
                ('UQ', 'Email', 'VARCHAR(100)')
            ]
        },
        'Orders': {
            'x': 10.4, 'y': 1.2, 'w': 3.4, 'h': 2.6,
            'title': 'Orders', 'header_bg': '#D97706',
            'cols': [
                ('PK', 'OrderID', 'INT (Identity)'),
                ('FK', 'CustomerID', 'INT'),
                ('  ', 'OrderDate', 'DATETIME (DF: GETDATE)'),
                ('  ', 'TotalAmount', 'DECIMAL(10,2)')
            ]
        },
        'OrderDetails': {
            'x': 5.8, 'y': 1.4, 'w': 3.4, 'h': 2.4,
            'title': 'OrderDetails (Ara Tablo)', 'header_bg': '#4F46E5',
            'cols': [
                ('PK', 'DetailID', 'INT (Identity)'),
                ('FK', 'OrderID', 'INT'),
                ('FK', 'ProductID', 'INT'),
                ('  ', 'Quantity', 'INT')
            ]
        }
    }

    # Render each table
    for name, t in tables.items():
        x, y, w, h = t['x'], t['y'], t['w'], t['h']
        
        # Outer Card shadow
        shadow = patches.FancyBboxPatch((x + 0.05, y - 0.05), w, h,
                                       boxstyle="round,pad=0.04,rounding_size=0.1",
                                       fc='#CBD5E1', ec='none', zorder=1)
        ax.add_patch(shadow)

        # Card body
        card = patches.FancyBboxPatch((x, y), w, h,
                                      boxstyle="round,pad=0.04,rounding_size=0.1",
                                      fc='#FFFFFF', ec='#94A3B8', lw=1.2, zorder=2)
        ax.add_patch(card)

        # Header banner
        header_h = 0.55
        header = patches.FancyBboxPatch((x, y + h - header_h), w, header_h,
                                        boxstyle="round,pad=0.04,rounding_size=0.1",
                                        fc=t['header_bg'], ec='none', zorder=3)
        ax.add_patch(header)

        # Header title
        ax.text(x + w/2, y + h - header_h/2, t['title'],
                fontsize=11, fontweight='bold', color='#FFFFFF', ha='center', va='center', zorder=4)

        # Columns
        col_y = y + h - header_h - 0.28
        for key_type, col_name, data_type in t['cols']:
            # Key badge
            if key_type == 'PK':
                ax.text(x + 0.2, col_y, 'PK', fontsize=8, fontweight='bold', color='#DC2626', ha='left', va='center', zorder=4)
            elif key_type == 'FK':
                ax.text(x + 0.2, col_y, 'FK', fontsize=8, fontweight='bold', color='#2563EB', ha='left', va='center', zorder=4)
            elif key_type == 'UQ':
                ax.text(x + 0.2, col_y, 'UQ', fontsize=8, fontweight='bold', color='#059669', ha='left', va='center', zorder=4)
            else:
                ax.text(x + 0.2, col_y, '•', fontsize=8, color='#94A3B8', ha='left', va='center', zorder=4)

            # Column Name
            ax.text(x + 0.55, col_y, col_name, fontsize=8.5, fontweight='semibold', color='#1E293B', ha='left', va='center', zorder=4)
            # Data Type
            ax.text(x + w - 0.15, col_y, data_type, fontsize=7.5, color='#64748B', ha='right', va='center', zorder=4)
            
            # Divider line
            ax.plot([x + 0.15, x + w - 0.15], [col_y - 0.14, col_y - 0.14], color='#F1F5F9', lw=0.8, zorder=4)
            col_y -= 0.38

    # Relationships (Arrows & Lines)
    # 1. Categories (1) -> Products (N)
    ax.annotate("", xy=(2.9, 4.0), xytext=(2.9, 5.2),
                arrowprops=dict(arrowstyle="-|>", color='#0284C7', lw=2, mutation_scale=15), zorder=5)
    ax.text(3.05, 4.6, "1 : N\n(CategoryID)", fontsize=8, fontweight='bold', color='#0284C7', va='center')

    # 2. Customers (1) -> Orders (N)
    ax.annotate("", xy=(12.1, 3.8), xytext=(12.1, 5.2),
                arrowprops=dict(arrowstyle="-|>", color='#D97706', lw=2, mutation_scale=15), zorder=5)
    ax.text(12.25, 4.5, "1 : N\n(CustomerID)", fontsize=8, fontweight='bold', color='#D97706', va='center')

    # 3. Products (1) -> OrderDetails (N)
    ax.annotate("", xy=(5.8, 2.5), xytext=(4.6, 2.5),
                arrowprops=dict(arrowstyle="-|>", color='#4F46E5', lw=2, mutation_scale=15), zorder=5)
    ax.text(5.2, 2.75, "1 : N (ProductID)", fontsize=8, fontweight='bold', color='#4F46E5', ha='center')

    # 4. Orders (1) -> OrderDetails (N)
    ax.annotate("", xy=(9.2, 2.5), xytext=(10.4, 2.5),
                arrowprops=dict(arrowstyle="-|>", color='#4F46E5', lw=2, mutation_scale=15), zorder=5)
    ax.text(9.8, 2.75, "1 : N (OrderID)", fontsize=8, fontweight='bold', color='#4F46E5', ha='center')

    # Legend / Explanatory Box
    leg_box = patches.FancyBboxPatch((4.5, 5.3), 5.4, 2.0,
                                     boxstyle="round,pad=0.03,rounding_size=0.1",
                                     fc='#FFFFFF', ec='#CBD5E1', lw=1, zorder=2)
    ax.add_patch(leg_box)
    ax.text(7.2, 7.05, "İlişkisel Bütünlük ve Açıklamalar", fontsize=9.5, fontweight='bold', color='#1E293B', ha='center')
    ax.text(4.8, 6.65, "• PK (Primary Key): Benzersiz otomatik artan birincil anahtar", fontsize=8, color='#334155')
    ax.text(4.8, 6.30, "• FK (Foreign Key): İlişkisel tablolar arası yabancı anahtar bağı", fontsize=8, color='#334155')
    ax.text(4.8, 5.95, "• UQ (Unique): Tekil / benzersiz müşteri e-posta kısıtlayıcısı", fontsize=8, color='#334155')
    ax.text(4.8, 5.60, "• OrderDetails: Orders ve Products arasındaki M:N ilişkiyi çözen ara tablo", fontsize=8, color='#4338CA', fontweight='semibold')

    plt.tight_layout()
    plt.savefig('/Users/Ertan/Desktop/ErtanYolcu_NovaStore_Proje/ErtanYolcu_NovaStore_Proje.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("ER Diagram generated successfully: ErtanYolcu_NovaStore_Proje.png")

if __name__ == '__main__':
    draw_er_diagram()
