import networkx as nx
import matplotlib
matplotlib.use('Agg')  # 指定使用Agg后端
import matplotlib.pyplot as plt

# 创建一个新的有向图
petri_net = nx.DiGraph()

# Add places (participants)
participants = ['Customer', 'Agency', 'Supplier', 'Bank', 'Check Credit and Stock']
for place in participants:
    petri_net.add_node(place)

# Add transitions (interactions)
transitions = ['Send Purchase Order', 'Query Credit', 'Query Stock', 'Check Credit',
               'Check Stock', 'Send Payment Request', 'Pay Order', 'Inform Supplier to Ship Goods',
               'Ship Goods', 'Send Receptions', 'Abort Transaction']
for transition in transitions:
    petri_net.add_node(transition)

# Add edges representing the flow of interactions
edges = [('Customer', 'Send Purchase Order'),
         ('Send Purchase Order', 'Agency'),
         ('Agency', 'Query Credit'),
         ('Query Customer Credit', 'Bank'),
         ('Bank', 'Check Credit'),
         ('Agency', 'Query Stock'),
         ('Query Stock', 'Supplier'),
         ('Supplier', 'Check Stock'),
         ('Check Credit', 'Check Credit and Stock'),
         ('Check Stock', 'Check Credit and Stock'),
         ('Check Credit and Stock', 'Send Payment Request'),
         ('Send Payment Request', 'Customer'),
         ('Customer', 'Pay Order'),
         ('Pay Order', 'Agency'),
         ('Agency', 'Inform Supplier to Ship Goods'),
         ('Inform Supplier to Ship Goods', 'Supplier'),
         ('Supplier', 'Ship Goods'),
         ('Ship Goods', 'Customer'),
         ('Customer', 'Send Receptions'),
         ('Send Receptions', 'Agency'),
         ('Send Receptions', 'Supplier'),
         ('Customer', 'Abort Transaction'),
         ('Agency', 'Abort Transaction'),
         ('Supplier', 'Abort Transaction'),
         ('Bank', 'Abort Transaction')
         ]
petri_net.add_edges_from(edges)

# Manually specify node positions for better layout
pos = {
    'Customer': (1, 4),
    'Agency': (2, 4),
    'Supplier': (3, 4),
    'Bank': (4, 4),
    'Payment Request Sent': (1, 3),
    'Goods Shipped': (2, 3),
    'Goods Received': (3, 3),
    'Send Purchase Order': (1, 2),
    'Query Customer Credit': (2, 2),
    'Check Credit and Stock': (3, 2),
    'Send Payment Request': (4, 2),
    'Pay Order': (1, 1),
    'Inform Supplier to Ship Goods': (2, 1),
    'Ship Goods': (3, 1),
    'Receive Goods': (4, 1),
    'Abort Transaction': (2.5, 0),
    'Notify Other Participants': (1, 0),
}

# Draw Petri net
plt.figure(figsize=(12, 8))
# Separate nodes by shape
places = [node for node in participants]
transitions = [node for node in transitions]

# Draw nodes by shape
nx.draw_networkx_nodes(petri_net, pos, nodelist=places, node_shape='o', node_color='skyblue')
nx.draw_networkx_nodes(petri_net, pos, nodelist=transitions, node_shape='s', node_color='skyblue')

nx.draw_networkx_labels(petri_net, pos, font_size=10, font_weight='bold')

# Draw edges
nx.draw_networkx_edges(petri_net, pos, edgelist=edges, arrows=True)


# 保存绘图为图片
plt.savefig('petri_net.png')

# 不需要显示图形
# plt.show()
