import graphviz

g = graphviz.Digraph('bpmn_as_is', format='png')
g.attr(rankdir='LR', splines='ortho', fontname='Helvetica', bgcolor='white')
g.attr('node', fontname='Helvetica', fontsize='11')
g.attr('edge', fontname='Helvetica', fontsize='9')

# Swimlanes as clusters
with g.subgraph(name='cluster_customer') as c:
    c.attr(label='Покупатель', style='filled', color='lightgrey', fillcolor='#F5F5F5')
    c.node('start', 'Начало\n(пишет в мессенджер)', shape='ellipse', style='filled', fillcolor='#D5E8D4')
    c.node('c1', 'Выбирает товар\nпо фото/каталогу', shape='box', style='filled', fillcolor='#DAE8FC')
    c.node('c2', 'Ждёт ответа\nоператора', shape='box', style='filled', fillcolor='#DAE8FC')
    c.node('c3', 'Переводит оплату\nвручную (карта/QR)', shape='box', style='filled', fillcolor='#DAE8FC')
    c.node('c4', 'Ждёт доставку\nбез трекинга', shape='box', style='filled', fillcolor='#DAE8FC')

with g.subgraph(name='cluster_operator') as o:
    o.attr(label='Оператор (вручную)', style='filled', color='lightgrey', fillcolor='#F5F5F5')
    o.node('o1', 'Проверяет наличие\nтовара вручную', shape='box', style='filled', fillcolor='#FFE6CC')
    o.node('o2', 'Считает сумму\nи реквизиты', shape='box', style='filled', fillcolor='#FFE6CC')
    o.node('o3', 'Проверяет поступление\nоплаты вручную', shape='box', style='filled', fillcolor='#FFE6CC')
    o.node('o_gw', 'Товар\nв наличии?', shape='diamond', style='filled', fillcolor='#FFF2CC')
    o.node('o4', 'Передаёт заказ\nна склад', shape='box', style='filled', fillcolor='#FFE6CC')
    o.node('end_fail', 'Сообщает об\nотсутствии товара', shape='ellipse', style='filled', fillcolor='#F8CECC')

with g.subgraph(name='cluster_warehouse') as w:
    w.attr(label='Склад', style='filled', color='lightgrey', fillcolor='#F5F5F5')
    w.node('w1', 'Собирает заказ\nвручную', shape='box', style='filled', fillcolor='#E1D5E7')
    w.node('w2', 'Передаёт курьеру\nбез трекинг-номера', shape='box', style='filled', fillcolor='#E1D5E7')
    w.node('end_ok', 'Конец:\nзаказ доставлен', shape='ellipse', style='filled', fillcolor='#D5E8D4')

g.edge('start', 'c1')
g.edge('c1', 'o1')
g.edge('o1', 'o_gw')
g.edge('o_gw', 'end_fail', label='нет')
g.edge('o_gw', 'o2', label='да')
g.edge('o2', 'c2')
g.edge('c2', 'c3')
g.edge('c3', 'o3')
g.edge('o3', 'o4')
g.edge('o4', 'w1')
g.edge('w1', 'w2')
g.edge('w2', 'c4')
g.edge('c4', 'end_ok')

g.render('/home/claude/ecommerce/docs/bpmn_as_is', cleanup=True)
print('done')
