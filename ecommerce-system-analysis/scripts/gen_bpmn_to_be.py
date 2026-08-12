import graphviz

g = graphviz.Digraph('bpmn_to_be', format='png')
g.attr(rankdir='LR', splines='ortho', fontname='Helvetica', bgcolor='white', nodesep='0.35', ranksep='0.5')
g.attr('node', fontname='Helvetica', fontsize='11')
g.attr('edge', fontname='Helvetica', fontsize='9')

with g.subgraph(name='cluster_customer') as c:
    c.attr(label='Покупатель', style='filled', color='lightgrey', fillcolor='#F5F5F5')
    c.node('start', 'Начало:\nоформляет заказ\nв каталоге', shape='ellipse', style='filled', fillcolor='#D5E8D4')
    c.node('c1', 'Подтверждает\nсостав корзины', shape='box', style='filled', fillcolor='#DAE8FC')
    c.node('c2', 'Оплачивает заказ\nчерез платёжный шлюз', shape='box', style='filled', fillcolor='#DAE8FC')
    c.node('c3', 'Получает push/email\nо смене статуса', shape='box', style='filled', fillcolor='#DAE8FC')

with g.subgraph(name='cluster_system') as s:
    s.attr(label='Система (автоматически)', style='filled', color='lightgrey', fillcolor='#F5F5F5')
    s.node('s1', 'Резервирует товар\nна складе (15 мин)', shape='box', style='filled', fillcolor='#FFE6CC')
    s.node('s_gw', 'Товар\nдоступен?', shape='diamond', style='filled', fillcolor='#FFF2CC')
    s.node('end_fail', 'Показывает "Нет\nв наличии", предлагает\nаналог', shape='ellipse', style='filled', fillcolor='#F8CECC')
    s.node('s2', 'Инициирует запрос\nв платёжный шлюз', shape='box', style='filled', fillcolor='#FFE6CC')
    s.node('s3', 'Принимает webhook\nоб оплате\n(идемпотентно)', shape='box', style='filled', fillcolor='#FFE6CC')
    s.node('s4', 'Меняет статус\n"Оплачен",\nуведомляет', shape='box', style='filled', fillcolor='#FFE6CC')
    s.node('s5', 'Формирует задание\nна сборку\nдля склада', shape='box', style='filled', fillcolor='#FFE6CC')

with g.subgraph(name='cluster_warehouse') as w:
    w.attr(label='Склад', style='filled', color='lightgrey', fillcolor='#F5F5F5')
    w.node('w1', 'Собирает заказ\nпо заданию\nв системе', shape='box', style='filled', fillcolor='#E1D5E7')
    w.node('w2', 'Сканирует и\nпередаёт в доставку\n(с трекингом)', shape='box', style='filled', fillcolor='#E1D5E7')
    w.node('end_ok', 'Конец:\nзаказ доставлен', shape='ellipse', style='filled', fillcolor='#D5E8D4')

g.edge('start', 'c1')
g.edge('c1', 's1')
g.edge('s1', 's_gw')
g.edge('s_gw', 'end_fail', label='нет')
g.edge('s_gw', 'c2', label='да')
g.edge('c2', 's2')
g.edge('s2', 's3')
g.edge('s3', 's4')
g.edge('s4', 'c3')
g.edge('s4', 's5')
g.edge('s5', 'w1')
g.edge('w1', 'w2')
g.edge('w2', 'end_ok')
g.edge('c3', 'end_ok', style='invis')

g.render('/home/claude/ecommerce/docs/bpmn_to_be', cleanup=True)
print('done')
