# import streamlit as st
# import numpy as np
# import matplotlib.pyplot as plt
# import time

# # --- Configuration ---
# st.set_page_config(page_title="K-Means Simulator", layout="wide")

# # --- State Initialization ---
# # We use st.session_state to remember the data between button clicks
# if 'points' not in st.session_state:
#     # Generate 100 points in 3 loose, natural clusters
#     np.random.seed(42)
#     c1 = np.random.randn(33, 2) + np.array([3, 3])
#     c2 = np.random.randn(33, 2) + np.array([-3, -3])
#     c3 = np.random.randn(34, 2) + np.array([3, -3])
#     st.session_state.points = np.vstack([c1, c2, c3])
#     st.session_state.centroids = None
#     st.session_state.labels = None
#     st.session_state.phase = "Uninitialized"
#     st.session_state.step = 0

# # Colors for clusters (supports up to 5 clusters as requested)
# COLORS = ['#3498db', '#e74c3c', '#2ecc71', '#9b59b6', '#f1c40f']

# # --- Helper Functions ---
# def reset_points():
#     np.random.seed(int(time.time())) # New random clusters
#     c1 = np.random.randn(33, 2) + np.array([np.random.randint(-4, 4), np.random.randint(-4, 4)])
#     c2 = np.random.randn(33, 2) + np.array([np.random.randint(-4, 4), np.random.randint(-4, 4)])
#     c3 = np.random.randn(34, 2) + np.array([np.random.randint(-4, 4), np.random.randint(-4, 4)])
#     st.session_state.points = np.vstack([c1, c2, c3])
#     st.session_state.centroids = None
#     st.session_state.labels = None
#     st.session_state.phase = "Uninitialized"
#     st.session_state.step = 0

# def randomize_centroids(k):
#     # Pick K random points from our dataset to act as initial centroids
#     indices = np.random.choice(len(st.session_state.points), k, replace=False)
#     st.session_state.centroids = st.session_state.points[indices].copy()
#     st.session_state.labels = None
#     st.session_state.phase = "Centroids Placed"
#     st.session_state.step = 0

# def assign_points():
#     points = st.session_state.points
#     centroids = st.session_state.centroids
    
#     # Calculate distances from every point to every centroid
#     distances = np.sqrt(((points - centroids[:, np.newaxis])**2).sum(axis=2))
#     new_labels = np.argmin(distances, axis=0)
    
#     # Check for convergence
#     if st.session_state.labels is not None and np.array_equal(st.session_state.labels, new_labels):
#         st.session_state.phase = "Converged"
#     else:
#         st.session_state.labels = new_labels
#         if st.session_state.phase != "Converged":
#             st.session_state.phase = "Points Assigned"
#             st.session_state.step += 1

# def update_centroids():
#     points = st.session_state.points
#     labels = st.session_state.labels
#     centroids = st.session_state.centroids
    
#     new_centroids = np.zeros_like(centroids)
#     for i in range(len(centroids)):
#         # Get all points assigned to cluster i
#         cluster_points = points[labels == i]
#         if len(cluster_points) > 0:
#             # Move centroid to the mathematical mean of those points
#             new_centroids[i] = cluster_points.mean(axis=0)
#         else:
#             # If a cluster is empty, keep centroid where it is
#             new_centroids[i] = centroids[i]
            
#     st.session_state.centroids = new_centroids
#     st.session_state.phase = "Centroids Updated"

# def step_forward():
#     if st.session_state.phase in ["Uninitialized", "Converged"]:
#         return # Do nothing
#     elif st.session_state.phase in ["Centroids Placed", "Centroids Updated"]:
#         assign_points()
#     elif st.session_state.phase == "Points Assigned":
#         update_centroids()

# # --- Plotting Function ---
# def create_plot():
#     fig, ax = plt.subplots(figsize=(3, 2))
#     ax.set_xlim(-4, 4)
#     ax.set_ylim(-4, 4)
#     ax.set_xticks([])
#     ax.set_yticks([])
#     ax.set_title(f"Phase: {st.session_state.phase} | Step: {st.session_state.step}", fontsize=5, pad=5)

#     points = st.session_state.points
#     labels = st.session_state.labels
#     centroids = st.session_state.centroids

