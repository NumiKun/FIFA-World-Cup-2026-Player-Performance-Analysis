import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os

# ─────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="FIFA World Cup 2026 — Analytics",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
#  GLOBAL STYLES
# ─────────────────────────────────────────────
st.markdown("""
<style>
/* ── Base ───────────────────────────────── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: linear-gradient(135deg, #0a0e1a 0%, #0d1117 50%, #0a1628 100%);
}

/* ── Sidebar ─────────────────────────────── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0d1b2e 0%, #0a1628 100%);
    border-right: 1px solid #1e3a5f;
}
[data-testid="stSidebar"] * {
    color: #c9d1d9 !important;
}
[data-testid="stSidebarNav"] {
    padding-top: 1rem;
}

/* ── Metric cards ────────────────────────── */
[data-testid="metric-container"] {
    background: linear-gradient(135deg, #0d1b2e 0%, #112240 100%);
    border: 1px solid #1e3a5f;
    border-radius: 12px;
    padding: 1rem 1.2rem;
    box-shadow: 0 4px 20px rgba(0,0,0,0.4);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}
[data-testid="metric-container"]:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 30px rgba(88, 166, 255, 0.15);
    border-color: #58a6ff;
}
[data-testid="metric-container"] label {
    color: #8b949e !important;
    font-size: 0.78rem !important;
    font-weight: 600 !important;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}
[data-testid="metric-container"] [data-testid="stMetricValue"] {
    color: #ffd700 !important;
    font-size: 1.7rem !important;
    font-weight: 700 !important;
}
[data-testid="stMetricDelta"] {
    color: #3fb950 !important;
}

/* ── Section headers ─────────────────────── */
.section-header {
    background: linear-gradient(90deg, #1e3a5f 0%, rgba(30,58,95,0.2) 100%);
    border-left: 4px solid #58a6ff;
    border-radius: 0 8px 8px 0;
    padding: 0.6rem 1.2rem;
    margin: 1.5rem 0 1rem 0;
    color: #e6edf3;
    font-size: 1.05rem;
    font-weight: 700;
}

/* ── Selectbox / multiselect ─────────────── */
[data-testid="stSelectbox"] > div > div,
[data-testid="stMultiSelect"] > div > div {
    background: #0d1b2e !important;
    border-color: #1e3a5f !important;
    color: #c9d1d9 !important;
    border-radius: 8px !important;
}

/* ── Slider ──────────────────────────────── */
[data-testid="stSlider"] .stSlider > div > div > div > div {
    background: #58a6ff !important;
}

/* ── Dataframe ───────────────────────────── */
[data-testid="stDataFrame"] {
    border: 1px solid #1e3a5f;
    border-radius: 8px;
}

/* ── Divider ─────────────────────────────── */
hr {
    border-color: #1e3a5f !important;
}

/* ── Tab styling ─────────────────────────── */
[data-testid="stTabs"] button {
    color: #8b949e !important;
    font-weight: 600;
    border-radius: 8px 8px 0 0;
}
[data-testid="stTabs"] button[aria-selected="true"] {
    color: #58a6ff !important;
    border-bottom-color: #58a6ff !important;
}

/* ── Header title ────────────────────────── */
.main-title {
    background: linear-gradient(135deg, #58a6ff, #ffd700, #3fb950);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    font-size: 2.5rem;
    font-weight: 800;
    line-height: 1.2;
    margin-bottom: 0.3rem;
}
.main-subtitle {
    color: #8b949e;
    font-size: 0.95rem;
    font-weight: 400;
    margin-bottom: 1.5rem;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  PLOTLY THEME
# ─────────────────────────────────────────────
LAYOUT_DEFAULTS = dict(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(13,27,46,0.6)',
    font=dict(family='Inter', color='#c9d1d9', size=11),
    title=dict(font=dict(color='#e6edf3', size=14, family='Inter'), x=0.01),
    xaxis=dict(gridcolor='#1e3a5f', linecolor='#1e3a5f', zerolinecolor='#1e3a5f', tickcolor='#8b949e'),
    yaxis=dict(gridcolor='#1e3a5f', linecolor='#1e3a5f', zerolinecolor='#1e3a5f', tickcolor='#8b949e'),
    legend=dict(bgcolor='rgba(13,27,46,0.8)', bordercolor='#1e3a5f', borderwidth=1),
    colorway=['#58a6ff','#3fb950','#f78166','#d2a8ff','#ffa657','#79c0ff','#ffd700'],
    margin=dict(l=40, r=20, t=50, b=40),
)

COLORS = {
    'blue':   '#58a6ff',
    'green':  '#3fb950',
    'red':    '#f78166',
    'purple': '#d2a8ff',
    'orange': '#ffa657',
    'gold':   '#ffd700',
    'teal':   '#79c0ff',
}

STAGE_ORDER = ['Group Stage','Round of 32','Round of 16','Quarter-Final','Semi-Final','Third Place','Final']

# ─────────────────────────────────────────────
#  DATA LOADING
# ─────────────────────────────────────────────
DATA_PATH = os.path.join(os.path.dirname(__file__), '..', 'Analysis', 'fifa_world_cup_2026_player_performance.csv')

@st.cache_data(show_spinner="⚽ Loading dataset...")
def load_data():
    df = pd.read_csv(DATA_PATH, parse_dates=['match_date'])
    return df

@st.cache_data(show_spinner=False)
def build_player_stats(df):
    ps = df.groupby(['player_id','player_name','team','position','nationality']).agg(
        total_matches       =('match_id','count'),
        total_minutes       =('minutes_played','sum'),
        total_goals         =('goals','sum'),
        total_assists       =('assists','sum'),
        total_shots         =('shots','sum'),
        total_shots_ot      =('shots_on_target','sum'),
        total_xG            =('expected_goals_xg','sum'),
        total_xA            =('expected_assists_xa','sum'),
        total_key_passes    =('key_passes','sum'),
        avg_pass_acc        =('pass_accuracy','mean'),
        total_dribbles      =('successful_dribbles','sum'),
        total_tackles       =('tackles','sum'),
        total_interceptions =('interceptions','sum'),
        total_clearances    =('clearances','sum'),
        avg_speed           =('top_speed_kmh','mean'),
        avg_distance        =('distance_covered_km','mean'),
        avg_stamina         =('stamina_score','mean'),
        avg_rating          =('player_rating','mean'),
        avg_perf_score      =('performance_score','mean'),
        player_of_match     =('player_of_match_awards','sum'),
        yellow_cards        =('yellow_cards','sum'),
        red_cards           =('red_cards','sum'),
    ).reset_index()
    ps['conversion_rate'] = (ps['total_goals'] / ps['total_shots'].replace(0, np.nan)).fillna(0)
    ps['xG_diff']         = ps['total_goals'] - ps['total_xG']
    ps['creativity_idx']  = ps['total_key_passes']*1.0 + ps['total_assists']*3.0 + ps['total_xA']*2.0
    ps['defensive_idx']   = ps['total_tackles']*2.0 + ps['total_interceptions']*2.5
    return ps

@st.cache_data(show_spinner=False)
def build_team_stats(df):
    mr = df.groupby(['match_id','team','tournament_stage','match_result']).agg(
        goals_scored   =('goals_team','first'),
        goals_conceded =('goals_opponent','first'),
        avg_rating     =('player_rating','mean'),
    ).reset_index()
    ta = mr.groupby('team').agg(
        total_matches =('match_id','count'),
        wins          =('match_result', lambda x: (x=='W').sum()),
        draws         =('match_result', lambda x: (x=='D').sum()),
        losses        =('match_result', lambda x: (x=='L').sum()),
        total_goals_f =('goals_scored','sum'),
        total_goals_a =('goals_conceded','sum'),
        avg_rating    =('avg_rating','mean'),
    ).reset_index()
    ta['win_rate']  = ta['wins'] / ta['total_matches'] * 100
    ta['goal_diff'] = ta['total_goals_f'] - ta['total_goals_a']
    ta['goals_pg']  = ta['total_goals_f'] / ta['total_matches']
    return ta

df = load_data()
player_stats = build_player_stats(df)
team_stats   = build_team_stats(df)
player_info  = df.drop_duplicates('player_id')[
    ['player_id','player_name','age','nationality','team','position',
     'height_cm','weight_kg','preferred_foot','club_name','market_value_eur']
].copy()

# ─────────────────────────────────────────────
#  SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
        <div style='text-align:center; padding: 1rem 0 0.5rem 0;'>
            <div style='font-size:2.5rem'>⚽</div>
            <div style='color:#ffd700; font-weight:800; font-size:1.1rem; line-height:1.3;'>
                FIFA World Cup<br>2026 Analytics
            </div>
            <div style='color:#8b949e; font-size:0.72rem; margin-top:0.3rem;'>
                Interactive Dashboard
            </div>
        </div>
        <hr style='border-color:#1e3a5f; margin: 0.5rem 0 1rem 0;'>
    """, unsafe_allow_html=True)

    page = st.radio(
        "Navigate",
        ["🏠  Overview",
         "👤  Player Explorer",
         "⚽  Attacking",
         "🛡️  Defensive",
         "💪  Physical",
         "🌍  Teams"],
        label_visibility="collapsed"
    )

    st.markdown("<hr style='border-color:#1e3a5f;'>", unsafe_allow_html=True)

    # Global filters
    st.markdown("<div style='color:#8b949e; font-size:0.78rem; font-weight:600; text-transform:uppercase; letter-spacing:0.05em;'>Global Filters</div>", unsafe_allow_html=True)

    sel_stages = st.multiselect(
        "Tournament Stage",
        options=[s for s in STAGE_ORDER if s in df['tournament_stage'].unique()],
        default=[s for s in STAGE_ORDER if s in df['tournament_stage'].unique()],
    )
    sel_positions = st.multiselect(
        "Position",
        options=df['position'].unique().tolist(),
        default=df['position'].unique().tolist(),
    )
    min_min = st.slider("Min. Minutes Played", 0, 600, 90, step=30)

    st.markdown("<hr style='border-color:#1e3a5f;'>", unsafe_allow_html=True)
    st.markdown("<div style='color:#8b949e; font-size:0.72rem; text-align:center;'>Dataset: 54,601 rows · 75 cols</div>", unsafe_allow_html=True)

