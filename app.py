import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time

# --- Configuration ---
st.set_page_config(page_title="K-Means Simulator", layout="wide")

# --- State Initialization ---
# We use st.session_state to remember the data between button clicks
if 'points' not in st.session_state:
    # Generate 100 points in 3 loose, natural clusters
    np.random.seed(42)
    c1 = np.random.randn(33, 2) + np.array([3, 3])
    c2 = np.random.randn(33, 2) + np.array([-3, -3])
    c3 = np.random.randn(34, 2) + np.array([3, -3])
    st.session_state.points = np.vstack([c1, c2, c3])
    st.session_state.centroids = None
    st.session_state.labels = None
    st.session_state.phase = "Uninitialized"
    st.session_state.step = 0

# Colors for clusters (supports up to 5 clusters as requested)
COLORS = ['#3498db', '#e74c3c', '#2ecc71', '#9b59b6', '#f1c40f']

# --- Helper Functions ---
def reset_points():
    np.random.seed(int(time.time())) # New random clusters
    c1 = np.random.randn(33, 2) + np.array([np.random.randint(-4, 4), np.random.randint(-4, 4)])
    c2 = np.random.randn(33, 2) + np.array([np.random.randint(-4, 4), np.random.randint(-4, 4)])
    c3 = np.random.randn(34, 2) + np.array([np.random.randint(-4, 4), np.random.randint(-4, 4)])
    st.session_state.points = np.vstack([c1, c2, c3])
    st.session_state.centroids = None
    st.session_state.labels = None
    st.session_state.phase = "Uninitialized"
    st.session_state.step = 0

def randomize_centroids(k):
    # Pick K random points from our dataset to act as initial centroids
    indices = np.random.choice(len(st.session_state.points), k, replace=False)
    st.session_state.centroids = st.session_state.points[indices].copy()
    st.session_state.labels = None
    st.session_state.phase = "Centroids Placed"
    st.session_state.step = 0

def assign_points():
    points = st.session_state.points
    centroids = st.session_state.centroids
    
    # Calculate distances from every point to every centroid
    distances = np.sqrt(((points - centroids[:, np.newaxis])**2).sum(axis=2))
    new_labels = np.argmin(distances, axis=0)
    
    # Check for convergence
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
        # Get all points assigned to cluster i
        cluster_points = points[labels == i]
        if len(cluster_points) > 0:
            # Move centroid to the mathematical mean of those points
            new_centroids[i] = cluster_points.mean(axis=0)
        else:
            # If a cluster is empty, keep centroid where it is
            new_centroids[i] = centroids[i]
            
    st.session_state.centroids = new_centroids
    st.session_state.phase = "Centroids Updated"

def step_forward():
    if st.session_state.phase in ["Uninitialized", "Converged"]:
        return # Do nothing
    elif st.session_state.phase in ["Centroids Placed", "Centroids Updated"]:
        assign_points()
    elif st.session_state.phase == "Points Assigned":
        update_centroids()

# --- Plotting Function ---
def create_plot():
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.set_xlim(-8, 8)
    ax.set_ylim(-8, 8)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title(f"Phase: {st.session_state.phase} | Step: {st.session_state.step}", fontsize=14, pad=15)

    points = st.session_state.points
    labels = st.session_state.labels
    centroids = st.session_state.centroids

    # Plot points
    if labels is None:
        # Neutral gray if not assigned
        ax.scatter(points[:, 0], points[:, 1], c='gray', alpha=0.6, s=50, edgecolors='w')
    else:
        # Color by assigned cluster
        point_colors = [COLORS[label] for label in labels]
        ax.scatter(points[:, 0], points[:, 1], c=point_colors, alpha=0.6, s=50, edgecolors='w')

    # Plot centroids
    if centroids is not None:
        for i, c in enumerate(centroids):
            ax.scatter(c[0], c[1], c=COLORS[i], marker='X', s=250, edgecolors='black', linewidths=2, zorder=10)
            
    return fig

# --- Sidebar UI ---
st.sidebar.header("Controls")
k = st.sidebar.slider("Number of Clusters (K)", min_value=1, max_value=5, value=3)

if st.sidebar.button("1. Randomize Centroids"):
    randomize_centroids(k)

if st.sidebar.button("2. Step Forward"):
    step_forward()

# We set up a flag for the run to convergence animation
run_clicked = st.sidebar.button("3. Run to Convergence")

if st.sidebar.button("4. Reset Points"):
    reset_points()

st.sidebar.markdown("---")
st.sidebar.markdown("**Instructions:**\n1. Pick $K$.\n2. Randomize Centroids.\n3. Step forward manually or run to convergence.")


# --- Main UI ---
st.title("Interactive K-Means Simulator")

# Placeholders for dynamic updating during animation
plot_placeholder = st.empty()

# Draw initial state
plot_placeholder.pyplot(create_plot())

# Handle Run to Convergence Animation
if run_clicked:
    if st.session_state.phase == "Uninitialized":
        randomize_centroids(k)
        plot_placeholder.pyplot(create_plot())
        time.sleep(0.5)
        
    while st.session_state.phase != "Converged":
        step_forward()
        plot_placeholder.pyplot(create_plot())
        time.sleep(0.5) # Short pause to animate the algorithm visually