#     # Plot points
#     if labels is None:
#         # Neutral gray if not assigned
#         ax.scatter(points[:, 0], points[:, 1], c='gray', alpha=0.6, s=50, edgecolors='w')
#     else:
#         # Color by assigned cluster
#         point_colors = [COLORS[label] for label in labels]
#         ax.scatter(points[:, 0], points[:, 1], c=point_colors, alpha=0.6, s=50, edgecolors='w')

#     # Plot centroids
#     if centroids is not None:
#         for i, c in enumerate(centroids):
#             ax.scatter(c[0], c[1], c=COLORS[i], marker='X', s=250, edgecolors='black', linewidths=2, zorder=10)
            
#     return fig

# # --- Sidebar UI ---
# st.sidebar.header("Controls")
# k = st.sidebar.slider("Number of Clusters (K)", min_value=1, max_value=5, value=3)

# if st.sidebar.button("1. Randomize Centroids"):
#     randomize_centroids(k)

# if st.sidebar.button("2. Step Forward"):
#     step_forward()

# # We set up a flag for the run to convergence animation
# run_clicked = st.sidebar.button("3. Run to Convergence")

# if st.sidebar.button("4. Reset Points"):
#     reset_points()

# st.sidebar.markdown("---")
# st.sidebar.markdown("**Instructions:**\n1. Pick $K$.\n2. Randomize Centroids.\n3. Step forward manually or run to convergence.")


# # --- Main UI ---
# st.title("Interactive K-Means Simulator")

# # Placeholders for dynamic updating during animation
# plot_placeholder = st.empty()

# # Draw initial state
# plot_placeholder.pyplot(create_plot())

# # Handle Run to Convergence Animation
# if run_clicked:
#     if st.session_state.phase == "Uninitialized":
#         randomize_centroids(k)
#         plot_placeholder.pyplot(create_plot())
#         time.sleep(0.5)
        
#     while st.session_state.phase != "Converged":
#         step_forward()
#         plot_placeholder.pyplot(create_plot())
#         time.sleep(0.5) # Short pause to animate the algorithm visually
import streamlit as st
import numpy as np
import plotly.graph_objects as go
import time

# --- Configuration ---
st.set_page_config(page_title="K-Means Simulator", layout="wide")

# --- State Initialization ---
if 'points' not in st.session_state:
    np.random.seed(42)
    c1 = np.random.randn(33, 2) + np.array([3, 3])
    c2 = np.random.randn(33, 2) + np.array([-3, -3])
    c3 = np.random.randn(34, 2) + np.array([3, -3])
    st.session_state.points = np.vstack([c1, c2, c3])
    st.session_state.centroids = None
    st.session_state.labels = None
    st.session_state.phase = "Uninitialized"
    st.session_state.step = 0

COLORS = ['#3498db', '#e74c3c', '#2ecc71', '#9b59b6', '#f1c40f']

# --- Helper Functions ---
def reset_points():
    np.random.seed(int(time.time())) 
    c1 = np.random.randn(33, 2) + np.array([np.random.randint(-4, 4), np.random.randint(-4, 4)])
    c2 = np.random.randn(33, 2) + np.array([np.random.randint(-4, 4), np.random.randint(-4, 4)])
    c3 = np.random.randn(34, 2) + np.array([np.random.randint(-4, 4), np.random.randint(-4, 4)])
    st.session_state.points = np.vstack([c1, c2, c3])
    st.session_state.centroids = None
    st.session_state.labels = None
    st.session_state.phase = "Uninitialized"
    st.session_state.step = 0

def randomize_centroids(k):
    indices = np.random.choice(len(st.session_state.points), k, replace=False)
    st.session_state.centroids = st.session_state.points[indices].copy()
    st.session_state.labels = None
    st.session_state.phase = "Centroids Placed"
    st.session_state.step = 0

def assign_points():
    points = st.session_state.points
    centroids = st.session_state.centroids
    
    distances = np.sqrt(((points - centroids[:, np.newaxis])**2).sum(axis=2))
    new_labels = np.argmin(distances, axis=0)
    
    if st.session_state.labels is not None and np.array_equal(st.session_state.labels, new_labels):
        st.session_state.phase = "Converged"
    else:
        st.session_state.labels = new_labels
        if st.session_state.phase != "Converged":
            st.session_state.phase = "Points Assigned"
            st.session_state.step += 1