# Apply global filter
df_f  = df[df['tournament_stage'].isin(sel_stages) & df['position'].isin(sel_positions)]
ps_f  = player_stats[
    player_stats['position'].isin(sel_positions) &
    (player_stats['total_minutes'] >= min_min)
]

# ═════════════════════════════════════════════
#  PAGE: OVERVIEW
# ═════════════════════════════════════════════
if "Overview" in page:
    st.markdown("<div class='main-title'>⚽ FIFA World Cup 2026</div>", unsafe_allow_html=True)
    st.markdown("<div class='main-subtitle'>Player Performance Analytics Dashboard — Interactive EDA</div>", unsafe_allow_html=True)

    # KPI Row
    c1,c2,c3,c4,c5,c6 = st.columns(6)
    c1.metric("🌍 Teams",       f"{df['team'].nunique()}")
    c2.metric("👤 Players",     f"{df['player_id'].nunique():,}")
    c3.metric("🎮 Matches",     f"{df['match_id'].nunique()}")
    c4.metric("⚽ Total Goals",  f"{int(df['goals'].sum()):,}")
    c5.metric("🎁 Total Assists",f"{int(df['assists'].sum()):,}")
    c6.metric("⭐ Avg Rating",  f"{df['player_rating'].mean():.2f}")

    st.markdown("<hr>", unsafe_allow_html=True)

    col_l, col_r = st.columns([1.4, 1])

    with col_l:
        st.markdown("<div class='section-header'>📅 Matches per Tournament Stage</div>", unsafe_allow_html=True)
        stage_cnts = df.groupby('tournament_stage')['match_id'].nunique().reset_index()
        stage_cnts.columns = ['stage','count']
        stage_cnts['order'] = stage_cnts['stage'].map({s:i for i,s in enumerate(STAGE_ORDER)})
        stage_cnts = stage_cnts.sort_values('order')
        fig = px.bar(stage_cnts, x='stage', y='count', text='count',
                     color='count', color_continuous_scale='Blues',
                     labels={'stage':'Stage','count':'Matches'})
        fig.update_traces(textposition='outside', marker_line_width=0)
        fig.update_layout(**LAYOUT_DEFAULTS, coloraxis_showscale=False)
        st.plotly_chart(fig, use_container_width=True)

    with col_r:
        st.markdown("<div class='section-header'>⚽ Position Distribution</div>", unsafe_allow_html=True)
        pos_c = player_info['position'].value_counts().reset_index()
        pos_c.columns = ['position','count']
        fig = px.pie(pos_c, names='position', values='count',
                     color_discrete_sequence=['#58a6ff','#3fb950','#f78166','#d2a8ff'],
                     hole=0.42)
        fig.update_traces(textinfo='label+percent', textfont_size=12,
                          marker=dict(line=dict(color='#0a0e1a', width=2)))
        fig.update_layout(**LAYOUT_DEFAULTS)
        st.plotly_chart(fig, use_container_width=True)

    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown("<div class='section-header'>📊 Goals & Assists per Stage</div>", unsafe_allow_html=True)
        ga_stage = df.groupby('tournament_stage').agg(
            goals=('goals','sum'), assists=('assists','sum')
        ).reset_index()
        ga_stage['order'] = ga_stage['tournament_stage'].map({s:i for i,s in enumerate(STAGE_ORDER)})
        ga_stage = ga_stage.sort_values('order')
        fig = go.Figure()
        fig.add_bar(x=ga_stage['tournament_stage'], y=ga_stage['goals'],   name='Goals',   marker_color=COLORS['gold'])
        fig.add_bar(x=ga_stage['tournament_stage'], y=ga_stage['assists'],  name='Assists', marker_color=COLORS['blue'])
        fig.update_layout(**LAYOUT_DEFAULTS, barmode='group')
        st.plotly_chart(fig, use_container_width=True)

    with col_b:
        st.markdown("<div class='section-header'>⭐ Avg Player Rating per Position</div>", unsafe_allow_html=True)
        rat_pos = df.groupby('position')['player_rating'].mean().reset_index()
        fig = px.bar(rat_pos, x='position', y='player_rating', text=rat_pos['player_rating'].round(2),
                     color='player_rating', color_continuous_scale='Viridis',
                     labels={'position':'Position','player_rating':'Avg Rating'})
        fig.update_traces(textposition='outside', marker_line_width=0)
        fig.update_layout(**LAYOUT_DEFAULTS, coloraxis_showscale=False)
        st.plotly_chart(fig, use_container_width=True)

    # Top 5 quick-view
    st.markdown("<div class='section-header'>🏆 Tournament Leaders at a Glance</div>", unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        r = ps_f.nlargest(1,'total_goals').iloc[0]
        st.markdown(f"**🥇 Top Scorer**<br>{r['player_name']}<br><span style='color:#ffd700;font-size:1.3rem;font-weight:700;'>{int(r['total_goals'])} goals</span><br><span style='color:#8b949e;font-size:0.8rem;'>{r['team']}</span>", unsafe_allow_html=True)
    with col2:
        r = ps_f.nlargest(1,'total_assists').iloc[0]
        st.markdown(f"**🎁 Top Assister**<br>{r['player_name']}<br><span style='color:#3fb950;font-size:1.3rem;font-weight:700;'>{int(r['total_assists'])} assists</span><br><span style='color:#8b949e;font-size:0.8rem;'>{r['team']}</span>", unsafe_allow_html=True)
    with col3:
        r = ps_f.nlargest(1,'avg_rating').iloc[0]
        st.markdown(f"**⭐ Best Rating**<br>{r['player_name']}<br><span style='color:#58a6ff;font-size:1.3rem;font-weight:700;'>{r['avg_rating']:.2f} rating</span><br><span style='color:#8b949e;font-size:0.8rem;'>{r['team']}</span>", unsafe_allow_html=True)
    with col4:
        r = ps_f.nlargest(1,'player_of_match').iloc[0]
        st.markdown(f"**🏅 Most POTM**<br>{r['player_name']}<br><span style='color:#ffa657;font-size:1.3rem;font-weight:700;'>{int(r['player_of_match'])} awards</span><br><span style='color:#8b949e;font-size:0.8rem;'>{r['team']}</span>", unsafe_allow_html=True)

# ═════════════════════════════════════════════
#  PAGE: PLAYER EXPLORER
# ═════════════════════════════════════════════
elif "Player Explorer" in page:
    st.markdown("<div class='main-title'>👤 Player Explorer</div>", unsafe_allow_html=True)
    st.markdown("<div class='main-subtitle'>Search, filter and compare individual player statistics</div>", unsafe_allow_html=True)

    # Filters
    col_f1, col_f2, col_f3 = st.columns(3)
    with col_f1:
        search_team = st.multiselect("Filter by Team", options=sorted(df['team'].unique()), default=[])
    with col_f2:
        search_nat  = st.multiselect("Filter by Nationality", options=sorted(df['nationality'].unique()), default=[])
    with col_f3:
        sort_by = st.selectbox("Sort by", ['avg_rating','total_goals','total_assists','total_xG',
                                            'avg_speed','avg_stamina','avg_perf_score','player_of_match'])

    display_df = ps_f.copy()
    if search_team:
        display_df = display_df[display_df['team'].isin(search_team)]
    if search_nat:
        display_df = display_df[display_df['nationality'].isin(search_nat)]
    display_df = display_df.sort_values(sort_by, ascending=False)

    st.markdown("<div class='section-header'>📋 Player Statistics Table</div>", unsafe_allow_html=True)
    show_cols = ['player_name','team','position','nationality','total_matches','total_minutes',
                 'total_goals','total_assists','total_xG','avg_pass_acc',
                 'total_tackles','avg_speed','avg_rating','avg_perf_score','player_of_match']
    st.dataframe(
        display_df[show_cols].rename(columns={
            'player_name':'Player','team':'Team','position':'Pos','nationality':'Nationality',
            'total_matches':'M','total_minutes':'Mins','total_goals':'G','total_assists':'A',
            'total_xG':'xG','avg_pass_acc':'Pass%','total_tackles':'Tkl',
            'avg_speed':'Speed','avg_rating':'Rating','avg_perf_score':'Perf','player_of_match':'POTM'
        }).reset_index(drop=True),
        use_container_width=True, height=340
    )

    st.markdown(f"<div style='color:#8b949e;font-size:0.8rem;'>Showing {len(display_df):,} players</div>", unsafe_allow_html=True)

    st.markdown("<div class='section-header'>🕸️ Player Radar Comparison</div>", unsafe_allow_html=True)
    all_names = ps_f.sort_values('avg_rating', ascending=False)['player_name'].tolist()
    sel_players = st.multiselect("Select up to 5 players to compare", all_names,
                                  default=all_names[:3], max_selections=5)

    if sel_players:
        radar_cols = ['total_goals','total_assists','avg_pass_acc','total_tackles','avg_speed','avg_stamina']
        radar_lbls = ['Goals','Assists','Pass Acc','Tackles','Speed','Stamina']
        rad_df = ps_f[ps_f['player_name'].isin(sel_players)][['player_name'] + radar_cols].copy()

        for col in radar_cols:
            col_min, col_max = player_stats[col].min(), player_stats[col].max()
            rad_df[col] = (rad_df[col] - col_min) / (col_max - col_min + 1e-9) * 100

        fig = go.Figure()
        pal = ['#58a6ff','#3fb950','#f78166','#d2a8ff','#ffa657']
        for i, row in rad_df.iterrows():
            vals = [row[c] for c in radar_cols]
            vals += vals[:1]
            lbls = radar_lbls + radar_lbls[:1]
            color = pal[list(rad_df.index).index(i) % len(pal)]
            fig.add_trace(go.Scatterpolar(
                r=vals, theta=lbls, fill='toself',
                name=row['player_name'],
                line_color=color,
                fillcolor=color.replace('ff','33').replace('#','rgba(').replace('33','33,0.18)') if False else color,
                opacity=0.85
            ))
        fig.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0,100], tickfont_color='#8b949e', gridcolor='#1e3a5f'),
                angularaxis=dict(gridcolor='#1e3a5f', linecolor='#1e3a5f', tickfont_color='#c9d1d9'),
                bgcolor='rgba(13,27,46,0.6)',
            ),
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family='Inter', color='#c9d1d9'),
            legend=dict(bgcolor='rgba(13,27,46,0.8)', bordercolor='#1e3a5f'),
            height=450,
        )
        st.plotly_chart(fig, use_container_width=True)

    # Age distribution
    st.markdown("<div class='section-header'>📊 Player Demographics</div>", unsafe_allow_html=True)
    col_d1, col_d2 = st.columns(2)
    with col_d1:
        fig = px.histogram(player_info[player_info['position'].isin(sel_positions)],
                           x='age', nbins=25, color='position',
                           color_discrete_sequence=['#58a6ff','#3fb950','#f78166','#d2a8ff'],
                           labels={'age':'Age','count':'Players'},
                           title='Age Distribution by Position')
        fig.update_layout(**LAYOUT_DEFAULTS)
        st.plotly_chart(fig, use_container_width=True)
    with col_d2:
        fig = px.box(player_info[player_info['position'].isin(sel_positions)],
                     x='position', y='height_cm', color='position',
                     color_discrete_sequence=['#58a6ff','#3fb950','#f78166','#d2a8ff'],
                     labels={'position':'Position','height_cm':'Height (cm)'},
                     title='Height Distribution by Position')
        fig.update_layout(**LAYOUT_DEFAULTS, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

# ═════════════════════════════════════════════
#  PAGE: ATTACKING
# ═════════════════════════════════════════════
elif "Attacking" in page:
    st.markdown("<div class='main-title'>⚽ Attacking Performance</div>", unsafe_allow_html=True)
    st.markdown("<div class='main-subtitle'>Goals, Expected Goals (xG), Assists, and Shooting Efficiency</div>", unsafe_allow_html=True)

    top_n = st.slider("Show Top N Players", 5, 30, 15)

    tab1, tab2, tab3, tab4 = st.tabs(["🥇 Top Scorers", "📈 xG Analysis", "🎁 Assists", "🎯 Shooting"])

    with tab1:
        st.markdown("<div class='section-header'>🥇 Top Goal Scorers</div>", unsafe_allow_html=True)
        top_s = ps_f.nlargest(top_n,'total_goals')
        fig = go.Figure()
        fig.add_trace(go.Bar(x=top_s['player_name'], y=top_s['total_goals'],
                             name='Goals', marker_color=COLORS['gold'],
                             text=top_s['total_goals'].astype(int), textposition='outside'))
        fig.add_trace(go.Bar(x=top_s['player_name'], y=top_s['total_xG'],
                             name='xG', marker_color=COLORS['blue'], opacity=0.8))
        fig.update_layout(**LAYOUT_DEFAULTS, barmode='overlay',
                          xaxis_tickangle=-35, title=f'Top {top_n} Goal Scorers vs Expected Goals (xG)')
        st.plotly_chart(fig, use_container_width=True)

        col_m1, col_m2, col_m3 = st.columns(3)
        col_m1.metric("Total Goals", f"{int(ps_f['total_goals'].sum()):,}")
        col_m2.metric("Total xG", f"{ps_f['total_xG'].sum():,.1f}")
        col_m3.metric("Avg Goals/Player", f"{ps_f['total_goals'].mean():.2f}")

    with tab2:
        st.markdown("<div class='section-header'>📈 xG vs Actual Goals — Overperformers</div>", unsafe_allow_html=True)
        atk = ps_f[ps_f['position'].isin(['Forward','Midfielder'])].copy()
        fig = px.scatter(atk, x='total_xG', y='total_goals', color='xG_diff',
                         color_continuous_scale='RdYlGn', range_color=[-6,6],
                         hover_name='player_name',
                         hover_data={'team':True, 'position':True, 'total_xG':':.2f',
                                     'total_goals':True, 'xG_diff':':.2f'},
                         size='total_shots',
                         labels={'total_xG':'Expected Goals (xG)','total_goals':'Actual Goals',
                                 'xG_diff':'Goals − xG'},
                         title='xG vs Actual Goals (size = shots; color = overperformance)')
        max_val = max(atk['total_xG'].max(), atk['total_goals'].max()) + 1
        fig.add_shape(type='line', x0=0, y0=0, x1=max_val, y1=max_val,
                      line=dict(color='#8b949e', width=1.5, dash='dash'))
        fig.add_annotation(x=max_val*0.7, y=max_val*0.7+2,
                           text="Above = Overperform", showarrow=False,
                           font=dict(color='#3fb950', size=11))
        fig.update_layout(**LAYOUT_DEFAULTS)
        st.plotly_chart(fig, use_container_width=True)

        col_x1, col_x2 = st.columns(2)
        with col_x1:
            st.markdown("**🟢 Top xG Overperformers**")
            st.dataframe(
                atk.nlargest(8,'xG_diff')[['player_name','team','total_goals','total_xG','xG_diff']]
                .rename(columns={'player_name':'Player','team':'Team','total_goals':'G','total_xG':'xG','xG_diff':'G-xG'})
                .reset_index(drop=True), use_container_width=True
            )
        with col_x2:
            st.markdown("**🔴 Top xG Underperformers**")
            st.dataframe(
                atk.nsmallest(8,'xG_diff')[['player_name','team','total_goals','total_xG','xG_diff']]
                .rename(columns={'player_name':'Player','team':'Team','total_goals':'G','total_xG':'xG','xG_diff':'G-xG'})
                .reset_index(drop=True), use_container_width=True
            )

    with tab3:
        st.markdown("<div class='section-header'>🎁 Top Assist Providers</div>", unsafe_allow_html=True)
        top_a = ps_f.nlargest(top_n,'total_assists')
        fig = go.Figure()
        fig.add_trace(go.Bar(name='Assists',   x=top_a['player_name'], y=top_a['total_assists'],   marker_color=COLORS['green']))
        fig.add_trace(go.Bar(name='xA',        x=top_a['player_name'], y=top_a['total_xA'],        marker_color=COLORS['blue'], opacity=0.8))
        fig.add_trace(go.Bar(name='Key Passes',x=top_a['player_name'], y=top_a['total_key_passes'],marker_color=COLORS['purple'], opacity=0.7))
        fig.update_layout(**LAYOUT_DEFAULTS, barmode='group', xaxis_tickangle=-35,
                          title=f'Top {top_n} Assist Providers — Assists, xA & Key Passes')
        st.plotly_chart(fig, use_container_width=True)

    with tab4:
        st.markdown("<div class='section-header'>🎯 Shot Conversion Rate</div>", unsafe_allow_html=True)
        conv = ps_f[ps_f['total_shots'] >= 5].nlargest(top_n, 'conversion_rate').copy()
        conv['conv_pct'] = conv['conversion_rate'] * 100
        fig = px.bar(conv, x='player_name', y='conv_pct', text=conv['conv_pct'].round(1),
                     color='conv_pct', color_continuous_scale='YlGn',
                     hover_data={'team':True,'total_goals':True,'total_shots':True},
                     labels={'player_name':'Player','conv_pct':'Conversion Rate (%)'},
                     title=f'Shot Conversion Rate — Top {top_n} (Min. 5 shots)')
        fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
        fig.update_layout(**LAYOUT_DEFAULTS, coloraxis_showscale=False, xaxis_tickangle=-35)
        st.plotly_chart(fig, use_container_width=True)

# ═════════════════════════════════════════════
#  PAGE: DEFENSIVE
# ═════════════════════════════════════════════
elif "Defensive" in page:
    st.markdown("<div class='main-title'>🛡️ Defensive Performance</div>", unsafe_allow_html=True)
    st.markdown("<div class='main-subtitle'>Tackles, Interceptions, Defensive Intensity & Disciplinary Records</div>", unsafe_allow_html=True)

    top_n_def = st.slider("Show Top N Players", 5, 25, 12)

    tab1, tab2, tab3 = st.tabs(["🛡️ Top Defenders", "📊 Stage Intensity", "🟨 Disciplinary"])

    with tab1:
        st.markdown("<div class='section-header'>🛡️ Top Defensive Players (Defenders & Midfielders)</div>", unsafe_allow_html=True)
        def_ps = ps_f[ps_f['position'].isin(['Defender','Midfielder'])].nlargest(top_n_def, 'defensive_idx')
        fig = go.Figure()
        fig.add_trace(go.Bar(name='Tackles', x=def_ps['player_name'], y=def_ps['total_tackles'],
                             marker_color=COLORS['red']))
        fig.add_trace(go.Bar(name='Interceptions', x=def_ps['player_name'], y=def_ps['total_interceptions'],
                             marker_color=COLORS['purple']))
        fig.add_trace(go.Bar(name='Clearances', x=def_ps['player_name'], y=def_ps['total_clearances'],
                             marker_color=COLORS['blue'], opacity=0.7))
        fig.update_layout(**LAYOUT_DEFAULTS, barmode='stack', xaxis_tickangle=-35,
                          title=f'Top {top_n_def} Defenders — Tackles, Interceptions & Clearances')
        st.plotly_chart(fig, use_container_width=True)

        col_d1, col_d2 = st.columns(2)
        col_d1.metric("Avg Tackles/Player", f"{ps_f['total_tackles'].mean():.1f}")
        col_d2.metric("Avg Interceptions/Player", f"{ps_f['total_interceptions'].mean():.1f}")

        st.markdown("<div class='section-header'>📋 Defensive Stats Table</div>", unsafe_allow_html=True)
        st.dataframe(
            def_ps[['player_name','team','total_matches','total_tackles','total_interceptions',
                     'total_clearances','defensive_idx']].rename(columns={
                'player_name':'Player','team':'Team','total_matches':'M',
                'total_tackles':'Tkl','total_interceptions':'Int',
                'total_clearances':'Clr','defensive_idx':'Def Index'
            }).reset_index(drop=True),
            use_container_width=True
        )

    with tab2:
        st.markdown("<div class='section-header'>📊 Defensive Intensity per Tournament Stage</div>", unsafe_allow_html=True)
        def_stage = df_f.groupby('tournament_stage').agg(
            avg_tackles       =('tackles','mean'),
            avg_interceptions =('interceptions','mean'),
            avg_clearances    =('clearances','mean'),
            avg_fouls         =('fouls_committed','mean'),
        ).reset_index()
        def_stage['order'] = def_stage['tournament_stage'].map({s:i for i,s in enumerate(STAGE_ORDER)})
        def_stage = def_stage.sort_values('order')

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=def_stage['tournament_stage'], y=def_stage['avg_tackles'],
                                  mode='lines+markers', name='Avg Tackles',
                                  line=dict(color=COLORS['red'], width=2.5),
                                  marker=dict(size=8)))
        fig.add_trace(go.Scatter(x=def_stage['tournament_stage'], y=def_stage['avg_interceptions'],
                                  mode='lines+markers', name='Avg Interceptions',
                                  line=dict(color=COLORS['purple'], width=2.5),
                                  marker=dict(size=8)))
        fig.add_trace(go.Scatter(x=def_stage['tournament_stage'], y=def_stage['avg_clearances'],
                                  mode='lines+markers', name='Avg Clearances',
                                  line=dict(color=COLORS['blue'], width=2.5),
                                  marker=dict(size=8)))
        fig.add_trace(go.Bar(x=def_stage['tournament_stage'], y=def_stage['avg_fouls'],
                              name='Avg Fouls', marker_color='rgba(255,166,87,0.4)', yaxis='y2'))
        fig.update_layout(
            **LAYOUT_DEFAULTS,
            yaxis2=dict(overlaying='y', side='right', gridcolor='#1e3a5f',
                        title='Avg Fouls', titlefont_color='#ffa657', tickfont_color='#8b949e'),
            title='Defensive Intensity Across Tournament Stages'
        )
        st.plotly_chart(fig, use_container_width=True)

    with tab3:
        st.markdown("<div class='section-header'>🟨 Yellow & Red Cards per Stage</div>", unsafe_allow_html=True)
        cards = df_f.groupby('tournament_stage').agg(
            yellow=('yellow_cards','sum'), red=('red_cards','sum')
        ).reset_index()
        cards['order'] = cards['tournament_stage'].map({s:i for i,s in enumerate(STAGE_ORDER)})
        cards = cards.sort_values('order')

        fig = go.Figure()
        fig.add_trace(go.Bar(x=cards['tournament_stage'], y=cards['yellow'],
                              name='Yellow Cards', marker_color=COLORS['gold'], text=cards['yellow'],
                              textposition='outside'))
        fig.add_trace(go.Bar(x=cards['tournament_stage'], y=cards['red'],
                              name='Red Cards', marker_color=COLORS['red'], text=cards['red'],
                              textposition='outside'))
        fig.update_layout(**LAYOUT_DEFAULTS, barmode='group',
                          title='Disciplinary Cards per Tournament Stage')
        st.plotly_chart(fig, use_container_width=True)

        col_c1, col_c2, col_c3 = st.columns(3)
        col_c1.metric("Total Yellow Cards", f"{int(df_f['yellow_cards'].sum())}")
        col_c2.metric("Total Red Cards",    f"{int(df_f['red_cards'].sum())}")
        col_c3.metric("Avg Fouls/Match",    f"{df_f.groupby('match_id')['fouls_committed'].sum().mean():.1f}")

