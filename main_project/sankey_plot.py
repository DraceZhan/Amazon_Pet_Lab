import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as pex

pd.options.mode.chained_assignment = None

def data_prep():
	df = pd.read_csv('pet_purchase.csv', index_col=0)
	df = df.rename(columns={'0_buy': 'First_buy', '1_buy': 'Second_buy'})
	top_twenty_df = df[np.logical_and(df['First_buy'].isin( 
                                   list(df['First_buy'].value_counts()[:20].keys())),
                                  df['Second_buy'].isin( 
                                   list(df['Second_buy'].value_counts()[:20].keys()))
                                  )]

	top_twenty_df['First_buy'] = top_twenty_df['First_buy'] + '1'

	return(top_twenty_df)

def plot_gen():

	top_twenty_df = data_prep()

	all_nodes = top_twenty_df['First_buy'].values.tolist() + top_twenty_df['Second_buy'].values.tolist()
	source_indices = [all_nodes.index(first) for first in top_twenty_df['First_buy']]
	target_indices = [all_nodes.index(second) for second in top_twenty_df['Second_buy']]

	colors = pex.colors.qualitative.D3

	node_colors_mappings = dict([(node,np.random.choice(colors)) for node in all_nodes])
	node_colors = [node_colors_mappings[node] for node in all_nodes]
	edge_colors = [node_colors_mappings[node] for node in top_twenty_df['Second_buy']]


	fig = go.Figure(data=[go.Sankey(
    # Define nodes
    node = dict(
      label =  all_nodes,
      color =  node_colors
    ),

    # Add links
    link = dict(
      source =  source_indices,
      target =  target_indices,
      value =  top_twenty_df.groupby(['First_buy', 'Second_buy']).count().reset_index()['overall_list_1'].values,
        color = edge_colors
	))])

	fig.update_layout(title_text="Map of First Purchased to Second Purchased Item", height=1000,
                  font_size=10)
	fig.show()

if __name__ == '__main__':
	plot_gen()