def update_centroids():
    points = st.session_state.points
    labels = st.session_state.labels
    centroids = st.session_state.centroids
    
    new_centroids = np.zeros_like(centroids)
    for i in range(len(centroids)):
        cluster_points = points[labels == i]
        if len(cluster_points) > 0:
            new_centroids[i] = cluster_points.mean(axis=0)
        else:
            new_centroids[i] = centroids[i]
            
    st.session_state.centroids = new_centroids
    st.session_state.phase = "Centroids Updated"

def step_forward():
    if st.session_state.phase in ["Uninitialized", "Converged"]:
        return 
    elif st.session_state.phase in ["Centroids Placed", "Centroids Updated"]:
        assign_points()
    elif st.session_state.phase == "Points Assigned":
        update_centroids()

# --- Plotly Plotting Function ---
def create_plot():
    points = st.session_state.points
    labels = st.session_state.labels
    centroids = st.session_state.centroids

    fig = go.Figure()

    # Plot data points
    if labels is None:
        fig.add_trace(go.Scatter(
            x=points[:, 0], y=points[:, 1],
            mode='markers',
            marker=dict(color='gray', size=10, opacity=0.7, line=dict(width=1, color='white')),
            name='Unassigned Points'
        ))
    else:
        for i in range(len(np.unique(labels))):
            cluster_points = points[labels == i]
            fig.add_trace(go.Scatter(
                x=cluster_points[:, 0], y=cluster_points[:, 1],
                mode='markers',
                marker=dict(color=COLORS[i], size=10, opacity=0.7, line=dict(width=1, color='white')),
                name=f'Cluster {i+1}'
            ))

    # Plot centroids
    if centroids is not None:
        for i, c in enumerate(centroids):
            fig.add_trace(go.Scatter(
                x=[c[0]], y=[c[1]],
                mode='markers',
                marker=dict(color=COLORS[i], size=18, symbol='x', line=dict(width=2, color='black')),
                name=f'Centroid {i+1}'
            ))

    # Make the layout dynamic and clean
    fig.update_layout(
        title=dict(text=f"<b>Phase: {st.session_state.phase} | Step: {st.session_state.step}</b>", font=dict(size=22)),
        xaxis=dict(title="Feature 1 (Dimension X)", zeroline=False, showgrid=True),
        yaxis=dict(title="Feature 2 (Dimension Y)", zeroline=False, showgrid=True),
        hovermode="closest",
        margin=dict(l=20, r=20, t=60, b=20),
        legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01, bgcolor="rgba(255,255,255,0.8)"),
        autosize=True # Ensures it responds to window size dynamically
    )
    return fig

# --- Sidebar UI ---
st.sidebar.header("Controls")
k = st.sidebar.slider("Number of Clusters (K)", min_value=1, max_value=5, value=3)

if st.sidebar.button("1. Randomize Centroids"):
    randomize_centroids(k)

if st.sidebar.button("2. Step Forward"):
    step_forward()

run_clicked = st.sidebar.button("3. Run to Convergence")

if st.sidebar.button("4. Reset Points"):
    reset_points()

st.sidebar.markdown("---")
st.sidebar.markdown("**Instructions:**\n1. Pick $K$.\n2. Randomize Centroids.\n3. Step forward manually or run to convergence.")

# --- Main UI ---
st.title("Interactive K-Means Simulator")

# Container for the plot and citations
plot_container = st.container()

with plot_container:
    plot_placeholder = st.empty()
    
    # Proper formatting and citation for the visualization
    st.caption("**Figure 1:** 2D Visualization of the K-Means clustering algorithm. Data points are synthetically generated using Gaussian distributions to simulate natural groupings.")
    st.markdown("<small><i>Algorithm objective: Minimize Within-Cluster Sum of Squares (WCSS) using Euclidean distance metrics.</i></small>", unsafe_allow_html=True)

# Draw initial state using use_container_width=True for dynamic sizing
plot_placeholder.plotly_chart(create_plot(), use_container_width=True)

# Handle Run to Convergence Animation
if run_clicked:
    if st.session_state.phase == "Uninitialized":
        randomize_centroids(k)
        plot_placeholder.plotly_chart(create_plot(), use_container_width=True)
        time.sleep(0.5)
        
    while st.session_state.phase != "Converged":
        step_forward()
        plot_placeholder.plotly_chart(create_plot(), use_container_width=True)
        time.sleep(0.5)