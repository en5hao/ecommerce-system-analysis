import graphviz

g = graphviz.Digraph('state_diagram', format='png')
g.attr(rankdir='LR', fontname='Helvetica', bgcolor='white', nodesep='0.5', ranksep='0.7')
g.attr('node', fontname='Helvetica', fontsize='11', shape='box', style='rounded,filled')
g.attr('edge', fontname='Helvetica', fontsize='9')

g.node('created', 'Создан', fillcolor='#DAE8FC')
g.node('pending_payment', 'Ожидает\nоплаты', fillcolor='#DAE8FC')
g.node('paid', 'Оплачен', fillcolor='#D5E8D4')
g.node('packing', 'Собирается', fillcolor='#D5E8D4')
g.node('shipped', 'Отгружен', fillcolor='#D5E8D4')
g.node('delivered', 'Доставлен', fillcolor='#D5E8D4', peripheries='2')

g.node('cancelled', 'Отменён', fillcolor='#F8CECC')
g.node('return_requested', 'Возврат\nоформлен', fillcolor='#FFE6CC')
g.node('return_received', 'Возврат\nполучен складом', fillcolor='#FFE6CC')
g.node('return_approved', 'Возврат\nодобрен\n(деньги возвращены)', fillcolor='#F8CECC', peripheries='2')
g.node('return_rejected', 'Возврат\nотклонён', fillcolor='#F8CECC', peripheries='2')

# main flow
g.edge('created', 'pending_payment')
g.edge('pending_payment', 'paid', label='webhook: оплата успешна')
g.edge('pending_payment', 'cancelled', label='таймаут 15 мин\nили отмена')
g.edge('paid', 'packing')
g.edge('packing', 'shipped')
g.edge('shipped', 'delivered')

# cancellations
g.edge('created', 'cancelled', label='покупатель отменил')
g.edge('paid', 'cancelled', label='отмена ДО сборки\n(возврат средств)')

# returns
g.edge('delivered', 'return_requested', label='покупатель\nоформил возврат\n(окно 14 дней)')
g.edge('return_requested', 'return_received', label='товар\nдоставлен на склад')
g.edge('return_received', 'return_approved', label='проверка ОК')
g.edge('return_received', 'return_rejected', label='товар повреждён\nне по вине магазина')

g.render('/home/claude/ecommerce/docs/state_diagram', cleanup=True)
print('done')