# ═════════════════════════════════════════════
#  PAGE: PHYSICAL
# ═════════════════════════════════════════════
elif "Physical" in page:
    st.markdown("<div class='main-title'>💪 Physical & Stamina Performance</div>", unsafe_allow_html=True)
    st.markdown("<div class='main-subtitle'>Speed, Distance, Stamina and Physical Fitness Analysis</div>", unsafe_allow_html=True)

    top_n_phys = st.slider("Show Top N Players", 5, 25, 12)

    tab1, tab2, tab3 = st.tabs(["⚡ Speed", "🏃 Distance", "🏋️ Stamina"])

    with tab1:
        st.markdown("<div class='section-header'>⚡ Fastest Players in the Tournament</div>", unsafe_allow_html=True)
        top_sp = ps_f.nlargest(top_n_phys, 'avg_speed')
        fig = px.bar(top_sp, x='avg_speed', y='player_name', orientation='h',
                     color='avg_speed', color_continuous_scale='Oranges',
                     text=top_sp['avg_speed'].round(1), hover_data={'team':True,'position':True},
                     labels={'avg_speed':'Avg Top Speed (km/h)','player_name':'Player'})
        fig.update_traces(texttemplate='%{text} km/h', textposition='outside')
        fig.update_layout(**LAYOUT_DEFAULTS, coloraxis_showscale=False,
                          yaxis=dict(autorange='reversed'),
                          title=f'Top {top_n_phys} Fastest Players (Avg Top Speed)')
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("<div class='section-header'>📊 Speed Distribution by Position</div>", unsafe_allow_html=True)
        fig = px.violin(df_f, y='top_speed_kmh', x='position', color='position',
                        box=True, points='outliers',
                        color_discrete_sequence=['#58a6ff','#3fb950','#f78166','#d2a8ff'],
                        labels={'top_speed_kmh':'Top Speed (km/h)','position':'Position'})
        fig.update_layout(**LAYOUT_DEFAULTS, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        st.markdown("<div class='section-header'>🏃 Distance Covered per Position</div>", unsafe_allow_html=True)
        dist_pos = df_f.groupby('position')['distance_covered_km'].agg(['mean','median','std']).reset_index()
        dist_pos.columns = ['Position','Mean','Median','Std']

        fig = go.Figure()
        fig.add_trace(go.Bar(x=dist_pos['Position'], y=dist_pos['Mean'],
                              name='Mean Distance', marker_color=COLORS['green'],
                              text=dist_pos['Mean'].round(2), textposition='outside',
                              error_y=dict(type='data', array=dist_pos['Std'], visible=True,
                                           color='rgba(255,255,255,0.4)')))
        fig.add_trace(go.Scatter(x=dist_pos['Position'], y=dist_pos['Median'],
                                  mode='markers', name='Median',
                                  marker=dict(symbol='diamond', size=12, color=COLORS['gold'],
                                              line=dict(width=2, color='#0d1117'))))
        fig.update_layout(**LAYOUT_DEFAULTS, title='Average Distance Covered per Laga — by Position')
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("<div class='section-header'>📈 Distance vs Sprint Distance (Scatter)</div>", unsafe_allow_html=True)
        samp = df_f[df_f['minutes_played'] >= 60].sample(min(2000, len(df_f)), random_state=42)
        fig = px.scatter(samp, x='distance_covered_km', y='sprint_distance_km',
                         color='position', opacity=0.5,
                         color_discrete_sequence=['#58a6ff','#3fb950','#f78166','#d2a8ff'],
                         labels={'distance_covered_km':'Total Distance (km)','sprint_distance_km':'Sprint Distance (km)'},
                         hover_name='player_name', hover_data={'team':True,'position':True})
        fig.update_layout(**LAYOUT_DEFAULTS, title='Total Distance vs Sprint Distance by Position')
        st.plotly_chart(fig, use_container_width=True)

    with tab3:
        st.markdown("<div class='section-header'>🏋️ Stamina Score vs Distance Covered</div>", unsafe_allow_html=True)
        samp2 = df_f[df_f['minutes_played'] >= 60].sample(min(2000, len(df_f)), random_state=99)
        fig = px.scatter(samp2, x='stamina_score', y='distance_covered_km',
                         color='position', trendline='ols',
                         opacity=0.5, color_discrete_sequence=['#58a6ff','#3fb950','#f78166','#d2a8ff'],
                         labels={'stamina_score':'Stamina Score','distance_covered_km':'Distance (km)'},
                         hover_name='player_name', hover_data={'team':True,'position':True},
                         title='Stamina Score vs Distance Covered (with OLS Trendline)')
        fig.update_layout(**LAYOUT_DEFAULTS)
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("<div class='section-header'>📊 Avg Physical Stats per Position</div>", unsafe_allow_html=True)
        phys_tbl = df_f.groupby('position').agg(
            avg_distance =('distance_covered_km','mean'),
            avg_sprint   =('sprint_distance_km','mean'),
            avg_speed    =('top_speed_kmh','mean'),
            avg_stamina  =('stamina_score','mean'),
        ).reset_index().rename(columns={
            'position':'Position','avg_distance':'Avg Distance (km)',
            'avg_sprint':'Avg Sprint (km)','avg_speed':'Avg Speed (km/h)',
            'avg_stamina':'Avg Stamina'
        })
        st.dataframe(phys_tbl.style.format({
            'Avg Distance (km)':'{:.2f}','Avg Sprint (km)':'{:.2f}',
            'Avg Speed (km/h)':'{:.1f}','Avg Stamina':'{:.1f}'
        }), use_container_width=True)

# ═════════════════════════════════════════════
#  PAGE: TEAMS
# ═════════════════════════════════════════════
elif "Teams" in page:
    st.markdown("<div class='main-title'>🌍 Team Analysis</div>", unsafe_allow_html=True)
    st.markdown("<div class='main-subtitle'>Win Rate, Goals, Performance and Team Comparison</div>", unsafe_allow_html=True)

    top_n_team = st.slider("Show Top N Teams", 5, 32, 15)
    min_matches = st.slider("Min. Matches Played", 1, 7, 3)

    ta_f = team_stats[team_stats['total_matches'] >= min_matches]

    tab1, tab2, tab3, tab4 = st.tabs(["🏆 Win Rate", "⚽ Goals", "📊 Comparison", "🫧 Bubble Chart"])

    with tab1:
        st.markdown("<div class='section-header'>🏆 Team Win Rate Ranking</div>", unsafe_allow_html=True)
        top_wr = ta_f.nlargest(top_n_team,'win_rate')
        fig = px.bar(top_wr, x='win_rate', y='team', orientation='h',
                     color='win_rate', color_continuous_scale='RdYlGn',
                     text=top_wr['win_rate'].round(1),
                     hover_data={'total_matches':True,'wins':True,'draws':True,'losses':True},
                     labels={'win_rate':'Win Rate (%)','team':'Team'})
        fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
        fig.update_layout(**LAYOUT_DEFAULTS, coloraxis_showscale=False,
                          yaxis=dict(autorange='reversed'),
                          title=f'Top {top_n_team} Teams by Win Rate')
        st.plotly_chart(fig, use_container_width=True)

        col_t1, col_t2, col_t3 = st.columns(3)
        best = ta_f.nlargest(1,'win_rate').iloc[0]
        col_t1.metric("🏆 Best Win Rate", f"{best['win_rate']:.1f}%", best['team'])
        most_g = ta_f.nlargest(1,'goals_pg').iloc[0]
        col_t2.metric("⚽ Most Goals/Game", f"{most_g['goals_pg']:.2f}", most_g['team'])
        best_gd = ta_f.nlargest(1,'goal_diff').iloc[0]
        col_t3.metric("📊 Best Goal Diff", f"+{int(best_gd['goal_diff'])}", best_gd['team'])

    with tab2:
        st.markdown("<div class='section-header'>⚽ Goals Scored vs Goals Conceded</div>", unsafe_allow_html=True)
        top_gf = ta_f.nlargest(top_n_team,'total_goals_f')
        fig = go.Figure()
        fig.add_trace(go.Bar(x=top_gf['team'], y=top_gf['total_goals_f'],
                              name='Goals Scored', marker_color=COLORS['gold'],
                              text=top_gf['total_goals_f'], textposition='outside'))
        fig.add_trace(go.Bar(x=top_gf['team'], y=-top_gf['total_goals_a'],
                              name='Goals Conceded', marker_color=COLORS['red'],
                              text=top_gf['total_goals_a'], textposition='outside'))
        fig.add_hline(y=0, line_width=1, line_color='#8b949e')
        fig.update_layout(**LAYOUT_DEFAULTS, barmode='relative', xaxis_tickangle=-35,
                          yaxis_title='Goals (positive = scored, negative = conceded)',
                          title=f'Goals Scored vs Conceded — Top {top_n_team} Teams')
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("<div class='section-header'>📋 Full Team Stats Table</div>", unsafe_allow_html=True)
        st.dataframe(
            ta_f.sort_values('win_rate', ascending=False)[
                ['team','total_matches','wins','draws','losses',
                 'total_goals_f','total_goals_a','goal_diff','win_rate','goals_pg','avg_rating']
            ].rename(columns={
                'team':'Team','total_matches':'P','wins':'W','draws':'D','losses':'L',
                'total_goals_f':'GF','total_goals_a':'GA','goal_diff':'GD',
                'win_rate':'Win%','goals_pg':'G/Game','avg_rating':'Avg Rating'
            }).reset_index(drop=True),
            use_container_width=True
        )

    with tab3:
        st.markdown("<div class='section-header'>📊 Team Performance Comparison</div>", unsafe_allow_html=True)
        sel_teams = st.multiselect(
            "Select teams to compare",
            options=sorted(ta_f['team'].tolist()),
            default=ta_f.nlargest(5,'win_rate')['team'].tolist()
        )
        if sel_teams:
            cmp_df = ta_f[ta_f['team'].isin(sel_teams)]
            metrics = ['win_rate','goals_pg','goal_diff','avg_rating']
            labels  = ['Win Rate (%)','Goals/Game','Goal Diff','Avg Rating']

            radar_cmp = cmp_df[['team'] + metrics].copy()
            for m in metrics:
                rmin, rmax = ta_f[m].min(), ta_f[m].max()
                radar_cmp[m] = (radar_cmp[m] - rmin) / (rmax - rmin + 1e-9) * 100

            fig = go.Figure()
            pal = ['#58a6ff','#3fb950','#f78166','#d2a8ff','#ffa657']
            for i, row in radar_cmp.iterrows():
                vals = [row[m] for m in metrics]
                vals += vals[:1]
                lbls = labels + labels[:1]
                color = pal[list(radar_cmp.index).index(i) % len(pal)]
                fig.add_trace(go.Scatterpolar(r=vals, theta=lbls, fill='toself',
                                               name=row['team'], line_color=color))
            fig.update_layout(
                polar=dict(
                    radialaxis=dict(visible=True, range=[0,100], gridcolor='#1e3a5f', tickfont_color='#8b949e'),
                    angularaxis=dict(gridcolor='#1e3a5f', tickfont_color='#c9d1d9'),
                    bgcolor='rgba(13,27,46,0.6)',
                ),
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(family='Inter', color='#c9d1d9'),
                legend=dict(bgcolor='rgba(13,27,46,0.8)', bordercolor='#1e3a5f'),
                height=450,
                title='Team Performance Radar Comparison'
            )
            st.plotly_chart(fig, use_container_width=True)

    with tab4:
        st.markdown("<div class='section-header'>🫧 Goals Scored vs Conceded — Bubble Chart</div>", unsafe_allow_html=True)
        fig = px.scatter(ta_f, x='total_goals_f', y='total_goals_a',
                         size='total_matches', color='win_rate',
                         color_continuous_scale='RdYlGn', range_color=[0,100],
                         hover_name='team',
                         hover_data={'total_matches':True,'wins':True,'goal_diff':True,'win_rate':':.1f'},
                         labels={'total_goals_f':'Goals Scored','total_goals_a':'Goals Conceded',
                                 'win_rate':'Win Rate (%)'},
                         title='Goals Scored vs Conceded (size = matches played, color = win rate)')
        max_g = max(ta_f['total_goals_f'].max(), ta_f['total_goals_a'].max()) + 2
        fig.add_shape(type='line', x0=0, y0=0, x1=max_g, y1=max_g,
                      line=dict(color='#8b949e', width=1.5, dash='dash'))
        fig.add_annotation(x=max_g*0.6, y=max_g*0.6+2, text='Equal Goals Line',
                           showarrow=False, font=dict(color='#8b949e', size=10))
        fig.update_layout(**LAYOUT_DEFAULTS)
        st.plotly_chart(fig, use_container_width=True)

# ─────────────────────────────────────────────
#  FOOTER
# ─────────────────────────────────────────────
st.markdown("""
<hr style='border-color:#1e3a5f; margin-top:3rem;'>
<div style='text-align:center; color:#8b949e; font-size:0.8rem; padding: 1rem 0;'>
    ⚽ FIFA World Cup 2026 Analytics Dashboard &nbsp;·&nbsp;
    Built with <strong style='color:#f78166;'>Streamlit</strong> &amp;
    <strong style='color:#58a6ff;'>Plotly</strong> &nbsp;·&nbsp;
    Dataset: 54,601 player performance records
</div>
""", unsafe_allow_html=True)
