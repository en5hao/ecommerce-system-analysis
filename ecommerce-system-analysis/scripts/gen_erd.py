import graphviz

g = graphviz.Digraph('erd', format='png')
g.attr(rankdir='LR', fontname='Helvetica', bgcolor='white', nodesep='0.5', ranksep='0.8')
g.attr('node', fontname='Helvetica', fontsize='10', shape='none')
g.attr('edge', fontname='Helvetica', fontsize='9', arrowhead='crow', arrowtail='none')

def table(name, title, rows):
    label = '<<table border="1" cellborder="0" cellspacing="0" cellpadding="4">'
    label += f'<tr><td bgcolor="#4472C4" align="center"><font color="white"><b>{title}</b></font></td></tr>'
    for r in rows:
        label += f'<tr><td align="left">{r}</td></tr>'
    label += '</table>>'
    g.node(name, label)

table('users', 'Users', [
    '<b>id</b> PK',
    'email',
    'phone',
    'full_name',
    'created_at',
])

table('categories', 'Categories', [
    '<b>id</b> PK',
    'name',
    'parent_id FK → Categories',
])

table('products', 'Products', [
    '<b>id</b> PK',
    'category_id FK → Categories',
    'name',
    'sku',
    'price',
    'description',
])

table('inventory', 'Inventory', [
    '<b>id</b> PK',
    'product_id FK → Products',
    'quantity_available',
    'quantity_reserved',
    'warehouse_location',
])

table('orders', 'Orders', [
    '<b>id</b> PK',
    'user_id FK → Users',
    'status',
    'total_amount',
    'created_at',
    'updated_at',
])

table('order_items', 'OrderItems', [
    '<b>id</b> PK',
    'order_id FK → Orders',
    'product_id FK → Products',
    'quantity',
    'price_at_purchase',
])

table('payments', 'Payments', [
    '<b>id</b> PK',
    'order_id FK → Orders',
    'amount',
    'status',
    'provider_transaction_id',
    'paid_at',
])

table('returns', 'Returns', [
    '<b>id</b> PK',
    'order_item_id FK → OrderItems',
    'reason',
    'status',
    'requested_at',
    'resolved_at',
])

g.edge('categories', 'categories', label='parent (self)')
g.edge('categories', 'products', label='1..N')
g.edge('products', 'inventory', label='1..1')
g.edge('users', 'orders', label='1..N')
g.edge('orders', 'order_items', label='1..N')
g.edge('products', 'order_items', label='1..N')
g.edge('orders', 'payments', label='1..N')
g.edge('order_items', 'returns', label='0..1')

g.render('/home/claude/ecommerce/docs/erd', cleanup=True)
print('done')
